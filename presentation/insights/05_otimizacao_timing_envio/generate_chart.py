"""
Gerador da visualização: Otimização de Timing de Envio e Curva de Decaimento (Decay Curve).
Atende à especificação de insights/03_prescriptive/otimizacao_timing_envio.md.
Paradigma funcional e declarativo com tipagem estrita (Type Annotations).
"""

from typing import Final
import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline

BASE_DIR: Final[str] = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
OUTPUT_IMAGE_PATH: Final[str] = os.path.join(
    os.path.dirname(__file__), "chart_05_otimizacao_timing_envio.png"
)

PARQUET_RESCUE_PATH: Final[str] = (
    os.path.join(BASE_DIR, "data", "mock", "output_cleaned", "parquet", "eventos_resgate.parquet")
    if os.path.exists(os.path.join(BASE_DIR, "data", "mock", "output_cleaned", "parquet", "eventos_resgate.parquet"))
    else os.path.join(BASE_DIR, "data", "mock", "output", "parquet", "eventos_resgate.parquet")
)

def load_data() -> pd.DataFrame:
    """Carrega dados de telemetria de disparos de resgate (Ground Truth)."""
    return pd.read_parquet(PARQUET_RESCUE_PATH)

def prepare_timing_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """Calcula taxas de abertura, cliques e conversões por régua de timing."""
    timing_order = ["lembrete_1h", "lembrete_24h", "desconto_48h", "urgencia_72h"]
    label_map = {
        "lembrete_1h": "Onda 1 (+1 hora)",
        "lembrete_24h": "Onda 2 (+24 horas)",
        "desconto_48h": "Onda 3 (+48 horas)",
        "urgencia_72h": "Onda 4 (+72 horas)"
    }
    hours_map = {
        "lembrete_1h": 1.0,
        "lembrete_24h": 24.0,
        "desconto_48h": 48.0,
        "urgencia_72h": 72.0
    }
    
    grouped = df.groupby("tipo_comunicacao").agg(
        total_envios=("resgate_id", "count"),
        total_aberturas=("data_abertura", lambda d: d.notna().sum()),
        total_cliques=("data_primeiro_clique", lambda d: d.notna().sum()),
        total_conversoes=("sucesso", lambda s: (s == True).sum())
    ).reindex(timing_order).reset_index()

    grouped["label"] = grouped["tipo_comunicacao"].map(label_map)
    grouped["horas"] = grouped["tipo_comunicacao"].map(hours_map)
    
    grouped["taxa_abertura"] = (grouped["total_aberturas"] / grouped["total_envios"]) * 100
    grouped["taxa_clique"] = (grouped["total_cliques"] / grouped["total_envios"]) * 100
    grouped["taxa_conversao"] = (grouped["total_conversoes"] / grouped["total_envios"]) * 100
    
    return grouped

def plot_decay_timing_chart(df_timing: pd.DataFrame) -> plt.Figure:
    """Gera visualização de Curva de Decaimento e Engajamento por Timing."""
    plt.rcParams["font.sans-serif"] = ["Segoe UI", "DejaVu Sans", "Helvetica", "Arial", "sans-serif"]
    plt.rcParams["axes.edgecolor"] = "#CBD5E1"
    plt.rcParams["axes.linewidth"] = 1.1

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14.0, 6.8), gridspec_kw={"width_ratios": [1.2, 1.0]})
    fig.patch.set_facecolor("#FFFFFF")

    # --- PAINEL 1: Curva de Decaimento de Conversão e Abertura ---
    ax1.set_facecolor("#FFFFFF")
    
    x_real = df_timing["horas"].to_numpy()
    y_open_real = df_timing["taxa_abertura"].to_numpy()
    y_conv_real = df_timing["taxa_conversao"].to_numpy()

    # Interpolação Spline Cúbica
    x_smooth = np.linspace(x_real.min(), x_real.max(), 200)
    spl_open = make_interp_spline(x_real, y_open_real, k=2)
    spl_conv = make_interp_spline(x_real, y_conv_real, k=2)
    
    y_open_smooth = np.maximum(0, spl_open(x_smooth))
    y_conv_smooth = np.maximum(0, spl_conv(x_smooth))

    # Plot das curvas
    ax1.plot(x_smooth, y_open_smooth, color="#2563EB", linewidth=2.5, label="Taxa de Abertura (%)")
    ax1.scatter(x_real, y_open_real, color="#1D4ED8", s=60, zorder=5, edgecolor="#FFFFFF", linewidth=1.5)
    
    ax1.fill_between(x_smooth, y_open_smooth, color="#2563EB", alpha=0.10)

    # Segundo eixo Y para Taxa de Conversão
    ax1_twin = ax1.twinx()
    ax1_twin.plot(x_smooth, y_conv_smooth, color="#059669", linewidth=2.8, linestyle="--", label="Taxa de Conversão (%)")
    ax1_twin.scatter(x_real, y_conv_real, color="#047857", s=70, zorder=5, edgecolor="#FFFFFF", linewidth=1.5)
    
    # Anotação do Ponto Ótimo (+1h)
    ax1_twin.annotate(
        "PONTO ÓTIMO DE DISPARO\n(+1h: Maior Abertura e Conversão)",
        xy=(1.0, y_conv_real[0]),
        xytext=(15, y_conv_real[0] * 0.90),
        arrowprops=dict(facecolor="#059669", shrink=0.08, width=1.5, headwidth=7),
        fontsize=9.5, fontweight="bold", color="#065F46",
        bbox=dict(boxstyle="round,pad=0.4", facecolor="#ECFDF5", edgecolor="#059669", alpha=0.95)
    )

    for h, op, cv in zip(x_real, y_open_real, y_conv_real):
        ax1.text(h, op + 1.2, f"{op:.1f}%", ha="center", fontsize=9, fontweight="bold", color="#1E40AF")
        ax1_twin.text(h, cv + 0.05, f"{cv:.2f}%", ha="center", fontsize=9, fontweight="bold", color="#065F46")

    ax1.set_xlabel("Latência Pós-Abandono (Horas)", fontsize=11, fontweight="bold", color="#334155")
    ax1.set_ylabel("Taxa de Abertura (%)", fontsize=11, fontweight="bold", color="#2563EB")
    ax1_twin.set_ylabel("Taxa de Conversão (%)", fontsize=11, fontweight="bold", color="#059669")
    ax1.set_title("Curva de Decaimento Temporal de Conversão (Decay Curve)", fontsize=13, fontweight="bold", color="#0F172A", pad=12)
    ax1.set_xticks([1, 12, 24, 36, 48, 60, 72])
    ax1.grid(True, linestyle="--", alpha=0.4, color="#CBD5E1")
    ax1.spines["top"].set_visible(False)
    ax1_twin.spines["top"].set_visible(False)

    # --- PAINEL 2: Volumetria de Envios & Sucessos Efetivos ---
    ax2.set_facecolor("#FFFFFF")
    
    y_pos = np.arange(len(df_timing))
    labels = df_timing["label"].to_list()
    envios = df_timing["total_envios"].to_numpy()
    conversoes = df_timing["total_conversoes"].to_numpy()
    
    bar_height = 0.50
    ax2.barh(y_pos, envios, height=bar_height, color="#94A3B8", alpha=0.7, label="Total de Envios", edgecolor="#475569")
    ax2.barh(y_pos, conversoes * 60, height=bar_height, color="#059669", alpha=0.9, label="Conversões (Escala ampliada)", edgecolor="#047857")

    for i, (env, conv) in enumerate(zip(envios, conversoes)):
        pct_conv_total = (conv / df_timing["total_conversoes"].sum()) * 100 if df_timing["total_conversoes"].sum() > 0 else 0
        ax2.text(
            env + 50, i,
            f"{env:,.0f} envios\n{conv} conv. ({pct_conv_total:.1f}% do total)",
            va="center", ha="left", fontsize=9.5, fontweight="bold", color="#0F172A"
        )

    ax2.set_yticks(y_pos)
    ax2.set_yticklabels(labels, fontsize=11, fontweight="bold", color="#1E293B")
    ax2.set_xlabel("Volume de Mensagens Enviadas (un)", fontsize=11, fontweight="bold", color="#334155")
    ax2.set_title("Volumetria por Régua & Concentração de Pedidos", fontsize=13, fontweight="bold", color="#0F172A", pad=12)
    ax2.set_xlim(0, max(envios) * 1.35)
    ax2.grid(axis="x", linestyle="--", alpha=0.5, color="#CBD5E1")
    ax2.legend(loc="lower right", frameon=True, facecolor="#F8FAFC", edgecolor="#CBD5E1", fontsize=9.5)
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)

    # Título Geral
    fig.suptitle("OTIMIZAÇÃO DE TIMING: CADÊNCIA DE DISPAROS & DECAIMENTO TEMPORAL (DADOSFERA)",
                 fontsize=15, fontweight="bold", color="#0F172A", y=0.98)

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    return fig

def main() -> None:
    df_rescue = load_data()
    df_timing = prepare_timing_metrics(df_rescue)
    fig = plot_decay_timing_chart(df_timing)
    
    os.makedirs(os.path.dirname(OUTPUT_IMAGE_PATH), exist_ok=True)
    fig.savefig(OUTPUT_IMAGE_PATH, dpi=300, bbox_inches="tight", facecolor="#FFFFFF")
    plt.close(fig)
    print(f"[SUCCESS] Gráfico de Otimização de Timing salvo em: {OUTPUT_IMAGE_PATH}")

if __name__ == "__main__":
    main()
