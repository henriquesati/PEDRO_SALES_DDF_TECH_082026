"""
_config.py — Camada de compatibilidade retroativa.

Re-exporta constantes e configurações do novo pacote declarativo `config/`.
Garante que scripts antigos que importam `_config` continuem funcionando 100%.
"""
from pathlib import Path
from datetime import datetime
import pytz

# Re-exportar constantes de domínio
from .config.constants import *
from .config.settings import VolumeConfig, AnomalyConfig, GeneratorSettings
from .config.profiles import load_profile, get_standard_profile, get_rich_profile, get_dev_profile

# ─── Configuração Ativa Padrão ──────────────────────────────────────────────
DEFAULT_SETTINGS = get_standard_profile(seed=42)

SEED = DEFAULT_SETTINGS.seed
MOCK_DIR = DEFAULT_SETTINGS.base_dir / "mock"
OUTPUT_DIR = DEFAULT_SETTINGS.output_dir
PARQUET_DIR = DEFAULT_SETTINGS.parquet_dir
CSV_DIR = DEFAULT_SETTINGS.csv_dir

TZ = DEFAULT_SETTINGS.timezone
PERIODO_INICIO = DEFAULT_SETTINGS.data_inicio.replace(tzinfo=TZ)
PERIODO_FIM = DEFAULT_SETTINGS.data_fim.replace(tzinfo=TZ)

N_CLIENTES = DEFAULT_SETTINGS.volumes.n_clientes
N_PRODUTOS = DEFAULT_SETTINGS.volumes.n_produtos
N_CARRINHOS = DEFAULT_SETTINGS.volumes.n_carrinhos

DIRTY_RATE = 0.05
