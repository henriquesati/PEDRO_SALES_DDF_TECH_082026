"""
Gerador da visualização: BI de Recuperação de Carrinhos (Versão Sinuosa - Recorte de 1 Semana).
Paradigma funcional e declarativo com tipagem estrita (Type Annotations).

Características:
- Recorte temporal focado em 1 semana (09 a 15 de Fevereiro de 2026).
- Linhas sinuosas orgânicas (Spline Cúbica) com variações de curvatura e cristas/vales.
- Linha Superior: Carrinhos Abandonados (Teto / Atrito).
- Linha Intermediária: Carrinhos Comprados Diretamente (Conversão no Checkout).
- Linha Inferior: Carrinhos Recuperados (Resgate Ativo Dadosfera).
- Fundo branco puro (#FFFFFF) com preenchimento colorido nas 3 zonas entre as linhas (fill_between).
- Vértices reais destacados para leitura clara das diferenças no eixo X e Y.
"""

from typing import Final
import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline

# Caminhos absolutos
BASE_DIR: Final[str] = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
OUTPUT_IMAGE_PATH: Final[str] = os.path.join(
    os.path.dirname(__file__), "chart_bi_recuperacao_carrinhos_sinuous_1week.png"
)

PARQUET_CARTS_PATH: Final[str] = os.path.join(
    BASE_DIR, "data", "mock", "output", "parquet", "carrinhos.parquet"
)

def load_data() -> pd.DataFrame:
    """Carrega dados transacionais de carrinhos em Parquet."""
    df_carts: pd.DataFrame = pd.read_parquet(PARQUET_CARTS_PATH)
    df_carts["data_criacao"] = pd.to_datetime(df_carts["data_criacao"])
    return df_carts

def prepare_1week_series(df_carts: pd.DataFrame) -> tuple[list[str], np.ndarray, np.ndarray, np.ndarray, int]:
    """Prepara a série temporal de 1 semana (09/Fev a 15/Fev) com contagens diárias."""
    start_dt = pd.to_datetime("2026-02-09 00:00:00+00:00")
    end_dt = pd.to_datetime("2026-02-15 23:59:59+00:00")
    
    df_week = df_carts[(df_carts["data_criacao"] >= start_dt) & (df_carts["data_criacao"] <= end_dt)]
    
    df_daily: pd.DataFrame = (
        df_week.groupby([pd.Grouper(key="data_criacao", freq="1D"), "status"])
        .size()
        .unstack(fill_value=0)
    )
    
    for col in ["abandonado", "comprado", "recuperado", "ativo", "expirado"]:
        if col not in df_daily.columns:
            df_daily[col] = 0
            
    df_daily["total_dia"] = df_daily.sum(axis=1)
    
    dias_rotulos: list[str] = [
        "Seg (09/Fev)",
        "Ter (10/Fev)",
        "Qua (11/Fev)",
        "Qui (12/Fev)",
        "Sex (13/Fev)",
        "Sáb (14/Fev)",
        "Dom (15/Fev)",
    ]
    
    y_aband = df_daily["abandonado"].to_numpy(dtype=float)
    y_comp = df_daily["comprado"].to_numpy(dtype=float)
    y_recup = df_daily["recuperado"].to_numpy(dtype=float)
    total_geral = int(df_daily["total_dia"].sum())
    
    return dias_rotulos, y_aband, y_comp, y_recup, total_geral

def plot_sinuous_1week_chart(
    dias_rotulos: list[str],
    y_aband: np.ndarray,
    y_comp: np.ndarray,
    y_recup: np.ndarray,
    total_geral: int
) -> plt.Figure:
    """Gera o gráfico sinuoso de 1 semana com spline, fundo branco e fill_between."""
    plt.rcParams["font.sans-serif"] = ["Segoe UI", "DejaVu Sans", "Helvetica", "Arial", "sans-serif"]
    plt.rcParams["axes.edgecolor"] = "#CBD5E1"
    plt.rcParams["axes.linewidth"] = 1.2
    
    fig, ax = plt.subplots(figsize=(14.0, 7.5), facecolor="#FFFFFF")
    ax.set_facecolor("#FFFFFF")
    
    x_indices = np.arange(len(dias_rotulos))
    
    # Interpolação Spline Cúbica hiper-suave (300 pontos) gerando curvas sinuosas
    x_smooth = np.linspace(x_indices.min(), x_indices.max(), 300)
    spl_aband = np.maximum(0, make_interp_spline(x_indices, y_aband, k=3)(x_smooth))
    spl_comp = np.maximum(0, make_interp_spline(x_indices, y_comp, k=3)(x_smooth))
    spl_recup = np.maximum(0, make_interp_spline(x_indices, y_recup, k=3)(x_smooth))
    
    # Cores Corporativas
    color_aband = "#E11D48"       # Vermelho / Rose vibrante
    color_comp = "#2563EB"        # Azul Royal
    color_recup = "#059669"       # Verde Esmeralda
    
    # Preenchimento de Zonas (fill_between)
    ax.fill_between(
        x_smooth, spl_comp, spl_aband,
        color="#FFE4E6", alpha=0.60,
        label="Zona de Atrito / Perda Não Convertida (Abandono no Checkout)"
    )
    ax.fill_between(
        x_smooth, spl_recup, spl_comp,
        color="#DBEAFE", alpha=0.55,
        label="Zona de Conversão Direta no Checkout (Orgânica)"
    )
    ax.fill_between(
        x_smooth, 0, spl_recup,
        color="#D1FAE5", alpha=0.85,
        label="Zona de Carrinhos Recuperados (Resgate Ativo Dadosfera)"
    )
    
    # Linhas Sinuosas com Curvatura Orgânica
    ax.plot(x_smooth, spl_aband, color=color_aband, linewidth=3.4, label="[1] Carrinhos Abandonados (Teto Superior: Atrito)", zorder=4)
    ax.plot(x_smooth, spl_comp, color=color_comp, linewidth=3.0, label="[2] Carrinhos Comprados Diretamente (Intermediário)", zorder=4)
    ax.plot(x_smooth, spl_recup, color=color_recup, linewidth=2.8, label="[3] Carrinhos Recuperados (Base / Resgate Ativo)", zorder=4)
    
    # Vértices reais destacados
    ax.scatter(x_indices, y_aband, color="#FFFFFF", edgecolor=color_aband, s=55, linewidth=2.2, zorder=5)
    ax.scatter(x_indices, y_comp, color="#FFFFFF", edgecolor=color_comp, s=55, linewidth=2.2, zorder=5)
    ax.scatter(x_indices, y_recup, color="#FFFFFF", edgecolor=color_recup, s=55, linewidth=2.2, zorder=5)
    
    # Anotações nos vértices para evidenciar a diferença valoral diária
    for i in range(len(dias_rotulos)):
        ax.annotate(f"{int(y_aband[i])}", (x_indices[i], y_aband[i] + 1.1), ha="center", fontsize=9.5, fontweight="bold", color="#9F1239")
        ax.annotate(f"{int(y_comp[i])}", (x_indices[i], y_comp[i] + 0.9), ha="center", fontsize=9.5, fontweight="bold", color="#1E40AF")
        if y_recup[i] > 0:
            ax.annotate(f"{int(y_recup[i])}", (x_indices[i], y_recup[i] + 0.8), ha="center", fontsize=9.5, fontweight="bold", color="#065F46")
            
    # Eixos e Formatação
    ax.set_xticks(x_indices)
    ax.set_xticklabels(dias_rotulos, fontsize=11, fontweight="bold", color="#1E293B")
    ax.set_xlabel("Dias da Semana (Recorte Focado de 1 Semana: 09 a 15 de Fevereiro de 2026)", fontsize=11, fontweight="bold", color="#1E293B", labelpad=10)
    
    ax.set_ylabel("Volume Diário de Carrinhos (Unidades)", fontsize=11, fontweight="bold", color="#1E293B", labelpad=10)
    ax.set_xlim(-0.2, len(dias_rotulos) - 0.8)
    ax.set_ylim(0, max(y_aband.max(), spl_aband.max()) * 1.18)
    
    # Grid sutil
    ax.grid(True, linestyle="--", alpha=0.5, color="#CBD5E1", zorder=1)
    
    # Título e Subtítulo
    ax.set_title(
        "BI de Recuperação de Carrinhos: Dinâmica Sinuosa em Janela Curta (1 Semana)\n"
        "(Curvas Orgânicas, Vértices Diários e Diferença Valoral entre as Faixas de Conversão)",
        fontsize=13.5,
        fontweight="bold",
        color="#0F172A",
        pad=16
    )
    
    # Card Resumo
    total_aband = int(y_aband.sum())
    total_comp = int(y_comp.sum())
    total_recup = int(y_recup.sum())
    
    card_text = (
        "RECORTE SEMANAL (09/FEV A 15/FEV):\n"
        f"• Total de Carrinhos: {total_geral} un (100%)\n"
        f"• Abandonados: {total_aband} un ({total_aband/total_geral*100:.1f}%)\n"
        f"• Comprados Diretos: {total_comp} un ({total_comp/total_geral*100:.1f}%)\n"
        f"• Resgates Ativos: {total_recup} un ({total_recup/total_geral*100:.1f}%)"
    )
    
    props = dict(boxstyle="round,pad=0.8", facecolor="#F8FAFC", edgecolor="#94A3B8", alpha=0.95, linewidth=1.2)
    ax.text(0.02, 0.95, card_text, transform=ax.transAxes, fontsize=9.5, fontweight="bold", color="#1E293B", va="top", bbox=props, zorder=6)
    
    # Legenda estruturada
    ax.legend(loc="upper right", fontsize=9.5, framealpha=0.95, facecolor="#FFFFFF", edgecolor="#CBD5E1")
    
    plt.tight_layout()
    return fig

def main() -> None:
    """Executa a extração dos dados e geração do gráfico sinuoso de 1 semana."""
    df_carts = load_data()
    dias_rotulos, y_aband, y_comp, y_recup, total_geral = prepare_1week_series(df_carts)
    fig = plot_sinuous_1week_chart(dias_rotulos, y_aband, y_comp, y_recup, total_geral)
    
    fig.savefig(OUTPUT_IMAGE_PATH, dpi=300, bbox_inches="tight", facecolor="#FFFFFF")
    plt.close(fig)
    print(f"[SUCCESS] Gráfico Sinuoso de 1 Semana gerado em: {OUTPUT_IMAGE_PATH}")

if __name__ == "__main__":
    main()
