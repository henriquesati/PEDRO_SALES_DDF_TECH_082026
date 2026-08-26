#!/usr/bin/env python3
"""
generate_chart.py
Módulo: presentation/pitch/roteiro/views-streamlit/03-copiloto-resgate
Função: Renderização executiva da Tela 3 do Data App Streamlit (Copiloto Prescritivo de Resgate com IA Generativa).
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
OUTPUT_IMAGE_PATH: Final[Path] = Path(__file__).resolve().parent / "chart_streamlit_copiloto_resgate.png"

# Paleta Semântica Corporativa Dadosfera
COLOR_PRIMARY: Final[str] = "#0F172A"       # Slate 900
COLOR_TEXT_MUTED: Final[str] = "#475569"    # Slate 600
COLOR_BLUE: Final[str] = "#2563EB"          # Blue 600 (E-mail / Destaque)
COLOR_GREEN: Final[str] = "#059669"         # Emerald 600 (WhatsApp / Sucesso)
COLOR_CORAL: Final[str] = "#E11D48"         # Rose 600 (Objeção / Alerta)
COLOR_PURPLE: Final[str] = "#7C3AED"        # Violet 600 (GenAI / LLM Gate)
COLOR_AMBER: Final[str] = "#D97706"         # Amber 600 (Scorecard)
COLOR_BG_CARD: Final[str] = "#F8FAFC"       # Slate 50
COLOR_BORDER: Final[str] = "#CBD5E1"        # Slate 300
COLOR_SIDEBAR: Final[str] = "#F1F5F9"       # Slate 100

def plot_streamlit_copilot_view() -> plt.Figure:
    """Renderiza a interface executiva da Aba 3 (Copiloto de IA) do Data App Streamlit."""
    plt.rcParams["text.parse_math"] = False
    plt.rcParams["font.sans-serif"] = ["Segoe UI", "DejaVu Sans", "Helvetica", "Arial", "sans-serif"]
    plt.rcParams["axes.edgecolor"] = COLOR_BORDER
    plt.rcParams["axes.linewidth"] = 1.1

    fig = plt.figure(figsize=(16.0, 9.0), facecolor="#FFFFFF")
    
    # 0. STREAMLIT APP HEADER & TABS BAR
    ax_top = fig.add_axes([0.04, 0.90, 0.92, 0.08])
    ax_top.axis("off")
    
    ax_top.text(0.0, 0.70, "DADOSFERA DATA APP  |  RECUPERAÇÃO DE CARRINHOS (ITEM 9 & BÔNUS)",
                fontsize=13.0, fontweight="bold", color=COLOR_PRIMARY)
    ax_top.text(0.0, 0.20, "Tenant: pedro-sales  •  Copiloto GenAI: Snowflake Cortex / Pydantic Gate  •  Schema: 100% Strict Validation",
                fontsize=8.5, fontweight="normal", color=COLOR_TEXT_MUTED)
    
    tabs = [
        ("1. Simulador de ROI & Sensibilidade", COLOR_TEXT_MUTED, False),
        ("2. Explorador Semântico de Catálogo", COLOR_TEXT_MUTED, False),
        ("[ATIVO] 3. Copiloto Prescritivo de Resgate", COLOR_BLUE, True),
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

    # 1. STREAMLIT SIDEBAR (Filtros e Seleção de Cliente / Carrinho)
    ax_side = fig.add_axes([0.04, 0.06, 0.22, 0.76])
    ax_side.axis("off")
    
    side_box = patches.FancyBboxPatch(
        (0.0, 0.0), 1.0, 1.0,
        boxstyle="round,pad=0.0,rounding_size=0.02",
        facecolor=COLOR_SIDEBAR, edgecolor=COLOR_BORDER, linewidth=1.2,
        transform=ax_side.transAxes
    )
    ax_side.add_patch(side_box)
    
    ax_side.text(0.08, 0.94, "FILA DE ACIONAMENTO IA", fontsize=9.5, fontweight="bold", color=COLOR_PRIMARY)
    ax_side.text(0.08, 0.90, "Selecione o carrinho para análise:", fontsize=8.0, color=COLOR_TEXT_MUTED)
    
    sidebar_items = [
        ("ID do Carrinho", "Carrinho #1042 (Telemetria)", 0.78),
        ("Cliente Identificado", "Carlos Mendes (Perfil VIP)", 0.64),
        ("Ticket em Risco", "R$ 2.499,00 (Ticket Alto)", 0.50),
        ("Produto Abandonado", "Smart TV 4K 55\" Bivolt", 0.36),
        ("Canal Prioritário", "WhatsApp API Consultivo", 0.22),
        ("Estratégia de Margem", "Zero Cupom (Preservar 28.5%)", 0.08),
    ]
    
    for label, val_text, y_c in sidebar_items:
        ax_side.text(0.08, y_c + 0.05, label, fontsize=8.2, fontweight="bold", color=COLOR_PRIMARY)
        pill = patches.FancyBboxPatch(
            (0.08, y_c - 0.02), 0.84, 0.045,
            boxstyle="round,pad=0.0,rounding_size=0.015",
            facecolor="#FFFFFF", edgecolor=COLOR_BORDER, linewidth=1.0,
            transform=ax_side.transAxes
        )
        ax_side.add_patch(pill)
        ax_side.text(0.12, y_c + 0.002, val_text, fontsize=8.0, fontweight="semibold", color=COLOR_BLUE)

    # 2. SCORECARD DE DIAGNÓSTICO CAUSAL DO LLM (Topo do Painel Principal)
    ax_diag = fig.add_axes([0.28, 0.64, 0.68, 0.18])
    ax_diag.axis("off")
    
    diag_box = patches.FancyBboxPatch(
        (0.0, 0.0), 1.0, 1.0,
        boxstyle="round,pad=0.0,rounding_size=0.03",
        facecolor=COLOR_BG_CARD, edgecolor=COLOR_PURPLE, linewidth=1.6,
        transform=ax_diag.transAxes
    )
    ax_diag.add_patch(diag_box)
    
    diag_tag = patches.FancyBboxPatch(
        (0.0, 0.80), 1.0, 0.20,
        boxstyle="round,pad=0.0,rounding_size=0.015",
        facecolor=COLOR_PURPLE, alpha=0.14, edgecolor="none",
        transform=ax_diag.transAxes
    )
    ax_diag.add_patch(diag_tag)
    
    ax_diag.text(0.03, 0.89, "DIAGNÓSTICO CAUSAL EM TEMPO REAL (SNOWFLAKE CORTEX LLM GATE)", fontsize=9.2, fontweight="bold", color=COLOR_PRIMARY)
    ax_diag.text(0.97, 0.89, "SCHEMA VALIDATION: 100% PYDANTIC", fontsize=8.0, fontweight="bold", color=COLOR_PURPLE, ha="right")
    
    # 4 Pilares do Diagnóstico
    pillars = [
        ("Motivo-Raiz Identificado", "Dúvida Técnica (Voltagem 127V)", COLOR_CORAL),
        ("Sentimento do Cliente", "Hesitante / Cuidadoso", COLOR_AMBER),
        ("Nível de Urgência", "Alto (Abandono há 28 min)", COLOR_PURPLE),
        ("Sensibilidade a Preço", "Baixa (Foco em Garantia)", COLOR_GREEN),
    ]
    p_w = 0.23
    for i, (p_title, p_val, p_col) in enumerate(pillars):
        px = 0.03 + i * (p_w + 0.02)
        ax_diag.text(px, 0.52, p_title.upper(), fontsize=7.8, fontweight="bold", color=COLOR_TEXT_MUTED)
        ax_diag.text(px, 0.24, p_val, fontsize=9.5, fontweight="bold", color=p_col)

    # 3. COPIES PERSONALIZADAS PRONTAS PARA DISPARO (Meio)
    # Card Esquerdo: WhatsApp API VIP
    ax_wpp = fig.add_axes([0.28, 0.18, 0.33, 0.42])
    ax_wpp.axis("off")
    
    wpp_box = patches.FancyBboxPatch(
        (0.0, 0.0), 1.0, 1.0,
        boxstyle="round,pad=0.0,rounding_size=0.03",
        facecolor=COLOR_BG_CARD, edgecolor=COLOR_GREEN, linewidth=1.5,
        transform=ax_wpp.transAxes
    )
    ax_wpp.add_patch(wpp_box)
    
    wpp_tag = patches.FancyBboxPatch(
        (0.0, 0.84), 1.0, 0.16,
        boxstyle="round,pad=0.0,rounding_size=0.015",
        facecolor="#ECFDF5", edgecolor="none", transform=ax_wpp.transAxes
    )
    ax_wpp.add_patch(wpp_tag)
    ax_wpp.text(0.04, 0.91, "WHATSAPP API (CONSULTIVO VIP)", fontsize=8.8, fontweight="bold", color=COLOR_GREEN)
    ax_wpp.text(0.96, 0.91, "Score: 94% • 1-Click Send", fontsize=8.0, fontweight="bold", color=COLOR_TEXT_MUTED, ha="right")
    
    copy_wpp = (
        "\"Olá Carlos! Vimos que você estava olhando a Smart TV 4K 55\".\n"
        "Confirmamos que o modelo é Bivolt Automático (127V/220V)\n"
        "com garantia oficial de 12 meses. Quer que a gente reserve\n"
        "a última unidade no seu carrinho?\""
    )
    ax_wpp.text(0.04, 0.72, copy_wpp, fontsize=8.4, fontstyle="italic", color=COLOR_PRIMARY, va="top", linespacing=1.35)
    
    # Botão de Ação Interativo
    btn_wpp = patches.FancyBboxPatch(
        (0.04, 0.10), 0.92, 0.18,
        boxstyle="round,pad=0.0,rounding_size=0.02",
        facecolor=COLOR_GREEN, edgecolor="none", transform=ax_wpp.transAxes
    )
    ax_wpp.add_patch(btn_wpp)
    ax_wpp.text(0.50, 0.19, "DISPARAR VIA WHATSAPP (ROI ESTIMADO: 8.2x)", fontsize=8.0, fontweight="bold",
                color="#FFFFFF", ha="center", va="center")

    # Card Direito: E-mail Transacional Dinâmico
    ax_mail = fig.add_axes([0.63, 0.18, 0.33, 0.42])
    ax_mail.axis("off")
    
    mail_box = patches.FancyBboxPatch(
        (0.0, 0.0), 1.0, 1.0,
        boxstyle="round,pad=0.0,rounding_size=0.03",
        facecolor=COLOR_BG_CARD, edgecolor=COLOR_BLUE, linewidth=1.5,
        transform=ax_mail.transAxes
    )
    ax_mail.add_patch(mail_box)
    
    mail_tag = patches.FancyBboxPatch(
        (0.0, 0.84), 1.0, 0.16,
        boxstyle="round,pad=0.0,rounding_size=0.015",
        facecolor="#EFF6FF", edgecolor="none", transform=ax_mail.transAxes
    )
    ax_mail.add_patch(mail_tag)
    ax_mail.text(0.04, 0.91, "E-MAIL TRANSACIONAL (CRM ESCALA)", fontsize=8.8, fontweight="bold", color=COLOR_BLUE)
    ax_mail.text(0.96, 0.91, "Score: 88% • Auto Trigger", fontsize=8.0, fontweight="bold", color=COLOR_TEXT_MUTED, ha="right")
    
    copy_mail = (
        "\"Carlos, restou alguma dúvida sobre a instalação da Smart TV 4K?\n"
        "O produto possui compatibilidade total Bivolt e suporte técnico\n"
        "incluso. Acesse seu carrinho salvo e conclua seu pedido com\n"
        "frete prioritário para sua região.\""
    )
    ax_mail.text(0.04, 0.72, copy_mail, fontsize=8.4, fontstyle="italic", color=COLOR_PRIMARY, va="top", linespacing=1.35)
    
    btn_mail = patches.FancyBboxPatch(
        (0.04, 0.10), 0.92, 0.18,
        boxstyle="round,pad=0.0,rounding_size=0.02",
        facecolor=COLOR_BLUE, edgecolor="none", transform=ax_mail.transAxes
    )
    ax_mail.add_patch(btn_mail)
    ax_mail.text(0.50, 0.19, "AGENDAR NA RÉGUA DE E-MAIL (ROI: 18.4x)", fontsize=8.0, fontweight="bold",
                color="#FFFFFF", ha="center", va="center")

    # 4. RODAPÉ TÉCNICO DE GOVERNANÇA & SLA DO MODELO
    ax_bot = fig.add_axes([0.28, 0.06, 0.68, 0.08])
    ax_bot.axis("off")
    
    bot_box = patches.FancyBboxPatch(
        (0.0, 0.0), 1.0, 1.0,
        boxstyle="round,pad=0.0,rounding_size=0.02",
        facecolor="#F8FAFC", edgecolor=COLOR_BORDER, linewidth=1.0,
        transform=ax_bot.transAxes
    )
    ax_bot.add_patch(bot_box)
    
    ax_bot.text(0.03, 0.50, "SLA & GOVERNANÇA GENAI:", fontsize=8.2, fontweight="bold", color=COLOR_PRIMARY, va="center")
    ax_bot.text(0.24, 0.50, "• Latência: 4.0 ms (In-Database Cortex)  • Custo: < R$ 0,0008 / SKU  • Blindagem Pydantic: Zero Alucinações  • LGPD: Sem exposição de PII",
                fontsize=8.0, color=COLOR_TEXT_MUTED, va="center")

    return fig

def main() -> None:
    fig = plot_streamlit_copilot_view()
    OUTPUT_IMAGE_PATH.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_IMAGE_PATH, dpi=300, bbox_inches="tight", facecolor="#FFFFFF")
    plt.close(fig)
    print(f"[SUCCESS] Tela Streamlit Copiloto de IA gerada com sucesso em: {OUTPUT_IMAGE_PATH}")

if __name__ == "__main__":
    main()
