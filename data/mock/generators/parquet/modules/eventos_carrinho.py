"""
Módulo Gerador: Eventos de Carrinho (Telemetria Comportamental).
"""
from typing import Optional, List
from datetime import timedelta
import json
import uuid
import pandas as pd
import numpy as np

try:
    from config.constants import TIPOS_EVENTO, METODOS_PAGAMENTO
    from config.settings import GeneratorSettings
    from core.base_generator import BaseGenerator
except (ImportError, ValueError):
    from ..config.constants import TIPOS_EVENTO, METODOS_PAGAMENTO
    from ..config.settings import GeneratorSettings
    from ..core.base_generator import BaseGenerator


FLUXO_COMPRADO = [
    'view_produto', 'view_produto', 'add_carrinho',
    'view_produto', 'add_carrinho', 'update_quantidade',
    'view_checkout', 'inicio_pagamento',
]

FLUXO_ABANDONADO = [
    'view_produto', 'view_produto', 'add_carrinho',
    'view_produto', 'add_carrinho',
    'view_checkout', 'abandono',
]

FLUXO_ABANDONADO_PAGAMENTO = [
    'view_produto', 'add_carrinho', 'view_produto', 'add_carrinho',
    'view_checkout', 'inicio_pagamento', 'erro_pagamento', 'abandono',
]

FLUXO_RECUPERADO = [
    'view_produto', 'add_carrinho', 'view_produto', 'add_carrinho',
    'view_checkout', 'abandono', 'retorno',
    'view_checkout', 'inicio_pagamento',
]


class EventosCarrinhoGenerator(BaseGenerator):
    name = "eventos_carrinho"
    dependencies = ["carrinhos"]

    def _gerar_dados_evento(self, tipo_evento: str, n_produtos: int) -> Optional[str]:
        dados = {}
        if tipo_evento == 'view_produto':
            dados = {
                'produto_id': int(np.random.randint(1, n_produtos + 1)),
                'tempo_visualizacao_s': int(np.random.randint(5, 180)),
                'scroll_depth': round(float(np.random.uniform(0.2, 1.0)), 2),
            }
        elif tipo_evento == 'add_carrinho':
            dados = {
                'produto_id': int(np.random.randint(1, n_produtos + 1)),
                'quantidade': int(np.random.choice([1, 1, 2, 3])),
                'origem': np.random.choice(['pagina_produto', 'busca', 'recomendacao']),
            }
        elif tipo_evento == 'remove_carrinho':
            dados = {
                'produto_id': int(np.random.randint(1, n_produtos + 1)),
                'motivo': np.random.choice(['mudou_ideia', 'quantidade_errada', 'encontrou_melhor', None]),
            }
        elif tipo_evento == 'update_quantidade':
            dados = {
                'produto_id': int(np.random.randint(1, n_produtos + 1)),
                'quantidade_anterior': int(np.random.randint(1, 4)),
                'quantidade_nova': int(np.random.randint(1, 6)),
            }
        elif tipo_evento == 'view_checkout':
            dados = {
                'etapa': np.random.choice(['endereco', 'pagamento', 'revisao']),
                'tempo_na_etapa_s': int(np.random.randint(10, 300)),
            }
        elif tipo_evento == 'inicio_pagamento':
            dados = {
                'metodo': np.random.choice(list(METODOS_PAGAMENTO.keys())),
                'parcelas': int(np.random.choice([1, 2, 3, 6, 10, 12])),
            }
        elif tipo_evento == 'erro_pagamento':
            dados = {
                'codigo_erro': np.random.choice(['cartao_recusado', 'saldo_insuficiente', 'timeout', 'dados_invalidos']),
                'metodo': np.random.choice(list(METODOS_PAGAMENTO.keys())),
            }
        elif tipo_evento == 'abandono':
            dados = {
                'pagina_saida': np.random.choice(['checkout', 'carrinho', 'pagamento', 'produto']),
                'tempo_inativo_s': int(np.random.randint(1800, 7200)),
            }
        elif tipo_evento == 'retorno':
            dados = {
                'origem_retorno': np.random.choice(['email_link', 'whatsapp_link', 'direto', 'push']),
                'horas_desde_abandono': int(np.random.randint(1, 96)),
            }

        return json.dumps(dados, ensure_ascii=False) if dados else None

    def _gerar_sequencia_eventos(self, lifecycle: str, motivo_abandono: Optional[str]) -> List[str]:
        if lifecycle == 'direto_comprado':
            base = list(FLUXO_COMPRADO)
        elif lifecycle in ('abandonado', 'expirado'):
            if motivo_abandono == 'pagamento':
                base = list(FLUXO_ABANDONADO_PAGAMENTO)
            else:
                base = list(FLUXO_ABANDONADO)
        elif lifecycle in ('recuperado_comprado', 'recuperado_pendente'):
            base = list(FLUXO_RECUPERADO)
        elif lifecycle == 'ativo':
            n_events = int(np.random.randint(2, 6))
            return [np.random.choice(['view_produto', 'add_carrinho', 'view_produto']) for _ in range(n_events)]
        else:
            base = list(FLUXO_ABANDONADO)

        extras = int(np.random.randint(0, 8))
        for _ in range(extras):
            pos = np.random.randint(1, max(2, len(base) - 1))
            evento = np.random.choice([
                'view_produto', 'view_produto', 'add_carrinho',
                'remove_carrinho', 'update_quantidade', 'view_produto',
            ])
            base.insert(pos, evento)

        return base

    def generate_raw(self, **context) -> pd.DataFrame:
        carrinhos_df = context.get('carrinhos_df')
        if carrinhos_df is None:
            raise ValueError("EventosCarrinhoGenerator requer 'carrinhos_df' no contexto.")

        np.random.seed(self.seed + 3)
        n_produtos = self.settings.volumes.n_produtos

        rows = []
        evento_id = 1

        for _, carrinho in carrinhos_df.iterrows():
            lifecycle = carrinho.get('_lifecycle', 'abandonado')
            motivo = carrinho.get('motivo_abandono', None)
            sessao_id = str(uuid.uuid4())[:12]
            data_base = carrinho['data_criacao']
            duracao = carrinho.get('duracao_sessao_minutos', 15)
            if pd.isna(duracao) or duracao < 2:
                duracao = 15

            sequencia = self._gerar_sequencia_eventos(lifecycle, motivo)
            total_eventos = len(sequencia)
            intervalo_base = duracao * 60 / max(total_eventos, 1)

            timestamp_atual = data_base

            for idx, tipo_evento in enumerate(sequencia):
                if idx > 0:
                    delta_s = max(1, int(intervalo_base * np.random.uniform(0.3, 1.7)))
                    timestamp_atual = timestamp_atual + timedelta(seconds=delta_s)

                if tipo_evento == 'retorno' and pd.notna(carrinho['data_abandono']):
                    horas_retorno = int(np.random.randint(1, 72))
                    timestamp_atual = carrinho['data_abandono'] + timedelta(hours=horas_retorno)
                    sessao_id = str(uuid.uuid4())[:12]

                duracao_evento = int(np.random.randint(2, 120)) if tipo_evento != 'abandono' else None
                dados_evento = self._gerar_dados_evento(tipo_evento, n_produtos)

                rows.append({
                    'evento_id':                evento_id,
                    'carrinho_id':              carrinho['carrinho_id'],
                    'cliente_id':               carrinho['cliente_id'],
                    'sessao_id':                sessao_id,
                    'timestamp_evento':         timestamp_atual,
                    'tipo_evento':              tipo_evento,
                    'duracao_evento_segundos':  duracao_evento,
                    'dados_evento':             dados_evento,
                })
                evento_id += 1

        df = pd.DataFrame(rows)
        df['timestamp_evento'] = pd.to_datetime(df['timestamp_evento'], utc=True)
        return df


def generate(carrinhos_df: pd.DataFrame, settings: Optional[GeneratorSettings] = None) -> pd.DataFrame:
    if settings is None:
        try:
            from config.profiles import get_standard_profile
        except (ImportError, ValueError):
            from ..config.profiles import get_standard_profile
        settings = get_standard_profile()
    generator = EventosCarrinhoGenerator(settings)
    return generator.run(carrinhos_df=carrinhos_df)
