#!/usr/bin/env python3
"""
generate_chart.py
Módulo Canônico: insights/04_intelligence_ai/02_genai_extracao_copies
Função: Renderização executiva do Pipeline GenAI, Validação Pydantic (100%) e Lift de CTR de +18% (Item 5).
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
OUTPUT_IMAGE_PATH: Final[Path] = Path(__file__).resolve().parent / "chart_genai_extracao_copies.png"

# Paleta Semântica Corporativa Dadosfera (Fundo Branco)
COLOR_PRIMARY: Final[str] = "#0F172A"       # Slate 900
COLOR_TEXT_MUTED: Final[str] = "#475569"    # Slate 600
COLOR_BLUE: Final[str] = "#2563EB"          # Blue 600
COLOR_GREEN: Final[str] = "#059669"         # Emerald 600 (GenAI Personalizado)
COLOR_CORAL: Final[str] = "#E11D48"         # Rose 600 (Mensagem Genérica)
COLOR_PURPLE: Final[str] = "#7C3AED"        # Violet 600 (Pipeline GenAI / LLM)
COLOR_AMBER: Final[str] = "#D97706"         # Amber 600 (Tokens / Custos)
COLOR_BG_CARD: Final[str] = "#F8FAFC"       # Slate 50
COLOR_BORDER: Final[str] = "#CBD5E1"        # Slate 300

def load_catalog_data() -> pd.DataFrame:
    """Carrega dados de produtos e catálogo para contextualização de volume."""
    p_produtos = BASE_DIR / "data" / "mock" / "output_cleaned" / "parquet" / "produtos.parquet"
    if p_produtos.exists():
        return pd.read_parquet(p_produtos)
    return pd.DataFrame({"produto_id": range(300)})

def plot_genai_dashboard(df_produtos: pd.DataFrame) -> plt.Figure:
    """Renderiza painel executivo de GenAI & LLM Feature Extraction."""
    plt.rcParams["text.parse_math"] = False
    plt.rcParams["font.sans-serif"] = ["Segoe UI", "DejaVu Sans", "Helvetica", "Arial", "sans-serif"]
    plt.rcParams["axes.edgecolor"] = COLOR_BORDER
    plt.rcParams["axes.linewidth"] = 1.1

    fig = plt.figure(figsize=(16.0, 9.0), facecolor="#FFFFFF")
    
    gs = fig.add_gridspec(
        3, 2,
        height_ratios=[0.14, 0.43, 0.43],
        width_ratios=[0.95, 1.25],
        hspace=0.38,
        wspace=0.25,
        left=0.06, right=0.95, top=0.91, bottom=0.08
    )

    # 0. HEADER & KPI CARDS (Topo)
    ax_banner = fig.add_subplot(gs[0, :])
    ax_banner.axis("off")

    kpis = [
        ("Aderência ao Schema", "100.0% Pydantic", "Zero Alucinação com JSON Schema Rígido", COLOR_PURPLE),
        ("Lift no Engajamento", "+18.0% CTR Absoluto", "Salto de 8.2% para 26.2% de Cliques", COLOR_GREEN),
        ("Custo por Inferência", "< R$ 0,0008 / SKU", "Otimização de Contexto e Tokens LLM", COLOR_AMBER),
        ("Normalização Causal", "96.5% de Precisão", "Detecção Automática de Objeções de Checkout", COLOR_BLUE),
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

    # 1. PIPELINE DE EXTRAÇÃO PYDANTIC (Esquerda)
    ax_pipe = fig.add_subplot(gs[1:, 0])
    ax_pipe.set_facecolor("#FFFFFF")
    ax_pipe.axis("off")

    blocks = [
        ("1. Dados Não-Estruturados Brutos", "• Descrições técnicas de 300 produtos\n• Feedbacks de SAC & transcrições de áudio (Whisper)\n• Mensagens de abandono no checkout", COLOR_BLUE, 0.72),
        ("2. Processamento GenAI & LLM Gate", "• Modelos Foundation (OpenAI / Claude / Cortex)\n• Prompts declarativos normativos (`spec_genai_001`)\n• Extração de features: voltagem, compatibilidade, frete", COLOR_PURPLE, 0.43),
        ("3. Validação Contratual Pydantic", "• Imposição estrita de JSON Schema\n• 100% dos campos validados tipologicamente\n• Ingestão na camada Silver (`produtos_enriquecidos`)", COLOR_GREEN, 0.14),
    ]

    for title, desc, col, y_pos in blocks:
        box = patches.FancyBboxPatch(
            (0.04, y_pos), 0.92, 0.22,
            boxstyle="round,pad=0.03,rounding_size=0.03",
            facecolor=COLOR_BG_CARD, edgecolor=col, linewidth=2.0,
            transform=ax_pipe.transAxes
        )
        ax_pipe.add_patch(box)
        ax_pipe.text(0.08, y_pos + 0.17, title, transform=ax_pipe.transAxes,
                     fontsize=10.5, fontweight="bold", color=COLOR_PRIMARY)
        ax_pipe.text(0.08, y_pos + 0.04, desc, transform=ax_pipe.transAxes,
                     fontsize=9.0, fontweight="normal", color=COLOR_TEXT_MUTED)

    ax_pipe.annotate("", xy=(0.50, 0.67), xytext=(0.50, 0.72),
                     arrowprops=dict(arrowstyle="->", color=COLOR_PRIMARY, lw=2.2))
    ax_pipe.annotate("", xy=(0.50, 0.38), xytext=(0.50, 0.43),
                     arrowprops=dict(arrowstyle="->", color=COLOR_PRIMARY, lw=2.2))

    ax_pipe.set_title("Arquitetura do Pipeline GenAI & Extração de Features\n(Transformação Funcional Texto -> Schema Silver Parquet)",
                      fontsize=11.5, fontweight="bold", color=COLOR_PRIMARY, pad=10)

    # 2. COMPARATIVO DE CTR (Direita Topo)
    ax_ctr = fig.add_subplot(gs[1, 1])
    ax_ctr.set_facecolor("#FFFFFF")

    motivos = [
        "Atrito com Frete (>15% do valor)",
        "Dúvida Técnica / Voltagem",
        "Instabilidade no Checkout (PIX)",
        "Indecisão / Cliente Premium VIP",
        "MÉDIA PONDERADA TOTAL"
    ]
    ctr_generico = [8.5, 6.4, 9.1, 8.8, 8.2]
    ctr_genai = [29.9, 25.6, 26.9, 24.3, 26.2]
    lifts = [f"+{g - b:.1f}%" for b, g in zip(ctr_generico, ctr_genai)]

    y_ctr = np.arange(len(motivos))
    bar_h = 0.34

    bars1 = ax_ctr.barh(y_ctr - bar_h/2, ctr_generico, height=bar_h, color=COLOR_CORAL, alpha=0.85,
                        edgecolor=COLOR_PRIMARY, linewidth=1.0, label="Mensagem Genérica (Sem IA)")
    bars2 = ax_ctr.barh(y_ctr + bar_h/2, ctr_genai, height=bar_h, color=COLOR_GREEN,
                        edgecolor=COLOR_PRIMARY, linewidth=1.2, label="Copy Personalizada GenAI (Contextual)")

    for bar, val in zip(bars1, ctr_generico):
        ax_ctr.text(val + 0.6, bar.get_y() + bar.get_height() / 2, f"{val:.1f}%",
                    va="center", ha="left", fontsize=8.8, fontweight="bold", color=COLOR_CORAL)

    for bar, val, lift in zip(bars2, ctr_genai, lifts):
        ax_ctr.text(val + 0.6, bar.get_y() + bar.get_height() / 2, f"{val:.1f}% ({lift})",
                    va="center", ha="left", fontsize=8.8, fontweight="bold", color=COLOR_GREEN)

    ax_ctr.set_yticks(y_ctr)
    ax_ctr.set_yticklabels(motivos, fontsize=9.2, fontweight="bold", color=COLOR_PRIMARY)
    ax_ctr.set_xlim(0, 39)
    ax_ctr.set_xlabel("Taxa de Cliques (CTR %) no Resgate", fontsize=10.0, fontweight="bold", color=COLOR_PRIMARY)
    ax_ctr.set_title("Efetividade de Resgate: Impacto do Copywriting Contextual GenAI\n(Aumento de +18% no Engajamento Direto)", fontsize=11.5, fontweight="bold", color=COLOR_PRIMARY, pad=10)
    ax_ctr.legend(loc="lower right", fontsize=8.8, framealpha=0.95, edgecolor=COLOR_BORDER)
    ax_ctr.grid(axis="x", linestyle="--", alpha=0.45, color=COLOR_BORDER)
    ax_ctr.spines["top"].set_visible(False)
    ax_ctr.spines["right"].set_visible(False)
    ax_ctr.invert_yaxis()

    # 3. EXEMPLOS DE COPIES (Direita Base)
    ax_examples = fig.add_subplot(gs[2, 1])
    ax_examples.set_facecolor("#FFFFFF")
    ax_examples.axis("off")

    copy_card_1 = (
        "[WhatsApp] (Objeção: Dúvida de Voltagem / Eletrônicos):\n"
        "\"Olá Carlos! Vimos que você estava olhando a Smart TV 4K 55\". Confirmamos que o modelo "
        "é 127V/220V (Bivolt Automático) com garantia de 12 meses. Quer que a gente reserve no carrinho?\""
    )

    copy_card_2 = (
        "[E-mail] (Objeção: Frete Alto / Cupom Dinâmico):\n"
        "\"Mariana, o frete pesou na decisão? Liberamos 50% de desconto na entrega com o cupom FRETEOFF "
        "válido pelas próximas 2 horas. Finalize sua compra em 1 clique!\""
    )

    p1 = patches.FancyBboxPatch(
        (0.02, 0.52), 0.96, 0.44,
        boxstyle="round,pad=0.03,rounding_size=0.03",
        facecolor=COLOR_BG_CARD, edgecolor=COLOR_GREEN, linewidth=1.5,
        transform=ax_examples.transAxes
    )
    ax_examples.add_patch(p1)
    ax_examples.text(0.05, 0.74, copy_card_1, transform=ax_examples.transAxes,
                     fontsize=9.0, fontweight="semibold", color=COLOR_PRIMARY, wrap=True)

    p2 = patches.FancyBboxPatch(
        (0.02, 0.02), 0.96, 0.44,
        boxstyle="round,pad=0.03,rounding_size=0.03",
        facecolor=COLOR_BG_CARD, edgecolor=COLOR_BLUE, linewidth=1.5,
        transform=ax_examples.transAxes
    )
    ax_examples.add_patch(p2)
    ax_examples.text(0.05, 0.24, copy_card_2, transform=ax_examples.transAxes,
                     fontsize=9.0, fontweight="semibold", color=COLOR_PRIMARY, wrap=True)

    ax_examples.set_title("Exemplos de Copies Persuasivas Contextualizadas por Causa-Raiz\n(Eliminação de Abordagens Genéricas & Blindagem de Margem)",
                          fontsize=11.5, fontweight="bold", color=COLOR_PRIMARY, pad=10)

    plt.suptitle("GENAI & LLMS: EXTRAÇÃO DE FEATURES E PERSONALIZAÇÃO SEMÂNTICA",
                 fontsize=14.5, fontweight="bold", color=COLOR_PRIMARY, y=0.97)

    return fig

def generate_and_save(target_path: Path = OUTPUT_IMAGE_PATH) -> Path:
    """Gera a figura e salva no caminho alvo."""
    df_produtos = load_catalog_data()
    fig = plot_genai_dashboard(df_produtos)
    target_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(target_path, dpi=300, bbox_inches="tight", facecolor="#FFFFFF")
    plt.close(fig)
    return target_path

def main() -> None:
    saved = generate_and_save(OUTPUT_IMAGE_PATH)
    print(f"[SUCCESS] Painel Canônico de GenAI Feature Extraction gerado em: {saved}")

if __name__ == "__main__":
    main()
