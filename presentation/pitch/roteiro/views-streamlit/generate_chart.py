#!/usr/bin/env python3
"""
generate_chart.py
Módulo: presentation/pitch/roteiro/views-streamlit
Função: Renderização executiva master do Data App Dadosfera (Visão Geral Consolidada da Arquitetura & Módulos).
Padrão Gráfico: Fundo Branco Puro (#FFFFFF), 16:9 Widescreen, 300 DPI, charts-maker standard.
"""

from typing import Final
from pathlib import Path
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
OUTPUT_IMAGE_PATH: Final[Path] = Path(__file__).resolve().parent / "chart_streamlit_data_app_overview.png"

# Paleta Semântica Corporativa Executiva
COLOR_PRIMARY: Final[str] = "#0F172A"       # Slate 900
COLOR_TEXT_MUTED: Final[str] = "#475569"    # Slate 600
COLOR_TEXT_LIGHT: Final[str] = "#64748B"    # Slate 500
COLOR_BLUE: Final[str] = "#2563EB"          # Blue 600
COLOR_GREEN: Final[str] = "#059669"         # Emerald 600
COLOR_TEAL: Final[str] = "#0D9488"          # Teal 600
COLOR_VIOLET: Final[str] = "#7C3AED"        # Violet 600
COLOR_AMBER: Final[str] = "#D97706"         # Amber 600
COLOR_BG_CARD: Final[str] = "#F8FAFC"       # Slate 50
COLOR_BORDER: Final[str] = "#CBD5E1"        # Slate 300
COLOR_DARK_HEADER: Final[str] = "#0F172A"   # Slate 900


def plot_streamlit_master_overview() -> plt.Figure:
    """Renderiza o overview executivo consolidado com arquitetura e os 5 módulos do Data App."""
    plt.rcParams["text.parse_math"] = False
    plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Segoe UI", "Helvetica", "Arial", "sans-serif"]
    plt.rcParams["axes.edgecolor"] = COLOR_BORDER
    plt.rcParams["axes.linewidth"] = 1.1

    fig = plt.figure(figsize=(16.0, 9.0), facecolor="#FFFFFF")

    # =========================================================================
    # 0. HEADER SUPERIOR EXECUTIVO
    # =========================================================================
    ax_top = fig.add_axes([0.03, 0.90, 0.94, 0.08])
    ax_top.axis("off")

    ax_top.text(0.0, 0.70, "Dadosfera Data App  |  Arquitetura de Consumo & Inteligência Analítica",
                fontsize=14.0, fontweight="bold", color=COLOR_PRIMARY)
    ax_top.text(0.0, 0.18, "Aplicação Modular em 5 Camadas (React/TypeScript Pattern)  •  Conexão Nativa com Snowflake Lakehouse  •  Deploy SaaS Elástico",
                fontsize=9.0, color=COLOR_TEXT_MUTED)

    # Badge de Governança no Topo Direito
    gov_badge = patches.FancyBboxPatch(
        (0.72, 0.25), 0.28, 0.60,
        boxstyle="round,pad=0.0,rounding_size=0.015",
        facecolor="#F1F5F9", edgecolor=COLOR_BORDER, linewidth=1.0,
        transform=ax_top.transAxes
    )
    ax_top.add_patch(gov_badge)
    ax_top.text(0.86, 0.55, "100% Ground Truth  •  Zero Local SQL (DEC-004)",
                fontsize=7.8, fontweight="bold", color=COLOR_PRIMARY, ha="center", va="center", transform=ax_top.transAxes)

    # =========================================================================
    # 1. BARRA DE ARQUITETURA EM 5 CAMADAS (HORIZONTAL FLOW)
    # =========================================================================
    ax_flow = fig.add_axes([0.03, 0.815, 0.94, 0.065])
    ax_flow.axis("off")

    flow_bg = patches.FancyBboxPatch(
        (0.0, 0.0), 1.0, 1.0,
        boxstyle="round,pad=0.0,rounding_size=0.012",
        facecolor="#0F172A", edgecolor="none",
        transform=ax_flow.transAxes
    )
    ax_flow.add_patch(flow_bg)

    layers = [
        ("1. TYPES", "Contratos & Models Pydantic", 0.02),
        ("2. CONSTANTS", "Imutabilidade MappingProxy", 0.22),
        ("3. SERVICES", "Funções Puras & Simulação", 0.42),
        ("4. COMPONENTS", "UI Modular & Desacoplada", 0.62),
        ("5. VIEWS", "Orquestração das 5 Abas", 0.82),
    ]

    for title, sub, lx in layers:
        ax_flow.text(lx + 0.08, 0.65, title, fontsize=8.2, fontfamily="monospace", fontweight="bold",
                     color="#38BDF8", ha="center", va="center", transform=ax_flow.transAxes)
        ax_flow.text(lx + 0.08, 0.28, sub, fontsize=7.0, color="#94A3B8",
                     ha="center", va="center", transform=ax_flow.transAxes)

    # Setas de fluxo
    for ax_arrow in [0.185, 0.385, 0.585, 0.785]:
        ax_flow.text(ax_arrow, 0.48, "➔", fontsize=10.0, color="#64748B",
                     ha="center", va="center", transform=ax_flow.transAxes)

    # =========================================================================
    # 2. GRID DOS 5 MÓDULOS EXECUTIVOS (3 NO TOPO, 2 EMBAIXO COM DESIGN PREMIUM)
    # =========================================================================
    ax_grid = fig.add_axes([0.03, 0.14, 0.94, 0.65])
    ax_grid.axis("off")

    modules = [
        # Linha 1 (3 Módulos)
        (
            "00. Central de Agentes & Skills",
            "Central de Engenharia Multi-Agente com 10 Especialistas autônomos. Inspeção fidedigna de arquivos .md, governança, decisões arquiteturais e rastreabilidade de código.",
            "• Leitura direta dos arquivos de agentes e skills\n• Contextos e referências arquiteturais (DECs)\n• Governança de escopo e avaliação Outlier",
            "10 Agentes  •  10 Skills Ativas",
            "#0F172A",
            0.0, 0.52, 0.315, 0.46
        ),
        (
            "01. Simulador de ROI & Sensibilidade",
            "Simulação dinâmica do mix de canais (E-mail, WhatsApp, SMS, Push) com retorno projetado de R$ 314,5k GMV resgatado, ROI de 45.2x e margem bruta preservada de 28.5%.",
            "• Sliders interativos de budget e conversão\n• Curva de sensibilidade e saturação de canal\n• Preservação de margem sem queima de cupom",
            "R$ 314.500 GMV  •  ROI 45.2x",
            COLOR_BLUE,
            0.342, 0.52, 0.315, 0.46
        ),
        (
            "02. Explorador Semântico de Catálogo",
            "Projeção vetorial 2D de 300 SKUs por afinidade semântica para recomendação automática de produtos substitutos com maior margem durante a recuperação de carrinhos.",
            "• Embeddings vetoriais em 2 dimensões\n• Similaridade de cosseno instantânea (>= 0.85)\n• Trajetórias de cluster e busca interativa",
            "300 SKUs  •  Lift +18% Conversão",
            COLOR_TEAL,
            0.685, 0.52, 0.315, 0.46
        ),
        # Linha 2 (2 Módulos Largos)
        (
            "03. Copiloto Prescritivo de Resgate",
            "Assistente inteligente de IA Generativa conectado a LLMs. Cruza telemetria comportamental e feedbacks de clientes para diagnosticar a causa-raiz do abandono e gerar copies personalizadas com Pydantic JSON Schema.",
            "• Diagnóstico causal de hesitação (dúvida técnica, frete, checkout)\n• Geração de copies persuasivas prontas para WhatsApp e E-mail\n• 100% Pydantic JSON Schema (zero alucinação e tipagem estrita)",
            "100% Pydantic Schema  •  Latência < 2.5 ms",
            COLOR_VIOLET,
            0.0, 0.0, 0.485, 0.47
        ),
        (
            "04. Vitrine de Produtos Enriquecidos",
            "Catálogo analítico conectado à camada Silver (PRODUTOS_ENRIQUECIDOS) do Lakehouse. Normalização de atributos técnicos via IA, compatibilidade e cruzamento com métricas de conversão de CRM sem necessidade de SQL.",
            "• Diferenciais técnicos e argumentos de venda extraídos por LLM\n• Normalização de especificações e filtros semânticos multidimensionais\n• Integração direta com a esteira Medallion do Snowflake Lakehouse",
            "Camada Silver Curated  •  Zero Inconsistência",
            COLOR_GREEN,
            0.515, 0.0, 0.485, 0.47
        ),
    ]

    for title, desc, bullets, metric, tag_color, mx, my, mw, mh in modules:
        # Container Card
        card_box = patches.FancyBboxPatch(
            (mx, my), mw, mh,
            boxstyle="round,pad=0.0,rounding_size=0.015",
            facecolor=COLOR_BG_CARD, edgecolor=COLOR_BORDER, linewidth=1.1,
            transform=ax_grid.transAxes
        )
        ax_grid.add_patch(card_box)

        # Header do Card com Tag Colorida
        header_h = 0.080
        head_box = patches.FancyBboxPatch(
            (mx, my + mh - header_h), mw, header_h,
            boxstyle="round,pad=0.0,rounding_size=0.012",
            facecolor=tag_color, edgecolor="none",
            transform=ax_grid.transAxes
        )
        ax_grid.add_patch(head_box)

        ax_grid.text(mx + 0.02, my + mh - header_h/2.0, title, fontsize=8.8, fontweight="bold",
                     color="#FFFFFF", va="center", transform=ax_grid.transAxes)

        # Descrição do Módulo
        ax_grid.text(mx + 0.02, my + mh - 0.105, desc, fontsize=7.6, color=COLOR_PRIMARY,
                     wrap=True, va="top", linespacing=1.3, transform=ax_grid.transAxes)

        # Bullets Técnicos
        ax_grid.text(mx + 0.02, my + 0.17, bullets, fontsize=7.2, color=COLOR_TEXT_MUTED,
                     linespacing=1.35, va="top", transform=ax_grid.transAxes)

        # Footer Pill de Métrica Executiva
        pill_h = 0.055
        pill_box = patches.FancyBboxPatch(
            (mx + 0.02, my + 0.025), mw - 0.04, pill_h,
            boxstyle="round,pad=0.0,rounding_size=0.008",
            facecolor="#0F172A", edgecolor="none",
            transform=ax_grid.transAxes
        )
        ax_grid.add_patch(pill_box)
        ax_grid.text(mx + mw/2.0, my + 0.025 + pill_h/2.0, metric, fontsize=7.4, fontfamily="monospace",
                     fontweight="bold", color="#F8FAFC", ha="center", va="center", transform=ax_grid.transAxes)

    # =========================================================================
    # 3. FAIXA INFERIOR DE KPIs EXECUTIVOS CONSOLIDADOS
    # =========================================================================
    ax_bot = fig.add_axes([0.03, 0.035, 0.94, 0.075])
    ax_bot.axis("off")

    bot_bg = patches.FancyBboxPatch(
        (0.0, 0.0), 1.0, 1.0,
        boxstyle="round,pad=0.0,rounding_size=0.012",
        facecolor="#F8FAFC", edgecolor=COLOR_BORDER, linewidth=1.1,
        transform=ax_bot.transAxes
    )
    ax_bot.add_patch(bot_bg)

    kpis = [
        ("RECEITA AUDITADA", "R$ 2.618.420", COLOR_PRIMARY, 0.05),
        ("GMV RESGATÁVEL", "R$ 314.500", COLOR_BLUE, 0.29),
        ("ROI DO RESGATE", "45.2x", COLOR_GREEN, 0.53),
        ("MARGEM PRESERVADA", "28.5%", COLOR_AMBER, 0.76),
    ]

    for label, val, col, kx in kpis:
        ax_bot.text(kx + 0.09, 0.70, label, fontsize=7.0, fontfamily="monospace",
                    fontweight="bold", color=COLOR_TEXT_LIGHT, ha="center", va="center", transform=ax_bot.transAxes)
        ax_bot.text(kx + 0.09, 0.28, val, fontsize=11.5, fontweight="bold",
                    color=col, ha="center", va="center", transform=ax_bot.transAxes)

    return fig


def main() -> None:
    fig = plot_streamlit_master_overview()
    OUTPUT_IMAGE_PATH.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_IMAGE_PATH, dpi=300, bbox_inches="tight", facecolor="#FFFFFF")
    plt.close(fig)
    print(f"[SUCCESS] Painel Master Consolidado do Data App gerado com sucesso em: {OUTPUT_IMAGE_PATH}")


if __name__ == "__main__":
    main()
