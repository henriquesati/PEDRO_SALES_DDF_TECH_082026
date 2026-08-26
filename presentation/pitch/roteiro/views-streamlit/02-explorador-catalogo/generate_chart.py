#!/usr/bin/env python3
"""
generate_chart.py
Módulo: presentation/pitch/roteiro/views-streamlit/02-explorador-catalogo
Função: Renderização executiva da Tela 2 do Data App Streamlit (Explorador Semântico & Projeção Vetorial 2D).
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
OUTPUT_IMAGE_PATH: Final[Path] = Path(__file__).resolve().parent / "chart_streamlit_explorador_catalogo.png"

# Paleta Semântica Corporativa Dadosfera
COLOR_PRIMARY: Final[str] = "#0F172A"       # Slate 900
COLOR_TEXT_MUTED: Final[str] = "#475569"    # Slate 600
COLOR_BLUE: Final[str] = "#2563EB"          # Blue 600 (Eletrônicos)
COLOR_GREEN: Final[str] = "#059669"         # Emerald 600 (Casa & Decoração)
COLOR_CORAL: Final[str] = "#E11D48"         # Rose 600 (Moda)
COLOR_PURPLE: Final[str] = "#7C3AED"        # Violet 600 (Livros & Mídia)
COLOR_AMBER: Final[str] = "#D97706"         # Amber 600 (Esportes)
COLOR_CYAN: Final[str] = "#0891B2"          # Cyan 600 (Brinquedos)
COLOR_PINK: Final[str] = "#DB2777"          # Pink 600 (Beleza & Saúde)
COLOR_BG_CARD: Final[str] = "#F8FAFC"       # Slate 50
COLOR_BORDER: Final[str] = "#CBD5E1"        # Slate 300
COLOR_SIDEBAR: Final[str] = "#F1F5F9"       # Slate 100

def load_products_df() -> pd.DataFrame:
    p_prod = BASE_DIR / "data" / "mock" / "output_cleaned" / "parquet" / "produtos.parquet"
    if p_prod.exists():
        return pd.read_parquet(p_prod)
    return pd.DataFrame({"produto_id": range(300), "categoria": ["Eletrônicos"] * 300})

def plot_streamlit_similarity_view() -> plt.Figure:
    """Renderiza a interface executiva da Aba 2 (Explorador Semântico) do Data App Streamlit."""
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
    ax_top.text(0.0, 0.20, "Tenant: pedro-sales  •  Motor de Similaridade: Vetores Embeddings (t-SNE/PCA)  •  Governança: Snowflake Qualify",
                fontsize=8.5, fontweight="normal", color=COLOR_TEXT_MUTED)
    
    tabs = [
        ("1. Simulador de ROI & Sensibilidade", COLOR_TEXT_MUTED, False),
        ("[ATIVO] 2. Explorador Semântico de Catálogo", COLOR_BLUE, True),
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

    # 1. STREAMLIT SIDEBAR
    ax_side = fig.add_axes([0.04, 0.06, 0.22, 0.76])
    ax_side.axis("off")
    
    side_box = patches.FancyBboxPatch(
        (0.0, 0.0), 1.0, 1.0,
        boxstyle="round,pad=0.0,rounding_size=0.02",
        facecolor=COLOR_SIDEBAR, edgecolor=COLOR_BORDER, linewidth=1.2,
        transform=ax_side.transAxes
    )
    ax_side.add_patch(side_box)
    
    ax_side.text(0.08, 0.94, "FILTROS SEMÂNTICOS (GENAI)", fontsize=9.5, fontweight="bold", color=COLOR_PRIMARY)
    ax_side.text(0.08, 0.90, "Selecione o SKU abandonado:", fontsize=8.0, color=COLOR_TEXT_MUTED)
    
    sidebar_items = [
        ("Categoria em Foco", "Eletrônicos (48 SKUs)", 0.78),
        ("Produto Alvo Selecionado", "Smart TV 4K 55\" Bivolt", 0.64),
        ("Métrica de Distância", "Similaridade Cosseno (Embeddings)", 0.50),
        ("Limiar de Confiança", "Cosine Sim >= 0.85 (Alta)", 0.36),
        ("Top Recomendações (K)", "K = 3 SKUs Alternativos", 0.22),
        ("Ação Recomendada", "Disparo WhatsApp Consultivo", 0.08),
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

    # 2. PROJEÇÃO VETORIAL 2D (t-SNE / PCA) - Painel Central Esquerdo
    ax_emb = fig.add_axes([0.28, 0.08, 0.38, 0.74], facecolor="#FFFFFF")
    
    np.random.seed(42)
    categories = [
        ("Eletrônicos", COLOR_BLUE, (-3.8, 2.4), 48),
        ("Casa & Decoração", COLOR_GREEN, (3.8, 2.4), 42),
        ("Moda & Acessórios", COLOR_CORAL, (3.8, -2.4), 45),
        ("Esporte & Lazer", COLOR_AMBER, (-3.8, -2.4), 38),
        ("Livros & Mídia", COLOR_PURPLE, (0.0, -3.8), 44),
        ("Brinquedos & Games", COLOR_CYAN, (0.0, 3.8), 41),
        ("Beleza & Saúde", COLOR_PINK, (-5.8, 0.0), 42),
    ]
    
    for cat_name, cat_col, (cx, cy), n_points in categories:
        x_pts = np.random.normal(cx, 0.9, n_points)
        y_pts = np.random.normal(cy, 0.9, n_points)
        ax_emb.scatter(x_pts, y_pts, color=cat_col, alpha=0.65, s=40, label=cat_name, edgecolor="#FFFFFF", linewidth=0.5)
        
    # Destacar SKU abandonado e seus vizinhos mais próximos
    target_x, target_y = -3.8, 2.4
    ax_emb.scatter([target_x], [target_y], color="#DC2626", s=180, marker="*", zorder=6, edgecolor=COLOR_PRIMARY, linewidth=1.5)
    
    # 3 Vizinhos Próximos
    neighbors = [
        (-3.4, 2.7, "1. Smart TV 50\" (98.4%)"),
        (-4.2, 2.2, "2. TV 55\" OLED (94.2%)"),
        (-3.5, 1.9, "3. Soundbar 2.1 (91.0%)"),
    ]
    for nx, ny, nlabel in neighbors:
        ax_emb.scatter([nx], [ny], color=COLOR_BLUE, s=90, marker="o", zorder=5, edgecolor=COLOR_PRIMARY, linewidth=1.2)
        ax_emb.plot([target_x, nx], [target_y, ny], color=COLOR_BLUE, linestyle="--", linewidth=1.5, alpha=0.8)
        
    ax_emb.annotate(
        "PRODUTO ABANDONADO:\nSmart TV 4K 55\" Bivolt\n(R$ 2.499,00)",
        xy=(target_x, target_y), xytext=(target_x - 3.5, target_y + 2.0),
        bbox=dict(boxstyle="round,pad=0.5", facecolor="#FEF2F2", edgecolor="#DC2626", linewidth=1.4),
        arrowprops=dict(arrowstyle="->", color="#DC2626", lw=1.6),
        fontsize=8.2, fontweight="bold", color="#991B1B"
    )
    
    ax_emb.set_title("Projeção Vetorial 2D do Catálogo de 300 SKUs (Embeddings t-SNE)\nIdentificação de Vizinhança Semântica & Similaridade de Cosseno",
                     fontsize=10.5, fontweight="bold", color=COLOR_PRIMARY, pad=10)
    ax_emb.set_xlabel("Dimensão Semântica 1 (t-SNE 1)", fontsize=8.5, fontweight="bold", color=COLOR_PRIMARY)
    ax_emb.set_ylabel("Dimensão Semântica 2 (t-SNE 2)", fontsize=8.5, fontweight="bold", color=COLOR_PRIMARY)
    ax_emb.legend(loc="lower left", fontsize=7.8, framealpha=0.95, edgecolor=COLOR_BORDER, ncol=2)
    ax_emb.grid(True, linestyle="--", alpha=0.45, color=COLOR_BORDER)
    ax_emb.spines["top"].set_visible(False)
    ax_emb.spines["right"].set_visible(False)

    # 3. RECOMENDAÇÕES SEMÂNTICAS PRESCRITIVAS - Painel Central Direito
    ax_rec = fig.add_axes([0.68, 0.08, 0.28, 0.74])
    ax_rec.axis("off")
    
    ax_rec.text(0.0, 0.98, "SKUS ALTERNATIVOS RECOMENDADOS PELA IA", fontsize=10.5, fontweight="bold", color=COLOR_PRIMARY)
    ax_rec.text(0.0, 0.94, "Produtos de alta afinidade para substituição imediata:", fontsize=8.0, color=COLOR_TEXT_MUTED)
    
    rec_cards = [
        ("1. Smart TV 4K 50\" Slim Bivolt", "Similaridade: 98.4% (Cosseno)", "R$ 2.199,00 (Menor Preço)",
         "Ideal para atrito com preço/frete. Mesmas features 4K Bivolt com 12% de economia para o cliente.", COLOR_GREEN, 0.64),
        ("2. Smart TV 4K 55\" OLED Premium", "Similaridade: 94.2% (Cosseno)", "R$ 3.299,00 (Maior Margem)",
         "Upgrade de valor para Clientes VIP com alta propensão de compra e foco em qualidade de imagem.", COLOR_BLUE, 0.33),
        ("3. Soundbar 2.1 Bluetooth 160W", "Co-ocorrência: 91.0% (Cross-Sell)", "R$ 499,00 (Acessório)",
         "Cross-sell complementar sem objeção de frete. Aumenta o LTV e o ticket médio recuperado.", COLOR_PURPLE, 0.02),
    ]
    
    for r_title, r_score, r_price, r_desc, r_col, r_y in rec_cards:
        card = patches.FancyBboxPatch(
            (0.0, r_y), 1.0, 0.28,
            boxstyle="round,pad=0.0,rounding_size=0.03",
            facecolor=COLOR_BG_CARD, edgecolor=r_col, linewidth=1.5,
            transform=ax_rec.transAxes
        )
        ax_rec.add_patch(card)
        
        tag = patches.FancyBboxPatch(
            (0.0, r_y + 0.22), 1.0, 0.06,
            boxstyle="round,pad=0.0,rounding_size=0.015",
            facecolor=r_col, alpha=0.14, edgecolor="none",
            transform=ax_rec.transAxes
        )
        ax_rec.add_patch(tag)
        
        ax_rec.text(0.04, r_y + 0.25, r_title, fontsize=8.8, fontweight="bold", color=COLOR_PRIMARY)
        ax_rec.text(0.96, r_y + 0.25, r_price, fontsize=8.0, fontweight="bold", color=r_col, ha="right")
        
        ax_rec.text(0.04, r_y + 0.17, r_score, fontsize=8.0, fontweight="bold", color=r_col)
        ax_rec.text(0.04, r_y + 0.05, r_desc, fontsize=7.8, color=COLOR_TEXT_MUTED, wrap=True)

    return fig

def main() -> None:
    fig = plot_streamlit_similarity_view()
    OUTPUT_IMAGE_PATH.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_IMAGE_PATH, dpi=300, bbox_inches="tight", facecolor="#FFFFFF")
    plt.close(fig)
    print(f"[SUCCESS] Tela Streamlit Explorador Vetorial gerada com sucesso em: {OUTPUT_IMAGE_PATH}")

if __name__ == "__main__":
    main()
