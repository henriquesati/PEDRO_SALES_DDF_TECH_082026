"""
Módulo Gerador: Pedidos.
"""
from typing import Optional
from datetime import timedelta
import pandas as pd
import numpy as np

try:
    from config.constants import METODOS_PAGAMENTO, STATUS_PEDIDO
    from config.settings import GeneratorSettings
    from core.base_generator import BaseGenerator
except (ImportError, ValueError):
    from ..config.constants import METODOS_PAGAMENTO, STATUS_PEDIDO
    from ..config.settings import GeneratorSettings
    from ..core.base_generator import BaseGenerator


class PedidosGenerator(BaseGenerator):
    name = "pedidos"
    dependencies = ["carrinhos", "clientes", "eventos_resgate"]

    def generate_raw(self, **context) -> pd.DataFrame:
        carrinhos_df = context.get('carrinhos_df')
        clientes_df = context.get('clientes_df')
        resgate_df = context.get('resgate_df')

        if carrinhos_df is None:
            raise ValueError("PedidosGenerator requer 'carrinhos_df' no contexto.")

        np.random.seed(self.seed + 5)

        comprados = carrinhos_df[carrinhos_df['status'] == 'comprado'].copy()

        resgate_sucesso = {}
        if resgate_df is not None and len(resgate_df) > 0:
            conversoes = resgate_df[resgate_df['sucesso'] == True]
            for _, r in conversoes.iterrows():
                resgate_sucesso[r['carrinho_id']] = r['resgate_id']

        metodos = list(METODOS_PAGAMENTO.keys())
        metodos_weights = list(METODOS_PAGAMENTO.values())
        statuses = list(STATUS_PEDIDO.keys())
        status_weights = list(STATUS_PEDIDO.values())

        rows = []
        pedido_id = 1

        for _, carrinho in comprados.iterrows():
            lifecycle = carrinho.get('_lifecycle', 'direto_comprado')
            is_recuperado = (lifecycle == 'recuperado_comprado')

            if is_recuperado and carrinho['carrinho_id'] in resgate_sucesso:
                resgate_row = resgate_df[resgate_df['resgate_id'] == resgate_sucesso[carrinho['carrinho_id']]]
                if len(resgate_row) > 0 and pd.notna(resgate_row.iloc[0]['data_conversao']):
                    data_pedido = resgate_row.iloc[0]['data_conversao'] + timedelta(minutes=int(np.random.randint(1, 30)))
                else:
                    data_pedido = carrinho['data_criacao'] + timedelta(hours=int(np.random.randint(1, 96)))
            else:
                duracao = carrinho.get('duracao_sessao_minutos', 30)
                if pd.isna(duracao):
                    duracao = 30
                data_pedido = carrinho['data_criacao'] + timedelta(minutes=int(duracao))

            valor_subtotal = carrinho['valor_subtotal']
            valor_frete = max(0.0, carrinho['valor_frete'])
            valor_desconto = carrinho['valor_desconto'] if pd.notna(carrinho['valor_desconto']) else 0.0

            if is_recuperado and carrinho['carrinho_id'] in resgate_sucesso:
                resgate_row = resgate_df[resgate_df['resgate_id'] == resgate_sucesso[carrinho['carrinho_id']]]
                if len(resgate_row) > 0:
                    desc_resgate = resgate_row.iloc[0]['desconto_oferecido']
                    if pd.notna(desc_resgate):
                        valor_desconto = float(desc_resgate)
                    if resgate_row.iloc[0].get('frete_gratis_oferecido', False):
                        valor_frete = 0.0

            valor_total = round(float(valor_subtotal + valor_frete - valor_desconto), 2)
            valor_total = max(valor_total, 1.0)

            metodo = np.random.choice(metodos, p=metodos_weights)
            status_pedido = np.random.choice(statuses, p=status_weights)

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
        df['resgate_id'] = df['resgate_id'].astype('Int64')
        return df


def generate(carrinhos_df: pd.DataFrame, clientes_df: pd.DataFrame, resgate_df: pd.DataFrame, settings: Optional[GeneratorSettings] = None) -> pd.DataFrame:
    if settings is None:
        try:
            from config.profiles import get_standard_profile
        except (ImportError, ValueError):
            from ..config.profiles import get_standard_profile
        settings = get_standard_profile()
    generator = PedidosGenerator(settings)
    return generator.run(carrinhos_df=carrinhos_df, clientes_df=clientes_df, resgate_df=resgate_df)
