#!/usr/bin/env python3
"""
generate_chart.py
Gera o gráfico executivo da view 'staff-pain-point' adaptado à argumentação do pitch da Dadosfera.
Utiliza a estilização de referência (Série Histórica + Bifurcação em 3 Cenários com Direct Labeling)
aplicada a estimativas moderadas e realistas de dimensionamento de equipe técnica (Engenheiros de Infra/DevOps na AWS DIY vs Analistas na Dadosfera).
Visualização corporativa (Fundo Branco Puro, 16:9 Widescreen, 300 DPI, Tipografia Moderna).
"""

from typing import Final, Dict, List, Tuple
import os
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

OUTPUT_DIR: Final[Path] = Path(__file__).resolve().parent
OUTPUT_IMAGE_PATH: Final[Path] = OUTPUT_DIR / "chart_staff_pain_point.png"

# Paleta Semântica Executiva Refinada
COLORS: Final[Dict[str, str]] = {
    "bg": "#FFFFFF",
    "title": "#1E293B",          # Slate 800
    "subtitle": "#64748B",       # Slate 500
    "axis_label": "#334155",     # Slate 700
    "tick_text": "#475569",      # Slate 600
    "grid": "#E2E8F0",           # Slate 200
    "border": "#CBD5E1",         # Slate 300
    "hist_blue": "#2563EB",      # Azul Royal (Histórico)
    "proj_red": "#DC2626",       # Vermelho Coral (AWS DIY - Alta Complexidade)
    "proj_yellow": "#D97706",    # Âmbar / Dourado (AWS DIY - Moderada)
    "proj_green": "#059669",     # Verde Esmeralda (Plataforma Dadosfera)
    "badge_bg": "#ECFDF5",       # Fundo Suave Verde
    "badge_border": "#6EE7B7",   # Borda Verde
}

def plot_staff_pain_point() -> plt.Figure:
    """Gera a figura executiva de evolução de headcount com estimativas moderadas e realistas."""
    plt.rcParams["font.sans-serif"] = ["Segoe UI", "DejaVu Sans", "Helvetica", "Arial", "sans-serif"]
    
    fig = plt.figure(figsize=(16, 9), facecolor=COLORS["bg"], dpi=300)
    
    # -------------------------------------------------------------
    # 1. Área Principal dos Eixos
    # -------------------------------------------------------------
    ax = fig.add_axes([0.08, 0.12, 0.86, 0.65], facecolor=COLORS["bg"])
    
    # Configuração dos eixos e spines
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    ax.spines["left"].set_color(COLORS["border"])
    ax.spines["left"].set_linewidth(1.3)
    ax.spines["bottom"].set_color(COLORS["border"])
    ax.spines["bottom"].set_linewidth(1.3)
    
    # -------------------------------------------------------------
    # 2. Dados das Séries Temporais (Estimativas Moderadas e Realistas)
    # -------------------------------------------------------------
    # Série Histórica: 2020 a 2024
    years_hist = np.array([2020, 2021, 2022, 2023, 2024])
    vals_hist = np.array([2.0, 2.0, 3.0, 3.0, 3.0])
    
    # Anos de Projeção: 2024 a 2030 (Bifurcação a partir do baseline 2024 = 3 staff)
    years_proj = np.array([2024, 2025, 2026, 2027, 2028, 2029, 2030])
    
    # Cenário 1: AWS DIY - Alta Complexidade (+Infra, DevOps, Shards, Redis & IAM)
    vals_p_high = np.array([3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 8.0])
    
    # Cenário 2: AWS DIY - Expansão Moderada
    vals_p_mod = np.array([3.0, 3.0, 4.0, 4.0, 5.0, 5.0, 5.0])
    
    # Cenário 3: Plataforma Dadosfera - Escala Elástica & Equipe Estável (Analytics Engineers / SQL)
    vals_p_ddf = np.array([3.0, 2.0, 2.0, 2.0, 2.0, 2.5, 2.5])
    
    # -------------------------------------------------------------
    # 3. Plotagem das Linhas e Séries
    # -------------------------------------------------------------
    # Linha Histórica (Azul)
    ax.plot(years_hist, vals_hist, color=COLORS["hist_blue"], linewidth=3.4, zorder=4)
    ax.scatter(years_hist[:-1], vals_hist[:-1], color=COLORS["hist_blue"], s=45, zorder=5)
    
    # Linhas de Projeção (Vermelho, Âmbar, Verde)
    ax.plot(years_proj, vals_p_high, color=COLORS["proj_red"], linewidth=3.2, zorder=4)
    ax.scatter(years_proj[1:], vals_p_high[1:], color=COLORS["proj_red"], s=45, zorder=5)
    
    ax.plot(years_proj, vals_p_mod, color=COLORS["proj_yellow"], linewidth=3.2, zorder=4)
    ax.scatter(years_proj[1:], vals_p_mod[1:], color=COLORS["proj_yellow"], s=45, zorder=5)
    
    ax.plot(years_proj, vals_p_ddf, color=COLORS["proj_green"], linewidth=3.4, zorder=4)
    ax.scatter(years_proj[1:], vals_p_ddf[1:], color=COLORS["proj_green"], s=55, zorder=5)
    
    # Marcador de bifurcação destacado em 2024
    ax.scatter([2024], [3.0], color=COLORS["hist_blue"], s=80, edgecolors=COLORS["bg"], linewidth=2.0, zorder=6)
    
    # -------------------------------------------------------------
    # 4. Rótulos Diretos de Valores nos Vértices (Direct Labeling)
    # -------------------------------------------------------------
    # Rótulos da série histórica
    ax.text(2020, 2.0 + 0.22, "2 staff", color=COLORS["hist_blue"], fontsize=10.5, fontweight="bold", ha="center", va="bottom")
    ax.text(2021, 2.0 + 0.22, "2 staff", color=COLORS["hist_blue"], fontsize=10.5, fontweight="bold", ha="center", va="bottom")
    ax.text(2022, 3.0 + 0.22, "3 staff", color=COLORS["hist_blue"], fontsize=10.5, fontweight="bold", ha="center", va="bottom")
    ax.text(2023, 3.0 + 0.22, "3 staff", color=COLORS["hist_blue"], fontsize=10.5, fontweight="bold", ha="center", va="bottom")
    ax.text(2024, 3.0 + 0.28, "3 staff\n(Baseline PoC)", color=COLORS["hist_blue"], fontsize=10.0, fontweight="bold", ha="center", va="bottom")
    
    # Rótulos da Projeção AWS DIY - Alta Complexidade (Vermelho)
    for yr, val in zip(years_proj[1:-1], vals_p_high[1:-1]):
        ax.text(yr, val + 0.22, f"{int(val)} staff", color=COLORS["proj_red"], fontsize=10.5, fontweight="bold", ha="center", va="bottom")
    # Ponto Final 2030 (com custo anual e foco de esforço)
    ax.text(2030, 8.0 + 0.25, "8 staff\n(R$ 1,0M/ano | 80% Infra)", color=COLORS["proj_red"], fontsize=11.0, fontweight="bold", ha="center", va="bottom")
    
    # Rótulos da Projeção AWS DIY - Moderada (Dourado)
    for yr, val in zip(years_proj[1:-1], vals_p_mod[1:-1]):
        offset_y = 0.22 if yr != 2025 else 0.22
        va_pos = "bottom"
        ax.text(yr, val + offset_y, f"{int(val)} staff", color=COLORS["proj_yellow"], fontsize=10.0, fontweight="bold", ha="center", va=va_pos)
    # Ponto Final 2030 (com custo anual)
    ax.text(2030 + 0.05, 5.0 + 0.22, "5 staff\n(R$ 650k/ano)", color=COLORS["proj_yellow"], fontsize=10.5, fontweight="bold", ha="left", va="center")
    
    # Rótulos da Dadosfera (Verde)
    ax.text(2025, 2.0 - 0.38, "2 staff", color=COLORS["proj_green"], fontsize=10.0, fontweight="bold", ha="center", va="top")
    ax.text(2026, 2.0 - 0.38, "2 staff", color=COLORS["proj_green"], fontsize=10.0, fontweight="bold", ha="center", va="top")
    ax.text(2027, 2.0 - 0.38, "2 staff", color=COLORS["proj_green"], fontsize=10.0, fontweight="bold", ha="center", va="top")
    ax.text(2028, 2.0 - 0.38, "2 staff", color=COLORS["proj_green"], fontsize=10.0, fontweight="bold", ha="center", va="top")
    ax.text(2029, 2.5 - 0.38, "2-3 staff", color=COLORS["proj_green"], fontsize=10.0, fontweight="bold", ha="center", va="top")
    # Ponto Final 2030 Dadosfera
    ax.text(2030, 2.5 - 0.45, "2 a 3 staff\n(R$ 300k/ano | 80% Negócio)", color=COLORS["proj_green"], fontsize=11.0, fontweight="bold", ha="center", va="top")
    
    # -------------------------------------------------------------
    # 5. Configuração dos Eixos X e Y
    # -------------------------------------------------------------
    ax.set_xlim(2019.4, 2030.8)
    ax.set_ylim(0.5, 9.5)
    
    # Ticks do Eixo X
    x_ticks = [2020, 2021, 2022, 2023, 2024, 2025, 2026, 2027, 2028, 2029, 2030]
    ax.set_xticks(x_ticks)
    ax.set_xticklabels([str(yr) for yr in x_ticks], fontsize=11.0, color=COLORS["tick_text"], fontweight="bold")
    ax.set_xlabel("Ano / Evolução Temporal & Expansão de Infraestrutura, Pipelines, Fontes e Casos de Uso", fontsize=12.0, color=COLORS["axis_label"], fontweight="bold", labelpad=12)
    
    # Ticks do Eixo Y
    y_ticks = [2, 4, 6, 8, 10]
    y_labels = ["2", "4", "6", "8", "10 staff"]
    ax.set_yticks(y_ticks)
    ax.set_yticklabels(y_labels, fontsize=11.0, color=COLORS["tick_text"], fontweight="bold")
    ax.set_ylabel("Headcount Técnico Necessário (Staff)", fontsize=12.0, color=COLORS["axis_label"], fontweight="bold", labelpad=12)
    
    # Grade horizontal sutil
    ax.grid(axis="y", color=COLORS["grid"], linestyle="--", linewidth=1.0, alpha=0.7, zorder=1)
    
    # -------------------------------------------------------------
    # 6. Cabeçalho Executivo & Legenda Superior no Padrão da Imagem
    # -------------------------------------------------------------
    # Título Principal
    fig.text(0.08, 0.92, "Projeção de Headcount Técnico & Sobrecarga de Infraestrutura", fontsize=21, fontweight="bold", color=COLORS["title"])
    # Subtítulo abrangente
    fig.text(0.08, 0.878, "Demanda de equipe com a expansão de infraestrutura, pipelines, DevOps, governança e casos de uso", fontsize=12.5, color=COLORS["subtitle"])
    
    # Legenda Superior com Swatches de Linhas
    legend_items = [
        ("Histórico (AWS DIY)", COLORS["hist_blue"]),
        ("AWS DIY: Alta Complexidade (+Infra / DevOps)", COLORS["proj_red"]),
        ("AWS DIY: Expansão Moderada", COLORS["proj_yellow"]),
        ("Plataforma Dadosfera: Equipe Enxuta & Estável", COLORS["proj_green"]),
    ]
    
    leg_x_start = 0.08
    for label, col in legend_items:
        fig.patches.append(patches.Rectangle((leg_x_start, 0.838), 0.014, 0.004, facecolor=col, edgecolor="none", transform=fig.transFigure))
        fig.text(leg_x_start + 0.018, 0.837, label, fontsize=10.0, color=COLORS["axis_label"], fontweight="bold", va="center")
        leg_x_start += 0.222
        
    return fig

def main() -> None:
    fig = plot_staff_pain_point()
    fig.savefig(str(OUTPUT_IMAGE_PATH), dpi=300, bbox_inches="tight", facecolor=COLORS["bg"])
    plt.close(fig)
    print(f"[SUCCESS] Gráfico executivo de staff pain point gerado com sucesso em: {OUTPUT_IMAGE_PATH}")

if __name__ == "__main__":
    main()
