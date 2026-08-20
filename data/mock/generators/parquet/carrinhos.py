"""
Generator: carrinhos
Gera ~6.000 carrinhos com lifecycle completo (ativo → abandonado → recuperado → comprado).
Métricas-alvo: 70% abandono, 10% recuperação dos abandonados, ~1.800 pedidos.
Dirty data: frete negativo (~3%), valor_total inconsistente (~5%).
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import pandas as pd
import numpy as np
from datetime import timedelta
import _config as cfg


def generate(clientes_df):
    """
    Gera DataFrame de carrinhos com lifecycle e valores monetários.

    Args:
        clientes_df: DataFrame de clientes (precisa de cliente_id, segmento_rfm)

    Returns:
        DataFrame com coluna extra '_lifecycle' para uso downstream (removida no save)
    """
    np.random.seed(cfg.SEED + 1)

    cliente_ids = clientes_df['cliente_id'].values
    cliente_rfm = dict(zip(clientes_df['cliente_id'], clientes_df['segmento_rfm']))

    # Distribuir lifecycles
    lifecycles = list(cfg.LIFECYCLE_DIST.keys())
    lc_weights = list(cfg.LIFECYCLE_DIST.values())

    # Gerar dispositivos e canais para reusar
    dispositivos = list(cfg.DISPOSITIVOS.keys())
    disp_weights = list(cfg.DISPOSITIVOS.values())
    canais = list(cfg.CANAIS_ORIGEM.keys())
    canais_weights = list(cfg.CANAIS_ORIGEM.values())
    motivos = list(cfg.MOTIVOS_ABANDONO.keys())
    motivos_weights = list(cfg.MOTIVOS_ABANDONO.values())

    # Sazonalidade: mais carrinhos em março (pós-carnaval) e maio (dia das mães)
    meses_weights = [0.14, 0.15, 0.19, 0.16, 0.20, 0.16]  # jan-jun

    rows = []

    for i in range(1, cfg.N_CARRINHOS + 1):
        lifecycle = np.random.choice(lifecycles, p=lc_weights)
        status = cfg.LIFECYCLE_TO_STATUS[lifecycle]
        cliente_id = int(np.random.choice(cliente_ids))
        segmento = cliente_rfm.get(cliente_id, 'regular')

        # Data de criação com sazonalidade mensal
        mes = np.random.choice(range(6), p=meses_weights)
        dia_no_mes = int(np.random.randint(1, 29))
        hora = int(np.random.randint(6, 24))
        minuto = int(np.random.randint(0, 60))
        data_criacao = cfg.PERIODO_INICIO.replace(
            month=mes + 1, day=dia_no_mes, hour=hora, minute=minuto
        )

        # Dispositivo e contexto
        dispositivo = np.random.choice(dispositivos, p=disp_weights)
        browser = np.random.choice(cfg.BROWSERS[dispositivo])
        canal_origem = np.random.choice(canais, p=canais_weights)
        cliente_novo = segmento == 'novo'

        # Duração da sessão (minutos)
        if lifecycle == 'ativo':
            duracao = int(np.random.randint(5, 60))
        elif lifecycle == 'direto_comprado':
            duracao = int(np.random.randint(10, 90))
        else:
            duracao = int(np.random.randint(3, 45))

        data_ultima_atividade = data_criacao + timedelta(minutes=duracao)

        # Valores monetários
        n_itens_estimado = max(1, int(np.random.normal(3, 1.2)))
        valor_subtotal = round(float(np.random.uniform(30, 800)) * (n_itens_estimado / 3), 2)
        valor_frete = round(float(np.random.uniform(5, 45)), 2)
        valor_desconto = 0.0
        valor_total = round(valor_subtotal + valor_frete - valor_desconto, 2)

        # Dirty data: ~3% frete negativo
        if np.random.random() < 0.03:
            valor_frete = round(-abs(float(np.random.uniform(5, 30))), 2)
            valor_total = round(valor_subtotal + valor_frete - valor_desconto, 2)

        # Dirty data: ~5% valor_total inconsistente com cálculo
        if np.random.random() < 0.05:
            valor_total = round(valor_total * np.random.uniform(0.7, 1.3), 2)

        # Datas e motivo dependem do lifecycle
        data_abandono = None
        motivo_abandono = None

        if lifecycle in ('abandonado', 'recuperado_comprado', 'recuperado_pendente', 'expirado'):
            # Definir data de abandono
            minutos_ate_abandono = int(np.random.randint(5, duracao + 1)) if duracao > 5 else 5
            data_abandono = data_criacao + timedelta(minutes=minutos_ate_abandono)
            data_ultima_atividade = data_abandono
            motivo_abandono = np.random.choice(motivos, p=motivos_weights)

            # Aplicar desconto para recuperados
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
            # Coluna interna para uso downstream (removida no save)
            '_lifecycle':               lifecycle,
            '_segmento_rfm':            segmento,
        })

    df = pd.DataFrame(rows)

    # Converter timestamps
    for col in ['data_criacao', 'data_ultima_atividade', 'data_abandono', 'created_at', 'updated_at']:
        df[col] = pd.to_datetime(df[col], utc=True)

    return df


def save_df(df):
    """Remove colunas internas antes de salvar."""
    return df.drop(columns=[c for c in df.columns if c.startswith('_')])


if __name__ == '__main__':
    # Teste standalone com clientes mock
    import clientes as gen_clientes
    clientes_df = gen_clientes.generate()
    df = generate(clientes_df)
    print(f"✓ Carrinhos: {len(df)} registros")
    print(f"  Status: {df['status'].value_counts().to_dict()}")
    print(f"  Lifecycle: {df['_lifecycle'].value_counts().to_dict()}")
    abandonados = df[df['_lifecycle'].isin(['abandonado', 'recuperado_comprado', 'recuperado_pendente', 'expirado'])]
    recuperados = df[df['_lifecycle'] == 'recuperado_comprado']
    print(f"  Taxa abandono: {len(abandonados)/len(df)*100:.1f}%")
    print(f"  Taxa recuperação: {len(recuperados)/len(abandonados)*100:.1f}%")
    dirty_frete = df[df['valor_frete'] < 0]
    print(f"  Dirty (frete negativo): {len(dirty_frete)} ({len(dirty_frete)/len(df)*100:.1f}%)")
