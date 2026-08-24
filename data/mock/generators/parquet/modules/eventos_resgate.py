"""
Módulo Gerador: Eventos de Resgate (Campanhas de Recuperação).
"""
from typing import Optional
from datetime import timedelta
import pandas as pd
import numpy as np

try:
    from config.constants import (
        SEQUENCIA_RESGATE, CONVERSAO_POR_TOQUE, ASSUNTOS_RESGATE,
        CUSTO_CANAL, FUNIL_CANAL
    )
    from config.settings import GeneratorSettings
    from core.base_generator import BaseGenerator
except (ImportError, ValueError):
    from ..config.constants import (
        SEQUENCIA_RESGATE, CONVERSAO_POR_TOQUE, ASSUNTOS_RESGATE,
        CUSTO_CANAL, FUNIL_CANAL
    )
    from ..config.settings import GeneratorSettings
    from ..core.base_generator import BaseGenerator


class EventosResgateGenerator(BaseGenerator):
    name = "eventos_resgate"
    dependencies = ["carrinhos", "clientes"]

    def generate_raw(self, **context) -> pd.DataFrame:
        carrinhos_df = context.get('carrinhos_df')
        clientes_df = context.get('clientes_df')

        if carrinhos_df is None:
            raise ValueError("EventosResgateGenerator requer 'carrinhos_df' no contexto.")
        if clientes_df is None:
            raise ValueError("EventosResgateGenerator requer 'clientes_df' no contexto.")

        np.random.seed(self.seed + 4)

        cliente_prefs = {
            c['cliente_id']: {
                'permite_email': c['permite_email'],
                'permite_sms':   c['permite_sms'],
                'permite_push':  c['permite_push'],
            }
            for _, c in clientes_df.iterrows()
        }

        abandonados = carrinhos_df[carrinhos_df['_lifecycle'].isin([
            'abandonado', 'recuperado_comprado', 'recuperado_pendente', 'expirado'
        ])].copy()

        mask_recebe = np.random.random(len(abandonados)) < 0.70
        abandonados_com_resgate = abandonados[mask_recebe]

        n_toques_dist = np.random.choice(
            [1, 2, 3, 4],
            size=len(abandonados_com_resgate),
            p=[0.55, 0.22, 0.13, 0.10]
        )

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
            vai_converter = carrinho['carrinho_id'] in recuperados_ids

            if pd.isna(data_abandono):
                continue

            toque_conversao = None
            if vai_converter:
                toques_possiveis = list(CONVERSAO_POR_TOQUE.keys())[:n_toques]
                if toques_possiveis:
                    pesos_toque = [CONVERSAO_POR_TOQUE[t] for t in toques_possiveis]
                    pesos_norm = [p / sum(pesos_toque) for p in pesos_toque]
                    toque_conversao = np.random.choice(toques_possiveis, p=pesos_norm)

            for toque_idx in range(n_toques):
                seq = SEQUENCIA_RESGATE[toque_idx]
                tipo = seq['tipo']
                horas_offset = seq['horas']

                canais_possiveis = []
                for canal in seq['canais']:
                    if canal == 'email' and prefs.get('permite_email', True):
                        canais_possiveis.append('email')
                    elif canal == 'sms' and prefs.get('permite_sms', False):
                        canais_possiveis.append('sms')
                    elif canal == 'push_app' and prefs.get('permite_push', False):
                        canais_possiveis.append('push_app')
                    elif canal == 'whatsapp':
                        canais_possiveis.append('whatsapp')

                if not canais_possiveis:
                    canais_possiveis = ['email']

                canal = np.random.choice(canais_possiveis)
                custo = CUSTO_CANAL.get(canal, 0.05)

                data_schedule = data_abandono + timedelta(hours=horas_offset)
                data_envio = data_schedule + timedelta(minutes=int(np.random.randint(0, 30)))

                desc_min, desc_max = seq['desconto']
                if desc_max > 0:
                    desconto_pct = np.random.uniform(desc_min, desc_max) / 100
                    desconto_oferecido = round(float(valor_carrinho * desconto_pct), 2)
                else:
                    desconto_oferecido = 0.0

                frete_gratis = tipo == 'urgencia_72h' or (
                    carrinho.get('motivo_abandono') == 'frete' and np.random.random() > 0.3
                )

                funil = FUNIL_CANAL.get(canal, FUNIL_CANAL['email'])
                foi_aberto = np.random.random() < funil['abertura']
                data_abertura = None
                data_clique = None
                link_clicado = None
                data_conversao = None
                sucesso = False
                valor_pedido_final = None

                if foi_aberto:
                    data_abertura = data_envio + timedelta(minutes=int(np.random.randint(5, 1440)))
                    foi_clicado = np.random.random() < funil['clique']
                    if foi_clicado:
                        data_clique = data_abertura + timedelta(minutes=int(np.random.randint(1, 60)))
                        link_clicado = f"https://marketplace.com.br/carrinho/{carrinho['carrinho_id']}?utm_source={canal}&utm_campaign=recovery"

                        if toque_conversao == tipo and vai_converter:
                            sucesso = True
                            data_conversao = data_clique + timedelta(minutes=int(np.random.randint(5, 120)))
                            valor_pedido_final = round(float(valor_carrinho - desconto_oferecido), 2)
                            if frete_gratis:
                                valor_pedido_final = round(valor_pedido_final - carrinho.get('valor_frete', 0), 2)
                            valor_pedido_final = max(valor_pedido_final, 10.0)

                assunto = np.random.choice(ASSUNTOS_RESGATE.get(tipo, ['Recupere seu carrinho']))

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

                if sucesso:
                    break

        df = pd.DataFrame(rows)
        ts_cols = ['data_schedule', 'data_envio', 'data_abertura', 'data_primeiro_clique', 'data_conversao', 'created_at']
        for col in ts_cols:
            df[col] = pd.to_datetime(df[col], utc=True)
        return df

    def apply_anomalies(self, df: pd.DataFrame) -> pd.DataFrame:
        total = len(df)
        anom_cfg = self.settings.anomalies

        abertos_idx = df[df['data_abertura'].notna()].index.values
        if len(abertos_idx) > 0:
            inv_sub_idx = self.engine.get_guaranteed_indices(
                len(abertos_idx),
                anom_cfg.min_temporal_inversion_resgate_pct,
                seed=self.seed + 501
            )
            actual_inv_idx = abertos_idx[inv_sub_idx]
            for idx in actual_inv_idx:
                df.loc[idx, 'data_abertura'] = df.loc[idx, 'data_envio'] - timedelta(minutes=int(np.random.randint(5, 60)))
            self.audit.record(
                'inversao_temporal_abertura',
                anom_cfg.min_temporal_inversion_resgate_pct,
                len(actual_inv_idx),
                len(abertos_idx),
                "Data de abertura registrada antes da data de envio da mensagem"
            )

        return df


def generate(carrinhos_df: pd.DataFrame, clientes_df: pd.DataFrame, settings: Optional[GeneratorSettings] = None) -> pd.DataFrame:
    if settings is None:
        try:
            from config.profiles import get_standard_profile
        except (ImportError, ValueError):
            from ..config.profiles import get_standard_profile
        settings = get_standard_profile()
    generator = EventosResgateGenerator(settings)
    return generator.run(carrinhos_df=carrinhos_df, clientes_df=clientes_df)
