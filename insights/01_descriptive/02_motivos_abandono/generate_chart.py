#!/usr/bin/env python3
"""
generate_chart.py
Módulo: views-04-insights/descritivos/motivosabandono (Ato 3 / Seção [4.1] - Causas-Raiz de Abandono)
Função: Renderização executiva da Concentração de Receita por Faixa de Ticket (Esquerda) e Decomposição das 6 Causas-Raiz (Direita).
Padrão Gráfico: Fundo Branco Puro (#FFFFFF), 16:9 Widescreen, 300 DPI, charts-maker standard.
"""

from typing import Final, Tuple, Dict, Any, List
import os
import sys
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# ==============================================================================
# CONFIGURAÇÃO DE CONSTANTES E DIRETÓRIOS
# ==============================================================================

VIEW_DIR: Final[Path] = Path(__file__).resolve().parent
OUTPUT_IMAGE_PATH: Final[Path] = VIEW_DIR / "chart_02_motivos_abandono.png"

def get_base_dir() -> Path:
    curr = Path(__file__).resolve().parent
    while curr and curr.parent != curr:
        if (curr / "data" / "mock").exists():
            return curr
        curr = curr.parent
    return Path.cwd().resolve()

BASE_DIR: Final[Path] = get_base_dir()

PARQUET_CARTS: Final[Path] = (
    BASE_DIR / "data" / "mock" / "output_cleaned" / "parquet" / "carrinhos.parquet"
    if (BASE_DIR / "data" / "mock" / "output_cleaned" / "parquet" / "carrinhos.parquet").exists()
    else (BASE_DIR / "data" / "mock" / "output_cleaned" / "parquet" / "carrinhos.parquet" if (BASE_DIR / "data" / "mock" / "output_cleaned" / "parquet" / "carrinhos.parquet").exists() else BASE_DIR / "data" / "mock" / "output" / "parquet" / "carrinhos.parquet")
)

# Paleta Semântica Corporativa (White Background Executive)
COLORS: Final[Dict[str, str]] = {
    "bg_canvas": "#FFFFFF",
    "bg_card": "#F8FAFC",
    "border_card": "#E2E8F0",
    "border_highlight": "#CBD5E1",
    "text_primary": "#0F172A",
    "text_secondary": "#1E293B",
    "text_muted": "#475569",
    "primary_blue": "#2563EB",
    "rescue_green": "#059669",
    "attrition_rose": "#E11D48",
    "warning_amber": "#D97706",
    "grid": "#CBD5E1"
}

# ==============================================================================
# CARGA E PROCESSAMENTO FUNCIONAL DOS DADOS (GROUND TRUTH)
# ==============================================================================

def load_ground_truth() -> Tuple[pd.DataFrame, int, float]:
    """Carrega dados persistidos de carrinhos que sofreram abandono no checkout."""
    df_carts = pd.read_parquet(PARQUET_CARTS)
    
    # Filtra os carrinhos que sofreram abandono (5.231 carrinhos com registro de motivo)
    df_aband = df_carts[df_carts["motivo_abandono"].notna() & (df_carts["motivo_abandono"] != "")].copy()
    
    total_vol_aband = len(df_aband)
    total_rec_aband = df_aband["valor_total"].sum()
    
    label_map = {
        "frete": "Frete Caro",
        "indecisao": "Indecisão / Dúvidas",
        "pagamento": "Erro no Pagamento / Checkout",
        "preco": "Preço Alto / Comparação",
        "nao_informado": "Não Informado",
        "estoque": "Estoque Indisponível"
    }
    df_aband["motivo_label"] = df_aband["motivo_abandono"].map(label_map).fillna(df_aband["motivo_abandono"])
    
    def get_faixa(v: float) -> str:
        if v < 100.0:
            return "Ticket Baixo (< R$ 100)"
        elif v <= 250.0:
            return "Ticket Médio-Baixo (R$ 100–250)"
        elif v <= 500.0:
            return "Ticket Médio-Alto (R$ 250–500)"
        else:
            return "Ticket Alto (> R$ 500)"
            
    df_aband["faixa_ticket"] = df_aband["valor_total"].apply(get_faixa)
    return df_aband, total_vol_aband, total_rec_aband

def compute_aggregations(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Calcula agregados por faixa de ticket e por motivo de abandono."""
    # 1. Agregação por Faixa de Ticket (Painel Esquerdo)
    order_faixas = [
        "Ticket Baixo (< R$ 100)",
        "Ticket Médio-Baixo (R$ 100–250)",
        "Ticket Médio-Alto (R$ 250–500)",
        "Ticket Alto (> R$ 500)"
    ]
    
    agg_tickets = df.groupby("faixa_ticket").agg(
        volume=("carrinho_id", "count"),
        receita_represada=("valor_total", "sum")
    ).reindex(order_faixas).reset_index().dropna()
    
    agg_tickets["pct_receita"] = (agg_tickets["receita_represada"] / agg_tickets["receita_represada"].sum()) * 100
    agg_tickets["pct_volume"] = (agg_tickets["volume"] / agg_tickets["volume"].sum()) * 100

    # 2. Agregação por Motivo de Abandono (Painel Direito)
    order_motivos = [
        "Frete Caro", "Indecisão / Dúvidas", "Erro no Pagamento / Checkout",
        "Preço Alto / Comparação", "Não Informado", "Estoque Indisponível"
    ]
    
    agg_motivos = df.groupby("motivo_label").agg(
        volume=("carrinho_id", "count"),
        receita_represada=("valor_total", "sum")
    ).reindex(order_motivos).reset_index().dropna()
    
    total_vol = agg_motivos["volume"].sum()
    agg_motivos["pct"] = (agg_motivos["volume"] / total_vol) * 100
    
    return agg_tickets, agg_motivos

# ==============================================================================
# RENDERIZAÇÃO VISUAL (16:9 WIDESCREEN)
# ==============================================================================

def plot_motivos_panel(
    df_tickets: pd.DataFrame,
    df_motivos: pd.DataFrame,
    total_vol: int,
    total_rec: float
) -> plt.Figure:
    """
    Gera o painel executivo com a ordem invertida:
    - Esquerda (ax1): Concentração Financeira por Faixa de Ticket (Apenas Carrinhos Abandonados)
    - Direita (ax2): Decomposição das 6 Causas-Raiz de Abandono
    """
    plt.rcParams["text.parse_math"] = False
    plt.rcParams["font.sans-serif"] = ["Segoe UI", "DejaVu Sans", "Helvetica", "Arial", "sans-serif"]
    plt.rcParams["axes.edgecolor"] = COLORS["border_highlight"]
    plt.rcParams["axes.linewidth"] = 1.1

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16.0, 7.2), gridspec_kw={"width_ratios": [1.05, 1.05]})
    fig.patch.set_facecolor(COLORS["bg_canvas"])

    # --- PAINEL ESQUERDO: Concentração de Receita por Faixa de Ticket (Carrinhos Abandonados) ---
    ax1.set_facecolor("#FFFFFF")
    
    y_pos_t = np.arange(len(df_tickets))
    labels_tickets = df_tickets["faixa_ticket"].tolist()[::-1]
    revs_t = (df_tickets["receita_represada"] / 1000).to_numpy()[::-1]
    pcts_t = df_tickets["pct_receita"].to_numpy()[::-1]
    vols_t = df_tickets["volume"].to_numpy()[::-1]
    
    # Cores com gradiente executivo de azul para destacar tickets mais altos
    ticket_colors = ["#CBD5E1", "#93C5FD", "#3B82F6", "#1D4ED8"]
    
    ax1.barh(y_pos_t, revs_t, height=0.55, color=ticket_colors, edgecolor="none", zorder=3)
    
    for i, (rev, pct, vol) in enumerate(zip(revs_t, pcts_t, vols_t)):
        ax1.text(
            rev + 14.0, i + 0.12,
            f"R$ {rev:,.1f}k ({pct:.1f}% da perda)",
            va="center", ha="left", fontsize=9.2, fontweight="bold", color=COLORS["text_primary"]
        )
        ax1.text(
            rev + 14.0, i - 0.15,
            f"Volume: {vol:,.0f} carrinhos abandonados",
            va="center", ha="left", fontsize=8.2, color=COLORS["text_muted"]
        )

    ax1.set_yticks(y_pos_t)
    ax1.set_yticklabels(labels_tickets, fontsize=9.5, fontweight="bold", color=COLORS["text_secondary"])
    ax1.set_xlabel(f"Receita Represada no Abandono (R$ mil) — Total: R$ {total_rec/1e6:.2f}M", fontsize=9.2, fontweight="bold", color=COLORS["text_secondary"])
    ax1.set_title("Concentração da Receita Perdida por Faixa de Ticket\n(Base Exclusiva: 5.231 Carrinhos que Sofreram Abandono)",
                  fontsize=11.2, fontweight="bold", color=COLORS["text_primary"], pad=10)
    ax1.set_xlim(0, max(revs_t) * 1.48)
    ax1.grid(axis="x", linestyle="--", alpha=0.45, color=COLORS["grid"])
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)

    # Callout destacando que tickets > R$ 250 concentram mais de 80% da perda
    pct_alto_medio = df_tickets[df_tickets["faixa_ticket"].isin(["Ticket Alto (> R$ 500)", "Ticket Médio-Alto (R$ 250–500)"])]["pct_receita"].sum()
    ax1.text(
        0.04, 0.05,
        f"• Insight de Negócio: Tickets acima de R$ 250 concentram {pct_alto_medio:.1f}% de todo o dinheiro perdido no checkout.",
        transform=ax1.transAxes, fontsize=8.2, fontweight="bold", color="#1E40AF",
        bbox=dict(boxstyle="round,pad=0.35", facecolor="#EFF6FF", edgecolor="#BFDBFE", linewidth=1.0)
    )

    # --- PAINEL DIREITO: Decomposição das 6 Causas-Raiz de Abandono ---
    ax2.set_facecolor("#FFFFFF")
    
    y_pos_m = np.arange(len(df_motivos))
    labels_motivos = df_motivos["motivo_label"].tolist()[::-1]
    pcts_m = df_motivos["pct"].to_numpy()[::-1]
    vols_m = df_motivos["volume"].to_numpy()[::-1]
    revs_m = (df_motivos["receita_represada"] / 1000).to_numpy()[::-1]
    
    bar_colors_m = ["#94A3B8", "#64748B", "#F59E0B", "#F43F5E", "#8B5CF6", "#E11D48"]
    
    ax2.barh(y_pos_m, pcts_m, height=0.55, color=bar_colors_m, edgecolor="none", zorder=3)
    
    for i, (pct, vol, rev) in enumerate(zip(pcts_m, vols_m, revs_m)):
        ax2.text(
            pct + 0.8, i + 0.12,
            f"{pct:.1f}% ({vol:,.0f} carrinhos)",
            va="center", ha="left", fontsize=9.2, fontweight="bold", color=COLORS["text_primary"]
        )
        ax2.text(
            pct + 0.8, i - 0.15,
            f"Perda Estimada: R$ {rev:,.1f}k",
            va="center", ha="left", fontsize=8.2, color=COLORS["text_muted"]
        )

    ax2.set_yticks(y_pos_m)
    ax2.set_yticklabels(labels_motivos, fontsize=9.5, fontweight="bold", color=COLORS["text_secondary"])
    ax2.set_xlabel(f"Representatividade sobre os Abandonos (%) — Total: {total_vol:,.0f} un", fontsize=9.2, fontweight="bold", color=COLORS["text_secondary"])
    ax2.set_title("Decomposição das 6 Causas-Raiz de Abandono\n(Origem do Atrito nos Mesmos 5.231 Carrinhos)",
                  fontsize=11.2, fontweight="bold", color=COLORS["text_primary"], pad=10)
    ax2.set_xlim(0, 48)
    ax2.grid(axis="x", linestyle="--", alpha=0.45, color=COLORS["grid"])
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)

    # Callout destacando Frete + Indecisão
    pct_frete_indecisao = df_motivos[df_motivos["motivo_label"].isin(["Frete Caro", "Indecisão / Dúvidas"])]["pct"].sum()
    ax2.text(
        0.04, 0.05,
        f"• Causa Crítica: Frete Caro + Indecisão somam {pct_frete_indecisao:.1f}% dos motivos de abandono observados.",
        transform=ax2.transAxes, fontsize=8.2, fontweight="bold", color="#991B1B",
        bbox=dict(boxstyle="round,pad=0.35", facecolor="#FEF2F2", edgecolor="#FECACA", linewidth=1.0)
    )

    # Título Geral Executivo
    fig.suptitle("DIAGNÓSTICO DE ABANDONO: CONCENTRAÇÃO FINANCEIRA POR TICKET & CAUSAS-RAIZ",
                 fontsize=14.0, fontweight="bold", color=COLORS["text_primary"], y=0.98)

    fig.subplots_adjust(top=0.86, bottom=0.12, left=0.18, right=0.96, wspace=0.38)
    return fig

# ==============================================================================
# EXECUÇÃO PRINCIPAL
# ==============================================================================

def main() -> None:
    df_aband, total_vol, total_rec = load_ground_truth()
    df_tickets, df_motivos = compute_aggregations(df_aband)
    
    fig = plot_motivos_panel(df_tickets, df_motivos, total_vol, total_rec)
    
    OUTPUT_IMAGE_PATH.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_IMAGE_PATH, dpi=300, bbox_inches="tight", facecolor=COLORS["bg_canvas"])
    plt.close(fig)
    print(f"[SUCCESS] Gráfico de Motivos de Abandono (Invertido & Clarificado) salvo em: {OUTPUT_IMAGE_PATH}")

if __name__ == "__main__":
    main()
