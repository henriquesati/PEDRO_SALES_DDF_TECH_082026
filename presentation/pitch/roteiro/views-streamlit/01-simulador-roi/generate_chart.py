#!/usr/bin/env python3
"""
generate_chart.py
Módulo: presentation/pitch/roteiro/views-streamlit/01-simulador-roi
Função: Renderização executiva em alta resolução da Tela 1 do Data App Streamlit (Simulador de ROI & Sensibilidade).
Padrão Gráfico: Fundo Branco Puro (#FFFFFF), 16:9 Widescreen, 300 DPI, charts-maker standard.
"""

from typing import Final, Tuple
import os
import sys
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def get_base_dir() -> Path:
    curr = Path(__file__).resolve().parent
    while curr and curr.parent != curr:
        if (curr / "data" / "mock").exists():
            return curr
        curr = curr.parent
    return Path.cwd().resolve()

BASE_DIR: Final[Path] = get_base_dir()
OUTPUT_IMAGE_PATH: Final[Path] = Path(__file__).resolve().parent / "chart_streamlit_simulador_roi.png"

# Paleta Semântica Corporativa Dadosfera
COLOR_PRIMARY: Final[str] = "#0F172A"       # Slate 900
COLOR_TEXT_MUTED: Final[str] = "#475569"    # Slate 600
COLOR_BLUE: Final[str] = "#2563EB"          # Blue 600 (E-mail / Destaque)
COLOR_GREEN: Final[str] = "#059669"         # Emerald 600 (ROI / Sucesso)
COLOR_AMBER: Final[str] = "#D97706"         # Amber 600 (SMS / Atenção)
COLOR_PURPLE: Final[str] = "#7C3AED"        # Violet 600 (WhatsApp VIP / IA)
COLOR_CORAL: Final[str] = "#E11D48"         # Rose 600 (Custo / Alerta)
COLOR_BG_CARD: Final[str] = "#F8FAFC"       # Slate 50
COLOR_BORDER: Final[str] = "#CBD5E1"        # Slate 300
COLOR_SIDEBAR: Final[str] = "#F1F5F9"       # Slate 100

def plot_streamlit_roi_view() -> plt.Figure:
    """Renderiza a interface executiva da Aba 1 (Simulador de ROI) do Data App Streamlit."""
    plt.rcParams["text.parse_math"] = False
    plt.rcParams["font.sans-serif"] = ["Segoe UI", "DejaVu Sans", "Helvetica", "Arial", "sans-serif"]
    plt.rcParams["axes.edgecolor"] = COLOR_BORDER
    plt.rcParams["axes.linewidth"] = 1.1

    fig = plt.figure(figsize=(16.0, 9.0), facecolor="#FFFFFF")
    
    # Layout Grid: Top App Header (0.08), Content (0.92) com Sidebar Esquerda (0.24) e Painel Principal (0.76)
    # Subdivisões do Painel Principal: KPIs (Top), Gráfico de Sensibilidade (Meio Esquerdo), Gráfico de Canais (Meio Direito)
    
    # 0. STREAMLIT APP HEADER & TABS BAR
    ax_top = fig.add_axes([0.04, 0.90, 0.92, 0.08])
    ax_top.axis("off")
    
    # App Banner
    ax_top.text(0.0, 0.70, "DADOSFERA DATA APP  |  RECUPERAÇÃO DE CARRINHOS (ITEM 9 & BÔNUS)",
                fontsize=13.0, fontweight="bold", color=COLOR_PRIMARY)
    ax_top.text(0.0, 0.20, "Tenant: pedro-sales  •  Lakehouse: Snowflake (Star Schema Gold)  •  Governança: 100% Pydantic & Data Quality",
                fontsize=8.5, fontweight="normal", color=COLOR_TEXT_MUTED)
    
    # Tabs Indicator
    tabs = [
        ("[ATIVO] 1. Simulador de ROI & Sensibilidade", COLOR_BLUE, True),
        ("2. Explorador Semântico de Catálogo", COLOR_TEXT_MUTED, False),
        ("3. Copiloto Prescritivo de Resgate", COLOR_TEXT_MUTED, False),
        ("4. Vitrine Visual de Produtos", COLOR_TEXT_MUTED, False),
    ]
    tab_w = 0.235
    for i, (t_name, t_col, is_active) in enumerate(tabs):
        tx = i * (tab_w + 0.015)
        t_box = patches.FancyBboxPatch(
            (tx, -0.65), tab_w, 0.55,
            boxstyle="round,pad=0.0,rounding_size=0.02",
            facecolor="#EFF6FF" if is_active else "#FFFFFF",
            edgecolor=COLOR_BLUE if is_active else COLOR_BORDER,
            linewidth=1.4 if is_active else 1.0,
            transform=ax_top.transAxes
        )
        ax_top.add_patch(t_box)
        ax_top.text(tx + tab_w/2.0, -0.38, t_name, transform=ax_top.transAxes,
                    fontsize=8.2, fontweight="bold" if is_active else "normal",
                    color=COLOR_BLUE if is_active else COLOR_TEXT_MUTED, ha="center", va="center")

    # 1. STREAMLIT SIDEBAR (Painel de Controles & Parâmetros de Simulação)
    ax_side = fig.add_axes([0.04, 0.06, 0.22, 0.76])
    ax_side.axis("off")
    
    side_box = patches.FancyBboxPatch(
        (0.0, 0.0), 1.0, 1.0,
        boxstyle="round,pad=0.0,rounding_size=0.02",
        facecolor=COLOR_SIDEBAR, edgecolor=COLOR_BORDER, linewidth=1.2,
        transform=ax_side.transAxes
    )
    ax_side.add_patch(side_box)
    
    ax_side.text(0.08, 0.94, "PARÂMETROS DO SIMULADOR", fontsize=9.5, fontweight="bold", color=COLOR_PRIMARY)
    ax_side.text(0.08, 0.90, "Ajuste os cenários em tempo real:", fontsize=8.0, color=COLOR_TEXT_MUTED)
    
    controls = [
        ("Orçamento Total de Disparos", "R$ 15.000,00", 0.78),
        ("Taxa Alvo de Conversão", "10.1% (+50% vs Basal)", 0.64),
        ("Margem Bruta Média", "28.5% (E-commerce)", 0.50),
        ("Mix E-mail Transacional", "85% do Budget (R$ 0,05/env)", 0.36),
        ("Mix WhatsApp VIP", "12% do Budget (R$ 0,30/env)", 0.22),
        ("Mix SMS & Push Marketing", "3% do Budget (Dispersão)", 0.08),
    ]
    
    for label, val_text, y_c in controls:
        ax_side.text(0.08, y_c + 0.05, label, fontsize=8.2, fontweight="bold", color=COLOR_PRIMARY)
        # Slider visual representation
        slider_bg = patches.FancyBboxPatch(
            (0.08, y_c - 0.01), 0.84, 0.035,
            boxstyle="round,pad=0.0,rounding_size=0.01",
            facecolor="#E2E8F0", edgecolor="none", transform=ax_side.transAxes
        )
        ax_side.add_patch(slider_bg)
        slider_fill = patches.FancyBboxPatch(
            (0.08, y_c - 0.01), 0.60, 0.035,
            boxstyle="round,pad=0.0,rounding_size=0.01",
            facecolor=COLOR_BLUE, edgecolor="none", transform=ax_side.transAxes
        )
        ax_side.add_patch(slider_fill)
        ax_side.text(0.08, y_c - 0.05, val_text, fontsize=8.0, fontweight="semibold", color=COLOR_BLUE)

    # 2. EXECUTIVE METRIC CARDS (Topo do Painel Principal)
    ax_kpi = fig.add_axes([0.28, 0.68, 0.68, 0.14])
    ax_kpi.axis("off")
    
    kpis = [
        ("GMV Líquido Resgatado", "R$ 314.500", "+50% sobre a média orgânica", COLOR_GREEN),
        ("ROI Financeiro Global", "45.2x", "R$ 45,20 por R$ 1 investido", COLOR_BLUE),
        ("Margem Bruta Preservada", "R$ 89.632", "28.5% de margem retida", COLOR_PURPLE),
        ("Custo Médio por Resgate", "R$ 0,07", "Otimização de mix de canais", COLOR_AMBER),
    ]
    
    c_w = 0.235
    c_gap = 0.02
    for i, (k_title, k_val, k_sub, k_col) in enumerate(kpis):
        cx = i * (c_w + c_gap)
        c_box = patches.FancyBboxPatch(
            (cx, 0.0), c_w, 0.95,
            boxstyle="round,pad=0.0,rounding_size=0.03",
            facecolor=COLOR_BG_CARD, edgecolor=k_col, linewidth=1.5,
            transform=ax_kpi.transAxes
        )
        ax_kpi.add_patch(c_box)
        
        ax_kpi.text(cx + c_w/2.0, 0.72, k_title.upper(), fontsize=8.5, fontweight="bold",
                    color=COLOR_TEXT_MUTED, ha="center", va="center", transform=ax_kpi.transAxes)
        ax_kpi.text(cx + c_w/2.0, 0.40, k_val, fontsize=14.5, fontweight="bold",
                    color=COLOR_PRIMARY, ha="center", va="center", transform=ax_kpi.transAxes)
        ax_kpi.text(cx + c_w/2.0, 0.15, k_sub, fontsize=8.0, fontweight="semibold",
                    color=k_col, ha="center", va="center", transform=ax_kpi.transAxes)

    # 3. GRÁFICO ESQUERDO: CURVA DE SENSIBILIDADE ORÇAMENTÁRIA (Retorno vs Budget)
    ax_sens = fig.add_axes([0.28, 0.08, 0.32, 0.54], facecolor="#FFFFFF")
    
    budget = np.linspace(2000, 30000, 100)
    # Modelo funcional de retorno marginal com saturação logarítmica
    retorno_liquido = 45.2 * budget / (1.0 + (budget / 25000.0)**1.2) / 1000.0  # em R$ mil
    roi_curva = (retorno_liquido * 1000.0) / budget
    
    ax_sens.plot(budget / 1000.0, retorno_liquido, color=COLOR_GREEN, linewidth=3.0, label="Receita Recuperada (R$ Mil)")
    ax_sens.fill_between(budget / 1000.0, retorno_liquido, 0, color=COLOR_GREEN, alpha=0.12)
    
    # Ponto de operação calibrado
    p_budget = 15.0  # R$ 15k
    p_retorno = 314.5 # R$ 314.5k
    ax_sens.scatter([p_budget], [p_retorno], color=COLOR_BLUE, s=90, zorder=5, edgecolor=COLOR_PRIMARY, linewidth=1.5)
    ax_sens.annotate(
        f"Ponto Ótimo Calibrado\n• Investimento: R$ 15.000\n• Retorno: R$ 314.500\n• ROI: 45.2x",
        xy=(p_budget, p_retorno), xytext=(p_budget - 8.0, p_retorno - 90.0),
        bbox=dict(boxstyle="round,pad=0.5", facecolor="#FFFFFF", edgecolor=COLOR_BLUE, linewidth=1.4),
        arrowprops=dict(arrowstyle="->", color=COLOR_BLUE, lw=1.5),
        fontsize=8.5, fontweight="bold", color=COLOR_PRIMARY
    )
    
    ax_sens.set_title("Curva de Sensibilidade: Retorno Líquido vs Budget", fontsize=10.5, fontweight="bold", color=COLOR_PRIMARY, pad=10)
    ax_sens.set_xlabel("Investimento em Campanhas (R$ Mil)", fontsize=9.0, fontweight="bold", color=COLOR_PRIMARY)
    ax_sens.set_ylabel("Faturamento Resgatado (R$ Mil)", fontsize=9.0, fontweight="bold", color=COLOR_PRIMARY)
    ax_sens.set_xlim(0, 32)
    ax_sens.set_ylim(0, 420)
    ax_sens.grid(True, linestyle="--", alpha=0.45, color=COLOR_BORDER)
    ax_sens.spines["top"].set_visible(False)
    ax_sens.spines["right"].set_visible(False)

    # 4. GRÁFICO DIREITO: ALOCAÇÃO DE VERBA & EFICIÊNCIA POR CANAL
    ax_can = fig.add_axes([0.64, 0.08, 0.32, 0.54], facecolor="#FFFFFF")
    
    canais = ["E-mail Transacional", "WhatsApp VIP", "SMS Marketing", "Push Notification"]
    roi_canal = [18.4, 8.2, 2.1, 4.5]
    budget_share = [85.0, 12.0, 2.0, 1.0]
    bar_colors = [COLOR_BLUE, COLOR_PURPLE, COLOR_AMBER, COLOR_CORAL]
    
    y_pos = np.arange(len(canais))
    b_bars = ax_can.barh(y_pos - 0.16, budget_share, height=0.30, color=bar_colors, edgecolor=COLOR_PRIMARY, linewidth=1.0, label="% Alocação Verba")
    r_bars = ax_can.barh(y_pos + 0.16, [r * 4.0 for r in roi_canal], height=0.30, color="#10B981", alpha=0.85, edgecolor=COLOR_PRIMARY, linewidth=1.0, label="ROI Relativo (Multiplicador)")
    
    for bar, val in zip(b_bars, budget_share):
        ax_can.text(val + 1.2, bar.get_y() + bar.get_height()/2.0, f"{val:.0f}%",
                    va="center", ha="left", fontsize=8.5, fontweight="bold", color=COLOR_PRIMARY)
        
    for bar, r_val in zip(r_bars, roi_canal):
        ax_can.text(bar.get_width() + 1.2, bar.get_y() + bar.get_height()/2.0, f"{r_val:.1f}x",
                    va="center", ha="left", fontsize=8.5, fontweight="bold", color="#059669")
        
    ax_can.set_yticks(y_pos)
    ax_can.set_yticklabels(canais, fontsize=9.0, fontweight="bold", color=COLOR_PRIMARY)
    ax_can.set_xlim(0, 105)
    ax_can.set_xlabel("Participação no Orçamento (%) vs Multiplicador de ROI", fontsize=9.0, fontweight="bold", color=COLOR_PRIMARY)
    ax_can.set_title("Rebalanceamento Orçamentário Prescritivo (De -> Para)", fontsize=10.5, fontweight="bold", color=COLOR_PRIMARY, pad=10)
    ax_can.legend(loc="lower right", fontsize=8.2, framealpha=0.95, edgecolor=COLOR_BORDER)
    ax_can.grid(axis="x", linestyle="--", alpha=0.45, color=COLOR_BORDER)
    ax_can.spines["top"].set_visible(False)
    ax_can.spines["right"].set_visible(False)
    ax_can.invert_yaxis()

    return fig

def main() -> None:
    fig = plot_streamlit_roi_view()
    OUTPUT_IMAGE_PATH.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_IMAGE_PATH, dpi=300, bbox_inches="tight", facecolor="#FFFFFF")
    plt.close(fig)
    print(f"[SUCCESS] Tela Streamlit Simulador de ROI gerada com sucesso em: {OUTPUT_IMAGE_PATH}")

if __name__ == "__main__":
    main()
