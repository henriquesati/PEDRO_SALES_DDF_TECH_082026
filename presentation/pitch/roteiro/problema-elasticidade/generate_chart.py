#!/usr/bin/env python3
"""
generate_chart.py
Gera o gráfico executivo de alto impacto para a view 'problema-elasticidade'.
Visualização corporativa (Fundo Branco Puro, 16:9 Widescreen, 300 DPI, Tipografia Moderna).
Template visual limpo sem título nem descrição (espaço 100% livre para títulos e textos no PowerPoint).
"""

from typing import Final
import os
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

OUTPUT_DIR: Final[Path] = Path(__file__).resolve().parent
OUTPUT_IMAGE_PATH: Final[Path] = OUTPUT_DIR / "chart_problema_elasticidade.png"

# Paleta Semântica Executiva (Padrão White Background)
COLORS = {
    "bg": "#FFFFFF",
    "card_bg": "#F8FAFC",
    "card_border": "#CBD5E1",
    "text_dark": "#0F172A",
    "text_muted": "#475569",
    "accent_coral": "#EF4444",      # Vermelho Alerta / Perda
    "accent_dark_red": "#991B1B",   # Vermelho Escuro
    "accent_amber": "#F59E0B",      # Âmbar / Atenção
    "accent_green": "#10B981",      # Verde / Sucesso
    "accent_blue": "#2563EB",       # Azul Corporativo
    "grid": "#E2E8F0"
}

def draw_card(ax, x: float, y: float, w: float, h: float, title: str, value: str, subtitle: str, color: str) -> None:
    """Desenha um card executivo com borda precisa e acabamento corporativo."""
    card_rect = patches.FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.0,rounding_size=0.03",
        facecolor=COLORS["card_bg"],
        edgecolor=color,
        linewidth=1.6,
        zorder=2
    )
    ax.add_patch(card_rect)
    
    # Barra de destaque horizontal no topo do card
    tag = patches.FancyBboxPatch(
        (x, y + h - 0.03), w, 0.03,
        boxstyle="round,pad=0.0,rounding_size=0.015",
        facecolor=color,
        edgecolor="none",
        zorder=3
    )
    ax.add_patch(tag)
    
    # Textos internos do card
    ax.text(x + w/2, y + h - 0.065, title.upper(), ha="center", va="top", fontsize=9.5, fontweight="bold", color=COLORS["text_muted"], zorder=4)
    ax.text(x + w/2, y + h/2 - 0.01, value, ha="center", va="center", fontsize=18, fontweight="bold", color=color, zorder=4)
    ax.text(x + w/2, y + 0.04, subtitle, ha="center", va="bottom", fontsize=8.5, color=COLORS["text_dark"], zorder=4)

def plot_elasticity_problem() -> plt.Figure:
    """Gera a figura executiva sem títulos ou descrições (100% pronta para overlay no PowerPoint)."""
    plt.rcParams["font.sans-serif"] = ["Segoe UI", "DejaVu Sans", "Helvetica", "Arial"]
    
    fig = plt.figure(figsize=(16, 9), facecolor=COLORS["bg"], dpi=300)
    
    # 1. Top Executive KPI Cards (3 Cards amplos e perfeitamente distribuídos)
    ax_cards = fig.add_axes([0.06, 0.74, 0.88, 0.18])
    ax_cards.set_xlim(0, 1)
    ax_cards.set_ylim(0, 1)
    ax_cards.axis("off")
    
    cards_data = [
        ("Vendas Perdidas por Minuto", "R$ 50k a 100k", "Faturamento no Checkout (Mercado Livre)", COLORS["accent_coral"]),
        ("Tempo de Parada do Checkout", "5 a 15 min", "Reconfiguração e Failover de Cache Redis", COLORS["accent_amber"]),
        ("Faturamento Total Perdido", "R$ 250k a 1,5M", "Perda Direta em Vendas na Black Friday", COLORS["accent_dark_red"]),
    ]
    
    card_w = 0.29
    gap = (1.0 - (3 * card_w)) / 2
    for i, (title, val, sub, col) in enumerate(cards_data):
        cx = i * (card_w + gap)
        draw_card(ax_cards, cx, 0.05, card_w, 0.90, title, val, sub, col)
        
    # 2. Gráfico Principal: Curva de Perda em Faturamento (Amplo e destacado)
    ax1 = fig.add_axes([0.06, 0.09, 0.88, 0.58], facecolor=COLORS["card_bg"])
    for spine in ax1.spines.values():
        spine.set_color(COLORS["card_border"])
        spine.set_linewidth(1.3)
        
    minutos = np.arange(0, 16, 1)
    perda_min = minutos * 50.0  # R$ em milhares
    perda_max = minutos * 100.0 # R$ em milhares
    
    ax1.fill_between(minutos, perda_min, perda_max, color=COLORS["accent_coral"], alpha=0.18, 
                     label="Faixa Estimada de Faturamento Perdido: R$ 50k a R$ 100k por minuto")
    ax1.plot(minutos, perda_max, color=COLORS["accent_coral"], linewidth=3.0, linestyle="-", 
             label="Cenário de Pico Máximo: R$ 100k por minuto em vendas perdidas")
    ax1.plot(minutos, perda_min, color=COLORS["accent_amber"], linewidth=2.5, linestyle="--", 
             label="Cenário de Pico Base: R$ 50k por minuto em vendas perdidas")
    
    # Destacar marcos de 5, 10 e 15 minutos com anotações claras de vendas perdidas
    marcos = [
        (5, 500, "5 min: -R$ 500k em vendas"), 
        (10, 1000, "10 min: -R$ 1,0 Milhão em vendas"), 
        (15, 1500, "15 min: -R$ 1,5 Milhão em vendas")
    ]
    for m_x, m_y, label in marcos:
        ax1.scatter([m_x], [m_y], color=COLORS["accent_dark_red"], s=90, zorder=5)
        ax1.annotate(label, xy=(m_x, m_y), xytext=(m_x - 1.6, m_y + 110),
                     fontsize=10.5, fontweight="bold", color=COLORS["accent_dark_red"],
                     arrowprops=dict(arrowstyle="->", color=COLORS["accent_dark_red"], lw=1.5))
                     
    ax1.set_title("Projeção de Faturamento Perdido em Vendas por Minutos de Indisponibilidade no Checkout", 
                  fontsize=14.0, fontweight="bold", color=COLORS["text_dark"], pad=14)
    ax1.set_xlabel("Duração da Instabilidade ou Parada de Cache em Minutos", fontsize=11.5, fontweight="bold", color=COLORS["text_dark"], labelpad=8)
    ax1.set_ylabel("Faturamento Perdido em Vendas (R$ Mil)", fontsize=11.5, fontweight="bold", color=COLORS["text_dark"], labelpad=8)
    ax1.set_xlim(0, 15.5)
    ax1.set_ylim(0, 1750)
    ax1.grid(True, linestyle="--", alpha=0.6, color=COLORS["grid"])
    ax1.legend(loc="upper left", fontsize=10.0, framealpha=0.92)
    
    # 3. Rodapé Discreto com Fonte Oficial
    fonte_texto = "Fonte: Relatório Anual Mercado Livre 2025 | GMV (Gross Merchandise Volume) = Volume Bruto Total de Vendas."
    fig.text(0.06, 0.035, fonte_texto, fontsize=8.5, color=COLORS["text_muted"], style="italic")
    
    return fig

def main() -> None:
    fig = plot_elasticity_problem()
    fig.savefig(str(OUTPUT_IMAGE_PATH), dpi=300, bbox_inches="tight", facecolor=COLORS["bg"])
    plt.close(fig)
    print(f"[SUCCESS] Gráfico executivo salvo com sucesso em: {OUTPUT_IMAGE_PATH}")

if __name__ == "__main__":
    main()
