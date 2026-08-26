"""Tema visual padronizado para gráficos Plotly (White Theme / charts-maker Standard)."""

from typing import Any, Dict
import plotly.graph_objects as go

# =============================================================================
# 🎨 TOKENS VISUAIS EXECUTIVOS
# =============================================================================
CANVAS_BG = "#FFFFFF"
CARD_BG = "#F8FAFC"
GRID_COLOR = "#E2E8F0"
BORDER_COLOR = "#CBD5E1"

TEXT_PRIMARY = "#0F172A"      # Slate 900
TEXT_SECONDARY = "#334155"    # Slate 700
TEXT_MUTED = "#64748B"        # Slate 500

# Paleta Semântica
COLOR_BLUE = "#2563EB"        # Blue 600 (Orgânico / Baseline / Destaque)
COLOR_NAVY = "#1E3A8A"        # Blue 900 (Primário Dadosfera)
COLOR_EMERALD = "#059669"     # Emerald 600 (Resgate / Margem / Sucesso)
COLOR_CORAL = "#E11D48"       # Rose 600 (Atrito / Abandono / Custo)
COLOR_AMBER = "#D97706"       # Amber 600 (Atenção / Risco Médio)
COLOR_PURPLE = "#7C3AED"      # Violet 600 (IA / ML / VIP)

FONT_FAMILY = "Segoe UI, Inter, -apple-system, BlinkMacSystemFont, Arial, sans-serif"

def apply_executive_layout(
    fig: go.Figure,
    title: str | None = None,
    height: int = 380,
    show_legend: bool = True,
    margin: Dict[str, int] | None = None,
) -> go.Figure:
    """Aplica o template visual executivo padrão (Fundo Branco Puro) a figuras Plotly."""
    default_margin = dict(l=30, r=30, t=50 if title else 25, b=30)
    final_margin = margin if margin is not None else default_margin

    fig.update_layout(
        title=dict(
            text=f"<b>{title}</b>" if title else "",
            font=dict(family=FONT_FAMILY, size=14, color=TEXT_PRIMARY),
            x=0.01,
            xanchor="left",
            y=0.96,
        ) if title else None,
        height=height,
        margin=final_margin,
        plot_bgcolor=CANVAS_BG,
        paper_bgcolor=CANVAS_BG,
        font=dict(family=FONT_FAMILY, color=TEXT_SECONDARY, size=11),
        showlegend=show_legend,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1.0,
            font=dict(size=10, color=TEXT_SECONDARY),
            bgcolor="rgba(255,255,255,0.85)",
            bordercolor=BORDER_COLOR,
            borderwidth=1,
        ) if show_legend else None,
        hoverlabel=dict(
            bgcolor=CANVAS_BG,
            font_size=11,
            font_family=FONT_FAMILY,
            bordercolor=BORDER_COLOR,
        ),
    )

    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor=GRID_COLOR,
        zeroline=False,
        showline=True,
        linewidth=1,
        linecolor=BORDER_COLOR,
        tickfont=dict(family=FONT_FAMILY, size=10, color=TEXT_MUTED),
        title_font=dict(family=FONT_FAMILY, size=11, color=TEXT_PRIMARY),
    )

    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor=GRID_COLOR,
        zeroline=False,
        showline=True,
        linewidth=1,
        linecolor=BORDER_COLOR,
        tickfont=dict(family=FONT_FAMILY, size=10, color=TEXT_MUTED),
        title_font=dict(family=FONT_FAMILY, size=11, color=TEXT_PRIMARY),
    )

    return fig
