"""
Generator: pedidos
Gera ~1.800 pedidos (compras diretas + recuperadas) fechando o ciclo carrinho → conversão.
Vincula pedidos de recuperação ao resgate_id correspondente.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import pandas as pd
import numpy as np
from datetime import timedelta
import _config as cfg


def generate(carrinhos_df, clientes_df, resgate_df):
    """
    Gera DataFrame de pedidos para carrinhos com status 'comprado'.

    Args:
        carrinhos_df: DataFrame com _lifecycle e valores monetários
        clientes_df: DataFrame de clientes
        resgate_df: DataFrame de eventos de resgate (para vincular resgate_id)
    """
    np.random.seed(cfg.SEED + 5)

    # Filtrar carrinhos comprados
    comprados = carrinhos_df[carrinhos_df['status'] == 'comprado'].copy()

    # Mapear resgate_id → carrinho_id (pegar o resgate que converteu)
    resgate_sucesso = {}
    if resgate_df is not None and len(resgate_df) > 0:
        conversoes = resgate_df[resgate_df['sucesso'] == True]
        for _, r in conversoes.iterrows():
            resgate_sucesso[r['carrinho_id']] = r['resgate_id']

    metodos = list(cfg.METODOS_PAGAMENTO.keys())
    metodos_weights = list(cfg.METODOS_PAGAMENTO.values())
    statuses = list(cfg.STATUS_PEDIDO.keys())
    status_weights = list(cfg.STATUS_PEDIDO.values())

    rows = []
    pedido_id = 1

    for _, carrinho in comprados.iterrows():
        lifecycle = carrinho.get('_lifecycle', 'direto_comprado')
        is_recuperado = lifecycle == 'recuperado_comprado'

        # Data do pedido
        if is_recuperado and carrinho['carrinho_id'] in resgate_sucesso:
            # Pedido ocorre após a conversão do resgate
            resgate_row = resgate_df[resgate_df['resgate_id'] == resgate_sucesso[carrinho['carrinho_id']]]
            if len(resgate_row) > 0 and pd.notna(resgate_row.iloc[0]['data_conversao']):
                data_pedido = resgate_row.iloc[0]['data_conversao'] + timedelta(minutes=int(np.random.randint(1, 30)))
            else:
                data_pedido = carrinho['data_criacao'] + timedelta(hours=int(np.random.randint(1, 96)))
        else:
            # Pedido direto: durante a sessão
            duracao = carrinho.get('duracao_sessao_minutos', 30)
            if pd.isna(duracao):
                duracao = 30
            data_pedido = carrinho['data_criacao'] + timedelta(minutes=int(duracao))

        # Valores
        valor_subtotal = carrinho['valor_subtotal']
        valor_frete = max(0, carrinho['valor_frete'])  # Corrigir frete negativo para pedido
        valor_desconto = carrinho['valor_desconto'] if not pd.isna(carrinho['valor_desconto']) else 0.0

        # Para recuperados, aplicar desconto do resgate
        if is_recuperado and carrinho['carrinho_id'] in resgate_sucesso:
            resgate_row = resgate_df[resgate_df['resgate_id'] == resgate_sucesso[carrinho['carrinho_id']]]
            if len(resgate_row) > 0:
                desc_resgate = resgate_row.iloc[0]['desconto_oferecido']
                if not pd.isna(desc_resgate):
                    valor_desconto = float(desc_resgate)
                if resgate_row.iloc[0].get('frete_gratis_oferecido', False):
                    valor_frete = 0.0

        valor_total = round(float(valor_subtotal + valor_frete - valor_desconto), 2)
        valor_total = max(valor_total, 1.0)  # Nunca negativo

        metodo = np.random.choice(metodos, p=metodos_weights)
        status_pedido = np.random.choice(statuses, p=status_weights)

        # Resgate_id para pedidos recuperados
        resgate_id = None
        if is_recuperado and carrinho['carrinho_id'] in resgate_sucesso:
            resgate_id = int(resgate_sucesso[carrinho['carrinho_id']])

        rows.append({
            'pedido_id':            pedido_id,
            'carrinho_id':          carrinho['carrinho_id'],
            'cliente_id':           carrinho['cliente_id'],
            'data_pedido':          data_pedido,
            'valor_subtotal':       round(float(valor_subtotal), 2),
            'valor_frete':          round(float(valor_frete), 2),
            'valor_desconto':       round(float(valor_desconto), 2),
            'valor_total':          round(float(valor_total), 2),
            'metodo_pagamento':     metodo,
            'status_pedido':        status_pedido,
            'origem_recuperacao':   is_recuperado,
            'resgate_id':           resgate_id,
            'created_at':           data_pedido,
        })
        pedido_id += 1

    df = pd.DataFrame(rows)
    df['data_pedido'] = pd.to_datetime(df['data_pedido'], utc=True)
    df['created_at'] = pd.to_datetime(df['created_at'], utc=True)

    # Converter resgate_id para nullable int
    df['resgate_id'] = df['resgate_id'].astype('Int64')

    return df


if __name__ == '__main__':
    import clientes as gen_clientes
    import carrinhos as gen_carrinhos
    import eventos_resgate as gen_resgate

    clientes_df = gen_clientes.generate()
    carrinhos_df = gen_carrinhos.generate(clientes_df)
    resgate_df = gen_resgate.generate(carrinhos_df, clientes_df)
    df = generate(carrinhos_df, clientes_df, resgate_df)

    print(f"✓ Pedidos: {len(df)} registros")
    print(f"  Recuperados: {df['origem_recuperacao'].sum()} ({df['origem_recuperacao'].mean()*100:.1f}%)")
    print(f"  Métodos: {df['metodo_pagamento'].value_counts().to_dict()}")
    print(f"  Status: {df['status_pedido'].value_counts().to_dict()}")
    print(f"  Valor médio: R${df['valor_total'].mean():.2f}")
