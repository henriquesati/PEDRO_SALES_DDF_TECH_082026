#!/usr/bin/env python3
"""
generate_cost_comparison_chart.py
Gera o gráfico conceitual minimalista de comparação de custos (Infra Própria AWS DIY vs. Dadosfera),
com identificação direta das linhas, ponto de inflexão/break-even e eixos conceituais X e Y,
otimizado para apresentação executiva de alto impacto no PowerPoint.

Padrão Visual: Fundo Branco Puro (#FFFFFF), 16:9 Widescreen (3600x2025 px), 300 DPI, Tipografia Sem Serifa Moderna.
"""

from typing import Final, Dict
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

OUTPUT_DIR: Final[Path] = Path(__file__).resolve().parent

# Paleta Semântica Executiva Minimalista
COLORS: Final[Dict[str, str]] = {
    "bg": "#FFFFFF",
    "axis_line": "#64748B",       # Slate 500 (linhas e setas de eixo)
    "axis_text": "#334155",       # Slate 700 (rótulos de eixos)
    "sub_text": "#475569",        # Slate 600
    "red_line": "#DC2626",        # Vermelho Coral (Custo com Infra Própria)
    "red_fill": "#FEE2E2",        # Vermelho Suave Translúcido
    "green_line": "#059669",      # Verde Esmeralda (Custo Dadosfera)
    "green_fill": "#D1FAE5",      # Verde Suave Translúcido
    "crossover_dot": "#1E293B",   # Ponto de Cruzamento / Break-even
}

def generate_smooth_curves(n_points: int = 250) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Gera curvas matemáticas ultra-suaves para a dinâmica de custos."""
    x = np.linspace(0.6, 9.0, n_points)
    
    # Curva 1 (Infra Própria): Começa em patamar menor, mas sofre aceleração exponencial
    # Representa provisionamento + headcount + apps + dados
    y_infra = 1.1 + 0.14 * x + 0.088 * (x ** 2)
    
    # Curva 2 (Dadosfera): Começa em patamar previsível e tem inclinação suave e linear
    # Representa custo SaaS elástico, previsível e sem sobrecarga de infraestrutura
    y_dadosfera = 2.8 + 0.38 * x
    
    return x, y_infra, y_dadosfera

def plot_crossover_chart() -> plt.Figure:
    """Gera 1 gráfico conceitual único com identificação clara das linhas e eixos conceituais X e Y."""
    plt.rcParams["font.sans-serif"] = ["Segoe UI", "DejaVu Sans", "Helvetica", "Arial", "sans-serif"]
    fig = plt.figure(figsize=(16, 9), facecolor=COLORS["bg"], dpi=300)
    
    ax = fig.add_axes([0.10, 0.12, 0.68, 0.76], facecolor=COLORS["bg"])
    
    # Remove todas as bordas padrão de gráfico
    for spine in ["top", "right", "left", "bottom"]:
        ax.spines[spine].set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])
    
    x, y_infra, y_dadosfera = generate_smooth_curves()
    
    # -------------------------------------------------------------
    # 1. Eixos Minimalistas com Setas Direcionais
    # -------------------------------------------------------------
    # Eixo X (Linha de Base Horizontal)
    ax.annotate(
        "", xy=(9.8, 0.6), xytext=(0.2, 0.6),
        arrowprops=dict(arrowstyle="-|>", color=COLORS["axis_line"], lw=2.2, mutation_scale=18),
        zorder=2
    )
    # Eixo Y (Linha Vertical)
    ax.annotate(
        "", xy=(0.2, np.max(y_infra) * 1.14), xytext=(0.2, 0.6),
        arrowprops=dict(arrowstyle="-|>", color=COLORS["axis_line"], lw=2.2, mutation_scale=18),
        zorder=2
    )
    
    # -------------------------------------------------------------
    # 2. Rótulos Conceituais dos Eixos X e Y
    # -------------------------------------------------------------
    # Rótulo do Eixo Y (Vertical no topo)
    ax.text(
        0.2, np.max(y_infra) * 1.18, "Custo Total de Operação & Sustentação (TCO)",
        color=COLORS["axis_text"], fontsize=12.5, fontweight="bold", ha="left", va="bottom"
    )
    ax.text(
        0.2, np.max(y_infra) * 1.13, "(Provisionamento, Headcount, Apps, Dados)",
        color=COLORS["sub_text"], fontsize=11.0, fontweight="semibold", ha="left", va="bottom"
    )
    
    # Rótulo do Eixo X (Horizontal no centro inferior)
    ax.text(
        5.0, 0.15, "Tempo / Volume de Dados & Expansão de Casos de Uso ->",
        color=COLORS["axis_text"], fontsize=12.0, fontweight="bold", ha="center", va="top"
    )
    
    # -------------------------------------------------------------
    # 3. Preenchimentos Suaves sob as Curvas
    # -------------------------------------------------------------
    ax.fill_between(x, 0.6, y_infra, color=COLORS["red_fill"], alpha=0.32, zorder=2)
    ax.fill_between(x, 0.6, y_dadosfera, color=COLORS["green_fill"], alpha=0.32, zorder=2)
    
    # -------------------------------------------------------------
    # 4. Curvas Principais de Tendência (com segmento final na seta)
    # -------------------------------------------------------------
    # Curva Vermelha (Infraestrutura Própria)
    ax.plot(x[:-10], y_infra[:-10], color=COLORS["red_line"], linewidth=4.8, zorder=4)
    # Seta final integrada da Curva Vermelha
    ax.annotate(
        "", xy=(x[-1], y_infra[-1]), xytext=(x[-12], y_infra[-12]),
        arrowprops=dict(arrowstyle="-|>", color=COLORS["red_line"], lw=4.8, mutation_scale=22),
        zorder=5
    )
    
    # Curva Verde (Dadosfera)
    ax.plot(x[:-10], y_dadosfera[:-10], color=COLORS["green_line"], linewidth=4.8, zorder=4)
    # Seta final integrada da Curva Verde
    ax.annotate(
        "", xy=(x[-1], y_dadosfera[-1]), xytext=(x[-12], y_dadosfera[-12]),
        arrowprops=dict(arrowstyle="-|>", color=COLORS["green_line"], lw=4.8, mutation_scale=22),
        zorder=5
    )
    
    # -------------------------------------------------------------
    # 5. Ponto de Cruzamento (Card Break-even Original)
    # -------------------------------------------------------------
    idx_cross = np.argmin(np.abs(y_infra - y_dadosfera))
    x_cross = x[idx_cross]
    y_cross = y_infra[idx_cross]
    
    # Linha vertical tracejada no ponto de cruzamento
    ax.plot([x_cross, x_cross], [0.6, y_cross], color=COLORS["axis_line"], linestyle=":", linewidth=2.0, zorder=3)
    ax.scatter([x_cross], [y_cross], color=COLORS["crossover_dot"], s=110, edgecolors=COLORS["bg"], linewidth=2.5, zorder=6)
    
    # Card / Badge do Ponto de Inflexão (Formato Original com 2 linhas e borda sutil)
    ax.text(
        x_cross, y_cross + 0.60, "Ponto de Inflexão\n(Break-even)",
        color=COLORS["crossover_dot"], fontsize=11.0, fontweight="bold", ha="center", va="bottom",
        bbox=dict(boxstyle="round,pad=0.25", facecolor=COLORS["bg"], edgecolor=COLORS["axis_line"], alpha=0.9)
    )
    
    # -------------------------------------------------------------
    # 6. Identificação Direta das Linhas
    # -------------------------------------------------------------
    # Rótulo da Linha Vermelha (Infraestrutura Própria)
    ax.text(
        x[-1] + 0.25, y_infra[-1] + 0.35, "Custo Infraestrutura Própria (AWS DIY)",
        color=COLORS["red_line"], fontsize=12.2, fontweight="bold", ha="left", va="bottom"
    )
    ax.text(
        x[-1] + 0.25, y_infra[-1] - 0.20, "• Crescimento Exponencial de Custos\n• Provisionamento, Headcount, Apps, Dados",
        color=COLORS["red_line"], fontsize=10.6, fontweight="semibold", ha="left", va="top"
    )
    
    # Rótulo da Linha Verde (Dadosfera)
    ax.text(
        x[-1] + 0.25, y_dadosfera[-1] + 0.35, "Custo com Dadosfera",
        color=COLORS["green_line"], fontsize=12.2, fontweight="bold", ha="left", va="bottom"
    )
    ax.text(
        x[-1] + 0.25, y_dadosfera[-1] - 0.20, "• Crescimento Suave e Previsível\n• Plataforma Unificada SaaS",
        color=COLORS["green_line"], fontsize=10.6, fontweight="semibold", ha="left", va="top"
    )
    
    ax.set_xlim(-0.1, 10.0)
    ax.set_ylim(0.0, np.max(y_infra) * 1.25)
    
    return fig

def main() -> None:
    fig_crossover = plot_crossover_chart()
    crossover_path = OUTPUT_DIR / "chart_custo_infra_vs_dadosfera_crossover.png"
    fig_crossover.savefig(str(crossover_path), dpi=300, bbox_inches="tight", facecolor=COLORS["bg"])
    plt.close(fig_crossover)
    print(f"[SUCCESS] Gráfico Crossover gerado em: {crossover_path}")

if __name__ == "__main__":
    main()
