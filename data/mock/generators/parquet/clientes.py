"""
Generator: clientes
Gera ~1.200 clientes com segmentação RFM e preferências de contato.
Dirty data: emails com casing variado (~5%), telefones sem máscara, nulos em opcionais.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import pandas as pd
import numpy as np
from faker import Faker
from datetime import date, timedelta
import _config as cfg

fake = Faker('pt_BR')


def generate():
    """Gera DataFrame de clientes com distribuição RFM e dirty data."""
    Faker.seed(cfg.SEED)
    np.random.seed(cfg.SEED)

    segmentos = list(cfg.RFM_DIST.keys())
    seg_weights = list(cfg.RFM_DIST.values())

    rows = []
    emails_usados = set()

    for i in range(1, cfg.N_CLIENTES + 1):
        segmento = np.random.choice(segmentos, p=seg_weights)

        primeiro_nome = fake.first_name()
        ultimo_nome = fake.last_name() if np.random.random() > 0.04 else None

        # Gerar email único
        base_email = f"{primeiro_nome.lower()}.{fake.last_name().lower()}{np.random.randint(1, 999)}@{fake.free_email_domain()}"
        base_email = base_email.replace(' ', '').replace("'", "")

        # Dirty data: ~5% emails com casing inconsistente
        if np.random.random() < cfg.DIRTY_RATE:
            base_email = ''.join(
                c.upper() if np.random.random() > 0.5 else c.lower()
                for c in base_email
            )

        # Garantir unicidade
        while base_email.lower() in emails_usados:
            base_email = f"{primeiro_nome.lower()}{np.random.randint(1, 9999)}@{fake.free_email_domain()}"
        emails_usados.add(base_email.lower())

        # Telefone
        telefone = fake.cellphone_number() if np.random.random() > 0.08 else None
        # Dirty data: ~5% telefones sem máscara
        if telefone and np.random.random() < cfg.DIRTY_RATE:
            telefone = telefone.replace('(', '').replace(')', '').replace('-', '').replace(' ', '')

        # Atributos baseados no segmento RFM
        ref_date = date(2026, 6, 30)

        if segmento == 'premium':
            total_compras = int(np.random.randint(5, 26))
            lifetime_value = round(float(np.random.uniform(2000, 15000)), 2)
            data_primeira = ref_date - timedelta(days=int(np.random.randint(180, 730)))
            data_ultima = ref_date - timedelta(days=int(np.random.randint(1, 30)))
            data_criacao = cfg.PERIODO_INICIO - timedelta(days=int(np.random.randint(180, 730)))

        elif segmento == 'regular':
            total_compras = int(np.random.randint(2, 5))
            lifetime_value = round(float(np.random.uniform(500, 2000)), 2)
            data_primeira = ref_date - timedelta(days=int(np.random.randint(90, 365)))
            data_ultima = ref_date - timedelta(days=int(np.random.randint(1, 90)))
            data_criacao = cfg.PERIODO_INICIO - timedelta(days=int(np.random.randint(90, 400)))

        elif segmento == 'dormant':
            total_compras = 1
            lifetime_value = round(float(np.random.uniform(50, 500)), 2)
            data_primeira = ref_date - timedelta(days=int(np.random.randint(180, 730)))
            data_ultima = data_primeira
            data_criacao = cfg.PERIODO_INICIO - timedelta(days=int(np.random.randint(180, 730)))

        else:  # novo
            total_compras = 0
            lifetime_value = 0.0
            data_primeira = None
            data_ultima = None
            # Novos se cadastram durante o período de análise
            days_into_period = int(np.random.randint(0, 180))
            data_criacao = cfg.PERIODO_INICIO + timedelta(days=days_into_period)

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


if __name__ == '__main__':
    df = generate()
    print(f"✓ Clientes: {len(df)} registros")
    print(f"  Distribuição RFM: {df['segmento_rfm'].value_counts().to_dict()}")
    print(f"  Emails nulos: {df['email'].isna().sum()}")
    print(f"  Telefones nulos: {df['telefone'].isna().sum()}")
    print(df.head())
