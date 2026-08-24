"""Configurações centralizadas e imutáveis para o Data App Streamlit (Item 9 & Bônus).

Este módulo define tokens de design, paleta corporativa Dadosfera, caminhos
de dados do Lakehouse e constantes financeiras de negócio.
"""

from dataclasses import dataclass
from types import MappingProxyType
from typing import Final, Literal, Mapping, TypeAlias
import os

AppTheme: TypeAlias = Literal["dadosfera_light", "dadosfera_dark"]

# =============================================================================
# 🎨 TOKENS DE DESIGN & PALETA CORPORATIVA DADOSFERA
# =============================================================================
COLOR_PRIMARY_NAVY: Final[str] = "#1E3A8A"      # Azul Dadosfera
COLOR_PRIMARY_BLUE: Final[str] = "#3B82F6"      # Azul Acento
COLOR_SUCCESS_GREEN: Final[str] = "#059669"     # Verde Conversão / Receita
COLOR_WARNING_AMBER: Final[str] = "#D97706"     # Âmbar Atenção / Risco
COLOR_DANGER_RED: Final[str] = "#DC2626"        # Vermelho Abandono / Custo
COLOR_BACKGROUND_LIGHT: Final[str] = "#F8FAFC"  # Fundo Neutro Claro
COLOR_CARD_BACKGROUND: Final[str] = "#FFFFFF"   # Fundo de Cards
COLOR_TEXT_PRIMARY: Final[str] = "#0F172A"      # Texto Principal
COLOR_TEXT_MUTED: Final[str] = "#64748B"        # Texto Secundário

CHANNEL_COLORS: Final[Mapping[str, str]] = MappingProxyType({
    "WhatsApp": "#25D366",
    "Email": "#3B82F6",
    "SMS": "#F59E0B",
    "Push": "#8B5CF6"
})

# =============================================================================
# 💰 CONSTANTES ECONÔMICAS & PARAMETRIZAÇÃO DE RESGATE (SSOT)
# =============================================================================
DEFAULT_TICKET_MEDIO: Final[float] = 348.80
DEFAULT_TAXA_ABANDONO: Final[float] = 0.697
DEFAULT_TAXA_CONVERSAO_BASE: Final[float] = 0.095

CUSTO_POR_DISPARO: Final[Mapping[str, float]] = MappingProxyType({
    "WhatsApp": 12.00,
    "SMS": 3.00,
    "Email": 1.02,
    "Push": 1.67
})

TAXA_CONVERSAO_POR_CANAL: Final[Mapping[str, float]] = MappingProxyType({
    "WhatsApp": 0.145,
    "Email": 0.082,
    "SMS": 0.068,
    "Push": 0.055
})

# =============================================================================
# 📁 RESOLUÇÃO DE CAMINHOS DE DADOS DO LAKEHOUSE (RESILIENTE)
# =============================================================================
BASE_DIR: Final[str] = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

DATA_PATHS: Final[Mapping[str, str]] = MappingProxyType({
    # Gold Views & Dimensions
    "v_abandonment_summary": os.path.join(BASE_DIR, "pipelines", "datalakes", "curated", "v_abandonment_summary", "data.parquet"),
    "v_recovery_roi_by_channel": os.path.join(BASE_DIR, "pipelines", "datalakes", "curated", "v_recovery_roi_by_channel", "data.parquet"),
    "fato_resgate": os.path.join(BASE_DIR, "pipelines", "datalakes", "curated", "fato_resgate", "data.parquet"),
    "fato_abandono": os.path.join(BASE_DIR, "pipelines", "datalakes", "curated", "fato_abandono", "data.parquet"),
    "dim_clientes": os.path.join(BASE_DIR, "pipelines", "datalakes", "curated", "dim_clientes", "data.parquet"),
    "dim_canal_resgate": os.path.join(BASE_DIR, "pipelines", "datalakes", "curated", "dim_canal_resgate", "data.parquet"),
    # Silver Qualify Enriquecida com GenAI
    "produtos_enriquecidos": os.path.join(BASE_DIR, "pipelines", "datalakes", "qualify", "produtos_enriquecidos_qualify", "produtos_enriquecidos.parquet"),
    # Raw Datasets
    "carrinhos_raw": os.path.join(BASE_DIR, "data", "mock", "output", "parquet", "carrinhos.parquet"),
    "produtos_raw": os.path.join(BASE_DIR, "data", "mock", "output", "parquet", "produtos.parquet"),
    "clientes_raw": os.path.join(BASE_DIR, "data", "mock", "output", "parquet", "clientes.parquet"),
    "eventos_resgate_raw": os.path.join(BASE_DIR, "data", "mock", "output", "parquet", "eventos_resgate.parquet"),
})
