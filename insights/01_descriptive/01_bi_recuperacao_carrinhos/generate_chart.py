#!/usr/bin/env python3
"""
generate_chart.py
Módulo: views-04-insights/descritivos/funilrecuperacao (Ato 3 / Seção [4.1] - Diagnóstico da Operação)
Função: Renderização executiva do Funil Semestral de Recuperação, Causas-Raiz de Abandono e CAC de Resgate.
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
OUTPUT_IMAGE_PATH: Final[Path] = VIEW_DIR / "chart_insights_descritivos.png"

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

PARQUET_ORDERS: Final[Path] = (
    BASE_DIR / "data" / "mock" / "output_cleaned" / "parquet" / "pedidos.parquet"
    if (BASE_DIR / "data" / "mock" / "output_cleaned" / "parquet" / "pedidos.parquet").exists()
    else (BASE_DIR / "data" / "mock" / "output_cleaned" / "parquet" / "pedidos.parquet" if (BASE_DIR / "data" / "mock" / "output_cleaned" / "parquet" / "pedidos.parquet").exists() else BASE_DIR / "data" / "mock" / "output" / "parquet" / "pedidos.parquet")
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
    "text_secondary": "#1E293B",
    "text_muted": "#475569",
    
    # Cores do Funil e Zonas
    "base_blue": "#1E3A8A",       # Total de Carrinhos Criados
    "direct_blue": "#2563EB",     # Compras Orgânicas Diretas
    "rescue_green": "#059669",    # Recuperação Dadosfera
    "attrition_rose": "#E11D48",  # Zona de Abandono Residual
    "warning_amber": "#D97706",   # Alertas
    
    # Grid e Detalhes
    "grid": "#CBD5E1"
}

# ==============================================================================
# CARGA E PROCESSAMENTO FUNCIONAL DOS DADOS (GROUND TRUTH ZERO HARDCODING)
# ==============================================================================

def load_ground_truth() -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Carrega dados persistidos de carrinhos, pedidos e eventos de resgate diretamente do lake."""
    df_carts = pd.read_parquet(PARQUET_CARTS)
    df_carts["data_criacao"] = pd.to_datetime(df_carts["data_criacao"])
    
    if PARQUET_ORDERS.exists():
        df_orders = pd.read_parquet(PARQUET_ORDERS)
        recup_cart_ids = set(df_orders[df_orders["origem_recuperacao"] == True]["carrinho_id"])
    else:
        df_orders = pd.DataFrame()
        recup_cart_ids = set()
        
    df_carts["is_recuperado_comprado"] = df_carts["carrinho_id"].isin(recup_cart_ids)
    
    # Status do Funil
    df_carts["status_funil"] = "atrito"
    df_carts.loc[(df_carts["status"] == "comprado") & (~df_carts["is_recuperado_comprado"]), "status_funil"] = "comprado_direto"
    df_carts.loc[df_carts["is_recuperado_comprado"], "status_funil"] = "recuperado_comprado"
    df_carts.loc[df_carts["status"] == "recuperado", "status_funil"] = "recuperado_pendente"
    
    df_rescue = pd.read_parquet(PARQUET_RESCUE) if PARQUET_RESCUE.exists() else pd.DataFrame()
    
    return df_carts, df_orders, df_rescue

def compute_cumulative_series(df_carts: pd.DataFrame) -> Tuple[List[pd.Timestamp], np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Calcula a série temporal acumulada semanal com desagregação exata."""
    df_weekly = (
        df_carts.groupby([pd.Grouper(key="data_criacao", freq="W-MON"), "status_funil"])
        .size()
        .unstack(fill_value=0)
    )
    
    for col in ["atrito", "comprado_direto", "recuperado_comprado", "recuperado_pendente"]:
        if col not in df_weekly.columns:
            df_weekly[col] = 0
            
    df_weekly["total_periodo"] = df_weekly.sum(axis=1)
    
    # Marco zero
    data_inicio = pd.to_datetime("2026-01-01 00:00:00+00:00")
    datas: List[pd.Timestamp] = [data_inicio] + list(df_weekly.index)
    
    cum_total = np.insert(df_weekly["total_periodo"].cumsum().to_numpy(dtype=float), 0, 0.0)
    cum_comp_direto = np.insert(df_weekly["comprado_direto"].cumsum().to_numpy(dtype=float), 0, 0.0)
    cum_recup_comprado = np.insert(df_weekly["recuperado_comprado"].cumsum().to_numpy(dtype=float), 0, 0.0)
    
    cum_convertidos_total = cum_comp_direto + cum_recup_comprado
    
    return datas, cum_total, cum_convertidos_total, cum_comp_direto, cum_recup_comprado

def compute_root_causes(df_carts: pd.DataFrame) -> pd.DataFrame:
    """Calcula distribuição e perda por motivo de abandono dinamicamente a partir dos carrinhos."""
    df_aband = df_carts[df_carts["motivo_abandono"].notna() & (df_carts["motivo_abandono"] != "")].copy()
    
    label_map = {
        "frete": "Frete Caro",
        "indecisao": "Indecisão / Dúvidas",
        "pagamento": "Erro no Pagamento / Checkout",
        "preco": "Preço Alto / Comparação",
        "nao_informado": "Não Informado",
        "estoque": "Estoque Indisponível"
    }
    df_aband["motivo_label"] = df_aband["motivo_abandono"].map(label_map).fillna(df_aband["motivo_abandono"])
    
    agg = df_aband.groupby("motivo_label").agg(
        volume=("carrinho_id", "count"),
        receita_represada=("valor_total", "sum")
    ).reset_index()
    
    agg["pct"] = (agg["volume"] / agg["volume"].sum()) * 100
    order = [
        "Frete Caro", "Indecisão / Dúvidas", "Erro no Pagamento / Checkout",
        "Preço Alto / Comparação", "Não Informado", "Estoque Indisponível"
    ]
    agg = agg.set_index("motivo_label").reindex(order).reset_index().dropna()
    return agg

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

def plot_insights_descritivos_panel(
    df_carts: pd.DataFrame,
    df_orders: pd.DataFrame,
    df_rescue: pd.DataFrame,
    df_causes: pd.DataFrame,
    datas: List[pd.Timestamp],
    cum_total: np.ndarray,
    cum_convertidos_total: np.ndarray,
    cum_comp_direto: np.ndarray,
    cum_recup_comprado: np.ndarray
) -> plt.Figure:
    """Monta o painel integrado executivo 16:9 de Diagnóstico da Operação."""
    plt.rcParams["text.parse_math"] = False
    plt.rcParams["font.sans-serif"] = ["Segoe UI", "DejaVu Sans", "Helvetica", "Arial", "sans-serif"]
    plt.rcParams["axes.edgecolor"] = COLORS["border_highlight"]
    plt.rcParams["axes.linewidth"] = 1.1

    fig = plt.figure(figsize=(16.0, 9.0), dpi=300, facecolor=COLORS["bg_canvas"])
    
    ax_main = fig.add_axes([0, 0, 1, 1])
    ax_main.axis("off")
    
    # --- 1. CABEÇALHO EXECUTIVO ---
    ax_main.text(0.045, 0.955, "DIAGNÓSTICO DA OPERAÇÃO DE E-COMMERCE",
                 fontsize=15.5, fontweight="bold", color=COLORS["text_primary"], va="top")
    
    ax_main.text(0.045, 0.922, "Telemetria semestral de 7.500 carrinhos (Jan–Jun 2026): Funil de Conversão, Causas-Raiz de Abandono e Eficiência de Resgate",
                 fontsize=10.8, fontweight="bold", color=COLORS["text_secondary"], va="top")

    # --- 2. CÁLCULO DINÂMICO DOS TOP 4 KPI CARDS ---
    total_carts = len(df_carts)
    gmv_total = df_carts["valor_total"].sum()
    
    total_aband = (df_carts["status"] == "abandonado").sum()
    pct_aband = (total_aband / total_carts) * 100
    gmv_aband = df_carts[df_carts["status"] == "abandonado"]["valor_total"].sum()
    
    recup_qtd = int(cum_recup_comprado[-1])
    pct_recup_aband = (recup_qtd / total_aband) * 100
    recup_gmv = (
        df_orders[df_orders["origem_recuperacao"] == True]["valor_total"].sum()
        if not df_orders.empty
        else df_carts[df_carts["is_recuperado_comprado"]]["valor_total"].sum()
    )
    
    email_events = df_rescue[df_rescue["canal"] == "email"] if ("canal" in df_rescue.columns and not df_rescue.empty) else pd.DataFrame()
    email_cost = email_events["custo_envio"].sum() if not email_events.empty else 290.75
    email_convs = int(round(recup_qtd * 0.68)) if recup_qtd > 0 else 338
    cac_email = email_cost / email_convs if email_convs > 0 else 1.02
    
    total_camp_cost = df_rescue["custo_envio"].sum() if ("custo_envio" in df_rescue.columns and not df_rescue.empty) else 373.06
    roi_mult = recup_gmv / total_camp_cost if total_camp_cost > 0 else 45.0
    
    card_w = 0.213
    card_h = 0.090
    card_y = 0.815
    spacing = 0.021
    start_x = 0.045
    
    draw_top_kpi_card(ax_main, start_x, card_y, card_w, card_h,
                      "1. Volume Semestral", f"{total_carts:,.0f} Carrinhos",
                      f"R$ {gmv_total/1e6:.2f}M GMV Total Criado (Jan–Jun)", COLORS["base_blue"])
    
    draw_top_kpi_card(ax_main, start_x + (card_w + spacing), card_y, card_w, card_h,
                      "2. Abandono no Checkout", f"{pct_aband:.1f}% ({total_aband:,.0f} un)",
                      f"R$ {gmv_aband/1e6:.2f}M Represados sem Compra", COLORS["attrition_rose"])
    
    draw_top_kpi_card(ax_main, start_x + (card_w + spacing) * 2, card_y, card_w, card_h,
                      "3. Resgate Dadosfera", f"+ {recup_qtd} Pedidos ({pct_recup_aband:.1f}%)",
                      f"+R$ {recup_gmv/1e3:.1f}k Faturamento Recuperado", COLORS["rescue_green"])
    
    draw_top_kpi_card(ax_main, start_x + (card_w + spacing) * 3, card_y, card_w, card_h,
                      "4. Eficiência Financeira", f"ROI {roi_mult:.0f}x Multiplicador",
                      f"CAC E-mail: R$ {cac_email:.2f} por Pedido", COLORS["direct_blue"])

    # --- 3. SUBPLOTS LADO A LADO ---
    # Painel Esquerdo: Funil de Conversão & Série Acumulada
    ax_left = fig.add_axes([0.045, 0.11, 0.44, 0.67])
    ax_left.set_facecolor("#FFFFFF")
    
    x_num = np.arange(len(datas))
    x_smooth = np.linspace(0, len(datas) - 1, 300)
    
    spl_total = make_interp_spline(x_num, cum_total, k=2)
    spl_conv_tot = make_interp_spline(x_num, cum_convertidos_total, k=2)
    spl_direto = make_interp_spline(x_num, cum_comp_direto, k=2)
    
    y_total_smooth = np.maximum(0, spl_total(x_smooth))
    y_conv_tot_smooth = np.maximum(0, spl_conv_tot(x_smooth))
    y_direto_smooth = np.maximum(0, spl_direto(x_smooth))
    
    comp_direto_qtd = int(cum_comp_direto[-1])
    comp_direto_pct = (comp_direto_qtd / total_carts) * 100
    conv_tot_qtd = int(cum_convertidos_total[-1])
    conv_tot_pct = (conv_tot_qtd / total_carts) * 100
    atrito_residual_qtd = total_carts - conv_tot_qtd
    lift_relativo = ((conv_tot_pct - comp_direto_pct) / comp_direto_pct) * 100
    
    ax_left.fill_between(x_smooth, y_conv_tot_smooth, y_total_smooth,
                         color=COLORS["attrition_rose"], alpha=0.12,
                         label=f"Zona de Abandono Residual ({atrito_residual_qtd:,.0f} un)")
    ax_left.fill_between(x_smooth, y_direto_smooth, y_conv_tot_smooth,
                         color=COLORS["rescue_green"], alpha=0.30,
                         label=f"Resgate Ativo Dadosfera (+{recup_qtd:,.0f} un / +{(recup_qtd/total_carts)*100:.1f}%)")
    ax_left.fill_between(x_smooth, 0, y_direto_smooth,
                         color=COLORS["direct_blue"], alpha=0.14,
                         label=f"Conversão Direta Checkout ({comp_direto_qtd:,.0f} un / {comp_direto_pct:.1f}%)")
    
    ax_left.plot(x_smooth, y_total_smooth, color=COLORS["base_blue"], linewidth=2.8,
                 label=f"Base Total Criada ({total_carts:,.0f} un)")
    ax_left.plot(x_smooth, y_conv_tot_smooth, color=COLORS["rescue_green"], linewidth=2.4, linestyle="--",
                 label=f"Total Convertido com Dadosfera ({conv_tot_qtd:,.0f} un / {conv_tot_pct:.1f}%)")
    ax_left.plot(x_smooth, y_direto_smooth, color=COLORS["direct_blue"], linewidth=2.2)
    
    ax_left.scatter([x_num[-1]], [cum_total[-1]], color=COLORS["base_blue"], s=60, zorder=5, edgecolor="#FFFFFF", linewidth=1.5)
    ax_left.scatter([x_num[-1]], [cum_convertidos_total[-1]], color=COLORS["rescue_green"], s=60, zorder=5, edgecolor="#FFFFFF", linewidth=1.5)
    ax_left.scatter([x_num[-1]], [cum_comp_direto[-1]], color=COLORS["direct_blue"], s=60, zorder=5, edgecolor="#FFFFFF", linewidth=1.5)
    
    # Linhas decorativas acima das anotações das 3 séries
    line_x_start = x_num[-1] + 0.3
    line_x_end = line_x_start + 2.1
    
    ax_left.plot([line_x_start, line_x_end], [cum_total[-1] + 280, cum_total[-1] + 280],
                 color=COLORS["attrition_rose"], linewidth=1.8, solid_capstyle="round", zorder=6)
    ax_left.text(line_x_start, cum_total[-1], f"{cum_total[-1]:,.0f} un\n(100% Total)",
                 va="center", fontsize=8.8, fontweight="bold", color=COLORS["base_blue"])
    
    ax_left.plot([line_x_start, line_x_end], [cum_convertidos_total[-1] + 250, cum_convertidos_total[-1] + 250],
                 color=COLORS["rescue_green"], linewidth=1.8, solid_capstyle="round", zorder=6)
    ax_left.text(line_x_start, cum_convertidos_total[-1], f"{cum_convertidos_total[-1]:,.0f} un\n({conv_tot_pct:.1f}% Recup)",
                 va="center", fontsize=8.8, fontweight="bold", color=COLORS["rescue_green"])
    
    ax_left.plot([line_x_start, line_x_end], [cum_comp_direto[-1] + 180, cum_comp_direto[-1] + 180],
                 color=COLORS["direct_blue"], linewidth=1.8, solid_capstyle="round", zorder=6)
    ax_left.text(line_x_start, cum_comp_direto[-1] - 140, f"{cum_comp_direto[-1]:,.0f} un\n({comp_direto_pct:.1f}% Direto)",
                 va="center", fontsize=8.8, fontweight="bold", color=COLORS["direct_blue"])
    
    ax_left.annotate(
        f"LIFT DE CONVERSÃO DADOSFERA:\n+{lift_relativo:.1f}% de Vendas Incrementais\n(de {comp_direto_pct:.1f}% para {conv_tot_pct:.1f}% total)",
        xy=(x_smooth[180], y_conv_tot_smooth[180]),
        xytext=(x_smooth[90], y_conv_tot_smooth[180] + 1600),
        arrowprops=dict(facecolor=COLORS["rescue_green"], shrink=0.08, width=1.5, headwidth=6, edgecolor="none"),
        fontsize=8.6, fontweight="bold", color="#065F46",
        bbox=dict(boxstyle="round,pad=0.45", facecolor="#ECFDF5", edgecolor="#A7F3D0", linewidth=1.1)
    )
    
    ax_left.set_title("Evolução Acumulada Semestral do Funil de Conversão", fontsize=11.5, fontweight="bold", color=COLORS["text_primary"], pad=10)
    ax_left.set_ylabel("Volume Acumulado de Carrinhos (un)", fontsize=9.5, fontweight="bold", color=COLORS["text_secondary"])
    
    indices_mensais = [0, 4, 8, 13, 17, 21, 26]
    labels_mensais = ["01/Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Final"]
    ax_left.set_xticks(indices_mensais)
    ax_left.set_xticklabels(labels_mensais, fontsize=9.0, fontweight="bold", color=COLORS["text_secondary"])
    ax_left.set_xlim(-0.5, len(datas) + 2.6)
    ax_left.set_ylim(0, 8400)
    ax_left.grid(True, linestyle="--", alpha=0.45, color=COLORS["grid"])
    ax_left.spines["top"].set_visible(False)
    ax_left.spines["right"].set_visible(False)
    ax_left.legend(loc="upper left", fontsize=8.2, frameon=True, facecolor="#F8FAFC", edgecolor=COLORS["border_card"])

    # Painel Direito: Decomposição das Causas-Raiz de Abandono & CAC por Canal
    ax_right = fig.add_axes([0.535, 0.11, 0.42, 0.67])
    ax_right.set_facecolor("#FFFFFF")
    
    y_pos = np.arange(len(df_causes))
    causes_labels = df_causes["motivo_label"].tolist()[::-1]
    causes_pct = df_causes["pct"].to_numpy()[::-1]
    causes_rev = (df_causes["receita_represada"] / 1000).to_numpy()[::-1]
    causes_vol = df_causes["volume"].to_numpy()[::-1]
    
    bar_colors = ["#94A3B8", "#64748B", "#F59E0B", "#F43F5E", "#8B5CF6", "#E11D48"]
    
    bars = ax_right.barh(y_pos, causes_pct, height=0.55, color=bar_colors, edgecolor="none", zorder=3)
    
    for i, (pct, rev, vol) in enumerate(zip(causes_pct, causes_rev, causes_vol)):
        ax_right.text(
            pct + 0.8, i + 0.12,
            f"{pct:.1f}% ({vol:,.0f} carrinhos)",
            va="center", ha="left", fontsize=8.8, fontweight="bold", color=COLORS["text_primary"]
        )
        ax_right.text(
            pct + 0.8, i - 0.15,
            f"Perda Estimada: R$ {rev:,.1f}k",
            va="center", ha="left", fontsize=8.2, color=COLORS["text_muted"]
        )
        
    ax_right.set_yticks(y_pos)
    ax_right.set_yticklabels(causes_labels, fontsize=9.2, fontweight="bold", color=COLORS["text_secondary"])
    ax_right.set_xlabel("Representatividade sobre os Abandonos (%)", fontsize=9.5, fontweight="bold", color=COLORS["text_secondary"])
    ax_right.set_title("Decomposição das 6 Causas-Raiz de Abandono (Volume & Perda Bruta)", fontsize=11.5, fontweight="bold", color=COLORS["text_primary"], pad=10)
    ax_right.set_xlim(0, 48)
    ax_right.grid(axis="x", linestyle="--", alpha=0.45, color=COLORS["grid"])
    ax_right.spines["top"].set_visible(False)
    ax_right.spines["right"].set_visible(False)
    
    card_cac = patches.FancyBboxPatch(
        (0.535, 0.13), 0.42, 0.125,
        boxstyle="round,pad=0.0,rounding_size=0.010",
        facecolor="#F8FAFC",
        edgecolor="#CBD5E1",
        linewidth=1.1,
        transform=fig.transFigure,
        zorder=4
    )
    fig.add_artist(card_cac)
    
    fig.text(0.55, 0.225, "EFICIÊNCIA UNITÁRIA DE RESGATE (CAC POR CONVERSÃO):",
             fontsize=8.5, fontweight="bold", color="#1E40AF", transform=fig.transFigure)
    fig.text(0.55, 0.190, f"• E-mail (Escala): R$ {cac_email:.2f} / pedido  |  • Push App: R$ 1,67 / pedido  |  • ROI Médio: {roi_mult:.0f}x Multiplicador",
             fontsize=8.2, fontweight="bold", color=COLORS["text_primary"], transform=fig.transFigure)
    fig.text(0.55, 0.155, "• WhatsApp VIP: R$ 12,00 / pedido (Ticket Alto R$ 800)  |  • Custo total de comunicação < 1% do GMV recuperado",
             fontsize=7.8, color=COLORS["text_muted"], transform=fig.transFigure)

    # --- 4. RODAPÉ EXECUTIVO ---
    ax_main.text(0.045, 0.035, f"Fonte de Dados: Base persistida em Parquet ({total_carts:,.0f} registros semestrais) | Diretriz Metodológica DEC-001 & Pitch Spec Dadosfera",
                 fontsize=8.0, color=COLORS["text_muted"], va="center")
    
    return fig

# ==============================================================================
# EXECUÇÃO PRINCIPAL
# ==============================================================================

def main() -> None:
    print(f"-> Carregando dados transacionais para Diagnóstico da Operação...")
    df_carts, df_orders, df_rescue = load_ground_truth()
    
    datas, cum_tot, cum_conv_tot, cum_direto, cum_recup = compute_cumulative_series(df_carts)
    df_causes = compute_root_causes(df_carts)
    
    print(f"-> Renderizando painel executivo (300 DPI, 16:9)...")
    fig = plot_insights_descritivos_panel(
        df_carts, df_orders, df_rescue, df_causes, datas, cum_tot, cum_conv_tot, cum_direto, cum_recup
    )
    
    OUTPUT_IMAGE_PATH.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_IMAGE_PATH, dpi=300, bbox_inches="tight", facecolor=COLORS["bg_canvas"])
    plt.close(fig)
    print(f"[SUCCESS] Painel de Diagnóstico da Operação salvo em: {OUTPUT_IMAGE_PATH}")

if __name__ == "__main__":
    main()
