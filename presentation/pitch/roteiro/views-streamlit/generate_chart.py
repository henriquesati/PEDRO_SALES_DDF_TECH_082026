#!/usr/bin/env python3
"""
generate_chart.py
Módulo: presentation/pitch/roteiro/views-streamlit
Função: Renderização executiva consolidada do Data App Streamlit em 4 Telas Modulares (Item 9 & Bônus GenAI).
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
OUTPUT_IMAGE_PATH: Final[Path] = Path(__file__).resolve().parent / "chart_streamlit_data_app_overview.png"

# Paleta Semântica Corporativa Dadosfera
COLOR_PRIMARY: Final[str] = "#0F172A"       # Slate 900
COLOR_TEXT_MUTED: Final[str] = "#475569"    # Slate 600
COLOR_BLUE: Final[str] = "#2563EB"          # Blue 600 (Simulador ROI)
COLOR_GREEN: Final[str] = "#059669"         # Emerald 600 (Vitrine / Sucesso)
COLOR_PURPLE: Final[str] = "#7C3AED"        # Violet 600 (Copiloto GenAI)
COLOR_AMBER: Final[str] = "#D97706"         # Amber 600 (Explorador Vetorial)
COLOR_CORAL: Final[str] = "#E11D48"         # Rose 600 (Alertas)
COLOR_BG_CARD: Final[str] = "#F8FAFC"       # Slate 50
COLOR_BORDER: Final[str] = "#CBD5E1"        # Slate 300
COLOR_SIDEBAR: Final[str] = "#F1F5F9"       # Slate 100

def plot_streamlit_master_overview() -> plt.Figure:
    """Renderiza a visão executiva consolidada do Data App Streamlit (4 Telas Modulares)."""
    plt.rcParams["text.parse_math"] = False
    plt.rcParams["font.sans-serif"] = ["Segoe UI", "DejaVu Sans", "Helvetica", "Arial", "sans-serif"]
    plt.rcParams["axes.edgecolor"] = COLOR_BORDER
    plt.rcParams["axes.linewidth"] = 1.1

    fig = plt.figure(figsize=(16.0, 9.0), facecolor="#FFFFFF")
    
    # Header Executivo
    ax_top = fig.add_axes([0.04, 0.90, 0.92, 0.08])
    ax_top.axis("off")
    
    ax_top.text(0.0, 0.70, "DADOSFERA DATA APPS  |  CONSUMO & ANALYTICS INTERATIVO (STREAMLIT)",
                fontsize=13.5, fontweight="bold", color=COLOR_PRIMARY)
    ax_top.text(0.0, 0.20, "Aplicação Modular em 4 Camadas (React/TS Pattern)  •  Conexão Nativa com Snowflake Lakehouse  •  Deploy Elástico SaaS",
                fontsize=8.8, fontweight="normal", color=COLOR_TEXT_MUTED)
    
    # 4 Quadrantes Representando as 4 Abas do Data App
    ax_grid = fig.add_axes([0.04, 0.08, 0.92, 0.78])
    ax_grid.axis("off")
    
    quadrants = [
        (
            "1. SIMULADOR DE ROI & SENSIBILIDADE",
            "Simulação em tempo real de mix de canais (E-mail 85%, WhatsApp 12%, SMS 2%, Push 1%) com retorno de R$ 314,5k GMV resgatado (ROI 45.2x e 28.5% margem).",
            "• Sliders interativos de budget e conversão\n• Curva de sensibilidade e saturação\n• Rebalanceamento orçamentário De -> Para",
            "R$ 314.500 GMV | ROI 45.2x",
            COLOR_BLUE,
            0.0, 0.52
        ),
        (
            "2. EXPLORADOR SEMÂNTICO (t-SNE / PCA)",
            "Projeção vetorial 2D de 300 produtos do catálogo agrupados por afinidade semântica para recomendação automática de SKUs substitutos em carrinhos abandonados.",
            "• Embeddings vetoriais em 2 dimensões\n• Similaridade de cosseno instantânea (>= 0.85)\n• Sugestão de itens similares com maior margem",
            "300 SKUs Mapeados | Lift +18%",
            COLOR_AMBER,
            0.52, 0.52
        ),
        (
            "3. COPILOTO PRESCRITIVO DE RESGATE",
            "Assistente inteligente de IA Generativa que cruza telemetria e feedbacks de clientes para diagnosticar a hesitação e gerar copies persuasivas validadas.",
            "• Diagnóstico causal (dúvida de voltagem, frete)\n• Geração de copies prontas para WhatsApp/E-mail\n• 100% Pydantic JSON Schema (zero alucinação)",
            "100% Pydantic | Latência 4.0 ms",
            COLOR_PURPLE,
            0.0, 0.0
        ),
        (
            "4. VITRINE DE PRODUTOS ENRIQUECIDOS",
            "Catálogo interativo conectado à camada Silver (PRODUTOS_ENRIQUECIDOS) com filtros semânticos e associação direta com métricas de conversão de CRM.",
            "• Diferenciais técnicos extraídos por LLM\n• Normalização de voltagem e compatibilidade\n• Democratização de dados sem necessidade de SQL",
            "Camada Silver | Zero Inconsistência",
            COLOR_GREEN,
            0.52, 0.0
        ),
    ]
    
    q_w = 0.46
    q_h = 0.44
    for q_title, q_desc, q_bullets, q_metric, q_col, q_x, q_y in quadrants:
        # Container Card
        q_box = patches.FancyBboxPatch(
            (q_x, q_y), q_w, q_h,
            boxstyle="round,pad=0.0,rounding_size=0.03",
            facecolor=COLOR_BG_CARD, edgecolor=q_col, linewidth=1.6,
            transform=ax_grid.transAxes
        )
        ax_grid.add_patch(q_box)
        
        # Header Tag
        q_tag = patches.FancyBboxPatch(
            (q_x, q_y + q_h - 0.08), q_w, 0.08,
            boxstyle="round,pad=0.0,rounding_size=0.015",
            facecolor=q_col, alpha=0.14, edgecolor="none",
            transform=ax_grid.transAxes
        )
        ax_grid.add_patch(q_tag)
        
        ax_grid.text(q_x + 0.02, q_y + q_h - 0.04, q_title, fontsize=9.2, fontweight="bold",
                     color=q_col, va="center", transform=ax_grid.transAxes)
        
        # Descrição
        ax_grid.text(q_x + 0.02, q_y + q_h - 0.12, q_desc, fontsize=8.2, color=COLOR_PRIMARY,
                     wrap=True, va="top", transform=ax_grid.transAxes)
        
        # Bullets Técnicos
        ax_grid.text(q_x + 0.02, q_y + 0.18, q_bullets, fontsize=8.0, color=COLOR_TEXT_MUTED,
                     linespacing=1.35, va="top", transform=ax_grid.transAxes)
        
        # Footer Pill de Métrica
        pill_box = patches.FancyBboxPatch(
            (q_x + 0.02, q_y + 0.03), q_w - 0.04, 0.06,
            boxstyle="round,pad=0.0,rounding_size=0.015",
            facecolor=q_col, edgecolor="none",
            transform=ax_grid.transAxes
        )
        ax_grid.add_patch(pill_box)
        ax_grid.text(q_x + q_w/2.0, q_y + 0.06, q_metric.upper(), fontsize=7.8, fontweight="bold",
                     color="#FFFFFF", ha="center", va="center", transform=ax_grid.transAxes)

    return fig

def main() -> None:
    fig = plot_streamlit_master_overview()
    OUTPUT_IMAGE_PATH.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_IMAGE_PATH, dpi=300, bbox_inches="tight", facecolor="#FFFFFF")
    plt.close(fig)
    print(f"[SUCCESS] Painel Consolidado do Data App Streamlit gerado com sucesso em: {OUTPUT_IMAGE_PATH}")

if __name__ == "__main__":
    main()
