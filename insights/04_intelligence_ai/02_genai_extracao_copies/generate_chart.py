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
ROTEIRO_IMAGE_PATH: Final[Path] = (
    BASE_DIR / "presentation" / "pitch" / "roteiro" / "views-05-insights-ia" / "genai-extracao-copies" / "chart_genai_extracao_copies.png"
)

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
    """Renderiza painel executivo de GenAI & LLM Feature Extraction com tipografia perfeitamente formatada."""
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

    # =========================================================================
    # 0. HEADER & KPI CARDS (Topo)
    # =========================================================================
    ax_banner = fig.add_subplot(gs[0, :])
    ax_banner.axis("off")

    kpis = [
        ("Aderência ao Schema", "100.0% Pydantic", "Zero Alucinação • JSON Schema Rígido", COLOR_PURPLE),
        ("Lift no Engajamento", "+18.0% CTR Absoluto", "Salto de 8,2% para 26,2% de Cliques", COLOR_GREEN),
        ("Custo por Inferência", "< R$ 0,0008 / SKU", "Otimização de Contexto e Tokens LLM", COLOR_AMBER),
        ("Normalização Causal", "96.5% de Precisão", "Detecção Automática de Objeções", COLOR_BLUE),
    ]

    card_width = 0.235
    card_gap = 0.02
    for i, (title, main_val, sub_val, col) in enumerate(kpis):
        x0 = i * (card_width + card_gap)
        cx = x0 + card_width / 2.0
        
        # Caixa do Card
        card_box = patches.FancyBboxPatch(
            (x0, 0.0), card_width, 0.95,
            boxstyle="round,pad=0.0,rounding_size=0.04",
            facecolor=COLOR_BG_CARD, edgecolor=COLOR_BORDER, linewidth=1.2,
            transform=ax_banner.transAxes, zorder=2
        )
        ax_banner.add_patch(card_box)
        
        # Barra de destaque colorida no topo do card
        accent_bar = patches.FancyBboxPatch(
            (x0, 0.88), card_width, 0.07,
            boxstyle="round,pad=0.0,rounding_size=0.02",
            facecolor=col, edgecolor="none",
            transform=ax_banner.transAxes, zorder=3
        )
        ax_banner.add_patch(accent_bar)
        
        # Textos do Card (Centralizados e sem sobreposição)
        ax_banner.text(cx, 0.70, title.upper(), transform=ax_banner.transAxes,
                       fontsize=9.0, fontweight="bold", color=COLOR_TEXT_MUTED, ha="center", va="center")
        ax_banner.text(cx, 0.40, main_val, transform=ax_banner.transAxes,
                       fontsize=13.5, fontweight="bold", color=COLOR_PRIMARY, ha="center", va="center")
        ax_banner.text(cx, 0.15, sub_val, transform=ax_banner.transAxes,
                       fontsize=8.2, fontweight="semibold", color=col, ha="center", va="center")

    # =========================================================================
    # 1. PIPELINE DE EXTRAÇÃO PYDANTIC (Esquerda)
    # =========================================================================
    ax_pipe = fig.add_subplot(gs[1:, 0])
    ax_pipe.set_facecolor("#FFFFFF")
    ax_pipe.axis("off")

    blocks = [
        (
            "1. INGESTÃO DE DADOS DESESTRUTURADOS",
            "[RAW INPUT]",
            (
                "• Descrições técnicas e manuais de 300 produtos\n"
                "• Feedbacks de SAC & transcrições de áudio (Whisper)\n"
                "• Mensagens de hesitação e saída no checkout"
            ),
            COLOR_BLUE,
            0.70,
            0.25
        ),
        (
            "2. PROCESSAMENTO GENAI & LLM GATE",
            "[CORTEX / LLM]",
            (
                "• Prompts estruturados normativos (spec_genai_001)\n"
                "• Extração semântica: voltagem, compatibilidade, frete\n"
                "• Custo < R$ 0,0008 / SKU • Latência média: 4.0 ms"
            ),
            COLOR_PURPLE,
            0.38,
            0.25
        ),
        (
            "3. VALIDAÇÃO CONTRATUAL PYDANTIC",
            "[SCHEMA 100%]",
            (
                "• Imposição estrita de JSON Schema (zero alucinação)\n"
                "• 100% dos campos validados e tipados formalmente\n"
                "• Ingestão na camada Silver (produtos_enriquecidos)"
            ),
            COLOR_GREEN,
            0.06,
            0.25
        ),
    ]

    for title, badge, desc, col, y_pos, h_box in blocks:
        # Container do Bloco
        box = patches.FancyBboxPatch(
            (0.04, y_pos), 0.92, h_box,
            boxstyle="round,pad=0.0,rounding_size=0.03",
            facecolor=COLOR_BG_CARD, edgecolor=col, linewidth=1.6,
            transform=ax_pipe.transAxes, zorder=2
        )
        ax_pipe.add_patch(box)
        
        # Barra / Cabeçalho do Bloco
        header_bg = patches.FancyBboxPatch(
            (0.04, y_pos + h_box - 0.065), 0.92, 0.065,
            boxstyle="round,pad=0.0,rounding_size=0.02",
            facecolor=col, alpha=0.12, edgecolor="none",
            transform=ax_pipe.transAxes, zorder=3
        )
        ax_pipe.add_patch(header_bg)
        
        # Título e Badge
        ax_pipe.text(0.07, y_pos + h_box - 0.032, title, transform=ax_pipe.transAxes,
                     fontsize=9.2, fontweight="bold", color=COLOR_PRIMARY, va="center")
        ax_pipe.text(0.93, y_pos + h_box - 0.032, badge, transform=ax_pipe.transAxes,
                     fontsize=8.0, fontweight="bold", color=col, ha="right", va="center")
        
        # Corpo de Texto Descritivo com Espaçamento Correto
        ax_pipe.text(0.07, y_pos + h_box - 0.085, desc, transform=ax_pipe.transAxes,
                     fontsize=8.8, fontweight="normal", color=COLOR_TEXT_MUTED, va="top", linespacing=1.4)

    # Setas conectoras com proporções exatas (sem tocar nas caixas)
    ax_pipe.annotate("", xy=(0.50, 0.64), xytext=(0.50, 0.69),
                     arrowprops=dict(arrowstyle="-|>", color=COLOR_PRIMARY, lw=1.8, mutation_scale=12))
    ax_pipe.annotate("", xy=(0.50, 0.32), xytext=(0.50, 0.37),
                     arrowprops=dict(arrowstyle="-|>", color=COLOR_PRIMARY, lw=1.8, mutation_scale=12))

    ax_pipe.set_title("Arquitetura do Pipeline GenAI & Extração de Features\n(Transformação Funcional: Texto Bruto -> Schema Silver Parquet)",
                      fontsize=11.5, fontweight="bold", color=COLOR_PRIMARY, pad=10)

    # =========================================================================
    # 2. COMPARATIVO DE CTR (Direita Topo)
    # =========================================================================
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
    bar_h = 0.32

    # Destaque de fundo suave para a linha de Média Ponderada Total
    ax_ctr.axhspan(3.5, 4.5, color="#F1F5F9", alpha=0.65, zorder=0)

    bars1 = ax_ctr.barh(y_ctr - bar_h/2 - 0.02, ctr_generico, height=bar_h, color=COLOR_CORAL, alpha=0.85,
                        edgecolor=COLOR_PRIMARY, linewidth=1.0, label="Mensagem Genérica (Sem IA)", zorder=3)
    bars2 = ax_ctr.barh(y_ctr + bar_h/2 + 0.02, ctr_genai, height=bar_h, color=COLOR_GREEN,
                        edgecolor=COLOR_PRIMARY, linewidth=1.2, label="Copy Personalizada GenAI (Contextual)", zorder=3)

    for bar, val in zip(bars1, ctr_generico):
        ax_ctr.text(val + 0.7, bar.get_y() + bar.get_height() / 2, f"{val:.1f}%",
                    va="center", ha="left", fontsize=8.8, fontweight="bold", color=COLOR_CORAL)

    for bar, val, lift in zip(bars2, ctr_genai, lifts):
        ax_ctr.text(val + 0.7, bar.get_y() + bar.get_height() / 2, f"{val:.1f}% ({lift})",
                    va="center", ha="left", fontsize=8.8, fontweight="bold", color=COLOR_GREEN)

    ax_ctr.set_yticks(y_ctr)
    ax_ctr.set_yticklabels(motivos, fontsize=9.2, fontweight="bold", color=COLOR_PRIMARY)
    ax_ctr.set_xlim(0, 42)
    ax_ctr.set_xlabel("Taxa de Cliques (CTR %) no Resgate", fontsize=10.0, fontweight="bold", color=COLOR_PRIMARY)
    ax_ctr.set_title("Efetividade de Resgate: Impacto do Copywriting Contextual GenAI\n(Aumento de +18% no Engajamento Direto vs Mensagens Genéricas)",
                      fontsize=11.5, fontweight="bold", color=COLOR_PRIMARY, pad=10)
    
    # Legenda no canto superior direito sem conflito com as barras
    ax_ctr.legend(loc="upper right", bbox_to_anchor=(0.99, 0.98), fontsize=8.5, framealpha=0.95, edgecolor=COLOR_BORDER)
    ax_ctr.grid(axis="x", linestyle="--", alpha=0.45, color=COLOR_BORDER, zorder=1)
    ax_ctr.spines["top"].set_visible(False)
    ax_ctr.spines["right"].set_visible(False)
    ax_ctr.invert_yaxis()

    # =========================================================================
    # 3. EXEMPLOS DE COPIES FORMATADAS (Direita Base)
    # =========================================================================
    ax_examples = fig.add_subplot(gs[2, 1])
    ax_examples.set_facecolor("#FFFFFF")
    ax_examples.axis("off")

    # Card 1: WhatsApp (Dúvida Técnica)
    p1 = patches.FancyBboxPatch(
        (0.02, 0.53), 0.96, 0.44,
        boxstyle="round,pad=0.0,rounding_size=0.03",
        facecolor=COLOR_BG_CARD, edgecolor=COLOR_GREEN, linewidth=1.5,
        transform=ax_examples.transAxes, zorder=2
    )
    ax_examples.add_patch(p1)

    p1_tag = patches.FancyBboxPatch(
        (0.035, 0.87), 0.93, 0.08,
        boxstyle="round,pad=0.0,rounding_size=0.02",
        facecolor="#ECFDF5", edgecolor=COLOR_GREEN, linewidth=0.8,
        transform=ax_examples.transAxes, zorder=3
    )
    ax_examples.add_patch(p1_tag)
    ax_examples.text(0.055, 0.91, "WHATSAPP API (ATENDIMENTO VIP CONSULTIVO)", transform=ax_examples.transAxes,
                     fontsize=8.8, fontweight="bold", color=COLOR_GREEN, va="center")
    ax_examples.text(0.945, 0.91, "Objeção: Dúvida de Voltagem (127V) • Score 94%", transform=ax_examples.transAxes,
                     fontsize=8.0, fontweight="bold", color=COLOR_TEXT_MUTED, ha="right", va="center")

    copy_text_1 = (
        "\"Olá Carlos! Notamos seu interesse na Smart TV 4K 55\\\". Confirmamos que o modelo é\n"
        "Bivolt Automático (127V/220V) com garantia oficial de 12 meses. Podemos reservar no carrinho?\""
    )
    ax_examples.text(0.055, 0.77, copy_text_1, transform=ax_examples.transAxes,
                     fontsize=8.6, fontweight="normal", fontstyle="italic", color=COLOR_PRIMARY, va="top", linespacing=1.35)

    ax_examples.text(0.055, 0.58, "CTR: 25.6% (+19.2% de Lift) • Estratégia: Suporte Técnico Proativo • Zero Desconto Concedido",
                     transform=ax_examples.transAxes, fontsize=7.8, fontweight="bold", color=COLOR_GREEN, va="center")

    # Card 2: E-mail (Atrito de Frete)
    p2 = patches.FancyBboxPatch(
        (0.02, 0.03), 0.96, 0.44,
        boxstyle="round,pad=0.0,rounding_size=0.03",
        facecolor=COLOR_BG_CARD, edgecolor=COLOR_BLUE, linewidth=1.5,
        transform=ax_examples.transAxes, zorder=2
    )
    ax_examples.add_patch(p2)

    p2_tag = patches.FancyBboxPatch(
        (0.035, 0.37), 0.93, 0.08,
        boxstyle="round,pad=0.0,rounding_size=0.02",
        facecolor="#EFF6FF", edgecolor=COLOR_BLUE, linewidth=0.8,
        transform=ax_examples.transAxes, zorder=3
    )
    ax_examples.add_patch(p2_tag)
    ax_examples.text(0.055, 0.41, "E-MAIL TRANSACIONAL (ESCALA & AUTOMAÇÃO CRM)", transform=ax_examples.transAxes,
                     fontsize=8.8, fontweight="bold", color=COLOR_BLUE, va="center")
    ax_examples.text(0.945, 0.41, "Objeção: Frete Alto • Gatilho: Cupom Expirável 2h", transform=ax_examples.transAxes,
                     fontsize=8.0, fontweight="bold", color=COLOR_TEXT_MUTED, ha="right", va="center")

    copy_text_2 = (
        "\"Mariana, o frete pesou na decisão? Liberamos 50% de desconto na entrega com o cupom\n"
        "FRETEOFF válido pelas próximas 2 horas. Finalize sua compra em 1 clique!\""
    )
    ax_examples.text(0.055, 0.27, copy_text_2, transform=ax_examples.transAxes,
                     fontsize=8.6, fontweight="normal", fontstyle="italic", color=COLOR_PRIMARY, va="top", linespacing=1.35)

    ax_examples.text(0.055, 0.08, "CTR: 29.9% (+21.4% de Lift) • Estratégia: Cupom Dinâmico de Frete • Conversão em < 2h",
                     transform=ax_examples.transAxes, fontsize=7.8, fontweight="bold", color=COLOR_BLUE, va="center")

    ax_examples.set_title("Exemplos de Copies Persuasivas Contextualizadas por Causa-Raiz\n(Eliminação de Abordagens Genéricas & Blindagem de Margem de Lucro)",
                          fontsize=11.5, fontweight="bold", color=COLOR_PRIMARY, pad=10)

    plt.suptitle("GENAI & LLMS: EXTRAÇÃO DE FEATURES E PERSONALIZAÇÃO SEMÂNTICA",
                 fontsize=14.5, fontweight="bold", color=COLOR_PRIMARY, y=0.97)

    return fig

def generate_and_save(target_path: Path = OUTPUT_IMAGE_PATH) -> Path:
    """Gera a figura e salva no caminho alvo (e sincroniza automaticamente com o roteiro se aplicável)."""
    df_produtos = load_catalog_data()
    fig = plot_genai_dashboard(df_produtos)
    
    # Salva no caminho canônico primário
    target_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(target_path, dpi=300, bbox_inches="tight", facecolor="#FFFFFF")
    
    # Sincronização automática para a pasta da view do roteiro se for diferente
    if target_path.resolve() != ROTEIRO_IMAGE_PATH.resolve():
        ROTEIRO_IMAGE_PATH.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(ROTEIRO_IMAGE_PATH, dpi=300, bbox_inches="tight", facecolor="#FFFFFF")
        print(f"[SYNC] Imagem sincronizada com a view do roteiro em: {ROTEIRO_IMAGE_PATH}")
        
    plt.close(fig)
    return target_path

def main() -> None:
    saved = generate_and_save(OUTPUT_IMAGE_PATH)
    print(f"[SUCCESS] Painel Canônico de GenAI Feature Extraction gerado em: {saved}")

if __name__ == "__main__":
    main()
