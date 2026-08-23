"""
Gerador da visualização: Matriz de Causas-Raiz de Abandono por Segmento RFM.
Paradigma funcional e declarativo com tipagem estrita (Type Annotations).
"""

from typing import Final
import os
import sys
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

BASE_DIR: Final[str] = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
PITCH_DIR: Final[str] = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PITCH_DIR not in sys.path:
    sys.path.insert(0, PITCH_DIR)

from config.chart_theme import apply_dadosfera_theme, save_chart_artifact, DADOSFERA_PALETTE

OUTPUT_IMAGE_PATH: Final[str] = os.path.join(
    os.path.dirname(__file__), "chart_04_matriz_motivos_rfm_heatmap.png"
)
PARQUET_CARTS_PATH: Final[str] = os.path.join(BASE_DIR, "data", "mock", "output", "parquet", "carrinhos.parquet")
PARQUET_CLIENTS_PATH: Final[str] = os.path.join(BASE_DIR, "data", "mock", "output", "parquet", "clientes.parquet")

def load_rfm_motivos_data() -> pd.DataFrame:
    """Carrega dados de carrinhos abandonados com segmento RFM dos clientes."""
    df_carts = pd.read_parquet(PARQUET_CARTS_PATH)
    df_clients = pd.read_parquet(PARQUET_CLIENTS_PATH)
    
    abandoned = df_carts[df_carts["status"] == "abandonado"]
    merged = abandoned.merge(df_clients[["cliente_id", "segmento_rfm"]], on="cliente_id", how="inner")
    return merged

def prepare_crosstab_matrix(df_data: pd.DataFrame) -> pd.DataFrame:
    """Gera matriz de contingência normalizada por segmento RFM (% dentro de cada perfil)."""
    crosstab = pd.crosstab(
        df_data["segmento_rfm"], 
        df_data["motivo_abandono"], 
        normalize="index"
    ) * 100
    
    # Ordenação lógica dos perfis
    ordered_rfm = ["premium", "regular", "novo", "dormant"]
    ordered_rfm = [r for r in ordered_rfm if r in crosstab.index]
    return crosstab.reindex(ordered_rfm)

def plot_heatmap(df_matrix: pd.DataFrame) -> plt.Figure:
    """Plota heatmap sofisticado da distribuição de motivos por segmento."""
    apply_dadosfera_theme()
    
    fig, ax = plt.subplots(figsize=(12.0, 6.8))
    
    cmap = sns.color_palette("Blues", as_cmap=True)
    
    sns.heatmap(
        df_matrix, 
        annot=True, 
        fmt=".1f", 
        cmap=cmap, 
        cbar_kws={"label": "Incidência Percentual no Segmento (%)"},
        linewidths=1.5, 
        linecolor=DADOSFERA_PALETTE.primary_dark,
        ax=ax,
        annot_kws={"size": 12, "weight": "bold", "color": "#FFFFFF"}
    )
    
    ax.set_title("Matriz Diagnóstica: Causas-Raiz de Abandono por Segmento RFM", fontsize=15, fontweight="bold", pad=15)
    ax.set_xlabel("Motivo Diagnosticado do Abandono", fontsize=12, fontweight="bold", color=DADOSFERA_PALETTE.text_light)
    ax.set_ylabel("Segmento RFM do Cliente", fontsize=12, fontweight="bold", color=DADOSFERA_PALETTE.text_light)
    ax.set_xticklabels([c.upper() for c in df_matrix.columns], fontsize=11, fontweight="bold")
    ax.set_yticklabels([r.upper() for r in df_matrix.index], fontsize=11, fontweight="bold", rotation=0)
    
    return fig

def main() -> None:
    df_data = load_rfm_motivos_data()
    df_matrix = prepare_crosstab_matrix(df_data)
    fig = plot_heatmap(df_matrix)
    saved_path = save_chart_artifact(fig, OUTPUT_IMAGE_PATH)
    print(f"[SUCCESS] Gráfico gerado em: {saved_path}")

if __name__ == "__main__":
    main()
