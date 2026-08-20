"""
run_all.py — Orquestrador de geração de dados mock em Parquet.

Executa todos os generators na ordem correta de dependência,
garante integridade referencial, salva Parquet e loga métricas finais.

Uso:
    python run_all.py
"""
import sys
import time
from pathlib import Path

# Configurar encoding do stdout/stderr para UTF-8 no Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# Garantir imports do diretório correto
sys.path.insert(0, str(Path(__file__).resolve().parent))

import pandas as pd
import numpy as np
import _config as cfg

# Imports dos generators
import clientes
import produtos
import carrinhos
import itens_carrinho
import eventos_carrinho
import eventos_resgate
import pedidos


def log(msg, level='INFO'):
    """Logger simples."""
    prefix = {'INFO': '📊', 'OK': '✅', 'WARN': '⚠️', 'HEAD': '═'*60}
    icon = prefix.get(level, '•')
    if level == 'HEAD':
        print(f"\n{icon}")
        print(f"  {msg}")
        print(f"{icon}")
    else:
        print(f"  {icon} {msg}")


def calcular_metricas(carrinhos_df, resgate_df, pedidos_df, clientes_df):
    """Calcula e exibe métricas finais vs targets."""
    log("MÉTRICAS FINAIS vs TARGETS", 'HEAD')

    total_carrinhos = len(carrinhos_df)
    abandonados = carrinhos_df[carrinhos_df['_lifecycle'].isin([
        'abandonado', 'recuperado_comprado', 'recuperado_pendente', 'expirado'
    ])]
    total_abandonados = len(abandonados)
    recuperados_compra = carrinhos_df[carrinhos_df['_lifecycle'] == 'recuperado_comprado']

    # ─── Camada 1: Conversão ─────────────────────────────────────────
    taxa_abandono = total_abandonados / total_carrinhos * 100
    taxa_recuperacao = len(recuperados_compra) / total_abandonados * 100 if total_abandonados > 0 else 0
    total_pedidos = len(pedidos_df)
    pedidos_diretos = pedidos_df[~pedidos_df['origem_recuperacao']].shape[0]
    pedidos_recuperados = pedidos_df[pedidos_df['origem_recuperacao']].shape[0]

    print(f"\n  {'─'*50}")
    print(f"  CAMADA 1 — Conversão & Recuperação")
    print(f"  {'─'*50}")
    print(f"  Taxa de abandono:         {taxa_abandono:.1f}%  (target: ~70%)")
    print(f"  Taxa de recuperação:      {taxa_recuperacao:.1f}%  (target: ~10%)")
    print(f"  Pedidos totais:           {total_pedidos}  (target: ~1.800)")
    print(f"    ├─ Diretos:             {pedidos_diretos}")
    print(f"    └─ Via recuperação:      {pedidos_recuperados}")

    # ─── Camada 2: Eficiência por canal ──────────────────────────────
    print(f"\n  {'─'*50}")
    print(f"  CAMADA 2 — Eficiência por Canal")
    print(f"  {'─'*50}")
    if len(resgate_df) > 0:
        for canal in ['email', 'whatsapp', 'sms', 'push_app']:
            canal_df = resgate_df[resgate_df['canal'] == canal]
            if len(canal_df) > 0:
                enviados = len(canal_df)
                abertos = canal_df['data_abertura'].notna().sum()
                clicados = canal_df['data_primeiro_clique'].notna().sum()
                convertidos = canal_df['sucesso'].sum()
                print(f"  {canal:12s}: envios={enviados:4d}  abertura={abertos/enviados*100:5.1f}%  "
                      f"clique={clicados/max(abertos,1)*100:5.1f}%  "
                      f"conversão={convertidos/total_abandonados*100:4.1f}%")

    # ─── Camada 3: RFM ───────────────────────────────────────────────
    print(f"\n  {'─'*50}")
    print(f"  CAMADA 3 — Eficiência por RFM")
    print(f"  {'─'*50}")
    for seg in ['premium', 'regular', 'dormant', 'novo']:
        seg_abandonados = abandonados[abandonados['_segmento_rfm'] == seg]
        seg_recuperados = seg_abandonados[seg_abandonados['_lifecycle'] == 'recuperado_comprado']
        if len(seg_abandonados) > 0:
            taxa = len(seg_recuperados) / len(seg_abandonados) * 100
            print(f"  {seg:12s}: {len(seg_abandonados):4d} abandonados → {len(seg_recuperados):3d} recuperados ({taxa:.1f}%)")

    # ─── Camada 4: Eficiência operacional ────────────────────────────
    print(f"\n  {'─'*50}")
    print(f"  CAMADA 4 — Eficiência Operacional")
    print(f"  {'─'*50}")
    if len(resgate_df) > 0:
        custo_total = resgate_df['custo_envio'].sum()
        receita_recuperada = resgate_df[resgate_df['sucesso'] == True]['valor_pedido_final'].sum()
        roi = (receita_recuperada - custo_total) / custo_total if custo_total > 0 else 0
        taxa_abertura_geral = resgate_df['data_abertura'].notna().mean() * 100
        taxa_conversao_geral = resgate_df['sucesso'].mean() * 100
        print(f"  ROI geral:                {roi:.1f}x  (target: ~45x)")
        print(f"  Custo total campanhas:    R${custo_total:.2f}")
        print(f"  Receita recuperada:       R${receita_recuperada:.2f}")
        print(f"  % campanhas c/ abertura:  {taxa_abertura_geral:.1f}%  (target: ~55%)")
        print(f"  % campanhas c/ conversão: {taxa_conversao_geral:.1f}%  (target: ~10%)")

    # ─── Camada 5: Timing ────────────────────────────────────────────
    print(f"\n  {'─'*50}")
    print(f"  CAMADA 5 — Timing & Sequência")
    print(f"  {'─'*50}")
    if len(resgate_df) > 0:
        conversoes = resgate_df[resgate_df['sucesso'] == True]
        total_conv = len(conversoes)
        if total_conv > 0:
            for tipo in ['lembrete_1h', 'lembrete_24h', 'desconto_48h', 'urgencia_72h']:
                n = len(conversoes[conversoes['tipo_comunicacao'] == tipo])
                print(f"  {tipo:20s}: {n:3d} conversões ({n/total_conv*100:5.1f}%)")


def main():
    """Orquestra a geração completa de dados mock."""
    start = time.time()
    log("GERAÇÃO DE DADOS MOCK — PARQUET", 'HEAD')
    log(f"Output: {cfg.OUTPUT_DIR}")

    # Garantir diretório de output
    cfg.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # ─── 1. Clientes (independente) ──────────────────────────────────
    log("Gerando clientes...")
    clientes_df = clientes.generate()
    log(f"Clientes: {len(clientes_df)} registros", 'OK')

    # ─── 2. Produtos (independente) ──────────────────────────────────
    log("Gerando produtos...")
    produtos_df = produtos.generate()
    log(f"Produtos: {len(produtos_df)} registros", 'OK')

    # ─── 3. Carrinhos (depende de clientes) ──────────────────────────
    log("Gerando carrinhos...")
    carrinhos_df = carrinhos.generate(clientes_df)
    log(f"Carrinhos: {len(carrinhos_df)} registros", 'OK')

    # ─── 4. Itens do carrinho (depende de carrinhos + produtos) ──────
    log("Gerando itens de carrinho...")
    itens_df = itens_carrinho.generate(carrinhos_df, produtos_df)
    log(f"Itens Carrinho: {len(itens_df)} registros", 'OK')

    # ─── 5. Eventos de carrinho (depende de carrinhos) ───────────────
    log("Gerando eventos de carrinho...")
    eventos_df = eventos_carrinho.generate(carrinhos_df)
    log(f"Eventos Carrinho: {len(eventos_df)} registros", 'OK')

    # ─── 6. Eventos de resgate (depende de carrinhos + clientes) ─────
    log("Gerando eventos de resgate...")
    resgate_df = eventos_resgate.generate(carrinhos_df, clientes_df)
    log(f"Eventos Resgate: {len(resgate_df)} registros", 'OK')

    # ─── 7. Pedidos (depende de carrinhos + clientes + resgate) ──────
    log("Gerando pedidos...")
    pedidos_df = pedidos.generate(carrinhos_df, clientes_df, resgate_df)
    log(f"Pedidos: {len(pedidos_df)} registros", 'OK')

    # ─── Salvar Parquet & CSV ──────────────────────────────────────────
    log("SALVANDO DADOS (PARQUET & CSV)", 'HEAD')

    cfg.PARQUET_DIR.mkdir(parents=True, exist_ok=True)
    cfg.CSV_DIR.mkdir(parents=True, exist_ok=True)

    datasets = {
        'clientes':         clientes_df,
        'produtos':         produtos_df,
        'carrinhos':        carrinhos.save_df(carrinhos_df),  # Remove colunas internas
        'itens_carrinho':   itens_df,
        'eventos_carrinho': eventos_df,
        'eventos_resgate':  resgate_df,
        'pedidos':          pedidos_df,
    }

    total_registros = 0
    for nome, df in datasets.items():
        parquet_path = cfg.PARQUET_DIR / f"{nome}.parquet"
        csv_path = cfg.CSV_DIR / f"{nome}.csv"

        df.to_parquet(parquet_path, index=False, engine='pyarrow')
        df.to_csv(csv_path, index=False, encoding='utf-8')

        tamanho_pq = parquet_path.stat().st_size / 1024
        tamanho_csv = csv_path.stat().st_size / 1024
        total_registros += len(df)
        log(f"{nome}: {len(df):>7,} registros | Parquet: {tamanho_pq:.0f} KB | CSV: {tamanho_csv:.0f} KB", 'OK')

    log(f"TOTAL: {total_registros:,} registros", 'OK')

    # ─── Métricas ────────────────────────────────────────────────────
    calcular_metricas(carrinhos_df, resgate_df, pedidos_df, clientes_df)

    elapsed = time.time() - start
    log(f"CONCLUÍDO em {elapsed:.1f}s", 'HEAD')


if __name__ == '__main__':
    main()
