"""
Perfis Pré-Configurados de Volumetria e Geração — Cart Recovery Mock Data.

Permite alternar facilmente entre perfis de execução:
- STANDARD: ~116k+ registros (baseline do case)
- RICH: ~160k+ registros (volumetria expandida e dados hiper-ricos)
- DEV: ~10k registros (desenvolvimento e testes rápidos)
"""
from typing import Dict
from .settings import GeneratorSettings, VolumeConfig, AnomalyConfig


def get_standard_profile(seed: int = 42) -> GeneratorSettings:
    """Perfil padrão do case: ~116k+ registros totais."""
    return GeneratorSettings(
        seed=seed,
        profile_name="standard",
        volumes=VolumeConfig(
            n_clientes=1_500,
            n_produtos=300,
            n_carrinhos=7_500,
            itens_por_carrinho_media=3.0,
            eventos_por_carrinho_media=12.0,
            toques_resgate_por_abandonado_media=1.8,
        ),
        anomalies=AnomalyConfig(),
    )


def get_rich_profile(seed: int = 42) -> GeneratorSettings:
    """Perfil rico expandido: ~160k+ registros totais com maior profundidade."""
    return GeneratorSettings(
        seed=seed,
        profile_name="rich",
        volumes=VolumeConfig(
            n_clientes=2_500,
            n_produtos=500,
            n_carrinhos=10_000,
            itens_por_carrinho_media=3.2,
            eventos_por_carrinho_media=14.0,
            toques_resgate_por_abandonado_media=2.0,
        ),
        anomalies=AnomalyConfig(),
    )


def get_dev_profile(seed: int = 42) -> GeneratorSettings:
    """Perfil leve para testes unitários e desenvolvimento rápido (~10k registros)."""
    return GeneratorSettings(
        seed=seed,
        profile_name="dev",
        volumes=VolumeConfig(
            n_clientes=200,
            n_produtos=50,
            n_carrinhos=800,
            itens_por_carrinho_media=2.5,
            eventos_por_carrinho_media=8.0,
            toques_resgate_por_abandonado_media=1.5,
        ),
        anomalies=AnomalyConfig(),
    )


PROFILES: Dict[str, GeneratorSettings] = {
    'standard': get_standard_profile(),
    'rich': get_rich_profile(),
    'dev': get_dev_profile(),
}


def load_profile(name: str = "standard", seed: int = 42, dirty_multiplier: float = 1.0) -> GeneratorSettings:
    """Carrega o perfil desejado aplicando overrides opcionais de seed e multiplicador de anomalias."""
    name_clean = name.lower().strip()
    if name_clean == "rich":
        settings = get_rich_profile(seed=seed)
    elif name_clean == "dev":
        settings = get_dev_profile(seed=seed)
    else:
        settings = get_standard_profile(seed=seed)

    if dirty_multiplier != 1.0:
        settings.anomalies = settings.anomalies.scale_rates(dirty_multiplier)

    return settings
