"""
Módulo Gerador: Itens do Carrinho.
"""
from typing import Optional
from datetime import timedelta
import pandas as pd
import numpy as np

try:
    from config.settings import GeneratorSettings
    from core.base_generator import BaseGenerator
except (ImportError, ValueError):
    from ..config.settings import GeneratorSettings
    from ..core.base_generator import BaseGenerator


class ItensCarrinhoGenerator(BaseGenerator):
    name = "itens_carrinho"
    dependencies = ["carrinhos", "produtos"]

    def generate_raw(self, **context) -> pd.DataFrame:
        carrinhos_df = context.get('carrinhos_df')
        produtos_df = context.get('produtos_df')

        if carrinhos_df is None:
            raise ValueError("ItensCarrinhoGenerator requer 'carrinhos_df' no contexto.")
        if produtos_df is None:
            raise ValueError("ItensCarrinhoGenerator requer 'produtos_df' no contexto.")

        np.random.seed(self.seed + 2)

        produto_ids = produtos_df['produto_id'].values
        precos = dict(zip(produtos_df['produto_id'], produtos_df['preco_atual']))

        rows = []
        item_id = 1

        n_carrinhos = len(carrinhos_df)
        empty_cart_idx = set(self.engine.get_guaranteed_indices(
            n_carrinhos,
            self.settings.anomalies.min_empty_or_orphan_carts_pct,
            seed=self.seed + 401
        ))

        for idx, (_, carrinho) in enumerate(carrinhos_df.iterrows()):
            if idx in empty_cart_idx:
                continue

            n_itens = max(1, min(8, int(np.random.normal(self.settings.volumes.itens_por_carrinho_media, 1.2))))

            if n_itens <= len(produto_ids):
                selected_produtos = np.random.choice(produto_ids, size=n_itens, replace=False)
            else:
                selected_produtos = np.random.choice(produto_ids, size=n_itens, replace=True)

            data_base = carrinho['data_criacao']
            duracao = carrinho.get('duracao_sessao_minutos', 10)
            if pd.isna(duracao) or duracao < 1:
                duracao = 10

            for j, prod_id in enumerate(selected_produtos):
                prod_id = int(prod_id)
                preco_unitario = precos.get(prod_id, 99.90)

                if np.random.random() < 0.15:
                    variacao = np.random.uniform(-0.05, 0.05)
                    preco_unitario = round(preco_unitario * (1 + variacao), 2)

                quantidade = int(np.random.choice([1, 1, 1, 2, 2, 3], p=[0.45, 0.15, 0.10, 0.15, 0.10, 0.05]))
                preco_total = round(preco_unitario * quantidade, 2)

                minutos_offset = int(np.random.uniform(0, min(duracao, duracao * (j + 1) / n_itens)))
                data_adicao = data_base + timedelta(minutes=minutos_offset)

                data_remocao = None
                if np.random.random() < 0.20:
                    minutos_remocao = minutos_offset + int(np.random.randint(1, max(2, duracao - minutos_offset)))
                    data_remocao = data_base + timedelta(minutes=minutos_remocao)

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

        self.audit.record(
            'carrinhos_sem_itens',
            self.settings.anomalies.min_empty_or_orphan_carts_pct,
            len(empty_cart_idx),
            n_carrinhos,
            "Sessões de carrinho sem itens adicionados (itens faltando / órfãos)"
        )

        df = pd.DataFrame(rows)
        df['data_adicao'] = pd.to_datetime(df['data_adicao'], utc=True)
        df['data_remocao'] = pd.to_datetime(df['data_remocao'], utc=True)
        return df

    def apply_anomalies(self, df: pd.DataFrame) -> pd.DataFrame:
        total = len(df)
        anom_cfg = self.settings.anomalies

        removidos_idx = df[df['data_remocao'].notna()].index.values
        if len(removidos_idx) > 0:
            inv_sub_idx = self.engine.get_guaranteed_indices(
                len(removidos_idx),
                anom_cfg.min_temporal_inversion_itens_pct,
                seed=self.seed + 402
            )
            actual_inv_idx = removidos_idx[inv_sub_idx]
            for idx in actual_inv_idx:
                df.loc[idx, 'data_remocao'] = df.loc[idx, 'data_adicao'] - timedelta(minutes=int(np.random.randint(1, 30)))
            self.audit.record(
                'inversao_temporal_item',
                anom_cfg.min_temporal_inversion_itens_pct,
                len(actual_inv_idx),
                len(removidos_idx),
                "Data de remoção anterior à data de adição no carrinho"
            )

        return df


def generate(carrinhos_df: pd.DataFrame, produtos_df: pd.DataFrame, settings: Optional[GeneratorSettings] = None) -> pd.DataFrame:
    if settings is None:
        try:
            from config.profiles import get_standard_profile
        except (ImportError, ValueError):
            from ..config.profiles import get_standard_profile
        settings = get_standard_profile()
    generator = ItensCarrinhoGenerator(settings)
    return generator.run(carrinhos_df=carrinhos_df, produtos_df=produtos_df)
