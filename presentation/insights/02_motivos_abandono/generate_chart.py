"""
Gerador da visualização: Decomposição Descritiva de Motivos de Abandono e Impacto Financeiro.
Atende à especificação de insights/01_descriptive/motivos_abandono.md.
Paradigma funcional e declarativo com tipagem estrita (Type Annotations).
"""

from typing import Final
import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR: Final[str] = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
OUTPUT_IMAGE_PATH: Final[str] = os.path.join(
    os.path.dirname(__file__), "chart_02_motivos_abandono.png"
)

PARQUET_CARTS_PATH: Final[str] = (
    os.path.join(BASE_DIR, "data", "mock", "output_cleaned", "parquet", "carrinhos.parquet")
    if os.path.exists(os.path.join(BASE_DIR, "data", "mock", "output_cleaned", "parquet", "carrinhos.parquet"))
    else os.path.join(BASE_DIR, "data", "mock", "output", "parquet", "carrinhos.parquet")
)

def load_data() -> pd.DataFrame:
    """Carrega carrinhos abandonados com motivos preenchidos (Ground Truth)."""
    df = pd.read_parquet(PARQUET_CARTS_PATH)
    df_aband = df[df["motivo_abandono"].notna() & (df["motivo_abandono"] != "")].copy()
    return df_aband

def prepare_metrics(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Calcula agregados por motivo e quebra por dispositivo."""
    label_map = {
        "preco": "Preço Alto",
        "frete": "Frete Caro",
        "indecisao": "Indecisão / Comparação",
        "pagamento": "Erro no Pagamento",
        "nao_informado": "Não Informado",
        "estoque": "Estoque Indisponível"
    }
    
    df["motivo_label"] = df["motivo_abandono"].map(label_map).fillna(df["motivo_abandono"])
    
    # 1. Agregação Geral por Motivo
    df_motivo = df.groupby("motivo_label").agg(
        volume=("carrinho_id", "count"),
        receita_represada=("valor_total", "sum"),
        ticket_medio=("valor_total", "mean")
    ).reset_index()
    
    total_vol = df_motivo["volume"].sum()
    df_motivo["pct_total"] = (df_motivo["volume"] / total_vol) * 100
    df_motivo = df_motivo.sort_values(by="volume", ascending=True).reset_index(drop=True)
    
    # 2. Decomposição por Dispositivo
    df_dev = (
        pd.crosstab(df["motivo_label"], df["dispositivo"], normalize="index") * 100
    ).loc[df_motivo["motivo_label"]].reset_index()
    
    return df_motivo, df_dev

def plot_motivos_chart(df_motivo: pd.DataFrame, df_dev: pd.DataFrame) -> plt.Figure:
    """Gera o painel duplo executivo em 300 DPI com fundo branco."""
    plt.rcParams["font.sans-serif"] = ["Segoe UI", "DejaVu Sans", "Helvetica", "Arial", "sans-serif"]
    plt.rcParams["axes.edgecolor"] = "#CBD5E1"
    plt.rcParams["axes.linewidth"] = 1.1

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14.0, 6.8), gridspec_kw={"width_ratios": [1.25, 1.0]})
    fig.patch.set_facecolor("#FFFFFF")

    y_pos = np.arange(len(df_motivo))
    motivos = df_motivo["motivo_label"].to_list()
    volumes = df_motivo["volume"].to_numpy()
    pcts = df_motivo["pct_total"].to_numpy()
    receitas_k = df_motivo["receita_represada"].to_numpy() / 1000.0
    tickets = df_motivo["ticket_medio"].to_numpy()

    # --- PAINEL 1: Volume & Distribuição por Dispositivo ---
    ax1.set_facecolor("#FFFFFF")
    
    # Proporções de dispositivos
    mob_pct = df_dev["mobile"].to_numpy() / 100.0 * volumes
    desk_pct = df_dev["desktop"].to_numpy() / 100.0 * volumes
    tab_pct = df_dev["tablet"].to_numpy() / 100.0 * volumes

    bar_height = 0.55
    ax1.barh(y_pos, mob_pct, height=bar_height, color="#2563EB", label="Mobile", alpha=0.90, edgecolor="#1D4ED8")
    ax1.barh(y_pos, desk_pct, height=bar_height, left=mob_pct, color="#059669", label="Desktop", alpha=0.90, edgecolor="#047857")
    ax1.barh(y_pos, tab_pct, height=bar_height, left=mob_pct + desk_pct, color="#F59E0B", label="Tablet", alpha=0.90, edgecolor="#D97706")

    for i, (vol, pct) in enumerate(zip(volumes, pcts)):
        ax1.text(vol + 25, i, f"{vol:,.0f} un ({pct:.1f}%)", va="center", ha="left",
                 fontsize=10, fontweight="bold", color="#0F172A")

    ax1.set_yticks(y_pos)
    ax1.set_yticklabels(motivos, fontsize=11, fontweight="bold", color="#1E293B")
    ax1.set_xlabel("Volume de Carrinhos Abandonados (un)", fontsize=11, fontweight="bold", color="#334155")
    ax1.set_title("Decomposição de Volume por Causa-Raiz & Dispositivo", fontsize=13, fontweight="bold", color="#0F172A", pad=12)
    ax1.set_xlim(0, max(volumes) * 1.25)
    ax1.grid(axis="x", linestyle="--", alpha=0.5, color="#CBD5E1")
    ax1.legend(loc="lower right", frameon=True, facecolor="#F8FAFC", edgecolor="#CBD5E1", fontsize=9.5)
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)

    # --- PAINEL 2: Impacto Financeiro Represado (R$) ---
    ax2.set_facecolor("#FFFFFF")
    colors_rec = ["#E2E8F0", "#E2E8F0", "#CBD5E1", "#94A3B8", "#F43F5E", "#E11D48"]
    bars2 = ax2.barh(y_pos, receitas_k, height=bar_height, color="#E11D48", alpha=0.85, edgecolor="#BE123C")

    for i, (rec, tkt) in enumerate(zip(receitas_k, tickets)):
        ax2.text(rec + 10, i, f"R$ {rec:,.1f}k\n(TM: R$ {tkt:,.0f})", va="center", ha="left",
                 fontsize=9.5, fontweight="bold", color="#0F172A")

    ax2.set_yticks(y_pos)
    ax2.set_yticklabels([])
    ax2.set_xlabel("Receita Represada em Abandono (R$ Milhares)", fontsize=11, fontweight="bold", color="#334155")
    ax2.set_title("Perda Financeira Represada por Motivo (R$)", fontsize=13, fontweight="bold", color="#0F172A", pad=12)
    ax2.set_xlim(0, max(receitas_k) * 1.30)
    ax2.grid(axis="x", linestyle="--", alpha=0.5, color="#CBD5E1")
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)

    # Título Geral
    fig.suptitle("ANÁLISE DESCRITIVA: CAUSAS-RAIZ DE ABANDONO & IMPACTO FINANCEIRO (DADOSFERA)",
                 fontsize=15, fontweight="bold", color="#0F172A", y=0.98)
    
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    return fig

def main() -> None:
    df_data = load_data()
    df_motivo, df_dev = prepare_metrics(df_data)
    fig = plot_motivos_chart(df_motivo, df_dev)
    
    os.makedirs(os.path.dirname(OUTPUT_IMAGE_PATH), exist_ok=True)
    fig.savefig(OUTPUT_IMAGE_PATH, dpi=300, bbox_inches="tight", facecolor="#FFFFFF")
    plt.close(fig)
    print(f"[SUCCESS] Gráfico de Motivos de Abandono salvo em: {OUTPUT_IMAGE_PATH}")

if __name__ == "__main__":
    main()
