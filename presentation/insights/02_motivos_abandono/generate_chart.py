"""
Gerador das visualizações do Módulo 02: Motivos de Abandono de Carrinho.
1. Gráfico de Dispersão: Decomposição de Volume e Carrinhos Abandonados por Causa-Raiz e Dispositivo.
2. Gráfico de Impacto Financeiro: Perda Financeira Represada (R$) e Ticket Médio por Motivo (Separado).
Atende estritamente à especificação de presentation/insights/02_motivos_abandono/spec.md.
Paradigma funcional e declarativo com tipagem estrita (Type Annotations).
"""

from typing import Final
import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR: Final[str] = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
MODULE_DIR: Final[str] = os.path.dirname(__file__)

OUTPUT_DISPERSION_PATH: Final[str] = os.path.join(
    MODULE_DIR, "chart_02_dispersao_motivos_abandono.png"
)
OUTPUT_FINANCIAL_PATH: Final[str] = os.path.join(
    MODULE_DIR, "chart_02_perda_financeira_motivos.png"
)
# Compatibilidade com o nome anterior
OUTPUT_LEGACY_PATH: Final[str] = os.path.join(
    MODULE_DIR, "chart_02_motivos_abandono.png"
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
        ticket_medio=("valor_total", "mean"),
        ticket_mediano=("valor_total", "median")
    ).reindex(order_motivos).reset_index()
    
    total_vol = agg["volume"].sum()
    total_rec = agg["receita_represada"].sum()
    
    agg["pct_volume"] = (agg["volume"] / total_vol) * 100
    agg["pct_receita"] = (agg["receita_represada"] / total_rec) * 100
    return agg

def plot_dispersion_chart(df: pd.DataFrame, agg: pd.DataFrame) -> plt.Figure:
    """Gera o Gráfico de Dispersão (Scatter/Strip plot) de carrinhos abandonados por causa-raiz."""
    plt.rcParams["font.sans-serif"] = ["Segoe UI", "DejaVu Sans", "Helvetica", "Arial", "sans-serif"]
    plt.rcParams["axes.edgecolor"] = "#CBD5E1"
    plt.rcParams["axes.linewidth"] = 1.2

    fig, ax = plt.subplots(figsize=(13.5, 7.2))
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")

    motivo_list = agg["motivo_label"].tolist()
    device_colors = {
        "mobile": "#2563EB",   # Azul
        "desktop": "#059669",  # Verde
        "tablet": "#F59E0B"    # Âmbar
    }
    device_labels = {
        "mobile": "Mobile",
        "desktop": "Desktop",
        "tablet": "Tablet"
    }

    np.random.seed(42)  # Reprodutibilidade estrita

    # Plotagem pontual dos carrinhos distribuídos por motivo
    for idx, motivo in enumerate(motivo_list):
        df_m = df[df["motivo_label"] == motivo]
        vol = len(df_m)
        pct = agg.loc[agg["motivo_label"] == motivo, "pct_volume"].values[0]
        tm = agg.loc[agg["motivo_label"] == motivo, "ticket_medio"].values[0]

        # Jitter horizontal controlado
        jitter = np.random.normal(0, 0.14, size=len(df_m))
        jitter = np.clip(jitter, -0.32, 0.32)
        x_vals = idx + jitter
        y_vals = df_m["valor_total"].to_numpy()

        for dev in ["mobile", "desktop", "tablet"]:
            mask_dev = (df_m["dispositivo"] == dev).to_numpy()
            if np.any(mask_dev):
                ax.scatter(
                    x_vals[mask_dev],
                    y_vals[mask_dev],
                    c=device_colors[dev],
                    s=22,
                    alpha=0.45,
                    edgecolors="none",
                    label=device_labels[dev] if idx == 0 else ""
                )

        # Marcador de Média
        ax.scatter(idx, tm, color="#0F172A", s=90, zorder=6, marker="D", edgecolors="#FFFFFF", linewidth=1.5)

        # Card superior com Volumetria
        ax.text(
            idx, 1530,
            f"{vol:,.0f} un\n({pct:.1f}%)",
            ha="center", va="center",
            fontsize=10, fontweight="bold", color="#0F172A",
            bbox=dict(boxstyle="round,pad=0.35", facecolor="#F1F5F9", edgecolor="#CBD5E1", alpha=0.95)
        )

        # Label de Ticket Médio
        ax.text(
            idx, tm + 45,
            f"TM R${tm:.0f}",
            ha="center", va="bottom",
            fontsize=8.5, fontweight="bold", color="#0F172A"
        )

    ax.set_xticks(range(len(motivo_list)))
    ax.set_xticklabels(motivo_list, fontsize=11, fontweight="bold", color="#1E293B")
    ax.set_ylabel("Valor do Carrinho Abandonado (R$)", fontsize=11.5, fontweight="bold", color="#334155")
    ax.set_ylim(0, 1650)
    ax.set_title("DECOMPOSIÇÃO DE VOLUME: DISPERSÃO DE CARRINHOS POR CAUSA-RAIZ & DISPOSITIVO",
                 fontsize=14, fontweight="bold", color="#0F172A", pad=15)
    
    ax.grid(axis="y", linestyle="--", alpha=0.5, color="#CBD5E1")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Legenda customizada
    handles, labels = ax.get_legend_handles_labels()
    mean_marker = plt.Line2D([0], [0], marker="D", color="w", markerfacecolor="#0F172A", markersize=8, label="Ticket Médio (R$)")
    handles.append(mean_marker)
    labels.append("Ticket Médio (R$)")
    
    ax.legend(handles=handles, labels=labels, loc="upper right", frameon=True,
              facecolor="#F8FAFC", edgecolor="#CBD5E1", fontsize=9.5)

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

    # Inverter para exibir o maior motivo no topo
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

    # 1. Gráfico de Dispersão
    fig_disp = plot_dispersion_chart(df_data, agg)
    fig_disp.savefig(OUTPUT_DISPERSION_PATH, dpi=300, bbox_inches="tight", facecolor="#FFFFFF")
    # Salvar também como legacy para manter compatibilidade
    fig_disp.savefig(OUTPUT_LEGACY_PATH, dpi=300, bbox_inches="tight", facecolor="#FFFFFF")
    plt.close(fig_disp)
    print(f"[SUCCESS] Gráfico de Dispersão de Motivos salvo em: {OUTPUT_DISPERSION_PATH}")

    # 2. Gráfico Separado de Perda Financeira
    fig_fin = plot_financial_loss_chart(agg)
    fig_fin.savefig(OUTPUT_FINANCIAL_PATH, dpi=300, bbox_inches="tight", facecolor="#FFFFFF")
    plt.close(fig_fin)
    print(f"[SUCCESS] Gráfico de Perda Financeira salvo em: {OUTPUT_FINANCIAL_PATH}")

if __name__ == "__main__":
    main()
