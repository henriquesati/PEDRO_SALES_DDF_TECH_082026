"""
Gerador da visualização: Eficiência Financeira e ROI por Canal de Resgate.
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
    os.path.dirname(__file__), "chart_03_roi_eficiencia_canais.png"
)
PARQUET_RESGATE_PATH: Final[str] = (
    os.path.join(BASE_DIR, "data", "mock", "output_cleaned", "parquet", "eventos_resgate.parquet")
    if os.path.exists(os.path.join(BASE_DIR, "data", "mock", "output_cleaned", "parquet", "eventos_resgate.parquet"))
    else os.path.join(BASE_DIR, "data", "mock", "output", "parquet", "eventos_resgate.parquet")
)

def load_resgate_data() -> pd.DataFrame:
    """Carrega dados de eventos de resgate com telemetria financeira (fonte limpa)."""
    return pd.read_parquet(PARQUET_RESGATE_PATH)

def calculate_channel_metrics(df_resgate: pd.DataFrame) -> pd.DataFrame:
    """Calcula agregados de custo, receita recuperada, conversões e ROI multiplicador."""
    grouped = df_resgate.groupby("canal").agg(
        total_envios=("resgate_id", "count"),
        conversoes=("sucesso", lambda s: (s == True).sum()),
        custo_total=("custo_envio", "sum"),
        receita_recuperada=("valor_pedido_final", lambda v: v.fillna(0).sum()),
        desconto_total=("desconto_oferecido", lambda d: d.fillna(0).sum())
    ).reset_index()
    
    # Cálculo puro de métricas
    metrics = grouped.assign(
        taxa_conversao=(grouped["conversoes"] / grouped["total_envios"]) * 100,
        receita_liquida=grouped["receita_recuperada"] - grouped["desconto_total"] - grouped["custo_total"],
        roi_multiplicador=lambda df: (df["receita_liquida"] / df["custo_total"].replace(0, 1)).clip(lower=0)
    ).sort_values(by="roi_multiplicador", ascending=False)
    
    return metrics

def plot_channel_efficiency(df_metrics: pd.DataFrame) -> plt.Figure:
    """Plota combo chart de conversões vs ROI multiplicador por canal."""
    apply_dadosfera_theme()
    
    fig, ax1 = plt.subplots(figsize=(12.0, 6.8))
    
    x = np.arange(len(df_metrics))
    width = 0.35
    
    # Barras de taxa de conversão (%)
    bars1 = ax1.bar(
        x - width/2, df_metrics["taxa_conversao"], 
        width=width, color=DADOSFERA_PALETTE.accent_blue, 
        label="Taxa de Conversão do Canal (%)", alpha=0.9
    )
    
    ax1.set_ylabel("Taxa de Conversão (%)", color=DADOSFERA_PALETTE.accent_blue, fontsize=12, fontweight="bold")
    ax1.set_xticks(x)
    ax1.set_xticklabels([c.upper() for c in df_metrics["canal"]], fontsize=11, fontweight="bold")
    ax1.set_ylim(0, max(df_metrics["taxa_conversao"]) * 1.35)
    
    # Eixo 2: ROI Multiplicador
    ax2 = ax1.twinx()
    bars2 = ax2.bar(
        x + width/2, df_metrics["roi_multiplicador"], 
        width=width, color=DADOSFERA_PALETTE.accent_green, 
        label="ROI Multiplicador (Retorno Líquido / Custo)", alpha=0.9
    )
    ax2.set_ylabel("Múltiplo de ROI (ex: 45x)", color=DADOSFERA_PALETTE.accent_green, fontsize=12, fontweight="bold")
    max_roi = float(df_metrics["roi_multiplicador"].max())
    ax2.set_ylim(0.0, max(max_roi * 1.3, 10.0))
    ax2.grid(False)
    
    plt.title("Eficiência de Canais: Taxa de Conversão (%) vs ROI Multiplicador", fontsize=15, fontweight="bold", pad=15)
    
    # Anotações nas barras de ROI
    for i, (_, row) in enumerate(df_metrics.iterrows()):
        roi_val = row["roi_multiplicador"]
        conv_val = row["taxa_conversao"]
        ax2.text(
            i + width/2, roi_val + 1.2, f"{roi_val:.1f}x", 
            ha="center", va="bottom", 
            color=DADOSFERA_PALETTE.accent_green, fontsize=10, fontweight="bold"
        )
        ax1.text(
            i - width/2, conv_val + 0.3, f"{conv_val:.1f}%", 
            ha="center", va="bottom", 
            color=DADOSFERA_PALETTE.accent_cyan, fontsize=10, fontweight="bold"
        )
    
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper right", framealpha=0.95)
    
    return fig

def main() -> None:
    df_resgate = load_resgate_data()
    df_metrics = calculate_channel_metrics(df_resgate)
    fig = plot_channel_efficiency(df_metrics)
    saved_path = save_chart_artifact(fig, OUTPUT_IMAGE_PATH)
    print(f"[SUCCESS] Gráfico gerado em: {saved_path}")

if __name__ == "__main__":
    main()
