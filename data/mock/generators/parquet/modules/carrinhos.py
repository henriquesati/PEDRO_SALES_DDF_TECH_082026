"""
Módulo Gerador: Carrinhos.
"""
from typing import Dict, Any, Optional
from datetime import timedelta
import pandas as pd
import numpy as np

try:
    from config.constants import (
        LIFECYCLE_DIST, LIFECYCLE_TO_STATUS, MOTIVOS_ABANDONO,
        DISPOSITIVOS, BROWSERS, CANAIS_ORIGEM, SAZONALIDADE_MESES
    )
    from config.settings import GeneratorSettings
    from core.base_generator import BaseGenerator
except (ImportError, ValueError):
    from ..config.constants import (
        LIFECYCLE_DIST, LIFECYCLE_TO_STATUS, MOTIVOS_ABANDONO,
        DISPOSITIVOS, BROWSERS, CANAIS_ORIGEM, SAZONALIDADE_MESES
    )
    from ..config.settings import GeneratorSettings
    from ..core.base_generator import BaseGenerator


class CarrinhosGenerator(BaseGenerator):
    name = "carrinhos"
    dependencies = ["clientes"]

    def generate_raw(self, **context) -> pd.DataFrame:
        clientes_df = context.get('clientes_df')
        if clientes_df is None:
            try:
                from modules.clientes import ClientesGenerator
            except (ImportError, ValueError):
                from .clientes import ClientesGenerator
            clientes_df = ClientesGenerator(self.settings).run()

        np.random.seed(self.seed + 1)

        cliente_ids = clientes_df['cliente_id'].values
        cliente_rfm = dict(zip(clientes_df['cliente_id'], clientes_df['segmento_rfm']))

        lifecycles = list(LIFECYCLE_DIST.keys())
        lc_weights = list(LIFECYCLE_DIST.values())

        dispositivos = list(DISPOSITIVOS.keys())
        disp_weights = list(DISPOSITIVOS.values())

        canais = list(CANAIS_ORIGEM.keys())
        canais_weights = list(CANAIS_ORIGEM.values())

        motivos = list(MOTIVOS_ABANDONO.keys())
        motivos_weights = list(MOTIVOS_ABANDONO.values())

        n_carrinhos = self.settings.volumes.n_carrinhos
        rows = []

        for i in range(1, n_carrinhos + 1):
            lifecycle = np.random.choice(lifecycles, p=lc_weights)
            status = LIFECYCLE_TO_STATUS[lifecycle]
            cliente_id = int(np.random.choice(cliente_ids))
            segmento = cliente_rfm.get(cliente_id, 'regular')

            mes = np.random.choice(range(6), p=SAZONALIDADE_MESES)
            dia_no_mes = int(np.random.randint(1, 29))
            hora = int(np.random.randint(6, 24))
            minuto = int(np.random.randint(0, 60))
            data_criacao = self.settings.data_inicio.replace(
                month=mes + 1, day=dia_no_mes, hour=hora, minute=minuto
            )

            dispositivo = np.random.choice(dispositivos, p=disp_weights)
            browser = np.random.choice(BROWSERS[dispositivo])
            canal_origem = np.random.choice(canais, p=canais_weights)
            cliente_novo = (segmento == 'novo')

            if lifecycle == 'ativo':
                duracao = int(np.random.randint(5, 60))
            elif lifecycle == 'direto_comprado':
                duracao = int(np.random.randint(10, 90))
            else:
                duracao = int(np.random.randint(3, 45))

            data_ultima_atividade = data_criacao + timedelta(minutes=duracao)

            n_itens_estimado = max(1, int(np.random.normal(3, 1.2)))
            valor_subtotal = round(float(np.random.uniform(30, 800)) * (n_itens_estimado / 3), 2)
            valor_frete = round(float(np.random.uniform(5, 45)), 2)
            valor_desconto = 0.0

            data_abandono = None
            motivo_abandono = None

            if lifecycle in ('abandonado', 'recuperado_comprado', 'recuperado_pendente', 'expirado'):
                minutos_ate_abandono = int(np.random.randint(5, duracao + 1)) if duracao > 5 else 5
                data_abandono = data_criacao + timedelta(minutes=minutos_ate_abandono)
                data_ultima_atividade = data_abandono
                motivo_abandono = np.random.choice(motivos, p=motivos_weights)

                if lifecycle in ('recuperado_comprado', 'recuperado_pendente'):
                    desconto_pct = np.random.uniform(0.05, 0.15)
                    valor_desconto = round(valor_subtotal * desconto_pct, 2)

            valor_total = round(valor_subtotal + valor_frete - valor_desconto, 2)

            rows.append({
                'carrinho_id':              i,
                'cliente_id':               cliente_id,
                'data_criacao':             data_criacao,
                'data_ultima_atividade':    data_ultima_atividade,
                'data_abandono':            data_abandono,
                'status':                   status,
                'motivo_abandono':          motivo_abandono,
                'valor_subtotal':           valor_subtotal,
                'valor_frete':              valor_frete,
                'valor_desconto':           valor_desconto,
                'valor_total':              valor_total,
                'duracao_sessao_minutos':   duracao,
                'dispositivo':              dispositivo,
                'browser':                  browser,
                'canal_origem':             canal_origem,
                'cliente_novo':             cliente_novo,
                'tem_conta_criada':         not cliente_novo or np.random.random() > 0.30,
                'created_at':               data_criacao,
                'updated_at':               data_ultima_atividade,
                '_lifecycle':               lifecycle,
                '_segmento_rfm':            segmento,
            })

        df = pd.DataFrame(rows)
        for col in ['data_criacao', 'data_ultima_atividade', 'data_abandono', 'created_at', 'updated_at']:
            df[col] = pd.to_datetime(df[col], utc=True)
        return df

    def apply_anomalies(self, df: pd.DataFrame) -> pd.DataFrame:
        total = len(df)
        anom_cfg = self.settings.anomalies
        used_indices = set()

        # 1. ANOM-01: Frete negativo
        frete_neg_idx = self.engine.get_guaranteed_indices(total, anom_cfg.min_negative_freight_pct, seed=self.seed + 301, exclude_indices=used_indices)
        for idx in frete_neg_idx:
            val_frete_neg = round(-abs(float(np.random.uniform(5, 30))), 2)
            df.loc[idx, 'valor_frete'] = val_frete_neg
            df.loc[idx, 'valor_total'] = round(df.loc[idx, 'valor_subtotal'] + val_frete_neg - df.loc[idx, 'valor_desconto'], 2)
        used_indices.update(frete_neg_idx)
        self.audit.record('frete_negativo', anom_cfg.min_negative_freight_pct, len(frete_neg_idx), total, "Valor de frete negativo gerando risco financeiro (ANOM-01)")

        # 2. ANOM-04: Divergência contábil no valor total
        total_incons_idx = self.engine.get_guaranteed_indices(total, anom_cfg.min_total_inconsistency_pct, seed=self.seed + 302, exclude_indices=used_indices)
        for idx in total_incons_idx:
            df.loc[idx, 'valor_total'] = round(df.loc[idx, 'valor_total'] * float(np.random.choice([0.75, 1.25, 1.40])), 2)
        used_indices.update(total_incons_idx)
        self.audit.record('total_inconsistente', anom_cfg.min_total_inconsistency_pct, len(total_incons_idx), total, "Valor total divergente da soma subtotal + frete - desconto (ANOM-04)")

        # 3. ANOM-02: Subtotal zerado ou negativo
        sub_zero_idx = self.engine.get_guaranteed_indices(total, anom_cfg.min_zero_or_negative_subtotal_pct, seed=self.seed + 303, exclude_indices=used_indices)
        for idx in sub_zero_idx:
            df.loc[idx, 'valor_subtotal'] = 0.00
            df.loc[idx, 'valor_total'] = round(df.loc[idx, 'valor_frete'] - df.loc[idx, 'valor_desconto'], 2)
        used_indices.update(sub_zero_idx)
        self.audit.record('subtotal_zerado', anom_cfg.min_zero_or_negative_subtotal_pct, len(sub_zero_idx), total, "Subtotal zerado em sessão com itens (ANOM-02)")

        # 4. ANOM-03: Desconto excessivo
        desc_anom_idx = self.engine.get_guaranteed_indices(total, anom_cfg.min_excessive_discount_pct, seed=self.seed + 304, exclude_indices=used_indices)
        for idx in desc_anom_idx:
            sub = df.loc[idx, 'valor_subtotal']
            df.loc[idx, 'valor_desconto'] = round(sub * float(np.random.uniform(1.2, 2.0)), 2)
            df.loc[idx, 'valor_total'] = round(sub + df.loc[idx, 'valor_frete'] - df.loc[idx, 'valor_desconto'], 2)
        self.audit.record('desconto_excessivo', anom_cfg.min_excessive_discount_pct, len(desc_anom_idx), total, "Desconto maior que subtotal gerando valor líquido negativo (ANOM-03)")

        return df


def generate(clientes_df: pd.DataFrame, settings: Optional[GeneratorSettings] = None) -> pd.DataFrame:
    if settings is None:
        try:
            from config.profiles import get_standard_profile
        except (ImportError, ValueError):
            from ..config.profiles import get_standard_profile
        settings = get_standard_profile()
    generator = CarrinhosGenerator(settings)
    return generator.run(clientes_df=clientes_df)


def save_df(df: pd.DataFrame) -> pd.DataFrame:
    return df.drop(columns=[c for c in df.columns if c.startswith('_')]) if any(c.startswith('_') for c in df.columns) else df
