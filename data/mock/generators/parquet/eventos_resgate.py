"""
Generator: eventos_resgate
Gera ~4.200 eventos de campanhas de recuperação para carrinhos abandonados.
Sequência: lembrete_1h → lembrete_24h → desconto_48h → urgencia_72h (max 4 por carrinho).
Respeita opt-in, custo por canal, e funil de conversão (abertura → clique → conversão).
Dirty data: data_abertura < data_envio (~5%).
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import pandas as pd
import numpy as np
from datetime import timedelta
import _config as cfg


ASSUNTOS = {
    'lembrete_1h': [
        'Você esqueceu algo no carrinho 🛒',
        'Seus produtos estão esperando por você!',
        'Finalize sua compra antes que acabe!',
    ],
    'lembrete_24h': [
        'Ainda pensando? Seus itens estão reservados ⏰',
        'Não perca! Seus produtos podem acabar',
        'Última chance de garantir seus itens',
    ],
    'desconto_48h': [
        '🎁 Desconto especial para finalizar sua compra!',
        'Presente para você: desconto exclusivo no seu carrinho',
        'Economize agora! Oferta limitada no seu carrinho',
    ],
    'urgencia_72h': [
        '🔥 ÚLTIMA CHANCE: desconto + frete grátis!',
        'Só hoje! Oferta exclusiva para você finalizar',
        'Não deixe escapar: melhor oferta no seu carrinho',
    ],
}


def generate(carrinhos_df, clientes_df):
    """
    Gera DataFrame de eventos de resgate para carrinhos abandonados.

    Args:
        carrinhos_df: DataFrame com _lifecycle e timestamps
        clientes_df: DataFrame com opt-in (permite_email, permite_sms, permite_push)
    """
    np.random.seed(cfg.SEED + 4)

    # Mapear preferências de contato por cliente
    cliente_prefs = {}
    for _, c in clientes_df.iterrows():
        cliente_prefs[c['cliente_id']] = {
            'permite_email': c['permite_email'],
            'permite_sms':   c['permite_sms'],
            'permite_push':  c['permite_push'],
        }

    # Filtrar carrinhos abandonados (qualquer lifecycle com abandono)
    abandonados = carrinhos_df[carrinhos_df['_lifecycle'].isin([
        'abandonado', 'recuperado_comprado', 'recuperado_pendente', 'expirado'
    ])].copy()

    # ~70% dos abandonados recebem pelo menos 1 resgate
    mask_recebe = np.random.random(len(abandonados)) < 0.70
    abandonados_com_resgate = abandonados[mask_recebe]

    # Determinar quantos toques cada carrinho recebe
    # Distribuição: 55% 1 toque, 22% 2, 13% 3, 10% 4
    n_toques_dist = np.random.choice(
        [1, 2, 3, 4],
        size=len(abandonados_com_resgate),
        p=[0.55, 0.22, 0.13, 0.10]
    )

    # Pré-determinar quais carrinhos convertem (para métricas)
    recuperados_ids = set(
        carrinhos_df[carrinhos_df['_lifecycle'] == 'recuperado_comprado']['carrinho_id'].values
    )

    rows = []
    resgate_id = 1

    for (_, carrinho), n_toques in zip(abandonados_com_resgate.iterrows(), n_toques_dist):
        cliente_id = carrinho['cliente_id']
        prefs = cliente_prefs.get(cliente_id, {'permite_email': True, 'permite_sms': False, 'permite_push': False})
        data_abandono = carrinho['data_abandono']
        valor_carrinho = carrinho.get('valor_subtotal', 200.0)
        segmento = carrinho.get('_segmento_rfm', 'regular')
        vai_converter = carrinho['carrinho_id'] in recuperados_ids

        if pd.isna(data_abandono):
            continue

        # Determinar em qual toque converte (se vai converter)
        toque_conversao = None
        if vai_converter:
            toques_possiveis = list(cfg.CONVERSAO_POR_TOQUE.keys())[:n_toques]
            if toques_possiveis:
                pesos_toque = [cfg.CONVERSAO_POR_TOQUE[t] for t in toques_possiveis]
                pesos_norm = [p / sum(pesos_toque) for p in pesos_toque]
                toque_conversao = np.random.choice(toques_possiveis, p=pesos_norm)

        for toque_idx in range(n_toques):
            seq = cfg.SEQUENCIA_RESGATE[toque_idx]
            tipo = seq['tipo']
            horas_offset = seq['horas']

            # Escolher canal respeitando opt-in
            canais_possiveis = []
            for canal in seq['canais']:
                if canal == 'email' and prefs.get('permite_email', True):
                    canais_possiveis.append('email')
                elif canal == 'sms' and prefs.get('permite_sms', False):
                    canais_possiveis.append('sms')
                elif canal == 'push_app' and prefs.get('permite_push', False):
                    canais_possiveis.append('push_app')
                elif canal == 'whatsapp':
                    # WhatsApp: assumimos opt-in se permite_sms ou tem telefone
                    canais_possiveis.append('whatsapp')

            if not canais_possiveis:
                canais_possiveis = ['email']  # Fallback

            canal = np.random.choice(canais_possiveis)
            custo = cfg.CUSTO_CANAL.get(canal, 0.05)

            # Timestamps
            data_schedule = data_abandono + timedelta(hours=horas_offset)
            # Envio ocorre 0-30min após schedule
            data_envio = data_schedule + timedelta(minutes=int(np.random.randint(0, 30)))

            # Desconto
            desc_min, desc_max = seq['desconto']
            if desc_max > 0:
                desconto_pct = np.random.uniform(desc_min, desc_max) / 100
                desconto_oferecido = round(float(valor_carrinho * desconto_pct), 2)
            else:
                desconto_oferecido = 0.0

            frete_gratis = tipo == 'urgencia_72h' or (
                carrinho.get('motivo_abandono') == 'frete' and np.random.random() > 0.3
            )

            # Funil de engajamento: abertura → clique → conversão
            funil = cfg.FUNIL_CANAL.get(canal, cfg.FUNIL_CANAL['email'])

            foi_aberto = np.random.random() < funil['abertura']
            data_abertura = None
            data_clique = None
            link_clicado = None
            data_conversao = None
            sucesso = False
            valor_pedido_final = None

            if foi_aberto:
                # Abertura: 5min a 24h após envio
                data_abertura = data_envio + timedelta(minutes=int(np.random.randint(5, 1440)))

                # Dirty data: ~5% data_abertura < data_envio
                if np.random.random() < cfg.DIRTY_RATE:
                    data_abertura = data_envio - timedelta(minutes=int(np.random.randint(5, 60)))

                foi_clicado = np.random.random() < funil['clique']
                if foi_clicado:
                    # Clique: 1-60min após abertura
                    data_clique = data_abertura + timedelta(minutes=int(np.random.randint(1, 60)))
                    link_clicado = f"https://marketplace.com.br/carrinho/{carrinho['carrinho_id']}?utm_source={canal}&utm_campaign=recovery"

                    # Conversão no toque certo
                    if toque_conversao == tipo and vai_converter:
                        sucesso = True
                        data_conversao = data_clique + timedelta(minutes=int(np.random.randint(5, 120)))
                        valor_pedido_final = round(float(valor_carrinho - desconto_oferecido), 2)
                        if frete_gratis:
                            valor_pedido_final = round(valor_pedido_final - carrinho.get('valor_frete', 0), 2)
                        valor_pedido_final = max(valor_pedido_final, 10.0)

            assunto = np.random.choice(ASSUNTOS.get(tipo, ['Recupere seu carrinho']))

            rows.append({
                'resgate_id':               resgate_id,
                'carrinho_id':              carrinho['carrinho_id'],
                'cliente_id':               cliente_id,
                'canal':                    canal,
                'tipo_comunicacao':         tipo,
                'data_schedule':            data_schedule,
                'data_envio':               data_envio,
                'assunto':                  assunto,
                'desconto_oferecido':       desconto_oferecido,
                'frete_gratis_oferecido':   frete_gratis,
                'custo_envio':              custo,
                'data_abertura':            data_abertura,
                'data_primeiro_clique':     data_clique,
                'link_clicado':             link_clicado,
                'data_conversao':           data_conversao,
                'sucesso':                  sucesso,
                'valor_pedido_final':       valor_pedido_final,
                'created_at':               data_schedule,
            })

            resgate_id += 1

            # Se converteu neste toque, não envia mais
            if sucesso:
                break

    df = pd.DataFrame(rows)

    # Converter timestamps
    ts_cols = ['data_schedule', 'data_envio', 'data_abertura', 'data_primeiro_clique',
               'data_conversao', 'created_at']
    for col in ts_cols:
        df[col] = pd.to_datetime(df[col], utc=True)

    return df


if __name__ == '__main__':
    import clientes as gen_clientes
    import carrinhos as gen_carrinhos

    clientes_df = gen_clientes.generate()
    carrinhos_df = gen_carrinhos.generate(clientes_df)
    df = generate(carrinhos_df, clientes_df)

    print(f"✓ Eventos Resgate: {len(df)} registros")
    print(f"  Canais: {df['canal'].value_counts().to_dict()}")
    print(f"  Tipos: {df['tipo_comunicacao'].value_counts().to_dict()}")
    print(f"  Conversões: {df['sucesso'].sum()} ({df['sucesso'].mean()*100:.1f}%)")
    dirty = df[df['data_abertura'].notna() & df['data_envio'].notna() & (df['data_abertura'] < df['data_envio'])]
    print(f"  Dirty (abertura < envio): {len(dirty)}")
