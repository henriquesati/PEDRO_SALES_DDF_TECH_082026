#!/usr/bin/env python3
"""
generate_chart.py
Módulo Canônico Master: insights/04_intelligence_ai
Função: Renderização executiva do Painel Master Consolidado de IA da Dadosfera (Arquitetura Antes x Agora & Tríade de IA).
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
OUTPUT_IMAGE_PATH: Final[Path] = Path(__file__).resolve().parent / "chart_insights_ia_master.png"

# Paleta Semântica Corporativa Dadosfera (Fundo Branco)
COLOR_PRIMARY: Final[str] = "#0F172A"       # Slate 900
COLOR_TEXT_MUTED: Final[str] = "#475569"    # Slate 600
COLOR_BLUE: Final[str] = "#2563EB"          # Blue 600
COLOR_GREEN: Final[str] = "#059669"         # Emerald 600 (Dadosfera)
COLOR_CORAL: Final[str] = "#E11D48"         # Rose 600 (Legado AWS DIY)
COLOR_PURPLE: Final[str] = "#7C3AED"        # Violet 600 (GenAI / ML)
COLOR_AMBER: Final[str] = "#D97706"         # Amber 600 (Alerta / Performance)
COLOR_BG_CARD: Final[str] = "#F8FAFC"       # Slate 50
COLOR_BORDER: Final[str] = "#CBD5E1"        # Slate 300

def plot_master_ai_dashboard() -> plt.Figure:
    """Renderiza painel executivo master da camada de Inteligência da Dadosfera."""
    plt.rcParams["text.parse_math"] = False
    plt.rcParams["font.sans-serif"] = ["Segoe UI", "DejaVu Sans", "Helvetica", "Arial", "sans-serif"]
    plt.rcParams["axes.edgecolor"] = COLOR_BORDER
    plt.rcParams["axes.linewidth"] = 1.1

    fig = plt.figure(figsize=(16.0, 9.0), facecolor="#FFFFFF")
    
    gs = fig.add_gridspec(
        3, 3,
        height_ratios=[0.14, 0.42, 0.44],
        hspace=0.38,
        wspace=0.22,
        left=0.05, right=0.95, top=0.91, bottom=0.08
    )

    # 0. HEADER & KPI CARDS (Topo)
    ax_banner = fig.add_subplot(gs[0, :])
    ax_banner.axis("off")

    kpis = [
        ("Módulo de Inteligência", "Stepsfera + Snowpark", "Orquestração sem atrito de DAGs e Steps de ML", COLOR_PURPLE),
        ("Poder Discriminativo ML", "ROC-AUC: 0.9478", "Classificação de Propensão com 99.53% Acurácia", COLOR_BLUE),
        ("Esteira GenAI Governança", "100% Pydantic Schema", "Copies Hiper-Contextualizadas (+18% CTR)", COLOR_GREEN),
        ("Consumo & Retorno", "45.0x ROI em Data App", "Deploy Streamlit Nativo (+R$ 167,9k Líquidos)", COLOR_AMBER),
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

    # 1. COMPARATIVO ARQUITETURAL: ANTES VS AGORA
    ax_comp = fig.add_subplot(gs[1, :])
    ax_comp.set_facecolor("#FFFFFF")
    ax_comp.axis("off")

    card_antes = (
        "[ANTES] Arquitetura Legada (AWS DIY / Serviços Desconectados):\n\n"
        "• Infraestrutura Fragmentada: Sobe instâncias EC2 manuais e provisiona clusters Glue/EMR.\n"
        "• Cold-Start Excessivo: Espera de 1 a 4 minutos apenas para alocar DPUs antes de rodar o código.\n"
        "• Orquestração Frágil: MWAA/Airflow exige escrever DAGs complexas e gerenciar Dockerfiles/ECR.\n"
        "• Silos de LLM: Chamadas desestruturadas sem validação de schema e com alto risco de alucinação.\n"
        "• Custo Marginal Crescente: Exige Engenheiros de Dados sêniores dedicados apenas a sustentar infra."
    )
    p_antes = patches.FancyBboxPatch(
        (0.01, 0.05), 0.47, 0.90,
        boxstyle="round,pad=0.03,rounding_size=0.03",
        facecolor=COLOR_BG_CARD, edgecolor=COLOR_CORAL, linewidth=2.0,
        transform=ax_comp.transAxes
    )
    ax_comp.add_patch(p_antes)
    ax_comp.text(0.03, 0.50, card_antes, transform=ax_comp.transAxes,
                 fontsize=9.2, fontweight="semibold", color=COLOR_PRIMARY, va="center")

    card_agora = (
        "[AGORA] Plataforma Dadosfera (Inteligência Integrada & Elástica):\n\n"
        "• Ambiente Unificado: Jupyter Notebooks integrados e steps modulares reutilizáveis (Stepsfera).\n"
        "• Pushdown Compute: Execução in-database (Snowpark) sem data egress e com latência ultrabaixa (111 ms).\n"
        "• Treinamento de Modelos: Treine Scikit-Learn, XGBoost ou LightGBM diretamente sobre a camada Gold.\n"
        "• Esteira GenAI com Pydantic: 100% de conformidade com JSON Schema e enriquecimento de catálogo.\n"
        "• Consumo Imediato: Deploy de Data Apps Streamlit em 1 clique para Marketing e CRM com 45x ROI."
    )
    p_agora = patches.FancyBboxPatch(
        (0.52, 0.05), 0.47, 0.90,
        boxstyle="round,pad=0.03,rounding_size=0.03",
        facecolor=COLOR_BG_CARD, edgecolor=COLOR_GREEN, linewidth=2.0,
        transform=ax_comp.transAxes
    )
    ax_comp.add_patch(p_agora)
    ax_comp.text(0.54, 0.50, card_agora, transform=ax_comp.transAxes,
                 fontsize=9.2, fontweight="semibold", color=COLOR_PRIMARY, va="center")

    ax_comp.set_title("Evolução da Maturidade de IA: Do Overhead de Infraestrutura à Entrega Direta de Valor de Negócio",
                      fontsize=12.0, fontweight="bold", color=COLOR_PRIMARY, pad=10)

    # 2. A TRÍADE DE INTELIGÊNCIA DA DADOSFERA
    ax_p1 = fig.add_subplot(gs[2, 0])
    ax_p1.set_facecolor("#FFFFFF")
    ax_p1.axis("off")

    p1_text = (
        "1. MODELOS DE NEGÓCIO (ML)\n"
        "-------------------------------------\n"
        "• Modelo: Regularized Classifier\n"
        "• Poder: ROC-AUC 0.9478\n"
        "• Acurácia: 99.53% (F1: 0.995)\n"
        "• Duração: 111.7 ms (In-Database)\n\n"
        "[Ação]: Ranqueia carrinhos por\n"
        "probabilidade de conversão para\n"
        "priorizar a fila de resgate ativo."
    )
    p_box1 = patches.FancyBboxPatch(
        (0.02, 0.05), 0.96, 0.90,
        boxstyle="round,pad=0.03,rounding_size=0.03",
        facecolor=COLOR_BG_CARD, edgecolor=COLOR_BLUE, linewidth=1.8,
        transform=ax_p1.transAxes
    )
    ax_p1.add_patch(p_box1)
    ax_p1.text(0.06, 0.50, p1_text, transform=ax_p1.transAxes,
               fontsize=9.2, fontweight="semibold", color=COLOR_PRIMARY, va="center", family="monospace")
    ax_p1.set_title("Classificação de Propensão (Item 8)", fontsize=11.0, fontweight="bold", color=COLOR_PRIMARY, pad=8)

    ax_p2 = fig.add_subplot(gs[2, 1])
    ax_p2.set_facecolor("#FFFFFF")
    ax_p2.axis("off")

    p2_text = (
        "2. GENAI & LLMS GOVERNADOS\n"
        "-------------------------------------\n"
        "• Schema Pydantic: 100% aderência\n"
        "• Detecção Causal: 96.5% precisão\n"
        "• Lift no CTR: +18.0% (de 8.2% -> 26.2%)\n"
        "• Custo: < R$ 0,0008 por SKU\n\n"
        "[Ação]: Extrai atributos críticos\n"
        "(voltagem/frete) e gera copies de\n"
        "resgate altamente persuasivas."
    )
    p_box2 = patches.FancyBboxPatch(
        (0.02, 0.05), 0.96, 0.90,
        boxstyle="round,pad=0.03,rounding_size=0.03",
        facecolor=COLOR_BG_CARD, edgecolor=COLOR_PURPLE, linewidth=1.8,
        transform=ax_p2.transAxes
    )
    ax_p2.add_patch(p_box2)
    ax_p2.text(0.06, 0.50, p2_text, transform=ax_p2.transAxes,
               fontsize=9.2, fontweight="semibold", color=COLOR_PRIMARY, va="center", family="monospace")
    ax_p2.set_title("Extração Semântica & Copies (Item 5)", fontsize=11.0, fontweight="bold", color=COLOR_PRIMARY, pad=8)

    ax_p3 = fig.add_subplot(gs[2, 2])
    ax_p3.set_facecolor("#FFFFFF")
    ax_p3.axis("off")

    p3_text = (
        "3. DATA APPS & SIMULADOR (CRM)\n"
        "-------------------------------------\n"
        "• Deploy: Streamlit Integrado\n"
        "• Retorno Financeiro: 45.0x ROI\n"
        "• Receita Líquida: +R$ 167.900,00\n"
        "• CAC E-mail: R$ 1,02 por resgate\n\n"
        "[Ação]: Gestores de CRM simulam\n"
        "impacto de réguas em tempo real\n"
        "com total autonomia de TI."
    )
    p_box3 = patches.FancyBboxPatch(
        (0.02, 0.05), 0.96, 0.90,
        boxstyle="round,pad=0.03,rounding_size=0.03",
        facecolor=COLOR_BG_CARD, edgecolor=COLOR_GREEN, linewidth=1.8,
        transform=ax_p3.transAxes
    )
    ax_p3.add_patch(p_box3)
    ax_p3.text(0.06, 0.50, p3_text, transform=ax_p3.transAxes,
               fontsize=9.2, fontweight="semibold", color=COLOR_PRIMARY, va="center", family="monospace")
    ax_p3.set_title("Consumo & Simulação de ROI (Item 9)", fontsize=11.0, fontweight="bold", color=COLOR_PRIMARY, pad=8)

    plt.suptitle("MÓDULO DE INTELIGÊNCIA, GENAI & DATA APPS (SEÇÃO [5] DO ROTEIRO)",
                 fontsize=14.5, fontweight="bold", color=COLOR_PRIMARY, y=0.97)

    return fig

def generate_and_save(target_path: Path = OUTPUT_IMAGE_PATH) -> Path:
    """Gera a figura e salva no caminho alvo."""
    fig = plot_master_ai_dashboard()
    target_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(target_path, dpi=300, bbox_inches="tight", facecolor="#FFFFFF")
    plt.close(fig)
    return target_path

def main() -> None:
    saved = generate_and_save(OUTPUT_IMAGE_PATH)
    print(f"[SUCCESS] Painel Canônico Master de IA gerado em: {saved}")

if __name__ == "__main__":
    main()
