"""
Generator: itens_carrinho
Gera ~18.000 itens de carrinho com snapshot de preço no momento da adição.
Média de ~3 itens por carrinho (range 1-8).
Dirty data: data_remocao < data_adicao (~5%, inversão temporal).
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import pandas as pd
import numpy as np
from datetime import timedelta
import _config as cfg


def generate(carrinhos_df, produtos_df):
    """
    Gera DataFrame de itens por carrinho.

    Args:
        carrinhos_df: DataFrame de carrinhos (com data_criacao, duracao_sessao_minutos)
        produtos_df: DataFrame de produtos (com produto_id, preco_atual)
    """
    np.random.seed(cfg.SEED + 2)

    produto_ids = produtos_df['produto_id'].values
    precos = dict(zip(produtos_df['produto_id'], produtos_df['preco_atual']))

    rows = []
    item_id = 1

    for _, carrinho in carrinhos_df.iterrows():
        # Número de itens: distribuição normal centrada em 3
        n_itens = max(1, min(8, int(np.random.normal(3, 1.2))))

        # Selecionar produtos aleatórios (sem repetição para mesmo carrinho)
        if n_itens <= len(produto_ids):
            selected_produtos = np.random.choice(produto_ids, size=n_itens, replace=False)
        else:
            selected_produtos = np.random.choice(produto_ids, size=n_itens, replace=True)

        data_base = carrinho['data_criacao']
        duracao = carrinho['duracao_sessao_minutos']
        if pd.isna(duracao) or duracao < 1:
            duracao = 10

        for j, prod_id in enumerate(selected_produtos):
            prod_id = int(prod_id)
            preco_unitario = precos.get(prod_id, 99.90)

            # Snapshot de preço: pode variar ±5% do preço atual (simulando mudança)
            if np.random.random() < 0.15:
                variacao = np.random.uniform(-0.05, 0.05)
                preco_unitario = round(preco_unitario * (1 + variacao), 2)

            quantidade = int(np.random.choice([1, 1, 1, 2, 2, 3], p=[0.45, 0.15, 0.10, 0.15, 0.10, 0.05]))
            preco_total = round(preco_unitario * quantidade, 2)

            # Data de adição: distribuída dentro da sessão
            minutos_offset = int(np.random.uniform(0, min(duracao, duracao * (j + 1) / n_itens)))
            data_adicao = data_base + timedelta(minutes=minutos_offset)

            # Alguns itens removidos (~20%)
            data_remocao = None
            if np.random.random() < 0.20:
                minutos_remocao = minutos_offset + int(np.random.randint(1, max(2, duracao - minutos_offset)))
                data_remocao = data_base + timedelta(minutes=minutos_remocao)

            # Dirty data: ~5% data_remocao < data_adicao (inversão temporal)
            if data_remocao and np.random.random() < cfg.DIRTY_RATE:
                data_remocao = data_adicao - timedelta(minutes=int(np.random.randint(1, 30)))

            rows.append({
                'item_id':        item_id,
                'carrinho_id':    carrinho['carrinho_id'],
                'produto_id':     prod_id,
                'quantidade':     quantidade,
                'preco_unitario': preco_unitario,
                'preco_total':    preco_total,
                'data_adicao':    data_adicao,
                'data_remocao':   data_remocao,
            })

            item_id += 1

    df = pd.DataFrame(rows)
    df['data_adicao'] = pd.to_datetime(df['data_adicao'], utc=True)
    df['data_remocao'] = pd.to_datetime(df['data_remocao'], utc=True)

    return df


if __name__ == '__main__':
    import clientes as gen_clientes
    import produtos as gen_produtos
    import carrinhos as gen_carrinhos

    clientes_df = gen_clientes.generate()
    produtos_df = gen_produtos.generate()
    carrinhos_df = gen_carrinhos.generate(clientes_df)

    df = generate(carrinhos_df, produtos_df)
    print(f"✓ Itens Carrinho: {len(df)} registros")
    print(f"  Média itens/carrinho: {len(df)/len(carrinhos_df):.1f}")
    print(f"  Itens removidos: {df['data_remocao'].notna().sum()}")
    dirty = df[df['data_remocao'].notna() & (df['data_remocao'] < df['data_adicao'])]
    print(f"  Dirty (inversão temporal): {len(dirty)} ({len(dirty)/len(df)*100:.1f}%)")
