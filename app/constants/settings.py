"""Constantes de UI, paleta corporativa Dadosfera e parâmetros canônicos de negócio (SSOT)."""

import os
from types import MappingProxyType
from typing import Final, Mapping

# =============================================================================
# 🎨 DESIGN TOKENS & PALETA CORPORATIVA DADOSFERA (WHITE THEME STANDARD)
# =============================================================================
COLOR_PRIMARY_NAVY: Final[str] = "#0F172A"      # Slate 900
COLOR_PRIMARY_BLUE: Final[str] = "#2563EB"      # Blue 600
COLOR_SUCCESS_GREEN: Final[str] = "#059669"     # Emerald 600
COLOR_SUCCESS_EMERALD: Final[str] = "#10B981"   # Emerald 500
COLOR_WARNING_AMBER: Final[str] = "#D97706"     # Amber 600
COLOR_DANGER_RED: Final[str] = "#E11D48"        # Rose 600
COLOR_ACCENT_PURPLE: Final[str] = "#7C3AED"     # Violet 600
COLOR_BACKGROUND_LIGHT: Final[str] = "#F8FAFC"  # Slate 50
COLOR_CARD_BACKGROUND: Final[str] = "#FFFFFF"   # Pure White
COLOR_TEXT_PRIMARY: Final[str] = "#0F172A"      # Texto Principal
COLOR_TEXT_MUTED: Final[str] = "#64748B"        # Texto Secundário
COLOR_BORDER: Final[str] = "#CBD5E1"            # Borda Slate 300

CHANNEL_COLORS: Final[Mapping[str, str]] = MappingProxyType({
    "WhatsApp": "#059669",
    "Email": "#2563EB",
    "SMS": "#D97706",
    "Push": "#7C3AED"
})

# =============================================================================
# 💰 BENCHMARKS CANÔNICOS DE NEGÓCIO (PITCH SPEC MASTER & GROUND TRUTH)
# =============================================================================
CANONICAL_TOTAL_CARTS: Final[int] = 7_500
DEFAULT_TICKET_MEDIO: Final[float] = 348.80
DEFAULT_TAXA_ABANDONO: Final[float] = 0.697        # Benchmark Baymard 69.7%
CANONICAL_RECOVERY_RATE_DADOSFERA: Final[float] = 0.101  # +10.1% (+757 carrinhos)
CANONICAL_RECOVERED_REVENUE: Final[float] = 264_041.60

# Mix Recomendado Dadosfera vs Convencional
PRESCRIBED_MIX: Final[Mapping[str, float]] = MappingProxyType({
    "Email": 0.85,
    "WhatsApp": 0.12,
    "SMS": 0.02,
    "Push": 0.01,
})

CONVENTIONAL_MIX: Final[Mapping[str, float]] = MappingProxyType({
    "Email": 0.40,
    "WhatsApp": 0.30,
    "SMS": 0.20,
    "Push": 0.10,
})

CUSTO_POR_DISPARO: Final[Mapping[str, float]] = MappingProxyType({
    "Email": 1.02,
    "WhatsApp": 12.00,
    "SMS": 3.00,
    "Push": 1.67,
})

TAXA_CONVERSAO_POR_CANAL: Final[Mapping[str, float]] = MappingProxyType({
    "WhatsApp": 0.145,
    "Email": 0.082,
    "SMS": 0.068,
    "Push": 0.055,
})

CAC_POR_CANAL: Final[Mapping[str, float]] = MappingProxyType({
    "Email": 12.44,
    "WhatsApp": 82.76,
    "SMS": 44.12,
    "Push": 30.36,
})

# =============================================================================
# 📁 CAMINHOS RESILIENTES DE DADOS DO LAKEHOUSE
# =============================================================================
BASE_DIR: Final[str] = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

DATA_PATHS: Final[Mapping[str, str]] = MappingProxyType({
    "carrinhos_cleaned": os.path.join(BASE_DIR, "data", "mock", "output_cleaned", "parquet", "carrinhos.parquet"),
    "produtos_cleaned": os.path.join(BASE_DIR, "data", "mock", "output_cleaned", "parquet", "produtos.parquet"),
    "eventos_resgate_cleaned": os.path.join(BASE_DIR, "data", "mock", "output_cleaned", "parquet", "eventos_resgate.parquet"),
    "clientes_cleaned": os.path.join(BASE_DIR, "data", "mock", "output_cleaned", "parquet", "clientes.parquet"),
    "itens_carrinho_cleaned": os.path.join(BASE_DIR, "data", "mock", "output_cleaned", "parquet", "itens_carrinho.parquet"),
    "produtos_enriquecidos_qualify": os.path.join(BASE_DIR, "pipelines", "datalakes", "qualify", "produtos_enriquecidos_qualify", "produtos_enriquecidos.parquet"),
    "v_abandonment_summary": os.path.join(BASE_DIR, "pipelines", "datalakes", "curated", "v_abandonment_summary", "data.parquet"),
    "v_recovery_roi_by_channel": os.path.join(BASE_DIR, "pipelines", "datalakes", "curated", "v_recovery_roi_by_channel", "data.parquet"),
})
