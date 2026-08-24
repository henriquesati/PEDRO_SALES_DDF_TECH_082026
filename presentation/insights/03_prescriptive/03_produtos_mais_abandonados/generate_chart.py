"""
Gerador da visualização: Produtos e Categorias Mais Abandonados & Intervenções Prescritivas.
Atende estritamente à especificação de presentation/insights/03_prescriptive/03_produtos_mais_abandonados/spec.md
e insights/03_prescriptive/produtos_mais_abandonados.md.
Paradigma funcional e declarativo com tipagem estrita (Type Annotations).
"""

from typing import Final, Tuple
import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR: Final[str] = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
MODULE_DIR: Final[str] = os.path.dirname(__file__)

OUTPUT_IMAGE_PATH: Final[str] = os.path.join(
    MODULE_DIR, "chart_03_produtos_mais_abandonados.png"
)

PARQUET_ITEMS_PATH: Final[str] = (
    os.path.join(BASE_DIR, "data", "mock", "output_cleaned", "parquet", "itens_carrinho.parquet")
    if os.path.exists(os.path.join(BASE_DIR, "data", "mock", "output_cleaned", "parquet", "itens_carrinho.parquet"))
    else os.path.join(BASE_DIR, "data", "mock", "output", "parquet", "itens_carrinho.parquet")
)

PARQUET_PRODS_PATH: Final[str] = (
    os.path.join(BASE_DIR, "data", "mock", "output_cleaned", "parquet", "produtos.parquet")
    if os.path.exists(os.path.join(BASE_DIR, "data", "mock", "output_cleaned", "parquet", "produtos.parquet"))
    else os.path.join(BASE_DIR, "data", "mock", "output", "parquet", "produtos.parquet")
)

PARQUET_CARTS_PATH: Final[str] = (
    os.path.join(BASE_DIR, "data", "mock", "output_cleaned", "parquet", "carrinhos.parquet")
    if os.path.exists(os.path.join(BASE_DIR, "data", "mock", "output_cleaned", "parquet", "carrinhos.parquet"))
    else os.path.join(BASE_DIR, "data", "mock", "output", "parquet", "carrinhos.parquet")
)

def load_data() -> pd.DataFrame:
    """Carrega e associa itens de carrinho, catálogo de produtos e status dos carrinhos."""
    df_items = pd.read_parquet(PARQUET_ITEMS_PATH)
    df_prods = pd.read_parquet(PARQUET_PRODS_PATH)
    df_carts = pd.read_parquet(PARQUET_CARTS_PATH)

    df_items_merged = df_items.merge(
        df_carts[["carrinho_id", "status", "motivo_abandono"]],
        on="carrinho_id",
        how="left"
    )
    df_items_merged = df_items_merged.merge(
        df_prods[["produto_id", "nome", "categoria", "subcategoria", "preco_atual", "avaliacao_media"]],
        on="produto_id",
        how="left"
    )

    # Considera itens ativos no carrinho (sem remoção)
    df_active = df_items_merged[df_items_merged["data_remocao"].isna()].copy()
    return df_active

def compute_category_abandonment(df_active: pd.DataFrame) -> pd.DataFrame:
    """Calcula métricas de abandono, receita represada e volume por categoria de produto."""
    cat_summary = df_active.groupby("categoria").agg(
        total_itens=("item_id", "count"),
        itens_abandonados=("status", lambda s: (s == "abandonado").sum()),
        receita_represada=("preco_total", lambda p: p[df_active.loc[p.index, "status"] == "abandonado"].sum()),
        preco_medio=("preco_atual", "mean"),
        avaliacao_media=("avaliacao_media", "mean")
    ).reset_index()

    cat_summary["taxa_abandono"] = (cat_summary["itens_abandonados"] / cat_summary["total_itens"]) * 100
    cat_summary["pct_receita_total"] = (cat_summary["receita_represada"] / cat_summary["receita_represada"].sum()) * 100

    # Ordena decrescente por receita represada
    cat_summary = cat_summary.sort_values(by="receita_represada", ascending=True).reset_index(drop=True)
    return cat_summary

def plot_product_category_chart(cat_summary: pd.DataFrame) -> plt.Figure:
    """Gera o painel duplo: Ranking de Receita por Categoria + Matriz Prescritiva de Intervenções."""
    plt.rcParams["font.sans-serif"] = ["Segoe UI", "DejaVu Sans", "Helvetica", "Arial", "sans-serif"]
    plt.rcParams["axes.edgecolor"] = "#CBD5E1"
    plt.rcParams["axes.linewidth"] = 1.1

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16.0, 7.2), gridspec_kw={"width_ratios": [1.1, 1.1]})
    fig.patch.set_facecolor("#FFFFFF")

    # --- PAINEL 1: Barras de Receita Represada por Categoria ---
    ax1.set_facecolor("#FFFFFF")

    categories = cat_summary["categoria"].tolist()
    y_pos = np.arange(len(categories))
    receita_k = cat_summary["receita_represada"].to_numpy() / 1000.0
    taxas = cat_summary["taxa_abandono"].to_numpy()
    itens = cat_summary["itens_abandonados"].to_numpy()
    pcts_rec = cat_summary["pct_receita_total"].to_numpy()

    # Cores personalizadas destacando as principais categorias
    color_map = {
        "Eletrônicos": "#2563EB",
        "Casa & Decoração": "#059669",
        "Moda": "#D97706",
        "Esportes": "#7C3AED",
        "Brinquedos": "#64748B",
        "Beleza": "#EC4899",
        "Livros": "#0EA5E9"
    }
    bar_colors = [color_map.get(cat, "#64748B") for cat in categories]

    bars = ax1.barh(y_pos, receita_k, height=0.55, color=bar_colors, alpha=0.90, edgecolor="#0F172A", linewidth=1.1)

    for i, (val, pct, taxa, it) in enumerate(zip(receita_k, pcts_rec, taxas, itens)):
        ax1.text(
            val + 35, i,
            f"R$ {val:,.1f}k ({pct:.1f}%)\nAbandono: {taxa:.1f}% ({it:,} un)",
            va="center", ha="left", fontsize=9.2, fontweight="bold", color="#0F172A"
        )

    ax1.set_yticks(y_pos)
    ax1.set_yticklabels(categories, fontsize=11, fontweight="bold", color="#1E293B")
    ax1.set_xlabel("Receita Represada em Carrinhos Abandonados (R$ Milhares)", fontsize=11, fontweight="bold", color="#334155")
    ax1.set_title("1. RECEITA REPRESADA POR CATEGORIA (R$ k)", fontsize=12.5, fontweight="bold", color="#0F172A", pad=12)
    ax1.set_xlim(0, max(receita_k) * 1.38)
    ax1.grid(axis="x", linestyle="--", alpha=0.4, color="#CBD5E1")
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)

    # --- PAINEL 2: Matriz Prescritiva de Intervenções por Categoria ---
    ax2.set_facecolor("#FFFFFF")
    ax2.axis("off")

    table_data = [
        ["Categoria", "Dor Principal do Cliente", "Gatilho Prescritivo no Resgate", "Ação Corretiva na Página (UX)"],
        ["ELETRÔNICOS\n(> R$ 1.000)", "Medo / Risco financeiro\n& Garantia", "Frete Grátis com Seguro +\nGarantia Estendida de 1 Ano", "Destacar selos de segurança,\ngarantia e reviews com fotos"],
        ["MODA\n(R$ 100 - 500)", "Dúvida de caimento,\ntamanho e modelagem", "Garantia de '1ª Troca Grátis\ne Sem Burocracia' no email", "Provador virtual interativo e\ntabela de medidas com fotos"],
        ["CASA & DEC.\n(R$ 50 - 400)", "Frete volumoso e\ndúvida de dimensões", "Cupom de subsídio de frete\nem compras > R$ 150", "Calculadora de ambiente 3D\ne simulador de medidas"],
        ["BELEZA / ACESS.\n(< R$ 100)", "Frete desproporcional\nao item individual", "Cross-sell: 'Adicione R$ 20\npara Frete Grátis'", "Kits promocionais e barra de\nprogresso de frete no carrinho"]
    ]

    table = ax2.table(
        cellText=table_data,
        cellLoc="center",
        loc="center",
        bbox=[0.0, 0.12, 1.0, 0.80]
    )
    table.auto_set_font_size(False)
    table.set_fontsize(8.8)

    for (row, col), cell in table.get_celld().items():
        cell.set_edgecolor("#CBD5E1")
        cell.set_linewidth(1.1)
        if row == 0:
            cell.set_facecolor("#0F172A")
            cell.set_text_props(weight="bold", color="#FFFFFF")
            cell.set_height(0.12)
        else:
            if row == 1:
                cell.set_facecolor("#EFF6FF")  # Azul Eletrônicos
            elif row == 2:
                cell.set_facecolor("#FEF3C7")  # Âmbar Moda
            elif row == 3:
                cell.set_facecolor("#ECFDF5")  # Verde Decoração
            else:
                cell.set_facecolor("#FDF2F8")  # Rosa Beleza
            cell.set_text_props(weight="bold" if col == 0 else "normal", color="#0F172A")
            cell.set_height(0.17)

    # Nota explicativa
    note_text = (
        "RESOLUÇÃO PRESCRITIVA POR CONTEXTO DE PRODUTO:\n"
        "• Em vez de disparar emails genéricos, a Dadosfera personaliza a copy e o incentivo conforme a categoria.\n"
        "• '1ª Troca Grátis' em Moda destrava +35% de conversão com custo real de devolução inferior a 3%.\n"
        "• Garantia estendida em Eletrônicos remove a hesitação de alto ticket sem queimar margem com cupons."
    )
    bbox_props = dict(boxstyle="round,pad=0.5", facecolor="#F8FAFC", edgecolor="#94A3B8", linewidth=1.1)
    ax2.text(0.0, 0.01, note_text, fontsize=8.3, color="#1E293B", va="bottom", bbox=bbox_props, transform=ax2.transAxes, family="monospace")

    ax2.set_title("2. MATRIZ PRESCRITIVA DE INTERVENÇÃO POR CATEGORIA", fontsize=12.5, fontweight="bold", color="#0F172A", pad=12)

    fig.suptitle("ANÁLISE DE PRODUTOS & CATEGORIAS MAIS ABANDONADOS: RECEITA REPRESADA & MATRIZ PRESCRITIVA",
                 fontsize=14.5, fontweight="bold", color="#0F172A", y=0.98)

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    return fig

def main() -> None:
    df_active = load_data()
    cat_summary = compute_category_abandonment(df_active)
    
    fig = plot_product_category_chart(cat_summary)
    os.makedirs(MODULE_DIR, exist_ok=True)
    fig.savefig(OUTPUT_IMAGE_PATH, dpi=300, bbox_inches="tight", facecolor="#FFFFFF")
    plt.close(fig)
    print(f"[SUCCESS] Gráfico de Categorias e Produtos Mais Abandonados salvo em: {OUTPUT_IMAGE_PATH}")

if __name__ == "__main__":
    main()
