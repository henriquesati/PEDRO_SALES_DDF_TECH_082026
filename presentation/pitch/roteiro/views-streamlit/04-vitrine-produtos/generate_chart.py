#!/usr/bin/env python3
"""
generate_chart.py
Módulo: presentation/pitch/roteiro/views-streamlit/04-vitrine-produtos
Função: Renderização executiva da Tela 4 do Data App Streamlit (Vitrine Visual de Produtos Enriquecidos).
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
OUTPUT_IMAGE_PATH: Final[Path] = Path(__file__).resolve().parent / "chart_streamlit_vitrine_produtos.png"

# Paleta Semântica Corporativa Dadosfera
COLOR_PRIMARY: Final[str] = "#0F172A"       # Slate 900
COLOR_TEXT_MUTED: Final[str] = "#475569"    # Slate 600
COLOR_BLUE: Final[str] = "#2563EB"          # Blue 600 (Eletrônicos)
COLOR_GREEN: Final[str] = "#059669"         # Emerald 600 (Casa & Decoração / Sucesso)
COLOR_CORAL: Final[str] = "#E11D48"         # Rose 600 (Tag de Urgência)
COLOR_PURPLE: Final[str] = "#7C3AED"        # Violet 600 (GenAI)
COLOR_AMBER: Final[str] = "#D97706"         # Amber 600 (Destaque)
COLOR_BG_CARD: Final[str] = "#F8FAFC"       # Slate 50
COLOR_BORDER: Final[str] = "#CBD5E1"        # Slate 300
COLOR_SIDEBAR: Final[str] = "#F1F5F9"       # Slate 100

def plot_streamlit_showcase_view() -> plt.Figure:
    """Renderiza a interface executiva da Aba 4 (Vitrine de Produtos) do Data App Streamlit."""
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
    ax_top.text(0.0, 0.20, "Tenant: pedro-sales  •  Catálogo Lakehouse: CART_RECOVERY.PRODUTOS_ENRIQUECIDOS  •  Data Quality: 100%",
                fontsize=8.5, fontweight="normal", color=COLOR_TEXT_MUTED)
    
    tabs = [
        ("1. Simulador de ROI & Sensibilidade", COLOR_TEXT_MUTED, False),
        ("2. Explorador Semântico de Catálogo", COLOR_TEXT_MUTED, False),
        ("3. Copiloto Prescritivo de Resgate", COLOR_TEXT_MUTED, False),
        ("[ATIVO] 4. Vitrine Visual de Produtos", COLOR_BLUE, True),
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

    # 1. STREAMLIT SIDEBAR (Filtros de Catálogo)
    ax_side = fig.add_axes([0.04, 0.06, 0.22, 0.76])
    ax_side.axis("off")
    
    side_box = patches.FancyBboxPatch(
        (0.0, 0.0), 1.0, 1.0,
        boxstyle="round,pad=0.0,rounding_size=0.02",
        facecolor=COLOR_SIDEBAR, edgecolor=COLOR_BORDER, linewidth=1.2,
        transform=ax_side.transAxes
    )
    ax_side.add_patch(side_box)
    
    ax_side.text(0.08, 0.94, "FILTROS DO CATÁLOGO", fontsize=9.5, fontweight="bold", color=COLOR_PRIMARY)
    ax_side.text(0.08, 0.90, "Explore os produtos enriquecidos:", fontsize=8.0, color=COLOR_TEXT_MUTED)
    
    sidebar_items = [
        ("Filtrar por Categoria", "Todas (300 Produtos)", 0.78),
        ("Faixa de Ticket", "R$ 500 a R$ 3.500", 0.64),
        ("Tags de Compatibilidade", "Bivolt Automático / 127V", 0.50),
        ("Status de Resgate", "Com Histórico de Abandono", 0.36),
        ("Ordenação", "Maior Volume de GMV", 0.22),
        ("Exportação Lakehouse", "Sincronizado Snowflake Silver", 0.08),
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

    # 2. TOP BANNER DE MÉTRICAS DO CATÁLOGO
    ax_banner = fig.add_axes([0.28, 0.72, 0.68, 0.10])
    ax_banner.axis("off")
    
    b_kpis = [
        ("Total de SKUs", "300 Produtos", "100% Catalogados no DW", COLOR_BLUE),
        ("Enriquecimento GenAI", "100.0% Pydantic", "Features Técnicas Extraídas", COLOR_PURPLE),
        ("Voltagem Normalizada", "100% Mapeado", "Zero Objeções de Compatibilidade", COLOR_GREEN),
        ("Ticket Médio do Catálogo", "R$ 348,80", "Base Sólida de Faturamento", COLOR_AMBER),
    ]
    
    b_w = 0.235
    for i, (b_title, b_val, b_sub, b_col) in enumerate(b_kpis):
        bx = i * (b_w + 0.02)
        c_box = patches.FancyBboxPatch(
            (bx, 0.0), b_w, 1.0,
            boxstyle="round,pad=0.0,rounding_size=0.03",
            facecolor=COLOR_BG_CARD, edgecolor=b_col, linewidth=1.4,
            transform=ax_banner.transAxes
        )
        ax_banner.add_patch(c_box)
        ax_banner.text(bx + b_w/2.0, 0.72, b_title.upper(), fontsize=8.2, fontweight="bold",
                       color=COLOR_TEXT_MUTED, ha="center", va="center", transform=ax_banner.transAxes)
        ax_banner.text(bx + b_w/2.0, 0.40, b_val, fontsize=12.5, fontweight="bold",
                       color=COLOR_PRIMARY, ha="center", va="center", transform=ax_banner.transAxes)
        ax_banner.text(bx + b_w/2.0, 0.15, b_sub, fontsize=7.8, fontweight="semibold",
                       color=b_col, ha="center", va="center", transform=ax_banner.transAxes)

    # 3. GRID DE CARDS VISUAIS DE PRODUTOS ENRIQUECIDOS
    ax_grid = fig.add_axes([0.28, 0.06, 0.68, 0.62])
    ax_grid.axis("off")
    
    products = [
        (
            "Smart TV 4K 55\" Ultra HD",
            "Eletrônicos",
            "R$ 2.499,00",
            "Painel IPS 120Hz • Processador AI • Bivolt Automático (127V/220V)",
            "Alta (Eletrônicos Premium)",
            "12 abandonos  •  4 recuperados (33.3% Conv)",
            "WhatsApp VIP (Consultivo)",
            COLOR_BLUE,
            0.0
        ),
        (
            "Fone Noise Cancelling Pro",
            "Eletrônicos",
            "R$ 899,00",
            "Cancelamento Ativo de Ruído 35dB • Bateria 40h • Bluetooth 5.3",
            "Média (Áudio Profissional)",
            "24 abandonos  •  11 recuperados (45.8% Conv)",
            "E-mail Transacional",
            COLOR_GREEN,
            0.35
        ),
        (
            "Robô Aspirador Laser Smart",
            "Casa & Decoração",
            "R$ 1.899,00",
            "Mapeamento LiDAR 360° • Sucção 4000Pa • Bivolt • App Wi-Fi",
            "Média (Eletroportáteis)",
            "18 abandonos  •  6 recuperados (33.3% Conv)",
            "WhatsApp + E-mail",
            COLOR_PURPLE,
            0.70
        ),
    ]
    
    p_card_w = 0.30
    for p_name, p_cat, p_price, p_feats, p_sens, p_hist, p_canal, p_col, px in products:
        p_box = patches.FancyBboxPatch(
            (px, 0.0), p_card_w, 1.0,
            boxstyle="round,pad=0.0,rounding_size=0.03",
            facecolor=COLOR_BG_CARD, edgecolor=p_col, linewidth=1.5,
            transform=ax_grid.transAxes
        )
        ax_grid.add_patch(p_box)
        
        # Header do Card
        p_tag = patches.FancyBboxPatch(
            (px, 0.90), p_card_w, 0.10,
            boxstyle="round,pad=0.0,rounding_size=0.015",
            facecolor=p_col, alpha=0.14, edgecolor="none",
            transform=ax_grid.transAxes
        )
        ax_grid.add_patch(p_tag)
        
        ax_grid.text(px + 0.02, 0.95, p_cat.upper(), fontsize=7.8, fontweight="bold", color=p_col, va="center", transform=ax_grid.transAxes)
        ax_grid.text(px + p_card_w - 0.02, 0.95, p_price, fontsize=8.8, fontweight="bold", color=COLOR_PRIMARY, ha="right", va="center", transform=ax_grid.transAxes)
        
        # Título do Produto
        ax_grid.text(px + 0.02, 0.84, p_name, fontsize=9.2, fontweight="bold", color=COLOR_PRIMARY, transform=ax_grid.transAxes)
        
        # Diferenciais Técnicos Extraídos por IA
        ax_grid.text(px + 0.02, 0.76, "DIFERENCIAIS TÉCNICOS (GENAI):", fontsize=7.5, fontweight="bold", color=COLOR_TEXT_MUTED, transform=ax_grid.transAxes)
        ax_grid.text(px + 0.02, 0.62, p_feats, fontsize=8.0, color=COLOR_PRIMARY, wrap=True, transform=ax_grid.transAxes)
        
        # Separador
        ax_grid.plot([px + 0.02, px + p_card_w - 0.02], [0.46, 0.46], color=COLOR_BORDER, linestyle="--", linewidth=1.0, transform=ax_grid.transAxes)
        
        # Telemetria & Resgate
        ax_grid.text(px + 0.02, 0.40, "TELEMETRIA DE CARRINHOS:", fontsize=7.5, fontweight="bold", color=COLOR_TEXT_MUTED, transform=ax_grid.transAxes)
        ax_grid.text(px + 0.02, 0.32, p_hist, fontsize=8.0, fontweight="semibold", color=COLOR_PRIMARY, transform=ax_grid.transAxes)
        
        ax_grid.text(px + 0.02, 0.22, "CANAL RECOMENDADO PELA IA:", fontsize=7.5, fontweight="bold", color=COLOR_TEXT_MUTED, transform=ax_grid.transAxes)
        ax_grid.text(px + 0.02, 0.14, p_canal, fontsize=8.2, fontweight="bold", color=p_col, transform=ax_grid.transAxes)
        
        # Botão Visual de Ação
        p_btn = patches.FancyBboxPatch(
            (px + 0.02, 0.03), p_card_w - 0.04, 0.07,
            boxstyle="round,pad=0.0,rounding_size=0.015",
            facecolor=p_col, edgecolor="none",
            transform=ax_grid.transAxes
        )
        ax_grid.add_patch(p_btn)
        ax_grid.text(px + p_card_w/2.0, 0.065, "VER NO LAKEHOUSE", fontsize=7.5, fontweight="bold",
                     color="#FFFFFF", ha="center", va="center", transform=ax_grid.transAxes)

    return fig

def main() -> None:
    fig = plot_streamlit_showcase_view()
    OUTPUT_IMAGE_PATH.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_IMAGE_PATH, dpi=300, bbox_inches="tight", facecolor="#FFFFFF")
    plt.close(fig)
    print(f"[SUCCESS] Tela Streamlit Vitrine de Produtos gerada com sucesso em: {OUTPUT_IMAGE_PATH}")

if __name__ == "__main__":
    main()
