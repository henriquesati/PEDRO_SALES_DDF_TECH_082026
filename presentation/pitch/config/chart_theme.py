"""
Configurações e tema visual centralizado para os gráficos do Pitch Dadosfera.
Paradigma funcional e declarativo com tipagem estrita (Type Annotations).
"""

from typing import Final, NamedTuple, Literal, TypeAlias
from types import MappingProxyType
import os
import matplotlib.pyplot as plt
import seaborn as sns

# ==============================================================================
# PALETA DE CORES CORPORATIVA DADOSFERA & DOMÍNIO
# ==============================================================================

class ColorPalette(NamedTuple):
    primary_dark: str    # Fundo escuro / Navy Dadosfera
    secondary_dark: str  # Card background
    accent_blue: str     # Azul Dadosfera
    accent_cyan: str     # Ciano destaque
    accent_green: str    # Verde sucesso / Recuperado
    accent_coral: str    # Coral / Alerta / Abandono
    accent_yellow: str   # Âmbar / Atenção
    accent_purple: str   # Roxo / IA & Segmentação
    text_light: str      # Texto principal
    text_muted: str      # Texto secundário / labels
    border_color: str    # Bordas sutis
    grid_color: str      # Linhas de grade sutis

DADOSFERA_PALETTE: Final[ColorPalette] = ColorPalette(
    primary_dark="#0F172A",     # Slate 900
    secondary_dark="#1E293B",   # Slate 800
    accent_blue="#2563EB",      # Blue 600
    accent_cyan="#06B6D4",      # Cyan 500
    accent_green="#10B981",     # Emerald 500
    accent_coral="#F43F5E",     # Rose 500
    accent_yellow="#F59E0B",    # Amber 500
    accent_purple="#8B5CF6",    # Violet 500
    text_light="#F8FAFC",       # Slate 50
    text_muted="#94A3B8",       # Slate 400
    border_color="#334155",     # Slate 700
    grid_color="#1E293B"        # Slate 800
)

# ==============================================================================
# CONFIGURAÇÕES DE EXPORTAÇÃO
# ==============================================================================

DPI_EXPORT: Final[int] = 300
FIGURE_WIDTH: Final[float] = 12.0
FIGURE_HEIGHT: Final[float] = 6.8

# ==============================================================================
# FUNÇÕES PURAS DE APLICAÇÃO DE TEMA
# ==============================================================================

def apply_dadosfera_theme() -> None:
    """Configura parâmetros globais do Matplotlib/Seaborn para o padrão estético Dadosfera."""
    plt.style.use("dark_background")
    
    plt.rcParams.update({
        "figure.facecolor": DADOSFERA_PALETTE.primary_dark,
        "axes.facecolor": DADOSFERA_PALETTE.secondary_dark,
        "axes.edgecolor": DADOSFERA_PALETTE.border_color,
        "axes.labelcolor": DADOSFERA_PALETTE.text_light,
        "axes.titlecolor": DADOSFERA_PALETTE.text_light,
        "xtick.color": DADOSFERA_PALETTE.text_muted,
        "ytick.color": DADOSFERA_PALETTE.text_muted,
        "grid.color": DADOSFERA_PALETTE.grid_color,
        "grid.linestyle": "--",
        "grid.alpha": 0.6,
        "font.family": "sans-serif",
        "font.sans-serif": ["Segoe UI", "DejaVu Sans", "Helvetica", "Arial"],
        "figure.titlesize": 16,
        "axes.titlesize": 14,
        "axes.labelsize": 11,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "legend.facecolor": DADOSFERA_PALETTE.secondary_dark,
        "legend.edgecolor": DADOSFERA_PALETTE.border_color,
        "legend.fontsize": 10,
        "savefig.dpi": DPI_EXPORT,
        "savefig.bbox": "tight",
        "savefig.facecolor": DADOSFERA_PALETTE.primary_dark,
        "savefig.edgecolor": "none",
    })

def save_chart_artifact(fig: plt.Figure, output_path: str) -> str:
    """Salva a figura em alta definição de forma declarativa e fecha a memória."""
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    fig.savefig(output_path, dpi=DPI_EXPORT, bbox_inches="tight", facecolor=DADOSFERA_PALETTE.primary_dark)
    plt.close(fig)
    return output_path
