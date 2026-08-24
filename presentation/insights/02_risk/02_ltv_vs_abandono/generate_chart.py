"""
Gerador da visualização: LTV vs Abandono de Carrinho & Sensibilidade Financeira por Segmento RFM.
Atende estritamente à especificação de presentation/insights/02_risk/02_ltv_vs_abandono/spec.md
e insights/02_risk/ltv_vs_abandono.md.
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
    MODULE_DIR, "chart_02_ltv_vs_abandono.png"
)

PARQUET_CARTS_PATH: Final[str] = (
    os.path.join(BASE_DIR, "data", "mock", "output_cleaned", "parquet", "carrinhos.parquet")
    if os.path.exists(os.path.join(BASE_DIR, "data", "mock", "output_cleaned", "parquet", "carrinhos.parquet"))
    else os.path.join(BASE_DIR, "data", "mock", "output", "parquet", "carrinhos.parquet")
)

PARQUET_CLIENTS_PATH: Final[str] = (
    os.path.join(BASE_DIR, "data", "mock", "output_cleaned", "parquet", "clientes.parquet")
    if os.path.exists(os.path.join(BASE_DIR, "data", "mock", "output_cleaned", "parquet", "clientes.parquet"))
    else os.path.join(BASE_DIR, "data", "mock", "output", "parquet", "clientes.parquet")
)

def load_data() -> pd.DataFrame:
    """Carrega dados transacionais de carrinhos e clientes com enriquecimento de LTV e RFM."""
    df_carts = pd.read_parquet(PARQUET_CARTS_PATH)
    df_clients = pd.read_parquet(PARQUET_CLIENTS_PATH)
    
    df_merged = df_carts.merge(
        df_clients[["cliente_id", "segmento_rfm", "lifetime_value", "total_compras"]],
        on="cliente_id",
        how="left"
    )
    df_merged["segmento_rfm"] = df_merged["segmento_rfm"].fillna("novo")
    return df_merged

def calculate_ltv_abandonment_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """Calcula métricas agregadas de abandono, ticket médio e LTV histórico por segmento RFM."""
    order = ["premium", "regular", "novo", "dormant"]
    
    summary = df.groupby("segmento_rfm").agg(
        total_carrinhos=("carrinho_id", "count"),
        abandonados=("status", lambda s: (s == "abandonado").sum()),
        recuperados=("status", lambda s: (s == "recuperado").sum()),
        valor_abandonado=("valor_total", lambda v: v[df.loc[v.index, "status"] == "abandonado"].sum()),
        ticket_medio_carrinho=("valor_total", "mean"),
        ticket_medio_abandono=("valor_total", lambda v: v[df.loc[v.index, "status"] == "abandonado"].mean()),
        ltv_medio=("lifetime_value", "mean")
    ).reindex(order).reset_index()

    summary["taxa_abandono"] = (summary["abandonados"] / summary["total_carrinhos"]) * 100
    summary["taxa_recuperacao"] = (summary["recuperados"] / summary["abandonados"]) * 100
    summary["pct_valor_total"] = (summary["valor_abandonado"] / summary["valor_abandonado"].sum()) * 100

    return summary

def plot_ltv_vs_abandonment(df_summary: pd.DataFrame) -> plt.Figure:
    """Gera o painel duplo: Gráfico de Bolhas (LTV vs Abandono) + Matriz de Decisão Econômica."""
    plt.rcParams["font.sans-serif"] = ["Segoe UI", "DejaVu Sans", "Helvetica", "Arial", "sans-serif"]
    plt.rcParams["axes.edgecolor"] = "#CBD5E1"
    plt.rcParams["axes.linewidth"] = 1.1

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15.5, 7.2), gridspec_kw={"width_ratios": [1.15, 1.05]})
    fig.patch.set_facecolor("#FFFFFF")

    # Cores semânticas por segmento
    segment_colors = {
        "premium": "#059669",
        "regular": "#2563EB",
        "novo": "#F59E0B",
        "dormant": "#8B5CF6"
    }
    segment_labels = {
        "premium": "Premium (LTV Alto)",
        "regular": "Regular (Recorrente)",
        "novo": "Novo (1ª Compra)",
        "dormant": "Dormant (Inativo)"
    }

    # --- PAINEL 1: Gráfico de Bolhas (Taxa de Abandono vs Ticket Médio vs R$ em Risco) ---
    ax1.set_facecolor("#FFFFFF")

    x_vals = df_summary["taxa_abandono"].to_numpy()
    y_vals = df_summary["ticket_medio_abandono"].to_numpy()
    sizes = df_summary["valor_abandonado"].to_numpy() / 500.0  # Fator de escala visual proporcional
    colors = [segment_colors[s] for s in df_summary["segmento_rfm"]]

    for _, row in df_summary.iterrows():
        s = row["segmento_rfm"]
        x = row["taxa_abandono"]
        y = row["ticket_medio_abandono"]
        val_k = row["valor_abandonado"] / 1000.0
        ltv = row["ltv_medio"]
        sz = row["valor_abandonado"] / 420.0

        ax1.scatter(
            x, y, s=sz, color=segment_colors[s], alpha=0.82,
            edgecolor="#0F172A", linewidth=1.4, label=segment_labels[s], zorder=4
        )

        offset_y = 6 if s in ["regular", "dormant"] else -12
        ax1.annotate(
            f"{s.upper()}\nPerda: R$ {val_k:,.1f}k ({row['pct_valor_total']:.1f}%)\nLTV Médio: R$ {ltv:,.0f}",
            xy=(x, y),
            xytext=(x + 0.45, y + offset_y),
            fontsize=9.2, fontweight="bold", color="#0F172A",
            bbox=dict(boxstyle="round,pad=0.35", facecolor="#F8FAFC", edgecolor=segment_colors[s], alpha=0.92),
            arrowprops=dict(arrowstyle="->", color=segment_colors[s], lw=1.1),
            zorder=5
        )

    # Linha de benchmark de abandono
    ax1.axvline(69.8, color="#94A3B8", linestyle=":", linewidth=1.3, label="Benchmark Global Baymard (~69.8%)", zorder=2)

    ax1.set_xlabel("Taxa de Abandono de Carrinho por Segmento (%)", fontsize=11.5, fontweight="bold", color="#334155")
    ax1.set_ylabel("Ticket Médio do Carrinho Abandonado (R$)", fontsize=11.5, fontweight="bold", color="#334155")
    ax1.set_title("1. MATRIZ DE VALOR: ABANDONO × TICKET × R$ EM RISCO", fontsize=12.5, fontweight="bold", color="#0F172A", pad=12)
    ax1.set_xlim(50.0, 72.0)
    ax1.set_ylim(320.0, 420.0)
    ax1.grid(True, linestyle="--", alpha=0.4, color="#CBD5E1")
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax1.legend(loc="lower left", frameon=True, facecolor="#F8FAFC", edgecolor="#CBD5E1", fontsize=9.0)

    # --- PAINEL 2: Matriz de Decisão Financeira & Canais Ótimos ---
    ax2.set_facecolor("#FFFFFF")
    ax2.axis("off")

    table_data = [
        ["Segmento", "LTV Médio Histórico", "Canal de Resgate", "Custo Envio", "Teto Desconto", "Expected ROI"],
        ["PREMIUM", "R$ 8.823", "WhatsApp VIP", "R$ 0,30", "0% (Zero Cupom)", "480x (R$ 144/R$)"],
        ["REGULAR", "R$ 1.242", "Email + Push", "R$ 0,07", "5% (Se > R$ 200)", "85x (R$ 25/R$)"],
        ["NOVO", "R$ 0 (1ª Compra)", "Email Inbound", "R$ 0,05", "10% Boas-Vindas", "280x (LTV Futuro)"],
        ["DORMANT", "R$ 283", "Push / Email", "R$ 0,02", "10% Condicionado", "35x (Reativação)"]
    ]

    table = ax2.table(
        cellText=table_data,
        cellLoc="center",
        loc="center",
        bbox=[0.0, 0.16, 1.0, 0.74]
    )
    table.auto_set_font_size(False)
    table.set_fontsize(9.2)

    for (row, col), cell in table.get_celld().items():
        cell.set_edgecolor("#CBD5E1")
        cell.set_linewidth(1.1)
        if row == 0:
            cell.set_facecolor("#0F172A")
            cell.set_text_props(weight="bold", color="#FFFFFF")
            cell.set_height(0.12)
        else:
            if row == 1:
                cell.set_facecolor("#ECFDF5")  # Verde Premium
            elif row == 2:
                cell.set_facecolor("#EFF6FF")  # Azul Regular
            elif row == 3:
                cell.set_facecolor("#FEF3C7")  # Âmbar Novo
            else:
                cell.set_facecolor("#F3E8FF")  # Roxo Dormant
            cell.set_text_props(weight="bold" if col in [0, 5] else "normal", color="#0F172A")
            cell.set_height(0.14)

    # Nota explicativa de governança
    note_text = (
        "PRINCÍPIO DE GOVERNANÇA ECONÔMICA (PRESERVAÇÃO DE MARGEM):\n"
        "• Clientes Premium justificam WhatsApp (R$ 0,30), pois o envio custa apenas 0,08% do ticket.\n"
        "• Proibido queimar margem dando cupom a quem já é fiel (Premium). Cupons são alocados\n"
        "  estrategicamente para Novos (aquisição de LTV) e Regulares (carrinhos acima de R$ 200)."
    )
    bbox_props = dict(boxstyle="round,pad=0.5", facecolor="#F8FAFC", edgecolor="#94A3B8", linewidth=1.1)
    ax2.text(0.0, 0.02, note_text, fontsize=8.5, color="#1E293B", va="bottom", bbox=bbox_props, transform=ax2.transAxes, family="monospace")

    ax2.set_title("2. MATRIZ DE SENSIBILIDADE ECONÔMICA & CANAL ÓTIMO", fontsize=12.5, fontweight="bold", color="#0F172A", pad=12)

    fig.suptitle("ANÁLISE DE LIFETIME VALUE (LTV) × ABANDONO: SENSIBILIDADE FINANCEIRA & ALOCAÇÃO DE CANAIS",
                 fontsize=14.5, fontweight="bold", color="#0F172A", y=0.98)

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    return fig

def main() -> None:
    df_data = load_data()
    df_summary = calculate_ltv_abandonment_metrics(df_data)
    
    fig = plot_ltv_vs_abandonment(df_summary)
    os.makedirs(MODULE_DIR, exist_ok=True)
    fig.savefig(OUTPUT_IMAGE_PATH, dpi=300, bbox_inches="tight", facecolor="#FFFFFF")
    plt.close(fig)
    print(f"[SUCCESS] Gráfico de LTV vs Abandono salvo em: {OUTPUT_IMAGE_PATH}")

if __name__ == "__main__":
    main()
