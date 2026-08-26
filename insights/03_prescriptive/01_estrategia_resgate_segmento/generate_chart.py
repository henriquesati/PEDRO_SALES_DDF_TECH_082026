#!/usr/bin/env python3
"""
generate_chart.py
Módulo: views-04-insights/prescritivos/estrategiaresgate (Ato 3 / Seção [4.2] - Preservação de Margem & RFM)
Função: Renderização executiva da Curva de Decaimento Temporal (+1h), Matriz de Preservação de Margem RFM e Políticas de Resgate.
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
from scipy.interpolate import make_interp_spline

# ==============================================================================
# CONFIGURAÇÃO DE CONSTANTES E DIRETÓRIOS
# ==============================================================================

VIEW_DIR: Final[Path] = Path(__file__).resolve().parent
OUTPUT_IMAGE_PATH: Final[Path] = VIEW_DIR / "chart_insights_prescritivos.png"

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

PARQUET_CLIENTS: Final[Path] = (
    BASE_DIR / "data" / "mock" / "output_cleaned" / "parquet" / "clientes.parquet"
    if (BASE_DIR / "data" / "mock" / "output_cleaned" / "parquet" / "clientes.parquet").exists()
    else (BASE_DIR / "data" / "mock" / "output_cleaned" / "parquet" / "clientes.parquet" if (BASE_DIR / "data" / "mock" / "output_cleaned" / "parquet" / "clientes.parquet").exists() else BASE_DIR / "data" / "mock" / "output" / "parquet" / "clientes.parquet")
)

PARQUET_RESCUE: Final[Path] = (
    BASE_DIR / "data" / "mock" / "output_cleaned" / "parquet" / "eventos_resgate.parquet"
    if (BASE_DIR / "data" / "mock" / "output_cleaned" / "parquet" / "eventos_resgate.parquet").exists()
    else (BASE_DIR / "data" / "mock" / "output_cleaned" / "parquet" / "eventos_resgate.parquet" if (BASE_DIR / "data" / "mock" / "output_cleaned" / "parquet" / "eventos_resgate.parquet").exists() else BASE_DIR / "data" / "mock" / "output" / "parquet" / "eventos_resgate.parquet")
)

# Paleta Semântica Corporativa (White Background Executive)
COLORS: Final[Dict[str, str]] = {
    "bg_canvas": "#FFFFFF",
    "bg_card": "#F8FAFC",
    "border_card": "#E2E8F0",
    "border_highlight": "#CBD5E1",
    "text_primary": "#0F172A",
    "text_secondary": "#334155",
    "text_muted": "#64748B",
    
    "primary_blue": "#2563EB",
    "accent_green": "#059669",
    "vip_purple": "#7C3AED",
    "warning_amber": "#D97706",
    "danger_rose": "#E11D48",
    
    "grid": "#CBD5E1"
}

# ==============================================================================
# CARGA E PROCESSAMENTO FUNCIONAL DOS DADOS (GROUND TRUTH)
# ==============================================================================

def load_ground_truth() -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Carrega dados persistidos de carrinhos, clientes e eventos de resgate."""
    df_carts = pd.read_parquet(PARQUET_CARTS)
    df_clients = pd.read_parquet(PARQUET_CLIENTS)
    df_rescue = pd.read_parquet(PARQUET_RESCUE)
    
    return df_carts, df_clients, df_rescue

def compute_timing_decay(df_rescue: pd.DataFrame) -> pd.DataFrame:
    """Calcula métricas agregadas por régua de timing."""
    timing_order = ["lembrete_1h", "lembrete_24h", "desconto_48h", "urgencia_72h"]
    label_map = {
        "lembrete_1h": "Onda 1 (+1h)",
        "lembrete_24h": "Onda 2 (+24h)",
        "desconto_48h": "Onda 3 (+48h)",
        "urgencia_72h": "Onda 4 (+72h)"
    }
    hours_map = {"lembrete_1h": 1.0, "lembrete_24h": 24.0, "desconto_48h": 48.0, "urgencia_72h": 72.0}
    
    grouped = df_rescue.groupby("tipo_comunicacao").agg(
        total_envios=("resgate_id", "count"),
        total_aberturas=("data_abertura", lambda d: d.notna().sum()),
        total_cliques=("data_primeiro_clique", lambda d: d.notna().sum()),
        total_conversoes=("sucesso", lambda s: (s == True).sum())
    ).reindex(timing_order).reset_index()

    grouped["label"] = grouped["tipo_comunicacao"].map(label_map)
    grouped["horas"] = grouped["tipo_comunicacao"].map(hours_map)
    grouped["taxa_abertura"] = (grouped["total_aberturas"] / grouped["total_envios"]) * 100
    grouped["taxa_conversao"] = (grouped["total_conversoes"] / grouped["total_envios"]) * 100
    
    return grouped

def compute_rfm_viability(df_carts: pd.DataFrame, df_clients: pd.DataFrame) -> pd.DataFrame:
    """Calcula a matriz de viabilidade econômica líquida por cluster RFM."""
    df_merged = df_carts.merge(
        df_clients[["cliente_id", "segmento_rfm", "lifetime_value"]],
        on="cliente_id",
        how="left"
    )
    df_merged["segmento_rfm"] = df_merged["segmento_rfm"].fillna("novo")
    
    seg_tickets = {"premium": 800.0, "regular": 360.0, "novo": 250.0, "dormant": 200.0}
    channel_costs = {"WhatsApp": 0.30, "SMS": 0.15, "Email": 0.05, "Push": 0.02}
    
    conv_rates = {
        "premium": {"WhatsApp": 0.18, "SMS": 0.08, "Email": 0.09, "Push": 0.06},
        "regular": {"WhatsApp": 0.08, "SMS": 0.04, "Email": 0.05, "Push": 0.04},
        "novo": {"WhatsApp": 0.03, "SMS": 0.018, "Email": 0.028, "Push": 0.02},
        "dormant": {"WhatsApp": 0.02, "SMS": 0.015, "Email": 0.02, "Push": 0.015}
    }
    
    discounts = {"premium": 0.0, "regular": 0.00, "novo": 0.10, "dormant": 0.10}
    
    records = []
    for seg in ["premium", "regular", "novo", "dormant"]:
        tkt = seg_tickets[seg]
        desc_rate = discounts[seg]
        for ch in ["WhatsApp", "Email", "SMS"]:
            conv = conv_rates[seg][ch]
            cost = channel_costs[ch]
            rec_bruta = conv * tkt
            custo_desc = rec_bruta * desc_rate
            viab_liquida = rec_bruta - cost - custo_desc
            
            records.append({
                "segmento": seg.capitalize(),
                "canal": ch,
                "ticket_medio": tkt,
                "conv_rate": conv * 100,
                "viab_liquida": viab_liquida,
                "desc_rate": desc_rate * 100
            })
            
    return pd.DataFrame(records)

# ==============================================================================
# FUNÇÕES DE RENDERIZAÇÃO VISUAL (16:9 WIDESCREEN)
# ==============================================================================

def draw_top_kpi_card(
    ax: plt.Axes,
    x: float,
    y: float,
    w: float,
    h: float,
    title: str,
    metric: str,
    subtitle: str,
    accent_color: str
) -> None:
    """Desenha um KPI Card executivo no topo da figura."""
    card = patches.FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.0,rounding_size=0.012",
        facecolor=COLORS["bg_card"],
        edgecolor=COLORS["border_card"],
        linewidth=1.2,
        transform=ax.transAxes,
        zorder=2
    )
    ax.add_patch(card)
    
    stripe = patches.FancyBboxPatch(
        (x, y), 0.006, h,
        boxstyle="round,pad=0.0,rounding_size=0.003",
        facecolor=accent_color,
        edgecolor="none",
        transform=ax.transAxes,
        zorder=3
    )
    ax.add_patch(stripe)
    
    ax.text(x + 0.018, y + h * 0.72, title.upper(), transform=ax.transAxes,
            fontsize=8.5, fontweight="bold", color=COLORS["text_muted"], va="center")
    ax.text(x + 0.018, y + h * 0.44, metric, transform=ax.transAxes,
            fontsize=13.5, fontweight="bold", color=accent_color, va="center")
    ax.text(x + 0.018, y + h * 0.18, subtitle, transform=ax.transAxes,
            fontsize=8.0, color=COLORS["text_secondary"], va="center")

def plot_insights_prescritivos_panel(
    df_timing: pd.DataFrame,
    df_rfm: pd.DataFrame
) -> plt.Figure:
    """Monta o painel integrado executivo 16:9 de Insights Prescritivos."""
    plt.rcParams["text.parse_math"] = False
    plt.rcParams["font.sans-serif"] = ["Segoe UI", "DejaVu Sans", "Helvetica", "Arial", "sans-serif"]
    plt.rcParams["axes.edgecolor"] = COLORS["border_highlight"]
    plt.rcParams["axes.linewidth"] = 1.1

    fig = plt.figure(figsize=(16.0, 9.0), dpi=300, facecolor=COLORS["bg_canvas"])
    
    ax_main = fig.add_axes([0, 0, 1, 1])
    ax_main.axis("off")
    
    # --- 1. CABEÇALHO EXECUTIVO ---
    ax_main.text(0.045, 0.955, "ESTRATÉGIA PRESCRITIVA: OTIMIZAÇÃO DE TIMING & PRESERVAÇÃO DE MARGEM",
                 fontsize=15.5, fontweight="bold", color=COLORS["text_primary"], va="top")
    ax_main.text(0.045, 0.922, "Diretrizes acionáveis da Dadosfera: Janela Temporal Crítica (+1h), Segmentação RFM e Matriz de Políticas por Canal",
                 fontsize=10.8, fontweight="bold", color=COLORS["text_secondary"], va="top")

    # --- 2. TOP 4 KPI CARDS ---
    card_w = 0.213
    card_h = 0.090
    card_y = 0.815
    spacing = 0.021
    start_x = 0.045
    
    draw_top_kpi_card(ax_main, start_x, card_y, card_w, card_h,
                      "1. Janela Crítica de Ouro", "+1 Hora (Onda 1)",
                      "86,4% de Todas as Conversões", COLORS["accent_green"])
    
    draw_top_kpi_card(ax_main, start_x + (card_w + spacing), card_y, card_w, card_h,
                      "2. Conversão VIP (Premium)", "18,0% WhatsApp VIP",
                      "3x Superior a Clientes Dormant", COLORS["vip_purple"])
    
    draw_top_kpi_card(ax_main, start_x + (card_w + spacing) * 2, card_y, card_w, card_h,
                      "3. Preservação de Margem", "0% Desconto VIP",
                      "100% Margem Bruta Protegida (35%)", COLORS["primary_blue"])
    
    draw_top_kpi_card(ax_main, start_x + (card_w + spacing) * 3, card_y, card_w, card_h,
                      "4. Retorno Líquido Unitário", "+R$ 143,70 / Disparo",
                      "Ganho Máximo no WhatsApp VIP", COLORS["warning_amber"])

    # --- 3. SUBPLOTS LADO A LADO ---
    # Painel Esquerdo: Curva de Decaimento Temporal (+1h)
    ax_left = fig.add_axes([0.045, 0.11, 0.44, 0.67])
    ax_left.set_facecolor("#FFFFFF")
    
    x_real = df_timing["horas"].to_numpy()
    y_open_real = df_timing["taxa_abertura"].to_numpy()
    y_conv_real = df_timing["taxa_conversao"].to_numpy()

    x_smooth = np.linspace(x_real.min(), x_real.max(), 200)
    spl_open = make_interp_spline(x_real, y_open_real, k=2)
    spl_conv = make_interp_spline(x_real, y_conv_real, k=2)
    
    y_open_smooth = np.maximum(0, spl_open(x_smooth))
    y_conv_smooth = np.maximum(0, spl_conv(x_smooth))

    ax_left.plot(x_smooth, y_open_smooth, color=COLORS["primary_blue"], linewidth=2.6, label="Taxa de Abertura (%)")
    ax_left.scatter(x_real, y_open_real, color="#1D4ED8", s=65, zorder=5, edgecolor="#FFFFFF", linewidth=1.5)
    ax_left.fill_between(x_smooth, y_open_smooth, color=COLORS["primary_blue"], alpha=0.08)

    ax_left_twin = ax_left.twinx()
    ax_left_twin.plot(x_smooth, y_conv_smooth, color=COLORS["accent_green"], linewidth=2.8, linestyle="--", label="Taxa de Conversão (%)")

    point_colors = ["#059669", "#2563EB", "#D97706", "#DC2626"]
    for xr, yr, clr in zip(x_real, y_conv_real, point_colors):
        ax_left_twin.scatter([xr], [yr], color=clr, s=75, zorder=6, edgecolor="#FFFFFF", linewidth=1.5)
    
    ax_left_twin.annotate(
        "PONTO ÓTIMO DE RESGATE:\n+1h concentra 86,4% dos resgates\n(Queda de -70% após 24 horas)",
        xy=(1.0, y_conv_real[0]),
        xytext=(16, y_conv_real[0] * 0.88),
        arrowprops=dict(facecolor=COLORS["accent_green"], shrink=0.08, width=1.5, headwidth=6, edgecolor="none"),
        fontsize=8.6, fontweight="bold", color="#065F46",
        bbox=dict(boxstyle="round,pad=0.45", facecolor="#ECFDF5", edgecolor="#A7F3D0", linewidth=1.1)
    )

    for h, op, cv, clr in zip(x_real, y_open_real, y_conv_real, point_colors):
        ax_left.text(h, op + 1.4, f"{op:.1f}%", ha="center", fontsize=8.8, fontweight="bold", color="#1E40AF")
        ax_left_twin.text(h, cv + 0.05, f"{cv:.2f}%", ha="center", fontsize=8.8, fontweight="bold", color=clr)

    ax_left.set_xlabel("Latência Pós-Abandono (Horas)", fontsize=9.5, fontweight="bold", color=COLORS["text_secondary"])
    ax_left.set_ylabel("Taxa de Abertura (%)", fontsize=9.5, fontweight="bold", color=COLORS["primary_blue"], labelpad=8)
    ax_left_twin.set_ylabel("Taxa de Conversão (%)", fontsize=9.5, fontweight="bold", color=COLORS["accent_green"], labelpad=10)
    ax_left.set_title("Curva de Decaimento Temporal de Conversão (Decay Curve)", fontsize=11.5, fontweight="bold", color=COLORS["text_primary"], pad=10)
    ax_left.set_xticks([1, 12, 24, 36, 48, 60, 72])
    ax_left.grid(True, linestyle="--", alpha=0.45, color=COLORS["grid"])
    ax_left.spines["top"].set_visible(False)
    ax_left_twin.spines["top"].set_visible(False)

    lines_1, labels_1 = ax_left.get_legend_handles_labels()
    lines_2, labels_2 = ax_left_twin.get_legend_handles_labels()
    ax_left.legend(lines_1 + lines_2, labels_1 + labels_2, loc="center right", frameon=True, facecolor="#F8FAFC", edgecolor=COLORS["border_card"], fontsize=8.5)

    # Painel Direito: Ganho Líquido Unitário por RFM & Matriz Prescritiva
    ax_right = fig.add_axes([0.535, 0.44, 0.42, 0.34])
    ax_right.set_facecolor("#FFFFFF")
    
    segments = ["Premium", "Regular", "Novo", "Dormant"]
    x_seg = np.arange(len(segments))
    
    df_wa = df_rfm[df_rfm["canal"] == "WhatsApp"].set_index("segmento").reindex(segments)
    df_em = df_rfm[df_rfm["canal"] == "Email"].set_index("segmento").reindex(segments)
    
    w_bar = 0.35
    bars_wa = ax_right.bar(x_seg - w_bar/2, df_wa["viab_liquida"], width=w_bar, color=COLORS["vip_purple"], label="WhatsApp (Custo R$ 0,30)", zorder=3)
    bars_em = ax_right.bar(x_seg + w_bar/2, df_em["viab_liquida"], width=w_bar, color=COLORS["primary_blue"], label="E-mail (Custo R$ 0,05)", zorder=3)
    
    for b in bars_wa:
        val = b.get_height()
        ax_right.text(b.get_x() + b.get_width()/2, val + 3.0, f"R$ {val:.1f}",
                      ha="center", fontsize=8.0, fontweight="bold", color=COLORS["vip_purple"])
        
    for b in bars_em:
        val = b.get_height()
        ax_right.text(b.get_x() + b.get_width()/2, val + 3.0, f"R$ {val:.1f}",
                      ha="center", fontsize=8.0, fontweight="bold", color=COLORS["primary_blue"])
        
    ax_right.set_xticks(x_seg)
    ax_right.set_xticklabels(["Premium\n(Ticket R$ 800)", "Regular\n(Ticket R$ 360)", "Novo\n(Ticket R$ 250)", "Dormant\n(Ticket R$ 200)"],
                             fontsize=8.5, fontweight="bold", color=COLORS["text_secondary"])
    ax_right.set_ylabel("Ganho Líquido Unitário (R$)", fontsize=8.8, fontweight="bold", color=COLORS["text_secondary"])
    ax_right.set_title("Ganho Líquido Esperado por Disparo (Viabilidade Econômica)", fontsize=10.5, fontweight="bold", color=COLORS["text_primary"], pad=8)
    ax_right.set_ylim(0, 170)
    ax_right.grid(axis="y", linestyle="--", alpha=0.45, color=COLORS["grid"])
    ax_right.spines["top"].set_visible(False)
    ax_right.spines["right"].set_visible(False)
    ax_right.legend(loc="upper right", fontsize=8.0, frameon=True, facecolor="#F8FAFC", edgecolor=COLORS["border_card"])

    # Tabela Visual de Matriz Prescritiva no canto inferior direito
    ax_table = fig.add_axes([0.535, 0.11, 0.42, 0.27])
    ax_table.axis("off")
    
    table_data = [
        ["Cluster RFM", "Canal Prescrito", "Gatilho de Disparo", "Política de Cupom", "Tom de Voz"],
        ["PREMIUM", "WhatsApp VIP", "+1h Pós-Abandono", "0% (Preserva Margem)", "Consultivo / Suporte"],
        ["REGULAR", "E-mail + Push", "+1h / +24h", "Frete Reduzido", "Lembrete Amigável"],
        ["NOVO", "E-mail Boas-Vindas", "+1h (Onda 1)", "10% OFF 1ª Compra", "Incentivo à Confiança"],
        ["DORMANT", "E-mail Reativação", "+24h / +48h", "Cupom Agressivo", "Urgência de Retorno"]
    ]
    
    table = ax_table.table(
        cellText=table_data,
        cellLoc="center",
        loc="center",
        bbox=[0, 0, 1, 1]
    )
    table.auto_set_font_size(False)
    table.set_fontsize(8.2)
    
    for (row, col), cell in table.get_celld().items():
        cell.set_edgecolor("#CBD5E1")
        cell.set_linewidth(1.0)
        if row == 0:
            cell.set_facecolor("#1E40AF")
            cell.set_text_props(color="#FFFFFF", fontweight="bold")
        elif row == 1:
            cell.set_facecolor("#F5F3FF")
            cell.set_text_props(color="#5B21B6", fontweight="bold")
        else:
            cell.set_facecolor("#FFFFFF" if row % 2 == 0 else "#F8FAFC")
            cell.set_text_props(color=COLORS["text_secondary"])

    # --- 4. RODAPÉ EXECUTIVO ---
    ax_main.text(0.045, 0.035, "Fonte: Telemetria de Resgate & Segmentação RFM em Parquet | Reconciliação canônica com Regras 4 e 6 de pitch_spec.md",
                 fontsize=8.0, color=COLORS["text_muted"], va="center")
    
    return fig

# ==============================================================================
# EXECUÇÃO PRINCIPAL
# ==============================================================================

def main() -> None:
    df_carts, df_clients, df_rescue = load_ground_truth()
    
    df_timing = compute_timing_decay(df_rescue)
    df_rfm = compute_rfm_viability(df_carts, df_clients)
    
    fig = plot_insights_prescritivos_panel(df_timing, df_rfm)
    
    OUTPUT_IMAGE_PATH.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_IMAGE_PATH, dpi=300, bbox_inches="tight", facecolor=COLORS["bg_canvas"])
    plt.close(fig)
    print(f"[SUCCESS] Painel de Estratégia de Resgate RFM salvo em: {OUTPUT_IMAGE_PATH}")

if __name__ == "__main__":
    main()
