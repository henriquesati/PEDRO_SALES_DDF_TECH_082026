"""
run_all.py — Orquestrador Declarativo de Geração de Dados Mock (Cart Recovery).

Executa o pipeline completo de geração de datasets sintéticos em Parquet e CSV,
gerencia dependências entre entidades, garante cotas mínimas determinísticas de
dados sujos/inúteis e anomalias de negócio, e exibe relatórios de auditoria e KPIs.

Uso:
    python run_all.py
    python run_all.py --profile rich
    python run_all.py --profile dev
    python run_all.py --dirty-multiplier 1.5 --seed 123
"""
import sys
import time
import argparse
from pathlib import Path
from typing import Dict, Any

# Forçar encoding UTF-8 no Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# Garantir import do diretório local
CURRENT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(CURRENT_DIR))

import pandas as pd
import numpy as np

from config.settings import GeneratorSettings
from config.profiles import load_profile, PROFILES
from modules.clientes import ClientesGenerator
from modules.produtos import ProdutosGenerator
from modules.carrinhos import CarrinhosGenerator
from modules.itens_carrinho import ItensCarrinhoGenerator
from modules.eventos_carrinho import EventosCarrinhoGenerator
from modules.eventos_resgate import EventosResgateGenerator
from modules.pedidos import PedidosGenerator


def log(msg: str, level: str = 'INFO'):
    """Logger formatado para terminal."""
    prefix = {'INFO': '📊', 'OK': '✅', 'WARN': '⚠️', 'HEAD': '═' * 65}
    icon = prefix.get(level, '•')
    if level == 'HEAD':
        print(f"\n{icon}")
        print(f"  {msg}")
        print(f"{icon}")
    else:
        print(f"  {icon} {msg}")


def exibir_auditoria_anomalias(audits: list):
    """Exibe tabela consolidada de auditoria de anomalias injetadas."""
    log("AUDITORIA DE DIRTY DATA & ANOMALIAS INJETADAS", 'HEAD')
    all_records = []
    for audit in audits:
        df_audit = audit.to_dataframe()
        if len(df_audit) > 0:
            all_records.append(df_audit)

    if all_records:
        full_audit_df = pd.concat(all_records, ignore_index=True)
        print(f"\n  {'Entidade':<18} {'Anomalia':<26} {'Min Alvo %':<12} {'Afetados':<10} {'Real %':<10}")
        print(f"  {'-'*18} {'-'*26} {'-'*12} {'-'*10} {'-'*10}")
        for _, r in full_audit_df.iterrows():
            print(f"  {r['entity']:<18} {r['anomaly']:<26} {r['target_min_pct']:>9.1f}%  {r['affected_rows']:>8d}  {r['actual_pct']:>8.1f}%")
    print()


def calcular_metricas_negocio(carrinhos_df: pd.DataFrame, resgate_df: pd.DataFrame, pedidos_df: pd.DataFrame):
    """Calcula e exibe métricas de negócio vs metas em camadas hierárquicas (DEC-001)."""
    log("MÉTRICAS DE NEGÓCIO vs TARGETS (DEC-001)", 'HEAD')

    total_carrinhos = len(carrinhos_df)
    abandonados = carrinhos_df[carrinhos_df['_lifecycle'].isin([
        'abandonado', 'recuperado_comprado', 'recuperado_pendente', 'expirado'
    ])]
    total_abandonados = len(abandonados)
    recuperados_compra = carrinhos_df[carrinhos_df['_lifecycle'] == 'recuperado_comprado']

    # Camada 1: Conversão & Recuperação
    taxa_abandono = total_abandonados / total_carrinhos * 100 if total_carrinhos > 0 else 0
    taxa_recuperacao = len(recuperados_compra) / total_abandonados * 100 if total_abandonados > 0 else 0
    total_pedidos = len(pedidos_df)
    pedidos_diretos = pedidos_df[~pedidos_df['origem_recuperacao']].shape[0]
    pedidos_recuperados = pedidos_df[pedidos_df['origem_recuperacao']].shape[0]

    print(f"\n  {'─'*55}")
    print(f"  CAMADA 1 — Conversão & Recuperação")
    print(f"  {'─'*55}")
    print(f"  Taxa de abandono:         {taxa_abandono:>6.1f}%  (target: ~70%)")
    print(f"  Taxa de recuperação:      {taxa_recuperacao:>6.1f}%  (target: ~10%)")
    print(f"  Pedidos totais:           {total_pedidos:>6d}")
    print(f"    ├─ Diretos:             {pedidos_diretos:>6d}")
    print(f"    └─ Via recuperação:      {pedidos_recuperados:>6d}")

    # Camada 2: Eficiência por Canal
    print(f"\n  {'─'*55}")
    print(f"  CAMADA 2 — Eficiência por Canal")
    print(f"  {'─'*55}")
    if len(resgate_df) > 0:
        for canal in ['email', 'whatsapp', 'sms', 'push_app']:
            canal_df = resgate_df[resgate_df['canal'] == canal]
            if len(canal_df) > 0:
                enviados = len(canal_df)
                abertos = canal_df['data_abertura'].notna().sum()
                clicados = canal_df['data_primeiro_clique'].notna().sum()
                convertidos = canal_df['sucesso'].sum()
                print(f"  {canal:<10s}: envios={enviados:4d} | abertura={abertos/enviados*100:5.1f}% | "
                      f"clique={clicados/max(abertos,1)*100:5.1f}% | "
                      f"conversão={convertidos/total_abandonados*100:4.1f}%")

    # Camada 3: Eficiência por RFM
    print(f"\n  {'─'*55}")
    print(f"  CAMADA 3 — Eficiência por RFM")
    print(f"  {'─'*55}")
    for seg in ['premium', 'regular', 'dormant', 'novo']:
        seg_abandonados = abandonados[abandonados['_segmento_rfm'] == seg]
        seg_recuperados = seg_abandonados[seg_abandonados['_lifecycle'] == 'recuperado_comprado']
        if len(seg_abandonados) > 0:
            taxa = len(seg_recuperados) / len(seg_abandonados) * 100
            print(f"  {seg:<10s}: {len(seg_abandonados):4d} abandonados → {len(seg_recuperados):3d} recuperados ({taxa:>5.1f}%)")

    # Camada 4: Eficiência Operacional & ROI
    print(f"\n  {'─'*55}")
    print(f"  CAMADA 4 — Eficiência Operacional & ROI")
    print(f"  {'─'*55}")
    if len(resgate_df) > 0:
        custo_total = resgate_df['custo_envio'].sum()
        receita_recuperada = resgate_df[resgate_df['sucesso'] == True]['valor_pedido_final'].sum()
        roi = (receita_recuperada - custo_total) / custo_total if custo_total > 0 else 0
        taxa_abertura_geral = resgate_df['data_abertura'].notna().mean() * 100
        taxa_conversao_geral = resgate_df['sucesso'].mean() * 100
        print(f"  ROI geral:                {roi:>6.1f}x  (target: ~35-45x)")
        print(f"  Custo total campanhas:    R${custo_total:>9.2f}")
        print(f"  Receita recuperada:       R${receita_recuperada:>9.2f}")
        print(f"  % campanhas c/ abertura:  {taxa_abertura_geral:>6.1f}%")
        print(f"  % campanhas c/ conversão: {taxa_conversao_geral:>6.1f}%")


def parse_args():
    parser = argparse.ArgumentParser(description="Pipeline Declarativo de Geração Mock Parquet/CSV — Cart Recovery")
    parser.add_argument('--profile', choices=['standard', 'rich', 'dev'], default='standard', help="Perfil de volumetria")
    parser.add_argument('--dirty-multiplier', type=float, default=1.0, help="Multiplicador para cotas de anomalias/dirty data")
    parser.add_argument('--seed', type=int, default=42, help="Seed para reprodutibilidade determinística")
    parser.add_argument('--output-dir', type=str, default=None, help="Diretório de saída customizado")
    return parser.parse_args()


def main():
    args = parse_args()
    start_time = time.time()

    # Carregar configurações do perfil
    settings = load_profile(name=args.profile, seed=args.seed, dirty_multiplier=args.dirty_multiplier)
    if args.output_dir:
        settings.output_dir = Path(args.output_dir)

    log(f"GERAÇÃO DE DADOS MOCK — PARQUET & CSV (Perfil: {settings.profile_name.upper()})", 'HEAD')
    log(f"Output: {settings.output_dir}")
    log(f"Seed: {settings.seed} | Dirty Multiplier: {args.dirty_multiplier}x")

    # Instanciar geradores modulares
    gen_clientes = ClientesGenerator(settings)
    gen_produtos = ProdutosGenerator(settings)
    gen_carrinhos = CarrinhosGenerator(settings)
    gen_itens = ItensCarrinhoGenerator(settings)
    gen_eventos = EventosCarrinhoGenerator(settings)
    gen_resgate = EventosResgateGenerator(settings)
    gen_pedidos = PedidosGenerator(settings)

    # 1. Clientes
    log("Gerando clientes...")
    clientes_df = gen_clientes.run()
    log(f"Clientes: {len(clientes_df):,} registros", 'OK')

    # 2. Produtos
    log("Gerando produtos...")
    produtos_df = gen_produtos.run()
    log(f"Produtos: {len(produtos_df):,} registros", 'OK')

    # 3. Carrinhos (depende de clientes)
    log("Gerando carrinhos...")
    carrinhos_df = gen_carrinhos.run(clientes_df=clientes_df)
    log(f"Carrinhos: {len(carrinhos_df):,} registros", 'OK')

    # 4. Itens do carrinho (depende de carrinhos + produtos)
    log("Gerando itens do carrinho...")
    itens_df = gen_itens.run(carrinhos_df=carrinhos_df, produtos_df=produtos_df)
    log(f"Itens do Carrinho: {len(itens_df):,} registros", 'OK')

    # 5. Eventos de telemetria do carrinho (depende de carrinhos)
    log("Gerando eventos comportamentais...")
    eventos_df = gen_eventos.run(carrinhos_df=carrinhos_df)
    log(f"Eventos do Carrinho: {len(eventos_df):,} registros", 'OK')

    # 6. Eventos de resgate (depende de carrinhos + clientes)
    log("Gerando eventos de resgate...")
    resgate_df = gen_resgate.run(carrinhos_df=carrinhos_df, clientes_df=clientes_df)
    log(f"Eventos de Resgate: {len(resgate_df):,} registros", 'OK')

    # 7. Pedidos (depende de carrinhos + clientes + resgate)
    log("Gerando pedidos...")
    pedidos_df = gen_pedidos.run(carrinhos_df=carrinhos_df, clientes_df=clientes_df, resgate_df=resgate_df)
    log(f"Pedidos: {len(pedidos_df):,} registros", 'OK')

    # ─── Salvar Datasets ───────────────────────────────────────────────
    log("EXPORTANDO ARQUIVOS (PARQUET & CSV)", 'HEAD')

    generators_map = {
        'clientes': (gen_clientes, clientes_df),
        'produtos': (gen_produtos, produtos_df),
        'carrinhos': (gen_carrinhos, carrinhos_df),
        'itens_carrinho': (gen_itens, itens_df),
        'eventos_carrinho': (gen_eventos, eventos_df),
        'eventos_resgate': (gen_resgate, resgate_df),
        'pedidos': (gen_pedidos, pedidos_df),
    }

    total_registros = 0
    for entity_name, (generator, df) in generators_map.items():
        paths = generator.save(df)
        pq_size = paths['parquet'].stat().st_size / 1024
        csv_size = paths['csv'].stat().st_size / 1024
        total_registros += len(df)
        log(f"{entity_name:<18}: {len(df):>7,} registros | Parquet: {pq_size:>6.0f} KB | CSV: {csv_size:>6.0f} KB", 'OK')

    log(f"VOLUMETRIA TOTAL: {total_registros:,} registros gerados com sucesso!", 'OK')

    # ─── Auditoria de Anomalias ─────────────────────────────────────────
    all_audits = [
        gen_clientes.audit, gen_produtos.audit, gen_carrinhos.audit,
        gen_itens.audit, gen_resgate.audit
    ]
    exibir_auditoria_anomalias(all_audits)

    # ─── Métricas de Negócio ───────────────────────────────────────────
    calcular_metricas_negocio(carrinhos_df, resgate_df, pedidos_df)

    elapsed = time.time() - start_time
    log(f"EXECUÇÃO CONCLUÍDA EM {elapsed:.2f}s", 'HEAD')


if __name__ == '__main__':
    main()
