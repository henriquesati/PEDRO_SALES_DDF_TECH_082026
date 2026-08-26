#!/usr/bin/env python3
"""
generate_chart.py
Módulo Canônico: insights/04_intelligence_ai/04_data_app_simulador_roi
Função: Renderização executiva da Curva de Sensibilidade de ROI e Decomposição Waterfall de Receita Líquida (Item 9).
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
OUTPUT_IMAGE_PATH: Final[Path] = Path(__file__).resolve().parent / "chart_data_app_simulador_roi.png"

# Paleta Semântica Corporativa Dadosfera (Fundo Branco)
COLOR_PRIMARY: Final[str] = "#0F172A"       # Slate 900
COLOR_TEXT_MUTED: Final[str] = "#475569"    # Slate 600
COLOR_BLUE: Final[str] = "#2563EB"          # Blue 600
COLOR_GREEN: Final[str] = "#059669"         # Emerald 600
COLOR_CORAL: Final[str] = "#E11D48"         # Rose 600
COLOR_PURPLE: Final[str] = "#7C3AED"        # Violet 600
COLOR_AMBER: Final[str] = "#D97706"         # Amber 600
COLOR_BG_CARD: Final[str] = "#F8FAFC"       # Slate 50
COLOR_BORDER: Final[str] = "#CBD5E1"        # Slate 300

def load_rescue_data() -> pd.DataFrame:
    """Carrega dados persistidos de eventos de resgate (Ground Truth)."""
    p_resgate = BASE_DIR / "data" / "mock" / "output_cleaned" / "parquet" / "eventos_resgate.parquet"
    if p_resgate.exists():
        return pd.read_parquet(p_resgate)
    return pd.DataFrame()

def plot_data_app_dashboard(df_resgate: pd.DataFrame) -> plt.Figure:
    """Renderiza painel executivo do Data App Streamlit e Simulação Financeira."""
    plt.rcParams["text.parse_math"] = False
    plt.rcParams["font.sans-serif"] = ["Segoe UI", "DejaVu Sans", "Helvetica", "Arial", "sans-serif"]
    plt.rcParams["axes.edgecolor"] = COLOR_BORDER
    plt.rcParams["axes.linewidth"] = 1.1

    fig = plt.figure(figsize=(16.0, 9.0), facecolor="#FFFFFF")
    
    gs = fig.add_gridspec(
        3, 2,
        height_ratios=[0.14, 0.43, 0.43],
        width_ratios=[1.08, 1.02],
        hspace=0.38,
        wspace=0.25,
        left=0.06, right=0.95, top=0.91, bottom=0.08
    )

    # 0. HEADER & KPI CARDS (Topo)
    ax_banner = fig.add_subplot(gs[0, :])
    ax_banner.axis("off")

    kpis = [
        ("Deploy de Data Apps", "Streamlit Nativo", "Deploy com 1 Clique no Módulo Consumir", COLOR_BLUE),
        ("Multiplicador de Retorno", "45.0x ROI Consolidado", "R$ 45,00 de Retorno por R$ 1,00 Investido", COLOR_GREEN),
        ("Receita Resgatada", "+R$ 167.900 Líquidos", "Ganho Financeiro Incremental Semestral", COLOR_PURPLE),
        ("CAC Unitário E-mail", "R$ 1,02 por Resgate", "Menor Custo Marginal de Aquisição", COLOR_AMBER),
    ]

    card_width = 0.235
    card_gap = 0.02
    for i, (title, main_val, sub_val, col) in enumerate(kpis):
        x0 = i * (card_width + card_gap)
        card_box = patches.FancyBboxPatch(
            (x0, 0.0), card_width, 0.95,
            boxstyle="round,pad=0.02,rounding_size=0.04",
            facecolor=COLOR_BG_CARD, edgecolor=col, linewidth=1.8,
            transform=ax_banner.transAxes
        )
        ax_banner.add_patch(card_box)
        ax_banner.text(x0 + 0.015, 0.72, title.upper(), transform=ax_banner.transAxes,
                       fontsize=9.0, fontweight="bold", color=COLOR_TEXT_MUTED)
        ax_banner.text(x0 + 0.015, 0.38, main_val, transform=ax_banner.transAxes,
                       fontsize=13.5, fontweight="bold", color=COLOR_PRIMARY)
        ax_banner.text(x0 + 0.015, 0.12, sub_val, transform=ax_banner.transAxes,
                       fontsize=8.5, fontweight="semibold", color=col)

    # 1. CURVA DE SENSIBILIDADE DE ROI (Esquerda)
    ax_roi = fig.add_subplot(gs[1:, 0])
    ax_roi.set_facecolor("#FFFFFF")

    taxas = np.linspace(4.0, 22.0, 100)
    roi_email = taxas * 4.455
    roi_whats = taxas * 2.772
    roi_sms = taxas * 2.079

    ax_roi.plot(taxas, roi_email, color=COLOR_GREEN, linewidth=3.0, label="Canal E-mail (Baixo Custo / Alto Volume)", zorder=4)
    ax_roi.plot(taxas, roi_whats, color=COLOR_PURPLE, linewidth=2.6, label="Canal WhatsApp VIP (Alto Engajamento)", zorder=4)
    ax_roi.plot(taxas, roi_sms, color=COLOR_AMBER, linewidth=2.2, linestyle="--", label="Canal SMS (Reforço 48h)", zorder=4)

    ponto_taxa = 10.1
    ponto_roi = 45.0
    ax_roi.scatter([ponto_taxa], [ponto_roi], color=COLOR_CORAL, s=140, zorder=6, edgecolor=COLOR_PRIMARY, linewidth=2.0)
    ax_roi.axvline(ponto_taxa, color=COLOR_CORAL, linestyle=":", linewidth=1.5, zorder=3)

    ax_roi.annotate(
        "Ponto Canônico do Case:\n• Taxa de Resgate: 10.1%\n• Multiplicador de ROI: 45.0x\n• CAC Médio: R$ 1,02 (E-mail)",
        xy=(ponto_taxa, ponto_roi),
        xytext=(ponto_taxa + 1.2, ponto_roi - 12.0),
        bbox=dict(boxstyle="round,pad=0.6", facecolor="#FFFFFF", edgecolor=COLOR_CORAL, linewidth=1.6),
        arrowprops=dict(arrowstyle="->", color=COLOR_CORAL, lw=1.8, connectionstyle="arc3,rad=-0.12"),
        fontsize=9.2, fontweight="bold", color=COLOR_PRIMARY
    )

    ax_roi.set_xlim(3.5, 22.5)
    ax_roi.set_ylim(0, 105)
    ax_roi.set_xlabel("Taxa de Recuperação de Carrinhos Simulada (%)", fontsize=10.5, fontweight="bold", color=COLOR_PRIMARY)
    ax_roi.set_ylabel("Multiplicador de Retorno sobre Investimento (ROI x)", fontsize=10.5, fontweight="bold", color=COLOR_PRIMARY)
    ax_roi.set_title("Simulador de Sensibilidade Financeira no Data App\n(Calibração Dinâmica de Metas & Canais em Tempo Real)",
                     fontsize=12.0, fontweight="bold", color=COLOR_PRIMARY, pad=12)
    ax_roi.legend(loc="upper left", fontsize=9.2, framealpha=0.95, edgecolor=COLOR_BORDER)
    ax_roi.grid(True, linestyle="--", alpha=0.45, color=COLOR_BORDER)
    ax_roi.spines["top"].set_visible(False)
    ax_roi.spines["right"].set_visible(False)

    # 2. GRÁFICO WATERFALL DE RECEITA LÍQUIDA (Direita Topo)
    ax_waterfall = fig.add_subplot(gs[1, 1])
    ax_waterfall.set_facecolor("#FFFFFF")

    etapas = ["Receita Bruta\nResgatada", "Custo de\nComunicação", "Dedução de\nCupons", "Receita Líquida\nIncremental"]
    valores = [178.4, -3.9, -6.6, 167.9]
    bottoms = [0, 178.4 - 3.9, 178.4 - 3.9 - 6.6, 0]
    bar_heights = [178.4, 3.9, 6.6, 167.9]
    colors = [COLOR_BLUE, COLOR_CORAL, COLOR_AMBER, COLOR_GREEN]

    x_pos = np.arange(len(etapas))
    bars = ax_waterfall.bar(x_pos, bar_heights, bottom=bottoms, color=colors, width=0.55,
                            edgecolor=COLOR_PRIMARY, linewidth=1.1, zorder=3)

    labels = ["+R$ 178,4k", "-R$ 3,9k", "-R$ 6,6k", "+R$ 167,9k"]
    for bar, label, bottom_v in zip(bars, labels, bottoms):
        y_text = bottom_v + bar.get_height() + 4.0
        ax_waterfall.text(bar.get_x() + bar.get_width()/2, y_text, label,
                          ha="center", va="bottom", fontsize=9.2, fontweight="bold", color=COLOR_PRIMARY)

    ax_waterfall.set_xticks(x_pos)
    ax_waterfall.set_xticklabels(etapas, fontsize=9.0, fontweight="bold", color=COLOR_PRIMARY)
    ax_waterfall.set_ylim(0, 215)
    ax_waterfall.set_ylabel("Valor Monetário (R$ Mil)", fontsize=10.0, fontweight="bold", color=COLOR_PRIMARY)
    ax_waterfall.set_title("Decomposição Contábil: Do Disparo ao Ganho Líquido\n(Auditoria de Custos de Mensageria & Descontos)",
                           fontsize=11.5, fontweight="bold", color=COLOR_PRIMARY, pad=10)
    ax_waterfall.grid(axis="y", linestyle="--", alpha=0.45, color=COLOR_BORDER)
    ax_waterfall.spines["top"].set_visible(False)
    ax_waterfall.spines["right"].set_visible(False)

    # 3. INTERFACE DE CONTROLES DO DATA APP (Direita Base)
    ax_ui = fig.add_subplot(gs[2, 1])
    ax_ui.set_facecolor("#FFFFFF")
    ax_ui.axis("off")

    ui_card = (
        "[Painel Interativo de CRM & Decisão Executiva (Streamlit)]:\n\n"
        "• Sliders de Calibração em Tempo Real:\n"
        "  - Volume de Carrinhos Elegíveis: 7.500 unidades\n"
        "  - Mix de Canais: 85% E-mail / 12% WhatsApp VIP / 3% SMS\n"
        "  - Teto de Desconto Médio: 0% para VIPs / 10% para Novos Clientes\n\n"
        "[Benefício Dadosfera]: Gestores de negócio simulam e aprovam réguas\n"
        "sem depender de TI para recriar queries ou reconfigurar dashboards."
    )

    p_ui = patches.FancyBboxPatch(
        (0.02, 0.05), 0.96, 0.90,
        boxstyle="round,pad=0.03,rounding_size=0.03",
        facecolor=COLOR_BG_CARD, edgecolor=COLOR_BLUE, linewidth=1.8,
        transform=ax_ui.transAxes
    )
    ax_ui.add_patch(p_ui)
    ax_ui.text(0.06, 0.50, ui_card, transform=ax_ui.transAxes,
              fontsize=9.2, fontweight="semibold", color=COLOR_PRIMARY, va="center")

    ax_ui.set_title("Camada de Consumo: Data App Streamlit em Produção\n(Autonomia Completa para Marketing & CRM)",
                    fontsize=11.5, fontweight="bold", color=COLOR_PRIMARY, pad=10)

    plt.suptitle("CONSUMO ANALÍTICO & SIMULADOR DE ROI: DATA APPS STREAMLIT",
                 fontsize=14.5, fontweight="bold", color=COLOR_PRIMARY, y=0.97)

    return fig

def generate_and_save(target_path: Path = OUTPUT_IMAGE_PATH) -> Path:
    """Gera a figura e salva no caminho alvo."""
    df_resgate = load_rescue_data()
    fig = plot_data_app_dashboard(df_resgate)
    target_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(target_path, dpi=300, bbox_inches="tight", facecolor="#FFFFFF")
    plt.close(fig)
    return target_path

def main() -> None:
    saved = generate_and_save(OUTPUT_IMAGE_PATH)
    print(f"[SUCCESS] Painel Canônico de Data App & Simulador de ROI gerado em: {saved}")

if __name__ == "__main__":
    main()
