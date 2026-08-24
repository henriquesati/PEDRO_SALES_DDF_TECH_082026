"""
Gerador da visualização: Matriz Diagnóstica de Risco de Abandono e Segmentação RFM.
Atende à especificação de insights/02_risk/segmentacao_risco_abandono.md.
Paradigma funcional e declarativo com tipagem estrita (Type Annotations).
"""

from typing import Final
import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

BASE_DIR: Final[str] = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
OUTPUT_IMAGE_PATH: Final[str] = os.path.join(
    os.path.dirname(__file__), "chart_03_segmentacao_risco.png"
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
    """Carrega dados de carrinhos e cruza com clientes para obter segmentos RFM (Ground Truth)."""
    df_carts = pd.read_parquet(PARQUET_CARTS_PATH)
    df_clients = pd.read_parquet(PARQUET_CLIENTS_PATH)
    
    df_merged = df_carts.merge(
        df_clients[["cliente_id", "segmento_rfm", "lifetime_value"]],
        on="cliente_id",
        how="left"
    )
    df_merged["segmento_rfm"] = df_merged["segmento_rfm"].fillna("novo")
    return df_merged

def calculate_risk_scores(df: pd.DataFrame) -> pd.DataFrame:
    """Calcula o Score de Risco da Sessão com base nas variáveis do dataset."""
    score = np.zeros(len(df), dtype=int)
    
    # 1. Valor do carrinho (> 500 = +2, senão +1)
    score += np.where(df["valor_total"] > 500.0, 2, 1)
    
    # 2. Dispositivo (Mobile = +2, senão +1)
    score += np.where(df["dispositivo"] == "mobile", 2, 1)
    
    # 3. Cliente Novo (+2, senão +1)
    score += np.where(df["cliente_novo"] == True, 2, 1)
    
    # 4. Duração da Sessão (< 5 min = +2, senão +1)
    score += np.where(df["duracao_sessao_minutos"] < 5, 2, 1)
    
    # 5. Atrito detectado no motivo (+3 se frete/pagamento/estoque)
    motivos_criticos = {"frete", "pagamento", "estoque"}
    score += np.where(df["motivo_abandono"].isin(motivos_criticos), 3, 0)
    
    df["risk_score"] = score
    
    # Classificação em níveis
    conditions = [
        df["risk_score"] >= 8,
        (df["risk_score"] >= 6) & (df["risk_score"] < 8),
        (df["risk_score"] >= 4) & (df["risk_score"] < 6),
    ]
    choices = ["Crítico", "Alto", "Médio"]
    df["risk_level"] = np.select(conditions, choices, default="Baixo")
    
    return df

def prepare_matrix(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Prepara matriz para o heatmap e agregações por faixa de risco."""
    rfm_order = ["premium", "regular", "dormant", "novo"]
    risk_order = ["Crítico", "Alto", "Médio", "Baixo"]
    
    # Matriz de contagem
    pivot_count = pd.crosstab(df["risk_level"], df["segmento_rfm"]).reindex(
        index=risk_order, columns=rfm_order, fill_value=0
    )
    
    # Agregações por nível de risco
    df_risk_summary = df.groupby("risk_level").agg(
        total_carrinhos=("carrinho_id", "count"),
        carrinhos_abandonados=("status", lambda s: (s == "abandonado").sum()),
        receita_represada=("valor_total", lambda v: v[df.loc[v.index, "status"] == "abandonado"].sum())
    ).reindex(risk_order).reset_index()
    
    df_risk_summary["taxa_abandono_pct"] = (
        df_risk_summary["carrinhos_abandonados"] / df_risk_summary["total_carrinhos"]
    ) * 100
    df_risk_summary["pct_base"] = (
        df_risk_summary["total_carrinhos"] / len(df)
    ) * 100
    
    return pivot_count, df_risk_summary

def plot_risk_segmentation_chart(pivot_count: pd.DataFrame, df_summary: pd.DataFrame) -> plt.Figure:
    """Gera visualização executiva combinando Heatmap e Resumo de Risco."""
    plt.rcParams["font.sans-serif"] = ["Segoe UI", "DejaVu Sans", "Helvetica", "Arial", "sans-serif"]
    plt.rcParams["axes.edgecolor"] = "#CBD5E1"
    plt.rcParams["axes.linewidth"] = 1.1

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14.0, 6.8), gridspec_kw={"width_ratios": [1.1, 1.1]})
    fig.patch.set_facecolor("#FFFFFF")

    # --- PAINEL 1: Heatmap Matriz Risco x Segmento RFM ---
    ax1.set_facecolor("#FFFFFF")
    
    rfm_labels = ["Premium", "Regular", "Dormant", "Novo"]
    risk_labels = ["Crítico (Score ≥8)", "Alto (Score 6-7)", "Médio (Score 4-5)", "Baixo (Score <4)"]
    
    cmap = sns.light_palette("#E11D48", as_cmap=True)
    sns.heatmap(
        pivot_count,
        annot=True,
        fmt="d",
        cmap=cmap,
        cbar=True,
        ax=ax1,
        linewidths=1.2,
        linecolor="#FFFFFF",
        annot_kws={"fontsize": 11, "fontweight": "bold", "color": "#0F172A"}
    )
    
    ax1.set_xticklabels(rfm_labels, fontsize=11, fontweight="bold", color="#1E293B")
    ax1.set_yticklabels(risk_labels, fontsize=10.5, fontweight="bold", color="#1E293B", rotation=0)
    ax1.set_xlabel("Segmento de Clientes (RFM)", fontsize=11, fontweight="bold", color="#334155", labelpad=10)
    ax1.set_ylabel("Nível de Risco em Tempo de Sessão", fontsize=11, fontweight="bold", color="#334155", labelpad=10)
    ax1.set_title("Matriz de Risco: Vulnerabilidade por Segmento RFM", fontsize=13, fontweight="bold", color="#0F172A", pad=12)

    # --- PAINEL 2: Volume e Taxa Observada de Abandono por Nível de Risco ---
    ax2.set_facecolor("#FFFFFF")
    
    y_pos = np.arange(len(df_summary))
    y_pos_rev = y_pos[::-1]
    
    volumes = df_summary["total_carrinhos"].to_numpy()
    taxas = df_summary["taxa_abandono_pct"].to_numpy()
    receitas_k = df_summary["receita_represada"].to_numpy() / 1000.0
    pcts = df_summary["pct_base"].to_numpy()
    
    colors = ["#E11D48", "#F59E0B", "#2563EB", "#059669"]  # Crítico, Alto, Médio, Baixo
    
    bar_height = 0.55
    bars = ax2.barh(y_pos_rev, volumes, height=bar_height, color=colors, alpha=0.90, edgecolor="#334155")
    
    for i, (idx, vol, pct, taxa, rec) in enumerate(zip(y_pos_rev, volumes, pcts, taxas, receitas_k)):
        ax2.text(
            vol + 60, idx,
            f"{vol:,.0f} un ({pct:.1f}% base)\nTaxa Abandono: {taxa:.1f}% | R$ {rec:,.1f}k em risco",
            va="center", ha="left", fontsize=9.5, fontweight="bold", color="#0F172A"
        )

    ax2.set_yticks(y_pos_rev)
    ax2.set_yticklabels(df_summary["risk_level"], fontsize=11, fontweight="bold", color="#1E293B")
    ax2.set_xlabel("Volume Total de Carrinhos na Faixa (un)", fontsize=11, fontweight="bold", color="#334155")
    ax2.set_title("Distribuição de Volume & Efetividade da Triagem de Risco", fontsize=13, fontweight="bold", color="#0F172A", pad=12)
    ax2.set_xlim(0, max(volumes) * 1.45)
    ax2.grid(axis="x", linestyle="--", alpha=0.5, color="#CBD5E1")
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)

    # Título Geral
    fig.suptitle("DIAGNÓSTICO DE RISCO DE ABANDONO: MATRIZ RFM & TRIAGEM DE SESSÃO (DADOSFERA)",
                 fontsize=15, fontweight="bold", color="#0F172A", y=0.98)

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    return fig

def main() -> None:
    df_data = load_data()
    df_scored = calculate_risk_scores(df_data)
    pivot_count, df_summary = prepare_matrix(df_scored)
    fig = plot_risk_segmentation_chart(pivot_count, df_summary)
    
    os.makedirs(os.path.dirname(OUTPUT_IMAGE_PATH), exist_ok=True)
    fig.savefig(OUTPUT_IMAGE_PATH, dpi=300, bbox_inches="tight", facecolor="#FFFFFF")
    plt.close(fig)
    print(f"[SUCCESS] Gráfico de Segmentação de Risco salvo em: {OUTPUT_IMAGE_PATH}")

if __name__ == "__main__":
    main()
