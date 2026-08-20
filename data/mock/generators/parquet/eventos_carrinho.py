"""
Generator: eventos_carrinho
Gera ~70.000 eventos comportamentais (time series) para os carrinhos.
Média de ~12 eventos por carrinho com sequência realista de ações.
Cada carrinho segue um fluxo coerente: view → add → checkout → pagamento/abandono.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import pandas as pd
import numpy as np
import json
import uuid
from datetime import timedelta
import _config as cfg


# Sequências de eventos típicas por lifecycle
# Cada sequência é uma lista de (tipo_evento, peso_probabilidade)
FLUXO_COMPRADO = [
    'view_produto', 'view_produto', 'add_carrinho',
    'view_produto', 'add_carrinho', 'update_quantidade',
    'view_checkout', 'inicio_pagamento',
]

FLUXO_ABANDONADO = [
    'view_produto', 'view_produto', 'add_carrinho',
    'view_produto', 'add_carrinho',
    'view_checkout', 'abandono',
]

FLUXO_ABANDONADO_PAGAMENTO = [
    'view_produto', 'add_carrinho', 'view_produto', 'add_carrinho',
    'view_checkout', 'inicio_pagamento', 'erro_pagamento', 'abandono',
]

FLUXO_RECUPERADO = [
    'view_produto', 'add_carrinho', 'view_produto', 'add_carrinho',
    'view_checkout', 'abandono', 'retorno',
    'view_checkout', 'inicio_pagamento',
]


def _gerar_dados_evento(tipo_evento, carrinho):
    """Gera dados contextuais (JSONB) por tipo de evento."""
    dados = {}

    if tipo_evento == 'view_produto':
        dados = {
            'produto_id': int(np.random.randint(1, cfg.N_PRODUTOS + 1)),
            'tempo_visualizacao_s': int(np.random.randint(5, 180)),
            'scroll_depth': round(float(np.random.uniform(0.2, 1.0)), 2),
        }
    elif tipo_evento == 'add_carrinho':
        dados = {
            'produto_id': int(np.random.randint(1, cfg.N_PRODUTOS + 1)),
            'quantidade': int(np.random.choice([1, 1, 2, 3])),
            'origem': np.random.choice(['pagina_produto', 'busca', 'recomendacao']),
        }
    elif tipo_evento == 'remove_carrinho':
        dados = {
            'produto_id': int(np.random.randint(1, cfg.N_PRODUTOS + 1)),
            'motivo': np.random.choice(['mudou_ideia', 'quantidade_errada', 'encontrou_melhor', None]),
        }
    elif tipo_evento == 'update_quantidade':
        dados = {
            'produto_id': int(np.random.randint(1, cfg.N_PRODUTOS + 1)),
            'quantidade_anterior': int(np.random.randint(1, 4)),
            'quantidade_nova': int(np.random.randint(1, 6)),
        }
    elif tipo_evento == 'view_checkout':
        dados = {
            'etapa': np.random.choice(['endereco', 'pagamento', 'revisao']),
            'tempo_na_etapa_s': int(np.random.randint(10, 300)),
        }
    elif tipo_evento == 'inicio_pagamento':
        dados = {
            'metodo': np.random.choice(list(cfg.METODOS_PAGAMENTO.keys())),
            'parcelas': int(np.random.choice([1, 2, 3, 6, 10, 12])),
        }
    elif tipo_evento == 'erro_pagamento':
        dados = {
            'codigo_erro': np.random.choice(['cartao_recusado', 'saldo_insuficiente', 'timeout', 'dados_invalidos']),
            'metodo': np.random.choice(list(cfg.METODOS_PAGAMENTO.keys())),
        }
    elif tipo_evento == 'abandono':
        dados = {
            'pagina_saida': np.random.choice(['checkout', 'carrinho', 'pagamento', 'produto']),
            'tempo_inativo_s': int(np.random.randint(1800, 7200)),  # 30min - 2h
        }
    elif tipo_evento == 'retorno':
        dados = {
            'origem_retorno': np.random.choice(['email_link', 'whatsapp_link', 'direto', 'push']),
            'horas_desde_abandono': int(np.random.randint(1, 96)),
        }

    return json.dumps(dados, ensure_ascii=False) if dados else None


def _gerar_sequencia_eventos(lifecycle, motivo_abandono):
    """Gera sequência de tipos de evento baseada no lifecycle do carrinho."""
    if lifecycle == 'direto_comprado':
        base = list(FLUXO_COMPRADO)
    elif lifecycle in ('abandonado', 'expirado'):
        if motivo_abandono == 'pagamento':
            base = list(FLUXO_ABANDONADO_PAGAMENTO)
        else:
            base = list(FLUXO_ABANDONADO)
    elif lifecycle in ('recuperado_comprado', 'recuperado_pendente'):
        base = list(FLUXO_RECUPERADO)
    elif lifecycle == 'ativo':
        # Sessão em andamento: apenas views e adds parciais
        n_events = int(np.random.randint(2, 6))
        base = []
        for _ in range(n_events):
            base.append(np.random.choice(['view_produto', 'add_carrinho', 'view_produto']))
        return base
    else:
        base = list(FLUXO_ABANDONADO)

    # Adicionar eventos extras aleatórios para variar o volume
    extras = int(np.random.randint(0, 8))
    for _ in range(extras):
        pos = np.random.randint(1, max(2, len(base) - 1))
        evento = np.random.choice([
            'view_produto', 'view_produto', 'add_carrinho',
            'remove_carrinho', 'update_quantidade', 'view_produto',
        ])
        base.insert(pos, evento)

    return base


def generate(carrinhos_df):
    """
    Gera DataFrame de eventos de carrinho (time series comportamental).

    Args:
        carrinhos_df: DataFrame de carrinhos (com _lifecycle, cliente_id, timestamps)
    """
    np.random.seed(cfg.SEED + 3)

    rows = []
    evento_id = 1

    for _, carrinho in carrinhos_df.iterrows():
        lifecycle = carrinho.get('_lifecycle', 'abandonado')
        motivo = carrinho.get('motivo_abandono', None)
        sessao_id = str(uuid.uuid4())[:12]
        data_base = carrinho['data_criacao']
        duracao = carrinho.get('duracao_sessao_minutos', 15)
        if pd.isna(duracao) or duracao < 2:
            duracao = 15

        # Gerar sequência de eventos
        sequencia = _gerar_sequencia_eventos(lifecycle, motivo)

        # Distribuir no tempo da sessão
        total_eventos = len(sequencia)
        intervalo_base = duracao * 60 / max(total_eventos, 1)  # segundos entre eventos

        timestamp_atual = data_base

        for idx, tipo_evento in enumerate(sequencia):
            # Intervalo entre eventos: variação aleatória
            if idx > 0:
                delta_s = max(1, int(intervalo_base * np.random.uniform(0.3, 1.7)))
                timestamp_atual = timestamp_atual + timedelta(seconds=delta_s)

            # Se é retorno (após abandono), pular tempo
            if tipo_evento == 'retorno' and carrinho['data_abandono'] is not None:
                horas_retorno = int(np.random.randint(1, 72))
                if pd.notna(carrinho['data_abandono']):
                    timestamp_atual = carrinho['data_abandono'] + timedelta(hours=horas_retorno)
                sessao_id = str(uuid.uuid4())[:12]  # nova sessão

            duracao_evento = int(np.random.randint(2, 120)) if tipo_evento != 'abandono' else None
            dados_evento = _gerar_dados_evento(tipo_evento, carrinho)

            rows.append({
                'evento_id':                evento_id,
                'carrinho_id':              carrinho['carrinho_id'],
                'cliente_id':               carrinho['cliente_id'],
                'sessao_id':                sessao_id,
                'timestamp_evento':         timestamp_atual,
                'tipo_evento':              tipo_evento,
                'duracao_evento_segundos':  duracao_evento,
                'dados_evento':             dados_evento,
            })
            evento_id += 1

    df = pd.DataFrame(rows)
    df['timestamp_evento'] = pd.to_datetime(df['timestamp_evento'], utc=True)

    return df


if __name__ == '__main__':
    import clientes as gen_clientes
    import carrinhos as gen_carrinhos

    clientes_df = gen_clientes.generate()
    carrinhos_df = gen_carrinhos.generate(clientes_df)
    df = generate(carrinhos_df)
    print(f"✓ Eventos Carrinho: {len(df)} registros")
    print(f"  Média eventos/carrinho: {len(df)/len(carrinhos_df):.1f}")
    print(f"  Tipos: {df['tipo_evento'].value_counts().to_dict()}")
