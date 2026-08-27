#!/usr/bin/env python3
"""
generate_chart.py
Módulo: presentation/pitch/roteiro/views-streamlit/05-galeria-insights
Função: Renderização executiva da Galeria de Insights & Artefatos (Navegação por Tipos, Gráficos 300 DPI e Specs Markdown Deslizáveis).
Padrão Gráfico: Fundo Branco Puro (#FFFFFF), 16:9 Widescreen, 300 DPI, charts-maker standard.
"""

from typing import Final
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as patches

OUTPUT_IMAGE_PATH: Final[Path] = Path(__file__).resolve().parent / "chart_streamlit_galeria_insights.png"

# Paleta Semântica Corporativa Sóbria & Elegante
COLOR_PRIMARY: Final[str] = "#0F172A"       # Slate 900
COLOR_SURFACE: Final[str] = "#090D16"       # Dark Jet Surface
COLOR_TEXT_MUTED: Final[str] = "#475569"    # Slate 600
COLOR_TEXT_LIGHT: Final[str] = "#94A3B8"    # Slate 400
COLOR_BLUE: Final[str] = "#2563EB"          # Blue 600
COLOR_AMBER: Final[str] = "#D97706"         # Amber 600
COLOR_GREEN: Final[str] = "#059669"         # Emerald 600
COLOR_VIOLET: Final[str] = "#7C3AED"        # Violet 600
COLOR_BORDER: Final[str] = "#CBD5E1"        # Slate 300
COLOR_DARK_BORDER: Final[str] = "#1E293B"   # Slate 800


def plot_streamlit_insights_gallery() -> plt.Figure:
    """Renderiza o layout executivo da Galeria de Insights & Artefatos com tabs e specs deslizáveis."""
    plt.rcParams["text.parse_math"] = False
    plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Segoe UI", "Helvetica", "Arial", "sans-serif"]
    plt.rcParams["axes.edgecolor"] = COLOR_BORDER
    plt.rcParams["axes.linewidth"] = 1.1

    fig = plt.figure(figsize=(16.0, 9.0), facecolor="#FFFFFF")

    # =========================================================================
    # 0. HEADER EXECUTIVO & SELETOR DE CATEGORIAS (4 TIPOS NO TOPO)
    # =========================================================================
    ax_top = fig.add_axes([0.03, 0.89, 0.94, 0.09])
    ax_top.axis("off")

    head_bg = patches.FancyBboxPatch(
        (0.0, 0.0), 1.0, 1.0,
        boxstyle="round,pad=0.0,rounding_size=0.015",
        facecolor=COLOR_SURFACE, edgecolor=COLOR_DARK_BORDER, linewidth=1.2,
        transform=ax_top.transAxes
    )
    ax_top.add_patch(head_bg)

    top_accent = patches.FancyBboxPatch(
        (0.0, 0.94), 1.0, 0.06,
        boxstyle="round,pad=0.0,rounding_size=0.005",
        facecolor=COLOR_BLUE, edgecolor="none",
        transform=ax_top.transAxes
    )
    ax_top.add_patch(top_accent)

    ax_top.text(0.025, 0.65, "Galeria de Insights & Artefatos", fontsize=14.5, fontfamily="monospace",
                fontweight="bold", color="#F0F6FC", transform=ax_top.transAxes)
    ax_top.text(0.025, 0.25, "Explorador de Blueprints, Gráficos Executivos (300 DPI) e Specs Analíticas do Diretório insights/",
                fontsize=8.2, color=COLOR_TEXT_LIGHT, transform=ax_top.transAxes)

    # 4 Botões de Categoria no Topo à Direita
    cats = [
        ("01. Descritivo", "#2563EB", True, 0.44),
        ("02. Risco", "#D97706", False, 0.58),
        ("03. Prescritivo", "#059669", False, 0.72),
        ("04. Inteligencia & IA", "#7C3AED", False, 0.86),
    ]

    cat_w = 0.13
    cat_h = 0.55
    for c_label, c_col, is_active, cx in cats:
        c_box = patches.FancyBboxPatch(
            (cx, 0.22), cat_w, cat_h,
            boxstyle="round,pad=0.0,rounding_size=0.01",
            facecolor=c_col if is_active else "#161B22",
            edgecolor=c_col if is_active else "#30363D",
            linewidth=1.2 if is_active else 0.8,
            transform=ax_top.transAxes
        )
        ax_top.add_patch(c_box)
        ax_top.text(cx + cat_w/2.0, 0.22 + cat_h/2.0, c_label, fontsize=7.6, fontfamily="monospace",
                    fontweight="bold", color="#FFFFFF" if is_active else "#8B949E", ha="center", va="center", transform=ax_top.transAxes)

    # =========================================================================
    # 1. BARRA DE NAVEGAÇÃO DE SUB-ITENS (TABS/PILLS WEB)
    # =========================================================================
    ax_sub = fig.add_axes([0.03, 0.825, 0.94, 0.05])
    ax_sub.axis("off")

    sub_bg = patches.FancyBboxPatch(
        (0.0, 0.0), 1.0, 1.0,
        boxstyle="round,pad=0.0,rounding_size=0.01",
        facecolor="#0D1117", edgecolor="#21262D", linewidth=1.0,
        transform=ax_sub.transAxes
    )
    ax_sub.add_patch(sub_bg)

    sub_items = [
        ("Funil Semestral de Recuperacao", True, 0.02, 0.31),
        ("Motivos de Abandono & Atrito", False, 0.345, 0.31),
        ("Custo de Recuperacao & ROI", False, 0.67, 0.31),
    ]

    for s_title, s_sel, sx, sw in sub_items:
        s_box = patches.FancyBboxPatch(
            (sx, 0.12), sw, 0.76,
            boxstyle="round,pad=0.0,rounding_size=0.008",
            facecolor="#1E293B" if s_sel else "none",
            edgecolor="#38BDF8" if s_sel else "none",
            linewidth=1.1 if s_sel else 0.0,
            transform=ax_sub.transAxes
        )
        ax_sub.add_patch(s_box)
        ax_sub.text(sx + sw/2.0, 0.50, s_title, fontsize=7.8, fontfamily="monospace",
                    fontweight="bold" if s_sel else "normal",
                    color="#38BDF8" if s_sel else "#8B949E", ha="center", va="center", transform=ax_sub.transAxes)

    # =========================================================================
    # 2. CONTEÚDO PRINCIPAL (DOIS PAINÉIS: GRÁFICO 300 DPI vs SPEC MARKDOWN DESLIZÁVEL)
    # =========================================================================
    # 2.1 Painel Esquerdo: Visualização do Gráfico (300 DPI)
    ax_chart_panel = fig.add_axes([0.03, 0.18, 0.56, 0.63])
    ax_chart_panel.axis("off")

    c_p_bg = patches.FancyBboxPatch(
        (0.0, 0.0), 1.0, 1.0,
        boxstyle="round,pad=0.0,rounding_size=0.012",
        facecolor="#F8FAFC", edgecolor=COLOR_BORDER, linewidth=1.1,
        transform=ax_chart_panel.transAxes
    )
    ax_chart_panel.add_patch(c_p_bg)

    c_top_tag = patches.FancyBboxPatch(
        (0.0, 0.92), 1.0, 0.08,
        boxstyle="round,pad=0.0,rounding_size=0.008",
        facecolor="#0F172A", edgecolor="none", transform=ax_chart_panel.transAxes
    )
    ax_chart_panel.add_patch(c_top_tag)
    ax_chart_panel.text(0.03, 0.96, "[CHART] Visualizacao Executiva do Grafico (300 DPI • Ground Truth)", fontsize=8.2,
                        fontfamily="monospace", fontweight="bold", color="#FFFFFF", va="center", transform=ax_chart_panel.transAxes)

    # Simulação da visualização do gráfico dentro do card
    ax_chart_inner = fig.add_axes([0.05, 0.22, 0.52, 0.52])
    ax_chart_inner.set_facecolor("#FFFFFF")
    for spine in ax_chart_inner.spines.values():
        spine.set_color(COLOR_BORDER)
    ax_chart_inner.grid(True, linestyle="--", alpha=0.4, color=COLOR_BORDER)

    weeks = ["Sem 1", "Sem 2", "Sem 3", "Sem 4", "Sem 5", "Sem 6"]
    abandoned = [850, 920, 890, 940, 910, 880]
    recovered = [85, 98, 92, 104, 96, 91]

    ax_chart_inner.plot(weeks, abandoned, color="#E11D48", marker="o", linewidth=2.0, label="Carrinhos Abandonados (~70%)")
    ax_chart_inner.plot(weeks, recovered, color="#059669", marker="s", linewidth=2.2, label="Resgatados Dadosfera (+10.1%)")
    ax_chart_inner.fill_between(weeks, recovered, color="#059669", alpha=0.15)
    ax_chart_inner.set_title("Evolucao Temporal de Abandono vs Resgate Omnicanal", fontsize=9.0, fontweight="bold", color=COLOR_PRIMARY)
    ax_chart_inner.legend(loc="upper right", fontsize=7.2, framealpha=0.9)
    ax_chart_inner.tick_params(labelsize=7.5)

    # 2.2 Painel Direito: Especificação da Análise (Markdown Spec Deslizável)
    ax_spec_panel = fig.add_axes([0.61, 0.18, 0.36, 0.63])
    ax_spec_panel.axis("off")

    s_p_bg = patches.FancyBboxPatch(
        (0.0, 0.0), 1.0, 1.0,
        boxstyle="round,pad=0.0,rounding_size=0.012",
        facecolor="#090D16", edgecolor=COLOR_DARK_BORDER, linewidth=1.2,
        transform=ax_spec_panel.transAxes
    )
    ax_spec_panel.add_patch(s_p_bg)

    s_top_tag = patches.FancyBboxPatch(
        (0.0, 0.92), 1.0, 0.08,
        boxstyle="round,pad=0.0,rounding_size=0.008",
        facecolor="#1E293B", edgecolor="none", transform=ax_spec_panel.transAxes
    )
    ax_spec_panel.add_patch(s_top_tag)
    ax_spec_panel.text(0.04, 0.96, "[SPEC] insights/01_descriptive/01_bi_recuperacao_carrinhos/spec.md",
                       fontsize=7.2, fontfamily="monospace", fontweight="bold", color="#38BDF8", va="center", transform=ax_spec_panel.transAxes)

    spec_lines = [
        ("# SPEC DE INSIGHT // FUNIL DE RECUPERACAO", "#38BDF8"),
        ("---", "#64748B"),
        ("id: insight-desc-001", "#FBBF24"),
        ("categoria: 01_descriptive", "#A7F3D0"),
        ("ground_truth_source: data/mock/output_cleaned/", "#94A3B8"),
        ("---", "#64748B"),
        ("", "#FFFFFF"),
        ("## 1. OBJETIVO DE NEGOCIO", "#38BDF8"),
        ("Demonstrar o volume semestral de 7.500 carrinhos,", "#E2E8F0"),
        ("com taxa de abandono basal de 69.7% e resgate", "#E2E8F0"),
        ("incremental de +10.1% gerando +R$ 167,9k GMV.", "#E2E8F0"),
        ("", "#FFFFFF"),
        ("## 2. METRICAS & SQL CONTRATOS", "#38BDF8"),
        ("• GMV Total: R$ 2.618.420,00", "#34D399"),
        ("• GMV Resgatado: R$ 314.500,00", "#34D399"),
        ("• CAC Unitario E-mail: R$ 1,02 (ROI 45.2x)", "#34D399"),
        ("• Margem Preservada: 28.5% (DEC-001)", "#34D399"),
        ("", "#FFFFFF"),
        ("## 3. ARQUITETURA LAKEHOUSE", "#38BDF8"),
        ("• Tabela Fato: fato_abandono (JOIN 1-Hop)", "#94A3B8"),
        ("• Dimensoes: dim_tempo, dim_canal_resgate", "#94A3B8"),
    ]

    y_spec = 0.865
    for s_line, s_color in spec_lines:
        if s_line:
            ax_spec_panel.text(0.04, y_spec, s_line, fontsize=6.4, fontfamily="monospace",
                               color=s_color, transform=ax_spec_panel.transAxes)
        y_spec -= 0.038

    # =========================================================================
    # 3. FAIXA INFERIOR DE CONTEXTOS ARQUITETURAIS (README SPEC FORMAT)
    # =========================================================================
    ax_bot = fig.add_axes([0.03, 0.035, 0.94, 0.125])
    ax_bot.axis("off")

    bot_bg = patches.FancyBboxPatch(
        (0.0, 0.0), 1.0, 1.0,
        boxstyle="round,pad=0.0,rounding_size=0.012",
        facecolor="#090D16", edgecolor=COLOR_DARK_BORDER, linewidth=1.1,
        transform=ax_bot.transAxes
    )
    ax_bot.add_patch(bot_bg)

    ax_bot.text(0.025, 0.78, "Contextos e Referencias do Artefato", fontsize=8.0, fontfamily="monospace",
                fontweight="bold", color="#38BDF8", transform=ax_bot.transAxes)

    ax_bot.text(0.025, 0.48, "[DIR] Diretorio: insights/01_descriptive/01_bi_recuperacao_carrinhos/  •  Script: generate_chart.py",
                fontsize=6.5, fontfamily="monospace", color="#94A3B8", transform=ax_bot.transAxes)
    ax_bot.text(0.025, 0.22, "[TASKS] [x] 100% Ground Truth dos Parquets  •  [x] Exportacao 300 DPI White Theme  •  [x] Integracao ao Lakehouse Snowflake",
                fontsize=6.5, fontfamily="monospace", color="#34D399", transform=ax_bot.transAxes)

    return fig


def main() -> None:
    fig = plot_streamlit_insights_gallery()
    OUTPUT_IMAGE_PATH.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_IMAGE_PATH, dpi=300, bbox_inches="tight", facecolor="#FFFFFF")
    plt.close(fig)
    print(f"[SUCCESS] Gráfico da Galeria de Insights salvo em: {OUTPUT_IMAGE_PATH}")


if __name__ == "__main__":
    main()
