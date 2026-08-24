"""
Gerador da visualização: Matriz Prescritiva de Viabilidade de Recuperação.
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
    os.path.dirname(__file__), "chart_05_dispersao_viabilidade_recuperacao.png"
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

def load_viability_data() -> pd.DataFrame:
    """Carrega dados de carrinhos e calcula score heurístico de viabilidade (fonte limpa)."""
    df_carts = pd.read_parquet(PARQUET_CARTS_PATH)
    df_clients = pd.read_parquet(PARQUET_CLIENTS_PATH)
    
    abandoned = df_carts[df_carts["status"] == "abandonado"].copy()
    merged = abandoned.merge(df_clients[["cliente_id", "segmento_rfm"]], on="cliente_id", how="inner")
    
    # Heurística prescritiva de probabilidade baseada no segmento e motivo
    prob_rfm = {"premium": 0.35, "regular": 0.22, "novo": 0.18, "dormant": 0.08}
    prob_motivo = {"indecisao": 0.12, "frete": 0.08, "pagamento": 0.05, "preco": 0.02, "estoque": -0.05}
    
    np.random.seed(42)
    noise = np.random.uniform(-0.04, 0.04, size=len(merged))
    
    base_p = merged["segmento_rfm"].map(prob_rfm).fillna(0.15)
    motivo_p = merged["motivo_abandono"].map(prob_motivo).fillna(0.0)
    
    merged["prob_recuperacao_pct"] = ((base_p + motivo_p + noise).clip(0.02, 0.75)) * 100
    
    # Classificação de Viabilidade
    def classify(row) -> str:
        p = row["prob_recuperacao_pct"]
        v = row["valor_total"]
        if p >= 25.0 and v >= 300.0:
            return "ALTA"
        elif p >= 15.0 or v >= 200.0:
            return "MEDIA"
        return "BAIXA"
        
    merged["viabilidade"] = merged.apply(classify, axis=1)
    return merged

def plot_viability_scatter(df_data: pd.DataFrame) -> plt.Figure:
    """Plota gráfico de dispersão com quadrantes prescritivos de ação."""
    apply_dadosfera_theme()
    
    fig, ax = plt.subplots(figsize=(12.0, 6.8))
    
    # Sample de pontos para visualização limpa
    sample_df = df_data.sample(n=min(800, len(df_data)), random_state=42)
    
    colors = {
        "ALTA": DADOSFERA_PALETTE.accent_green,
        "MEDIA": DADOSFERA_PALETTE.accent_yellow,
        "BAIXA": DADOSFERA_PALETTE.accent_coral
    }
    
    for viab, color in colors.items():
        subset = sample_df[sample_df["viabilidade"] == viab]
        ax.scatter(
            subset["prob_recuperacao_pct"], subset["valor_total"],
            c=color, label=f"Viabilidade {viab}",
            alpha=0.65, edgecolors="none", s=45
        )
    
    # Linhas de quadrante
    ax.axvline(25.0, color=DADOSFERA_PALETTE.border_color, linestyle="--", alpha=0.7)
    ax.axhline(300.0, color=DADOSFERA_PALETTE.border_color, linestyle="--", alpha=0.7)
    
    # Textos dos quadrantes
    ax.text(50, 1100, "[RESGATE PRIORITARIO]\n(Alto Valor + Alta Conversao)", color=DADOSFERA_PALETTE.accent_green, fontsize=10, fontweight="bold", ha="center")
    ax.text(10, 1100, "[ATENCAO / AQUECER]\n(Alto Valor + Frio)", color=DADOSFERA_PALETTE.accent_yellow, fontsize=10, fontweight="bold", ha="center")
    ax.text(50, 50, "[AUTOMACAO LEVE]\n(Baixo Ticket + Alto Engajamento)", color=DADOSFERA_PALETTE.accent_cyan, fontsize=10, fontweight="bold", ha="center")
    
    ax.set_title("Matriz de Decisão Prescritiva: Probabilidade de Resgate vs Valor do Carrinho", fontsize=15, fontweight="bold", pad=15)
    ax.set_xlabel("Probabilidade Estimada de Recuperação (%)", fontsize=12, fontweight="bold", color=DADOSFERA_PALETTE.text_light)
    ax.set_ylabel("Valor Total do Carrinho (R$)", fontsize=12, fontweight="bold", color=DADOSFERA_PALETTE.text_light)
    ax.set_ylim(0, 1400)
    ax.set_xlim(0, 80)
    
    ax.legend(loc="upper right", framealpha=0.95)
    ax.grid(True, linestyle="--", alpha=0.3)
    
    return fig

def main() -> None:
    df_data = load_viability_data()
    fig = plot_viability_scatter(df_data)
    saved_path = save_chart_artifact(fig, OUTPUT_IMAGE_PATH)
    print(f"[SUCCESS] Gráfico gerado em: {saved_path}")

if __name__ == "__main__":
    main()
