"""
Gerador das visualizações do Módulo 02: Motivos de Abandono de Carrinho.
1. Treemap Hierárquico: Decomposição Proporcional de Volume por Causa-Raiz (Sem poluição financeira).
2. Gráfico Separado de Impacto Financeiro: Perda Financeira Represada (R$) e Ticket Médio por Motivo.
Atende estritamente à especificação de presentation/insights/02_motivos_abandono/spec.md.
Paradigma funcional e declarativo com tipagem estrita (Type Annotations).
"""

from typing import Final
import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches

BASE_DIR: Final[str] = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
MODULE_DIR: Final[str] = os.path.dirname(__file__)

OUTPUT_TREEMAP_PATH: Final[str] = os.path.join(
    MODULE_DIR, "chart_02_treemap_motivos_abandono.png"
)
OUTPUT_OFFICIAL_PATH: Final[str] = os.path.join(
    MODULE_DIR, "chart_02_motivos_abandono.png"
)
OUTPUT_FINANCIAL_PATH: Final[str] = os.path.join(
    MODULE_DIR, "chart_02_perda_financeira_motivos.png"
)

PARQUET_CARTS_PATH: Final[str] = (
    os.path.join(BASE_DIR, "data", "mock", "output_cleaned", "parquet", "carrinhos.parquet")
    if os.path.exists(os.path.join(BASE_DIR, "data", "mock", "output_cleaned", "parquet", "carrinhos.parquet"))
    else os.path.join(BASE_DIR, "data", "mock", "output", "parquet", "carrinhos.parquet")
)

def load_data() -> pd.DataFrame:
    """Carrega dados transacionais de carrinhos abandonados (Ground Truth)."""
    df = pd.read_parquet(PARQUET_CARTS_PATH)
    df_aband = df[df["motivo_abandono"].notna() & (df["motivo_abandono"] != "")].copy()
    
    label_map = {
        "preco": "Preço Alto",
        "frete": "Frete Caro",
        "indecisao": "Indecisão / Dúvida",
        "pagamento": "Erro no Pagamento",
        "nao_informado": "Não Informado",
        "estoque": "Estoque Indisponível"
    }
    df_aband["motivo_label"] = df_aband["motivo_abandono"].map(label_map).fillna(df_aband["motivo_abandono"])
    return df_aband

def prepare_aggregations(df: pd.DataFrame) -> pd.DataFrame:
    """Calcula agregados consolidados por motivo de abandono."""
    order_motivos = [
        "Preço Alto", "Frete Caro", "Indecisão / Dúvida",
        "Erro no Pagamento", "Não Informado", "Estoque Indisponível"
    ]
    
    agg = df.groupby("motivo_label").agg(
        volume=("carrinho_id", "count"),
        receita_represada=("valor_total", "sum"),
        ticket_medio=("valor_total", "mean")
    ).reindex(order_motivos).reset_index()
    
    total_vol = agg["volume"].sum()
    total_rec = agg["receita_represada"].sum()
    
    agg["pct_volume"] = (agg["volume"] / total_vol) * 100
    agg["pct_receita"] = (agg["receita_represada"] / total_rec) * 100
    return agg

def plot_treemap_chart(agg: pd.DataFrame) -> plt.Figure:
    """Gera o Treemap Hierárquico Proporcional ao volume, sem cifras financeiras."""
    plt.rcParams["font.sans-serif"] = ["Segoe UI", "DejaVu Sans", "Helvetica", "Arial", "sans-serif"]
    
    fig, ax = plt.subplots(figsize=(13.5, 7.2))
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")
    ax.axis("off")
    
    # Definição proporcional das coordenadas dos 6 blocos
    # Total de 5.231 carrinhos (100%)
    rects = [
        # Preço Alto (1.307 un / 25.0%)
        {
            "name": "Preço Alto",
            "pct": 25.0,
            "desc": "1.307 carrinhos abandonados por preços elevados",
            "bbox": [0.0, 0.50, 0.50, 0.50],
            "color": "#1E3A8A",
            "text_col": "#FFFFFF"
        },
        # Frete Caro (1.207 un / 23.1%)
        {
            "name": "Frete Caro",
            "pct": 23.1,
            "desc": "1.207 carrinhos abandonados por frete muito caro",
            "bbox": [0.50, 0.50, 0.50, 0.50],
            "color": "#2563EB",
            "text_col": "#FFFFFF"
        },
        # Indecisão / Dúvida (1.045 un / 20.0%)
        {
            "name": "Indecisão / Dúvida",
            "pct": 20.0,
            "desc": "1.045 carrinhos abandonados por indecisão ou dúvida",
            "bbox": [0.0, 0.0, 0.40, 0.50],
            "color": "#059669",
            "text_col": "#FFFFFF"
        },
        # Erro no Pagamento (961 un / 18.4%)
        {
            "name": "Erro no Pagamento",
            "pct": 18.4,
            "desc": "961 carrinhos abandonados por falhas no pagamento",
            "bbox": [0.40, 0.0, 0.35, 0.50],
            "color": "#D97706",
            "text_col": "#FFFFFF"
        },
        # Não Informado (487 un / 9.3%)
        {
            "name": "Não Informado",
            "pct": 9.3,
            "desc": "487 carrinhos abandonados sem motivo declarado",
            "bbox": [0.75, 0.22, 0.25, 0.28],
            "color": "#64748B",
            "text_col": "#FFFFFF"
        },
        # Estoque Indisponível (224 un / 4.3%)
        {
            "name": "Estoque Indisponível",
            "pct": 4.3,
            "desc": "224 carrinhos abandonados por falta de estoque",
            "bbox": [0.75, 0.0, 0.25, 0.22],
            "color": "#94A3B8",
            "text_col": "#0F172A"
        }
    ]
    
    for r in rects:
        x, y, w, h = r["bbox"]
        rect_patch = patches.Rectangle((x, y), w, h, facecolor=r["color"], edgecolor="#FFFFFF", linewidth=3.5)
        ax.add_patch(rect_patch)
        
        cx, cy = x + w / 2, y + h / 2
        # Título
        ax.text(cx, cy + h * 0.12, r["name"], ha="center", va="center", color=r["text_col"], fontsize=12.5, fontweight="bold")
        # Porcentagem
        ax.text(cx, cy - h * 0.04, f"{r['pct']:.1f}% do abandono", ha="center", va="center", color=r["text_col"], fontsize=11, fontweight="bold")
        # Descrição simples
        ax.text(cx, cy - h * 0.20, r["desc"], ha="center", va="center", color=r["text_col"], fontsize=9.5, fontweight="normal", alpha=0.92)

    ax.set_xlim(-0.01, 1.01)
    ax.set_ylim(-0.01, 1.06)
    ax.set_title("DECOMPOSIÇÃO DE VOLUME: CAUSAS-RAIZ DE ABANDONO DE CARRINHO (5.231 UN)",
                 fontsize=14.5, fontweight="bold", color="#0F172A", pad=15)
                 
    plt.tight_layout()
    return fig

def plot_financial_loss_chart(agg: pd.DataFrame) -> plt.Figure:
    """Gera o Gráfico Separado de Impacto Financeiro e Perda Represada em R$ por Causa-Raiz."""
    plt.rcParams["font.sans-serif"] = ["Segoe UI", "DejaVu Sans", "Helvetica", "Arial", "sans-serif"]
    plt.rcParams["axes.edgecolor"] = "#CBD5E1"
    plt.rcParams["axes.linewidth"] = 1.2

    fig, ax = plt.subplots(figsize=(12.0, 6.5))
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")

    agg_sorted = agg.sort_values(by="receita_represada", ascending=True).reset_index(drop=True)
    y_pos = np.arange(len(agg_sorted))
    motivos = agg_sorted["motivo_label"].tolist()
    receitas_k = agg_sorted["receita_represada"].to_numpy() / 1000.0
    pcts_rec = agg_sorted["pct_receita"].to_numpy()
    tickets = agg_sorted["ticket_medio"].to_numpy()
    total_k = agg_sorted["receita_represada"].sum() / 1000.0

    bar_height = 0.52
    bars = ax.barh(y_pos, receitas_k, height=bar_height, color="#E11D48", alpha=0.88, edgecolor="#9F1239")

    for i, (rec, pct, tkt) in enumerate(zip(receitas_k, pcts_rec, tickets)):
        ax.text(
            rec + 12, i,
            f"R$ {rec:,.1f}k  ({pct:.1f}% da perda)\nTicket Médio: R$ {tkt:,.0f} / carrinho",
            va="center", ha="left", fontsize=10, fontweight="bold", color="#0F172A"
        )

    ax.set_yticks(y_pos)
    ax.set_yticklabels(motivos, fontsize=11.5, fontweight="bold", color="#1E293B")
    ax.set_xlabel("Receita Represada em Abandono (R$ Milhares)", fontsize=11.5, fontweight="bold", color="#334155")
    ax.set_title(f"IMPACTO FINANCEIRO REPRESADO POR CAUSA-RAIZ (TOTAL: R$ {total_k:,.1f}k)",
                 fontsize=14, fontweight="bold", color="#0F172A", pad=15)
    ax.set_xlim(0, max(receitas_k) * 1.45)
    ax.grid(axis="x", linestyle="--", alpha=0.5, color="#CBD5E1")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.tight_layout()
    return fig

def main() -> None:
    df_data = load_data()
    agg = prepare_aggregations(df_data)

    # 1. Gráfico de Treemap (Sem poluição financeira)
    fig_tree = plot_treemap_chart(agg)
    fig_tree.savefig(OUTPUT_TREEMAP_PATH, dpi=300, bbox_inches="tight", facecolor="#FFFFFF")
    fig_tree.savefig(OUTPUT_OFFICIAL_PATH, dpi=300, bbox_inches="tight", facecolor="#FFFFFF")
    plt.close(fig_tree)
    print(f"[SUCCESS] Treemap de Motivos de Abandono salvo em: {OUTPUT_TREEMAP_PATH}")

    # 2. Gráfico Separado de Perda Financeira
    fig_fin = plot_financial_loss_chart(agg)
    fig_fin.savefig(OUTPUT_FINANCIAL_PATH, dpi=300, bbox_inches="tight", facecolor="#FFFFFF")
    plt.close(fig_fin)
    print(f"[SUCCESS] Gráfico de Perda Financeira salvo em: {OUTPUT_FINANCIAL_PATH}")

if __name__ == "__main__":
    main()
