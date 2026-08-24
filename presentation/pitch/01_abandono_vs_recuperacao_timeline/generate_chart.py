"""
Gerador da visualização: Série Temporal de Abandono vs Recuperação.
Paradigma funcional e declarativo com tipagem estrita (Type Annotations).
"""

from typing import Final
import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Adiciona o diretório raiz ao sys.path para importações relativas
BASE_DIR: Final[str] = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
PITCH_DIR: Final[str] = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PITCH_DIR not in sys.path:
    sys.path.insert(0, PITCH_DIR)

from config.chart_theme import apply_dadosfera_theme, save_chart_artifact, DADOSFERA_PALETTE

OUTPUT_IMAGE_PATH: Final[str] = os.path.join(
    os.path.dirname(__file__), "chart_01_serie_temporal_abandono_resgate.png"
)
PARQUET_CARTS_PATH: Final[str] = (
    os.path.join(BASE_DIR, "data", "mock", "output_cleaned", "parquet", "carrinhos.parquet")
    if os.path.exists(os.path.join(BASE_DIR, "data", "mock", "output_cleaned", "parquet", "carrinhos.parquet"))
    else os.path.join(BASE_DIR, "data", "mock", "output", "parquet", "carrinhos.parquet")
)
PARQUET_RESGATE_PATH: Final[str] = (
    os.path.join(BASE_DIR, "data", "mock", "output_cleaned", "parquet", "eventos_resgate.parquet")
    if os.path.exists(os.path.join(BASE_DIR, "data", "mock", "output_cleaned", "parquet", "eventos_resgate.parquet"))
    else os.path.join(BASE_DIR, "data", "mock", "output", "parquet", "eventos_resgate.parquet")
)

def load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Carrega dados das entidades carrinhos e eventos_resgate (fonte limpa)."""
    df_carts = pd.read_parquet(PARQUET_CARTS_PATH)
    df_resgate = pd.read_parquet(PARQUET_RESGATE_PATH)
    return df_carts, df_resgate

def prepare_time_series(df_carts: pd.DataFrame, df_resgate: pd.DataFrame) -> pd.DataFrame:
    """Prepara série temporal semanal agregando abandono e conversões de resgate."""
    df_c = df_carts.assign(
        data_criacao=pd.to_datetime(df_carts["data_criacao"]),
        is_abandoned=(df_carts["status"] == "abandonado").astype(int)
    )
    df_c = df_c.set_index("data_criacao")
    weekly_carts = df_c.resample("W").agg(
        total_carrinhos=("carrinho_id", "count"),
        abandonados=("is_abandoned", "sum")
    )
    
    df_r = df_resgate.assign(
        data_envio=pd.to_datetime(df_resgate["data_envio"]),
        is_recuperado=(df_resgate["sucesso"] == True).astype(int)
    ).set_index("data_envio")
    weekly_resgate = df_r.resample("W").agg(
        disparos=("resgate_id", "count"),
        recuperados=("is_recuperado", "sum")
    )
    
    df_merged = weekly_carts.join(weekly_resgate, how="outer").fillna(0)
    
    # Cálculos puros de taxas em %
    df_ts = df_merged.assign(
        taxa_abandono=(df_merged["abandonados"] / df_merged["total_carrinhos"].replace(0, 1)) * 100,
        taxa_recuperacao=(df_merged["recuperados"] / df_merged["abandonados"].replace(0, 1)) * 100
    )
    return df_ts

def plot_time_series(df_ts: pd.DataFrame) -> plt.Figure:
    """Gera o gráfico estilizado em alta definição."""
    apply_dadosfera_theme()
    
    fig, ax1 = plt.subplots(figsize=(12.0, 6.5))
    
    # Eixo 1: Taxas em %
    ax1.plot(
        df_ts.index, df_ts["taxa_abandono"], 
        color=DADOSFERA_PALETTE.accent_coral, 
        linewidth=2.8, 
        marker="o", 
        markersize=6, 
        label="Taxa de Abandono (Target ~69.7%)"
    )
    ax1.plot(
        df_ts.index, df_ts["taxa_recuperacao"], 
        color=DADOSFERA_PALETTE.accent_green, 
        linewidth=2.8, 
        marker="s", 
        markersize=6, 
        label="Taxa de Recuperação (Target ~10.1%)"
    )
    
    ax1.set_ylabel("Taxa Percentual (%)", color=DADOSFERA_PALETTE.text_light, fontsize=12, fontweight="bold")
    ax1.set_ylim(0, 100)
    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%b/%y"))
    ax1.xaxis.set_major_locator(mdates.MonthLocator())
    
    # Linha de benchmark global
    ax1.axhline(69.8, color=DADOSFERA_PALETTE.accent_yellow, linestyle=":", alpha=0.8, label="Benchmark Global Baymard (69.8%)")
    
    # Eixo 2: Volume Absoluto de Carrinhos
    ax2 = ax1.twinx()
    ax2.bar(
        df_ts.index, df_ts["abandonados"], 
        width=4, alpha=0.25, 
        color=DADOSFERA_PALETTE.accent_blue, 
        label="Volume Abandonado (Semanal)"
    )
    ax2.set_ylabel("Volume de Carrinhos", color=DADOSFERA_PALETTE.accent_cyan, fontsize=11)
    ax2.grid(False)
    
    plt.title("Evolução Temporal: Abandono vs Recuperação de Carrinhos (Jan–Jun 2026)", fontsize=15, fontweight="bold", pad=15)
    
    # Combina legendas
    lines_1, labels_1 = ax1.get_legend_handles_labels()
    lines_2, labels_2 = ax2.get_legend_handles_labels()
    ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc="upper left", framealpha=0.9)
    
    return fig

def main() -> None:
    df_carts, df_resgate = load_data()
    df_ts = prepare_time_series(df_carts, df_resgate)
    fig = plot_time_series(df_ts)
    saved_path = save_chart_artifact(fig, OUTPUT_IMAGE_PATH)
    print(f"[SUCCESS] Gráfico gerado em: {saved_path}")

if __name__ == "__main__":
    main()
