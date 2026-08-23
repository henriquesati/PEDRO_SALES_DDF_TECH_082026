"""
Gerador da visualização: Painel Comparativo Arquitetura Dadosfera vs Stack Legada AWS.
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
    os.path.dirname(__file__), "chart_07_arquitetura_dadosfera_vs_aws.png"
)

def plot_architecture_comparison() -> plt.Figure:
    """Gera visualização comparativa de lead time e eficiência arquitetural."""
    apply_dadosfera_theme()
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.0, 6.5))
    
    # Gráfico 1: Lead Time para Novas Análises e Pipelines (Dias)
    etapas = [
        "Ingestão & Conexão\n(Kinesis Sharding vs Plug&Play)",
        "Data Quality & Silver\n(S3 sem schema vs Great Expect.)",
        "Modelagem & DW\n(Redis Cluster vs Snowflake Kimball)",
        "Deploy de Data App\n(Manual Multi-serviço vs Streamlit)"
    ]
    aws_days = [7, 10, 8, 12]  # ~37 dias total (~5-6 semanas)
    ddf_days = [1, 1, 1, 2]    # ~5 dias total (< 1 semana)
    
    y = np.arange(len(etapas))
    height = 0.35
    
    ax1.barh(y - height/2, aws_days, height=height, color=DADOSFERA_PALETTE.accent_coral, label="Stack AWS Legada (Fragmentada)", alpha=0.9)
    ax1.barh(y + height/2, ddf_days, height=height, color=DADOSFERA_PALETTE.accent_green, label="Plataforma Dadosfera (SaaS All-in-One)", alpha=0.9)
    
    ax1.set_yticks(y)
    ax1.set_yticklabels(etapas, fontsize=9.5, fontweight="bold", color=DADOSFERA_PALETTE.text_light)
    ax1.set_xlabel("Lead Time de Entrega (Dias)", fontsize=11, fontweight="bold", color=DADOSFERA_PALETTE.text_light)
    ax1.set_title("Time-to-Value: Lead Time por Etapa\n(-86% no Tempo Total de Ciclo)", fontsize=13, fontweight="bold", pad=12)
    ax1.set_xlim(0, 15)
    ax1.legend(loc="lower right", fontsize=9, framealpha=0.9)
    ax1.grid(axis="x", linestyle="--", alpha=0.3)
    
    # Anotações nas barras
    for i in range(len(etapas)):
        ax1.text(aws_days[i] + 0.3, y[i] - height/2, f"{aws_days[i]}d", va="center", color=DADOSFERA_PALETTE.accent_coral, fontsize=9, fontweight="bold")
        ax1.text(ddf_days[i] + 0.3, y[i] + height/2, f"{ddf_days[i]}d", va="center", color=DADOSFERA_PALETTE.accent_green, fontsize=9, fontweight="bold")
    
    # Gráfico 2: Eficiência Operacional & Mitigação de Riscos
    dimensoes = [
        "Governança\nNativa (IAM)",
        "Resiliência em\nPicos (Black Friday)",
        "Economia de\nHeadcount",
        "Velocidade de\nData Apps",
        "GenAI & LLMs\nIntegrados"
    ]
    pontuacao_aws = [30, 25, 35, 30, 15]  # AWS sofre com Kinesis shards, Redis downtime e integrações manuais
    pontuacao_ddf = [95, 95, 90, 95, 95]  # Dadosfera SaaS
    
    x = np.arange(len(dimensoes))
    ax2.bar(x - 0.2, pontuacao_aws, width=0.4, color=DADOSFERA_PALETTE.accent_coral, label="AWS (Lambda/Kinesis/Redis/S3)", alpha=0.85)
    ax2.bar(x + 0.2, pontuacao_ddf, width=0.4, color=DADOSFERA_PALETTE.accent_blue, label="Dadosfera Sistema Operacional", alpha=0.85)
    
    ax2.set_xticks(x)
    ax2.set_xticklabels(dimensoes, fontsize=8.5, fontweight="bold", color=DADOSFERA_PALETTE.text_light)
    ax2.set_ylabel("Índice de Eficiência / Maturidade (0-100)", fontsize=11, fontweight="bold", color=DADOSFERA_PALETTE.text_light)
    ax2.set_title("Comparativo Estratégico de Capacidades\n(Governança, TCO & Zero Risco em Picos)", fontsize=13, fontweight="bold", pad=12)
    ax2.set_ylim(0, 118)
    ax2.legend(loc="upper left", fontsize=9, framealpha=0.9)
    ax2.grid(axis="y", linestyle="--", alpha=0.3)
    
    for i in range(len(dimensoes)):
        ax2.text(i - 0.2, pontuacao_aws[i] + 2, f"{pontuacao_aws[i]}", ha="center", color=DADOSFERA_PALETTE.accent_coral, fontsize=9, fontweight="bold")
        ax2.text(i + 0.2, pontuacao_ddf[i] + 2, f"{pontuacao_ddf[i]}", ha="center", color=DADOSFERA_PALETTE.accent_cyan, fontsize=9, fontweight="bold")
    
    plt.suptitle("Arquitetura Moderna: Dadosfera vs Stack Fragmentada AWS (Análise Estratégica)", fontsize=14, fontweight="bold", y=0.98)
    plt.tight_layout()
    
    return fig

def main() -> None:
    fig = plot_architecture_comparison()
    saved_path = save_chart_artifact(fig, OUTPUT_IMAGE_PATH)
    print(f"[SUCCESS] Gráfico gerado em: {saved_path}")

if __name__ == "__main__":
    main()
