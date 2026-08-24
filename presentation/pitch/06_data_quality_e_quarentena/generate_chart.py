"""
Gerador da visualização: Scorecard de Data Quality e Quarentena Dual-Artifact.
Paradigma funcional e declarativo com tipagem estrita (Type Annotations).
"""

from typing import Final
import os
import sys
import numpy as np
import matplotlib.pyplot as plt

BASE_DIR: Final[str] = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
PITCH_DIR: Final[str] = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PITCH_DIR not in sys.path:
    sys.path.insert(0, PITCH_DIR)

from config.chart_theme import apply_dadosfera_theme, save_chart_artifact, DADOSFERA_PALETTE

OUTPUT_IMAGE_PATH: Final[str] = os.path.join(
    os.path.dirname(__file__), "chart_06_scorecard_data_quality.png"
)

def plot_data_quality_scorecard() -> plt.Figure:
    """Gera visualização de scorecard de conformidade e quarentena de anomalias Silver."""
    apply_dadosfera_theme()
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.0, 6.5), gridspec_kw={"width_ratios": [1, 1.2]})
    
    # Gráfico 1: Rosca de Conformidade Global
    sizes = [94.2, 5.8]
    colors = [DADOSFERA_PALETTE.accent_green, DADOSFERA_PALETTE.accent_coral]
    labels = ["Camada Qualify\n(Aprovados: 94.2%)", "Quarentena Anomalies\n(Anomalias: 5.8%)"]
    
    wedges, texts, autotexts = ax1.pie(
        sizes, 
        labels=labels, 
        autopct="%1.1f%%", 
        startangle=140, 
        colors=colors, 
        wedgeprops=dict(width=0.4, edgecolor=DADOSFERA_PALETTE.primary_dark, linewidth=2),
        textprops=dict(color=DADOSFERA_PALETTE.text_light, fontsize=10, weight="bold")
    )
    for at in autotexts:
        at.set_color("#FFFFFF")
        at.set_fontsize(11)
        at.set_weight("bold")
        
    ax1.set_title("Conformidade Global (Item 4)\nSuíte Great Expectations (18 Regras)", fontsize=13, fontweight="bold", pad=10)
    
    # Gráfico 2: Detalhamento de Anomalias Interceptadas (%)
    anomalias = [
        "ANOM-04: Total Inconsistente",
        "ANOM-01: Frete Negativo",
        "E-mail Sintaxe Inválida",
        "E-mail Ausente (Null)",
        "Promoção Invertida",
        "ANOM-03: Desconto Excessivo",
        "ANOM-02: Subtotal Zerado"
    ]
    taxas = [5.1, 4.2, 3.2, 4.9, 4.8, 2.1, 1.9]
    y_pos = np.arange(len(anomalias))
    
    bars = ax2.barh(y_pos, taxas, color=DADOSFERA_PALETTE.accent_coral, alpha=0.85, height=0.55)
    ax2.set_yticks(y_pos)
    ax2.set_yticklabels(anomalias, fontsize=10, fontweight="bold", color=DADOSFERA_PALETTE.text_light)
    ax2.set_xlabel("Taxa de Incidência Interceptada (%)", fontsize=11, fontweight="bold", color=DADOSFERA_PALETTE.text_light)
    ax2.set_title("Quarentena Silver: Anomalias Isoladas", fontsize=13, fontweight="bold", pad=10)
    ax2.set_xlim(0, 7.5)
    
    for i, bar in enumerate(bars):
        val = taxas[i]
        ax2.text(val + 0.15, bar.get_y() + bar.get_height()/2, f"{val:.1f}%", va="center", ha="left", color=DADOSFERA_PALETTE.accent_yellow, fontsize=9, fontweight="bold")
        
    ax2.grid(axis="x", linestyle="--", alpha=0.3)
    
    plt.suptitle("Governança & Data Quality: Arquitetura Dual-Artifact Silver (DEC-006)", fontsize=15, fontweight="bold", y=0.98)
    plt.tight_layout()
    
    return fig

def main() -> None:
    fig = plot_data_quality_scorecard()
    saved_path = save_chart_artifact(fig, OUTPUT_IMAGE_PATH)
    print(f"[SUCCESS] Gráfico gerado em: {saved_path}")

if __name__ == "__main__":
    main()
