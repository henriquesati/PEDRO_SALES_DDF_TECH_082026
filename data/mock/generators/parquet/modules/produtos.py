"""
Módulo Gerador: Produtos.
"""
from typing import Optional
from datetime import timedelta
import pandas as pd
import numpy as np

try:
    from config.constants import CATEGORIAS, NOMES_PRODUTO_TEMPLATES, SUFIXOS_PRODUTO
    from config.settings import GeneratorSettings
    from core.base_generator import BaseGenerator
except (ImportError, ValueError):
    from ..config.constants import CATEGORIAS, NOMES_PRODUTO_TEMPLATES, SUFIXOS_PRODUTO
    from ..config.settings import GeneratorSettings
    from ..core.base_generator import BaseGenerator


class ProdutosGenerator(BaseGenerator):
    name = "produtos"
    dependencies = []

    def generate_raw(self, **context) -> pd.DataFrame:
        np.random.seed(self.seed)

        n_produtos = self.settings.volumes.n_produtos
        categorias = list(CATEGORIAS.keys())
        pesos_cat = [CATEGORIAS[c]['peso'] for c in categorias]

        qtds = np.random.multinomial(n_produtos, pesos_cat)
        rows = []
        produto_id = 1

        for cat, qtd in zip(categorias, qtds):
            info = CATEGORIAS[cat]
            preco_min, preco_max = info['faixa_preco']

            for _ in range(qtd):
                subcat = np.random.choice(info['subcategorias'])
                marca = np.random.choice(info['marcas'])

                templates = NOMES_PRODUTO_TEMPLATES.get(cat, {}).get(subcat, ['{m} Produto'])
                template = np.random.choice(templates)
                sufixo = np.random.choice(SUFIXOS_PRODUTO)
                nome = template.format(m=sufixo)

                preco_original = round(float(np.random.uniform(preco_min, preco_max)), 2)

                if np.random.random() < 0.30:
                    desconto = np.random.uniform(0.05, 0.35)
                    preco_atual = round(preco_original * (1 - desconto), 2)
                else:
                    preco_atual = preco_original

                tem_avaliacao = np.random.random() > self.settings.anomalies.min_missing_evaluations_pct
                if tem_avaliacao:
                    avaliacao_media = round(float(np.clip(np.random.normal(3.8, 0.8), 1.0, 5.0)), 1)
                    total_avaliacoes = int(np.random.randint(1, 2000))
                else:
                    avaliacao_media = None
                    total_avaliacoes = 0

                days_offset = int(np.random.randint(0, 365))
                data_cadastro = self.settings.data_inicio - timedelta(days=days_offset)

                rows.append({
                    'produto_id':       produto_id,
                    'nome':             f"{marca} {nome}",
                    'categoria':        cat,
                    'subcategoria':     subcat,
                    'marca':            marca,
                    'preco_atual':      preco_atual,
                    'preco_original':   preco_original,
                    'em_estoque':       bool(np.random.random() > 0.08),
                    'avaliacao_media':  avaliacao_media,
                    'total_avaliacoes': total_avaliacoes,
                    'url_imagem':       f"https://cdn.marketplace.com.br/img/{produto_id}.jpg",
                    'data_cadastro':    data_cadastro,
                    'ativo':            bool(np.random.random() > 0.05),
                })
                produto_id += 1

        df = pd.DataFrame(rows)
        df['data_cadastro'] = pd.to_datetime(df['data_cadastro'], utc=True)
        return df

    def apply_anomalies(self, df: pd.DataFrame) -> pd.DataFrame:
        total = len(df)
        anom_cfg = self.settings.anomalies

        inv_idx = self.engine.get_guaranteed_indices(total, anom_cfg.min_inverted_price_pct, seed=self.seed + 201)
        for idx in inv_idx:
            orig = df.loc[idx, 'preco_original']
            df.loc[idx, 'preco_atual'] = round(orig * float(np.random.uniform(1.10, 1.45)), 2)
        self.audit.record('preco_invertido', anom_cfg.min_inverted_price_pct, len(inv_idx), total, "Preço promocional maior que original (promoção invertida)")

        return df


def generate(settings: Optional[GeneratorSettings] = None) -> pd.DataFrame:
    if settings is None:
        try:
            from config.profiles import get_standard_profile
        except (ImportError, ValueError):
            from ..config.profiles import get_standard_profile
        settings = get_standard_profile()
    generator = ProdutosGenerator(settings)
    return generator.run()
