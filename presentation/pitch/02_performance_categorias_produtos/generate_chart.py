"""
Gerador da visualização: Performance de Catálogo e Abandono por Categoria.
Paradigma funcional e declarativo com tipagem estrita (Type Annotations).
"""

from typing import Final
import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

BASE_DIR: Final[str] = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
PITCH_DIR: Final[str] = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PITCH_DIR not in sys.path:
    sys.path.insert(0, PITCH_DIR)

from config.chart_theme import apply_dadosfera_theme, save_chart_artifact, DADOSFERA_PALETTE

OUTPUT_IMAGE_PATH: Final[str] = os.path.join(
    os.path.dirname(__file__), "chart_02_performance_categorias.png"
)
PARQUET_PRODUCTS_PATH: Final[str] = (
    os.path.join(BASE_DIR, "data", "mock", "output_cleaned", "parquet", "produtos.parquet")
    if os.path.exists(os.path.join(BASE_DIR, "data", "mock", "output_cleaned", "parquet", "produtos.parquet"))
    else os.path.join(BASE_DIR, "data", "mock", "output", "parquet", "produtos.parquet")
)
PARQUET_ITEMS_PATH: Final[str] = (
    os.path.join(BASE_DIR, "data", "mock", "output_cleaned", "parquet", "itens_carrinho.parquet")
    if os.path.exists(os.path.join(BASE_DIR, "data", "mock", "output_cleaned", "parquet", "itens_carrinho.parquet"))
    else os.path.join(BASE_DIR, "data", "mock", "output", "parquet", "itens_carrinho.parquet")
)
PARQUET_CARTS_PATH: Final[str] = (
    os.path.join(BASE_DIR, "data", "mock", "output_cleaned", "parquet", "carrinhos.parquet")
    if os.path.exists(os.path.join(BASE_DIR, "data", "mock", "output_cleaned", "parquet", "carrinhos.parquet"))
    else os.path.join(BASE_DIR, "data", "mock", "output", "parquet", "carrinhos.parquet")
)

def load_category_data() -> pd.DataFrame:
    """Carrega dados combinados de itens, produtos e status do carrinho (fonte limpa)."""
    df_products = pd.read_parquet(PARQUET_PRODUCTS_PATH)
    df_items = pd.read_parquet(PARQUET_ITEMS_PATH)
    df_carts = pd.read_parquet(PARQUET_CARTS_PATH)
    
    df_merged = df_items.merge(df_products[["produto_id", "categoria"]], on="produto_id", how="inner")
    df_full = df_merged.merge(df_carts[["carrinho_id", "status"]], on="carrinho_id", how="inner")
    return df_full

def aggregate_by_category(df_full: pd.DataFrame) -> pd.DataFrame:
    """Agrega volumes de abandono, compras e calcula a taxa percentual de atrito."""
    grouped = df_full.groupby("categoria").agg(
        total_itens=("item_id", "count"),
        abandonados=("status", lambda s: (s == "abandonado").sum()),
        comprados=("status", lambda s: (s.isin(["comprado", "recuperado"])).sum())
    ).reset_index()
    
    # Adiciona taxa percentual de abandono por categoria
    result = grouped.assign(
        taxa_abandono=(grouped["abandonados"] / grouped["total_itens"].replace(0, 1)) * 100
    ).sort_values(by="total_itens", ascending=True)
    return result

def plot_category_performance(df_cat: pd.DataFrame) -> plt.Figure:
    """Plota gráfico de barras horizontais empilhadas com indicadores percentuais."""
    apply_dadosfera_theme()
    
    fig, ax = plt.subplots(figsize=(12.0, 6.8))
    
    y_pos = np.arange(len(df_cat))
    height = 0.55
    
    # Barras de itens convertidos
    bars_comp = ax.barh(
        y_pos, df_cat["comprados"], 
        height=height, color=DADOSFERA_PALETTE.accent_green, 
        label="Convertidos / Recuperados", alpha=0.9
    )
    
    # Barras de itens abandonados (empilhadas)
    bars_aban = ax.barh(
        y_pos, df_cat["abandonados"], 
        left=df_cat["comprados"],
        height=height, color=DADOSFERA_PALETTE.accent_coral, 
        label="Abandonados", alpha=0.9
    )
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(df_cat["categoria"], fontsize=11, fontweight="bold", color=DADOSFERA_PALETTE.text_light)
    ax.set_xlabel("Volume Total de Itens em Carrinho", fontsize=11, fontweight="bold", color=DADOSFERA_PALETTE.text_light)
    ax.set_title("Performance de Catálogo: Atrito & Taxa de Abandono por Categoria", fontsize=15, fontweight="bold", pad=15)
    
    # Anotações de taxa percentual
    for i, (_, row) in enumerate(df_cat.iterrows()):
        total = row["total_itens"]
        taxa = row["taxa_abandono"]
        ax.text(
            total + 15, i, f"Taxa: {taxa:.1f}%", 
            va="center", ha="left", 
            color=DADOSFERA_PALETTE.accent_yellow, 
            fontsize=10, fontweight="bold"
        )
    
    ax.legend(loc="lower right", framealpha=0.95)
    ax.grid(axis="x", linestyle="--", alpha=0.3)
    
    return fig

def main() -> None:
    df_full = load_category_data()
    df_cat = aggregate_by_category(df_full)
    fig = plot_category_performance(df_cat)
    saved_path = save_chart_artifact(fig, OUTPUT_IMAGE_PATH)
    print(f"[SUCCESS] Gráfico gerado em: {saved_path}")

if __name__ == "__main__":
    main()
