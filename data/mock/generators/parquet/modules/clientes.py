"""
Módulo Gerador: Clientes.
"""
from typing import Dict, Any, Optional
from datetime import date, timedelta
import pandas as pd
import numpy as np
from faker import Faker

try:
    from config.constants import RFM_DIST
    from config.settings import GeneratorSettings
    from core.base_generator import BaseGenerator
except (ImportError, ValueError):
    from ..config.constants import RFM_DIST
    from ..config.settings import GeneratorSettings
    from ..core.base_generator import BaseGenerator


class ClientesGenerator(BaseGenerator):
    name = "clientes"
    dependencies = []

    def generate_raw(self, **context) -> pd.DataFrame:
        fake = Faker('pt_BR')
        Faker.seed(self.seed)
        np.random.seed(self.seed)

        n_clientes = self.settings.volumes.n_clientes
        segmentos = list(RFM_DIST.keys())
        seg_weights = list(RFM_DIST.values())

        rows = []
        emails_usados = set()
        ref_date = date(2026, 6, 30)

        for i in range(1, n_clientes + 1):
            segmento = np.random.choice(segmentos, p=seg_weights)
            primeiro_nome = fake.first_name()
            ultimo_nome = fake.last_name() if np.random.random() > 0.04 else None

            sobrenome_slug = (ultimo_nome or fake.last_name()).lower().replace(' ', '').replace("'", "")
            base_email = f"{primeiro_nome.lower()}.{sobrenome_slug}{np.random.randint(1, 999)}@{fake.free_email_domain()}"
            while base_email.lower() in emails_usados:
                base_email = f"{primeiro_nome.lower()}{np.random.randint(1, 9999)}@{fake.free_email_domain()}"
            emails_usados.add(base_email.lower())

            telefone = fake.cellphone_number() if np.random.random() > 0.08 else None

            if segmento == 'premium':
                total_compras = int(np.random.randint(5, 26))
                lifetime_value = round(float(np.random.uniform(2000, 15000)), 2)
                data_primeira = ref_date - timedelta(days=int(np.random.randint(180, 730)))
                data_ultima = ref_date - timedelta(days=int(np.random.randint(1, 30)))
                data_criacao = self.settings.data_inicio - timedelta(days=int(np.random.randint(180, 730)))
            elif segmento == 'regular':
                total_compras = int(np.random.randint(2, 5))
                lifetime_value = round(float(np.random.uniform(500, 2000)), 2)
                data_primeira = ref_date - timedelta(days=int(np.random.randint(90, 365)))
                data_ultima = ref_date - timedelta(days=int(np.random.randint(1, 90)))
                data_criacao = self.settings.data_inicio - timedelta(days=int(np.random.randint(90, 400)))
            elif segmento == 'dormant':
                total_compras = 1
                lifetime_value = round(float(np.random.uniform(50, 500)), 2)
                data_primeira = ref_date - timedelta(days=int(np.random.randint(180, 730)))
                data_ultima = data_primeira
                data_criacao = self.settings.data_inicio - timedelta(days=int(np.random.randint(180, 730)))
            else:  # novo
                total_compras = 0
                lifetime_value = 0.0
                data_primeira = None
                data_ultima = None
                days_into_period = int(np.random.randint(0, 180))
                data_criacao = self.settings.data_inicio + timedelta(days=days_into_period)

            rows.append({
                'cliente_id':           i,
                'primeiro_nome':        primeiro_nome,
                'ultimo_nome':          ultimo_nome,
                'email':                base_email,
                'telefone':             telefone,
                'segmento_rfm':         segmento,
                'data_primeira_compra': data_primeira,
                'data_ultima_compra':   data_ultima,
                'total_compras':        total_compras,
                'lifetime_value':       lifetime_value,
                'permite_email':        bool(np.random.random() > 0.05),
                'permite_sms':          bool(np.random.random() > 0.70),
                'permite_push':         bool(np.random.random() > 0.65),
                'status_ativo':         bool(np.random.random() > 0.03),
                'data_criacao':         data_criacao,
            })

        df = pd.DataFrame(rows)
        df['data_criacao'] = pd.to_datetime(df['data_criacao'], utc=True)
        df['data_primeira_compra'] = pd.to_datetime(df['data_primeira_compra'])
        df['data_ultima_compra'] = pd.to_datetime(df['data_ultima_compra'])
        return df

    def apply_anomalies(self, df: pd.DataFrame) -> pd.DataFrame:
        total = len(df)
        anom_cfg = self.settings.anomalies
        used_indices = set()

        # 1. Cotas garantidas de e-mails nulos
        null_idx = self.engine.get_guaranteed_indices(total, anom_cfg.min_null_emails_pct, seed=self.seed + 101, exclude_indices=used_indices)
        df.loc[null_idx, 'email'] = None
        used_indices.update(null_idx)
        self.audit.record('email_null', anom_cfg.min_null_emails_pct, len(null_idx), total, "E-mails nulos / ausentes para teste de completude cadastral")

        # 2. Cotas garantidas de e-mails malformados
        inv_idx = self.engine.get_guaranteed_indices(total, anom_cfg.min_invalid_emails_pct, seed=self.seed + 102, exclude_indices=used_indices)
        for idx in inv_idx:
            orig = str(df.loc[idx, 'email'] or 'usuario@dominio.com')
            df.loc[idx, 'email'] = orig.replace('@', '@@').replace('.com', '..com_invalido')
        used_indices.update(inv_idx)
        self.audit.record('email_invalido', anom_cfg.min_invalid_emails_pct, len(inv_idx), total, "E-mails com sintaxe inválida (ANOM-01)")

        # 3. Cotas garantidas de casing inconsistente
        case_idx = self.engine.get_guaranteed_indices(total, anom_cfg.min_casing_inconsistent_pct, seed=self.seed + 103, exclude_indices=used_indices)
        for idx in case_idx:
            email_val = df.loc[idx, 'email']
            if email_val:
                df.loc[idx, 'email'] = ''.join(c.upper() if i % 2 == 0 else c.lower() for i, c in enumerate(email_val))
        self.audit.record('email_casing', anom_cfg.min_casing_inconsistent_pct, len(case_idx), total, "E-mails com caixa alta/mista despadronizada")

        # 4. Telefones sem máscara
        phone_mask_idx = df[df['telefone'].notna()].index.values
        if len(phone_mask_idx) > 0:
            unmasked_idx = self.engine.get_guaranteed_indices(len(phone_mask_idx), anom_cfg.min_unmasked_phones_pct, seed=self.seed + 104)
            actual_phone_idx = phone_mask_idx[unmasked_idx]
            for idx in actual_phone_idx:
                t = str(df.loc[idx, 'telefone'])
                df.loc[idx, 'telefone'] = t.replace('(', '').replace(')', '').replace('-', '').replace(' ', '')
            self.audit.record('telefone_sem_mascara', anom_cfg.min_unmasked_phones_pct, len(actual_phone_idx), total, "Telefones sem máscara ou formatação")

        # 5. Inconsistência LTV vs Compras
        novo_idx = df[df['total_compras'] == 0].index.values
        if len(novo_idx) > 0:
            ltv_anom_sub = self.engine.get_guaranteed_indices(len(novo_idx), anom_cfg.min_ltv_inconsistency_pct, seed=self.seed + 105)
            actual_ltv_idx = novo_idx[ltv_anom_sub]
            for idx in actual_ltv_idx:
                df.loc[idx, 'lifetime_value'] = round(float(np.random.uniform(500, 3000)), 2)
            self.audit.record('ltv_inconsistente', anom_cfg.min_ltv_inconsistency_pct, len(actual_ltv_idx), total, "LTV positivo para cliente sem compras (ANOM-02)")

        return df


def generate(settings: Optional[GeneratorSettings] = None) -> pd.DataFrame:
    if settings is None:
        try:
            from config.profiles import get_standard_profile
        except (ImportError, ValueError):
            from ..config.profiles import get_standard_profile
        settings = get_standard_profile()
    generator = ClientesGenerator(settings)
    return generator.run()
