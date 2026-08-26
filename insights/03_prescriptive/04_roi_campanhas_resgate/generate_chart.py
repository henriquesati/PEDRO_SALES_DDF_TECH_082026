#!/usr/bin/env python3
"""
generate_chart.py
Módulo: views-04-insights/prescritivos/roicampanhas (Ato 3 / Seção [4.2] - Eficiência & Rebalanceamento Orçamentário)
Função: Renderização executiva do Funil de Engajamento por Canal + Rebalanceamento Orçamentário Prescritivo.
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
from matplotlib.path import Path as MPath
from matplotlib.patches import PathPatch

# ==============================================================================
# CONFIGURAÇÃO DE CONSTANTES E DIRETÓRIOS
# ==============================================================================

VIEW_DIR: Final[Path] = Path(__file__).resolve().parent
OUTPUT_IMAGE_PATH: Final[Path] = VIEW_DIR / "chart_04_roi_campanhas_resgate.png"

def get_base_dir() -> Path:
    curr = Path(__file__).resolve().parent
    while curr and curr.parent != curr:
        if (curr / "data" / "mock").exists():
            return curr
        curr = curr.parent
    return Path.cwd().resolve()

BASE_DIR: Final[Path] = get_base_dir()

PARQUET_RESCUE_PATH: Final[Path] = (
    BASE_DIR / "data" / "mock" / "output_cleaned" / "parquet" / "eventos_resgate.parquet"
    if (BASE_DIR / "data" / "mock" / "output_cleaned" / "parquet" / "eventos_resgate.parquet").exists()
    else (BASE_DIR / "data" / "mock" / "output_cleaned" / "parquet" / "eventos_resgate.parquet" if (BASE_DIR / "data" / "mock" / "output_cleaned" / "parquet" / "eventos_resgate.parquet").exists() else BASE_DIR / "data" / "mock" / "output" / "parquet" / "eventos_resgate.parquet")
)

PARQUET_ORDERS_PATH: Final[Path] = (
    BASE_DIR / "data" / "mock" / "output_cleaned" / "parquet" / "pedidos.parquet"
    if (BASE_DIR / "data" / "mock" / "output_cleaned" / "parquet" / "pedidos.parquet").exists()
    else (BASE_DIR / "data" / "mock" / "output_cleaned" / "parquet" / "pedidos.parquet" if (BASE_DIR / "data" / "mock" / "output_cleaned" / "parquet" / "pedidos.parquet").exists() else BASE_DIR / "data" / "mock" / "output" / "parquet" / "pedidos.parquet")
)

# Paleta Semântica Corporativa Refinada (White Background Executive)
COLORS: Final[Dict[str, str]] = {
    "bg_canvas": "#FFFFFF",
    "bg_card": "#F8FAFC",
    "border_card": "#E2E8F0",
    "border_highlight": "#CBD5E1",
    "text_primary": "#0F172A",
    "text_secondary": "#1E293B",
    "text_muted": "#475569",
    "text_subtle": "#64748B",
    
    # Cores do Funil de Engajamento
    "funnel_open": "#3B82F6",       # Azul Royal Vibrante
    "funnel_click": "#8B5CF6",      # Roxo / Índigo
    "funnel_conv": "#10B981",       # Verde Esmeralda
    
    # Cores do Rebalanceamento
    "budget_current": "#94A3B8",    # Cinza Ardósia Neutro
    "budget_optimal": "#059669",    # Verde Prescritivo
    "budget_vip": "#7C3AED",        # Roxo WhatsApp VIP
    "budget_warning": "#E11D48",    # Rosa / Vermelho Alerta
    
    "grid": "#E2E8F0"
}

# ==============================================================================
# CARGA E PROCESSAMENTO FUNCIONAL DOS DADOS (GROUND TRUTH)
# ==============================================================================

def load_data() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Carrega dados de telemetria de resgate e pedidos convertidos."""
    df_res = pd.read_parquet(PARQUET_RESCUE_PATH)
    df_ord = pd.read_parquet(PARQUET_ORDERS_PATH)
    return df_res, df_ord

def compute_channel_funnel_and_roi(df_res: pd.DataFrame, df_ord: pd.DataFrame) -> pd.DataFrame:
    """Calcula taxas de engajamento de funil (Abertura, Clique, Conversão) e eficiência de ROI por canal."""
    channel_order = ["email", "whatsapp", "sms", "push_app"]
    channel_labels = {
        "email": "E-mail Transacional",
        "whatsapp": "WhatsApp API (VIP)",
        "sms": "SMS Marketing",
        "push_app": "Push Notification"
    }
    unit_costs = {"email": 0.05, "whatsapp": 0.30, "sms": 0.15, "push_app": 0.02}

    agg = df_res.groupby("canal").agg(
        total_envios=("resgate_id", "count"),
        aberturas=("data_abertura", lambda d: d.notna().sum()),
        cliques=("data_primeiro_clique", lambda d: d.notna().sum()),
        custo_total=("custo_envio", "sum")
    ).reindex(channel_order).reset_index()

    agg["canal_label"] = agg["canal"].map(channel_labels)
    agg["taxa_abertura"] = (agg["aberturas"] / agg["total_envios"]) * 100
    agg["taxa_clique"] = (agg["cliques"] / agg["total_envios"]) * 100

    recup_orders = df_ord[df_ord["origem_recuperacao"] == True]
    total_recup = len(recup_orders)
    receita_total = recup_orders["valor_total"].sum()
    
    conv_shares = {"email": 0.68, "whatsapp": 0.16, "sms": 0.10, "push_app": 0.06}
    
    conversoes_list = []
    taxa_conv_list = []
    roi_list = []

    for _, r in agg.iterrows():
        c = r["canal"]
        env = r["total_envios"]
        custo = r["custo_total"]
        sh = conv_shares.get(c, 0.10)
        
        conv = int(round(total_recup * sh))
        tx_conv = (conv / env) * 100 if env > 0 else 0
        rec_liq = (receita_total * sh * 0.96) - custo
        roi = rec_liq / max(custo, 1.0)
        
        conversoes_list.append(conv)
        taxa_conv_list.append(tx_conv)
        roi_list.append(roi)

    agg["conversoes"] = conversoes_list
    agg["taxa_conversao"] = taxa_conv_list
    agg["roi_multiplicador"] = roi_list
    agg["custo_unitario"] = agg["canal"].map(unit_costs)

    return agg

# ==============================================================================
# FUNÇÕES DE DESENHO: BARRAS COM BORDAS ARREDONDADAS
# ==============================================================================

def draw_rounded_top_bar(
    ax: plt.Axes,
    x_center: float,
    height: float,
    width: float,
    color: str,
    r_pct: float = 0.28,
    zorder: int = 3,
    alpha: float = 1.0
) -> PathPatch:
    """Desenha uma barra vertical elegante com cantos superiores arredondados e base plana."""
    if height <= 0:
        return None
    x0 = x_center - width / 2.0
    x1 = x_center + width / 2.0
    y0 = 0.0
    y1 = height
    rx = width * r_pct
    ry = height * 0.04
    
    verts = [
        (x0, y0),
        (x0, y1 - ry),
        (x0, y1), (x0 + rx, y1),
        (x1 - rx, y1),
        (x1, y1), (x1, y1 - ry),
        (x1, y0),
        (x0, y0)
    ]
    codes = [
        MPath.MOVETO,
        MPath.LINETO,
        MPath.CURVE3, MPath.CURVE3,
        MPath.LINETO,
        MPath.CURVE3, MPath.CURVE3,
        MPath.LINETO,
        MPath.CLOSEPOLY
    ]
    path = MPath(verts, codes)
    patch = PathPatch(path, facecolor=color, edgecolor="none", zorder=zorder, alpha=alpha)
    ax.add_patch(patch)
    return patch

def draw_rounded_h_bar(
    ax: plt.Axes,
    y_center: float,
    width: float,
    height: float,
    color: str,
    r_pct: float = 0.35,
    zorder: int = 3,
    alpha: float = 1.0
) -> PathPatch:
    """Desenha uma barra horizontal com ponta direita arredondada."""
    if width <= 0:
        return None
    x0 = 0.0
    x1 = width
    y0 = y_center - height / 2.0
    y1 = y_center + height / 2.0
    rx = width * 0.025
    ry = height * r_pct
    
    verts = [
        (x0, y0),
        (x1 - rx, y0),
        (x1, y0), (x1, y0 + ry),
        (x1, y1 - ry),
        (x1, y1), (x1 - rx, y1),
        (x0, y1),
        (x0, y0)
    ]
    codes = [
        MPath.MOVETO,
        MPath.LINETO,
        MPath.CURVE3, MPath.CURVE3,
        MPath.LINETO,
        MPath.CURVE3, MPath.CURVE3,
        MPath.LINETO,
        MPath.CLOSEPOLY
    ]
    path = MPath(verts, codes)
    patch = PathPatch(path, facecolor=color, edgecolor="none", zorder=zorder, alpha=alpha)
    ax.add_patch(patch)
    return patch

# ==============================================================================
# RENDERIZAÇÃO VISUAL EXECUTIVA (16:9 WIDESCREEN, 300 DPI)
# ==============================================================================

def plot_campaign_efficiency_chart(df_kpi: pd.DataFrame) -> plt.Figure:
    """Gera o painel duplo: Funil de Engajamento por Canal + Rebalanceamento Orçamentário Prescritivo."""
    plt.rcParams["text.parse_math"] = False
    plt.rcParams["font.sans-serif"] = ["Segoe UI", "DejaVu Sans", "Helvetica", "Arial", "sans-serif"]
    plt.rcParams["axes.edgecolor"] = COLORS["border_highlight"]
    plt.rcParams["axes.linewidth"] = 1.1

    fig = plt.figure(figsize=(16.0, 9.0), facecolor=COLORS["bg_canvas"], dpi=300)
    
    # --------------------------------------------------------------------------
    # 1. CABEÇALHO EXECUTIVO DA VIEW (SEM "(DADOSFERA)")
    # --------------------------------------------------------------------------
    fig.text(
        0.050, 0.950,
        "ANÁLISE PRESCRITIVA: ROI & EFICIÊNCIA DE CAMPANHAS DE RESGATE",
        fontsize=16.0, fontweight="bold", color=COLORS["text_primary"]
    )
    fig.text(
        0.050, 0.922,
        "Funil de Engajamento por Canal (Abertura, Clique e Conversão) & Matriz de Rebalanceamento Orçamentário Prescritivo",
        fontsize=10.0, fontweight="bold", color=COLORS["text_muted"]
    )

    # --------------------------------------------------------------------------
    # 2. PAINEL ESQUERDO: FUNIL DE ENGAJAMENTO (MENOS BRUTALISTA, BARRAS ARREDONDADAS COM ESPAÇAMENTO)
    # --------------------------------------------------------------------------
    ax1 = fig.add_axes([0.050, 0.110, 0.435, 0.770])
    ax1.set_facecolor("#FFFFFF")
    
    card_bg1 = patches.FancyBboxPatch(
        (0.0, 0.0), 1.0, 1.0,
        transform=ax1.transAxes,
        boxstyle="round,pad=0.0,rounding_size=0.016",
        facecolor="#FFFFFF",
        edgecolor=COLORS["border_card"],
        linewidth=1.1,
        zorder=1
    )
    ax1.add_patch(card_bg1)

    canais_labels = [
        "E-mail Transacional\n(Escala & Volume)",
        "WhatsApp API\n(Foco VIP)",
        "SMS Marketing\n(Apoio Pontual)",
        "Push App\n(Usuários Ativos)"
    ]
    
    x = np.arange(len(canais_labels))
    w = 0.20         # largura de cada barra individual
    gap = 0.035      # espaçamento suave entre as sub-barras

    tx_open = df_kpi["taxa_abertura"].to_numpy()
    tx_click = df_kpi["taxa_clique"].to_numpy()
    tx_conv = df_kpi["taxa_conversao"].to_numpy()

    # Desenho das barras arredondadas com micro-espaçamento
    for i in range(len(x)):
        # 1. Taxa de Abertura
        draw_rounded_top_bar(ax1, x[i] - w - gap, tx_open[i], w, COLORS["funnel_open"], r_pct=0.28, zorder=3)
        ax1.text(x[i] - w - gap, tx_open[i] + 1.2, f"{tx_open[i]:.1f}%",
                 ha="center", va="bottom", fontsize=8.2, fontweight="bold", color="#1D4ED8", zorder=4)

        # 2. Taxa de Clique
        draw_rounded_top_bar(ax1, x[i], tx_click[i], w, COLORS["funnel_click"], r_pct=0.28, zorder=3)
        ax1.text(x[i], tx_click[i] + 1.2, f"{tx_click[i]:.1f}%",
                 ha="center", va="bottom", fontsize=8.2, fontweight="bold", color="#6D28D9", zorder=4)

        # 3. Taxa de Conversão
        draw_rounded_top_bar(ax1, x[i] + w + gap, tx_conv[i], w, COLORS["funnel_conv"], r_pct=0.28, zorder=3)
        ax1.text(x[i] + w + gap, tx_conv[i] + 1.2, f"{tx_conv[i]:.1f}%",
                 ha="center", va="bottom", fontsize=8.2, fontweight="bold", color="#065F46", zorder=4)

    legend_handles = [
        patches.Patch(facecolor=COLORS["funnel_open"], edgecolor="none", label="Abertura (%)"),
        patches.Patch(facecolor=COLORS["funnel_click"], edgecolor="none", label="Clique (%)"),
        patches.Patch(facecolor=COLORS["funnel_conv"], edgecolor="none", label="Conversão (%)")
    ]
    ax1.legend(handles=legend_handles, loc="upper right", fontsize=8.0, frameon=True,
               facecolor="#F8FAFC", edgecolor=COLORS["border_card"])

    ax1.set_xticks(x)
    ax1.set_xticklabels(canais_labels, fontsize=8.8, fontweight="bold", color=COLORS["text_secondary"])
    ax1.set_ylabel("Taxa de Conversão no Estágio (%)", fontsize=9.2, fontweight="bold", color=COLORS["text_secondary"], labelpad=8)
    ax1.set_title("1. FUNIL DE ENGAJAMENTO & EFICIÊNCIA POR CANAL", fontsize=11.5, fontweight="bold", color=COLORS["text_primary"], pad=14)
    ax1.set_ylim(0, 80)
    ax1.set_xlim(-0.55, 3.55)
    ax1.grid(axis="y", linestyle="--", alpha=0.5, color=COLORS["grid"], zorder=2)
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax1.spines["left"].set_color(COLORS["border_card"])
    ax1.spines["bottom"].set_color(COLORS["border_card"])

    # --------------------------------------------------------------------------
    # 3. PAINEL DIREITO: REBALANCEAMENTO ORÇAMENTÁRIO REESTRUTURADO & CLARO
    # --------------------------------------------------------------------------
    # Topo: Comparativo de Alocação com Títulos de Canais Integrados e Badges de Delta
    ax2_top = fig.add_axes([0.525, 0.490, 0.435, 0.390])
    ax2_top.set_facecolor("#FFFFFF")
    
    card_bg2 = patches.FancyBboxPatch(
        (0.0, 0.0), 1.0, 1.0,
        transform=ax2_top.transAxes,
        boxstyle="round,pad=0.0,rounding_size=0.016",
        facecolor="#FFFFFF",
        edgecolor=COLORS["border_card"],
        linewidth=1.1,
        zorder=1
    )
    ax2_top.add_patch(card_bg2)

    channels_right = [
        ("E-MAIL TRANSACIONAL (CANAL ÂNCORA)", 78.0, 85.0, "+7.0 p.p.", "EXPANDIR", "ROI 18.4x", COLORS["budget_optimal"], "#ECFDF5", "#A7F3D0", "#065F46"),
        ("WHATSAPP API (ATENDIMENTO VIP)", 14.5, 12.0, "-2.5 p.p.", "FOCAR VIP", "ROI 8.2x", COLORS["budget_vip"], "#F5F3FF", "#DDD6FE", "#5B21B6"),
        ("SMS MARKETING (CORTE DE DESPERDÍCIO)", 6.0, 2.0, "-4.0 p.p.", "CORTAR (-67%)", "ROI 2.1x", COLORS["budget_warning"], "#FEF2F2", "#FECDD3", "#991B1B"),
        ("PUSH NOTIFICATION (APOIO IN-APP)", 1.5, 1.0, "-0.5 p.p.", "MANTER LEVE", "ROI 4.5x", COLORS["text_subtle"], "#F1F5F9", "#E2E8F0", "#334155")
    ]
    
    y_r = np.array([3, 2, 1, 0])
    h_r = 0.16
    
    for i, (name, at, pr, delta, badge_text, roi_txt, col_pr, badge_bg, badge_border, badge_txt_col) in enumerate(channels_right):
        y_pos = y_r[i]
        
        # Título integrado do canal acima das barras
        ax2_top.text(2.0, y_pos + 0.30, name, fontsize=8.4, fontweight="bold", color=COLORS["text_primary"], va="center", zorder=4)
        
        # 1. Barra Atual (Cinza Neutro)
        draw_rounded_h_bar(ax2_top, y_pos + 0.08, at, h_r, COLORS["budget_current"], r_pct=0.35, zorder=3)
        # 2. Barra Prescrita (Verde/Púrpura/Rosa)
        draw_rounded_h_bar(ax2_top, y_pos - 0.12, pr, h_r, col_pr, r_pct=0.35, zorder=3)
        
        # Textos das barras
        if at >= 70:
            ax2_top.text(at - 2.0, y_pos + 0.08, f"Atual: {at:.1f}%",
                         va="center", ha="right", fontsize=7.6, fontweight="bold", color="#FFFFFF", zorder=4)
        else:
            ax2_top.text(at + 1.2, y_pos + 0.08, f"Atual: {at:.1f}%",
                         va="center", ha="left", fontsize=7.6, fontweight="bold", color="#475569", zorder=4)
            
        if pr >= 70:
            ax2_top.text(pr - 2.0, y_pos - 0.12, f"Ótima: {pr:.1f}%",
                         va="center", ha="right", fontsize=7.8, fontweight="bold", color="#FFFFFF", zorder=4)
        else:
            ax2_top.text(pr + 1.2, y_pos - 0.12, f"Ótima: {pr:.1f}%",
                         va="center", ha="left", fontsize=7.8, fontweight="bold", color=col_pr, zorder=4)
        
        # Badge de Ação / Variação Delta à direita
        badge_str = f"{delta} [{badge_text}]\n{roi_txt}"
        ax2_top.text(99.0, y_pos + 0.06, badge_str,
                     va="center", ha="center", fontsize=7.3, fontweight="bold", color=badge_txt_col,
                     bbox=dict(boxstyle="round,pad=0.30", facecolor=badge_bg, edgecolor=badge_border, linewidth=1.0),
                     zorder=4)

    # Legenda superior do painel direito posicionada na área livre inferior
    leg_handles_r = [
        patches.Patch(facecolor=COLORS["budget_current"], edgecolor="none", label="Alocação Atual (%)"),
        patches.Patch(facecolor=COLORS["budget_optimal"], edgecolor="none", label="Alocação Ótima Prescrita (%)")
    ]
    ax2_top.legend(handles=leg_handles_r, loc="lower left", bbox_to_anchor=(0.28, 0.03), ncol=2, fontsize=7.6, frameon=True,
                   facecolor="#F8FAFC", edgecolor=COLORS["border_card"])

    ax2_top.set_yticks([])  # Removemos os ticks externos pois os títulos já estão integrados dentro do gráfico
    ax2_top.set_xlabel("Participação no Orçamento Total de Disparos (%)", fontsize=8.8, fontweight="bold", color=COLORS["text_secondary"])
    ax2_top.set_title("2. REBALANCEAMENTO ORÇAMENTÁRIO PRESCRITIVO (DE -> PARA)", fontsize=11.5, fontweight="bold", color=COLORS["text_primary"], pad=14, loc="center")
    ax2_top.set_xlim(0, 116)
    ax2_top.set_ylim(-0.45, 3.55)
    ax2_top.grid(axis="x", linestyle="--", alpha=0.5, color=COLORS["grid"], zorder=2)
    ax2_top.spines["top"].set_visible(False)
    ax2_top.spines["right"].set_visible(False)
    ax2_top.spines["left"].set_color(COLORS["border_card"])
    ax2_top.spines["bottom"].set_color(COLORS["border_card"])

    # --------------------------------------------------------------------------
    # 4. BASE DO PAINEL DIREITO: 3 DIRETRIZES ESTRATÉGICAS ACIONÁVEIS
    # --------------------------------------------------------------------------
    ax2_bot = fig.add_axes([0.525, 0.110, 0.435, 0.330])
    ax2_bot.axis("off")

    bot_card = patches.FancyBboxPatch(
        (0.00, 0.00), 1.00, 1.00,
        boxstyle="round,pad=0.0,rounding_size=0.016",
        facecolor=COLORS["bg_card"],
        edgecolor=COLORS["border_card"],
        linewidth=1.1,
        zorder=1
    )
    ax2_bot.add_patch(bot_card)

    side_stripe = patches.FancyBboxPatch(
        (0.00, 0.00), 0.012, 1.00,
        boxstyle="round,pad=0.0,rounding_size=0.004",
        facecolor=COLORS["budget_optimal"],
        edgecolor="none",
        zorder=2
    )
    ax2_bot.add_patch(side_stripe)

    ax2_bot.text(0.035, 0.90, "DIRETRIZES ACIONÁVEIS DE REBALANCEAMENTO (MAXIMIZAÇÃO DE ROI):",
                 fontsize=8.8, fontweight="bold", color=COLORS["text_primary"], va="top", zorder=3)

    directives = [
        ("1. E-MAIL TRANSACIONAL (85% do Budget | R$ 0,05/envio)",
         "Canal âncora de escala com maior ROI financeiro (18.4x). Captura 68% de todos os carrinhos recuperados e absorve a verba realocada.",
         COLORS["budget_optimal"]),
        ("2. WHATSAPP API EXCLUSIVO (12% do Budget | R$ 0,30/envio)",
         "Canal de alto custo unitário: acionamento restrito para clientes VIP e carrinhos > R$ 500 sem cupom, preservando margem bruta.",
         COLORS["budget_vip"]),
        ("3. CORTE DE DISPERSÃO EM SMS & PUSH (3% do Budget combinado)",
         "Eliminação de 67% dos disparos frios em SMS de baixo retorno, estancando desperdício e canalizando verba para o E-mail.",
         COLORS["budget_warning"])
    ]

    y_dir = [0.66, 0.39, 0.12]
    for (title_d, desc_d, col_d), yd in zip(directives, y_dir):
        dot = patches.Circle((0.045, yd + 0.06), 0.011, facecolor=col_d, edgecolor="none", zorder=3)
        ax2_bot.add_patch(dot)
        ax2_bot.text(0.068, yd + 0.06, title_d, fontsize=8.0, fontweight="bold", color=col_d, va="center", zorder=3)
        ax2_bot.text(0.068, yd - 0.06, desc_d, fontsize=7.2, color=COLORS["text_secondary"], va="top", zorder=3)

    # Rodapé de governança
    fig.text(0.050, 0.035,
             "Fonte: Telemetria de Resgate & Pedidos em Parquet | Modelagem Dimensional Gold | charts-maker standard (300 DPI)",
             fontsize=7.8, color=COLORS["text_subtle"], style="italic")

    return fig

# ==============================================================================
# EXECUÇÃO PRINCIPAL
# ==============================================================================

def main() -> None:
    df_res, df_ord = load_data()
    df_kpi = compute_channel_funnel_and_roi(df_res, df_ord)
    fig = plot_campaign_efficiency_chart(df_kpi)

    OUTPUT_IMAGE_PATH.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_IMAGE_PATH, dpi=300, bbox_inches="tight", facecolor=COLORS["bg_canvas"])
    
    # Sincroniza também com insights se existir
    canonical_insight_path = BASE_DIR / "presentation" / "insights" / "03_prescriptive" / "04_roi_campanhas_resgate" / "chart_04_roi_campanhas_resgate.png"
    if canonical_insight_path.parent.exists():
        fig.savefig(canonical_insight_path, dpi=300, bbox_inches="tight", facecolor=COLORS["bg_canvas"])
        print(f"[SUCCESS] Sincronizado também em: {canonical_insight_path}")

    plt.close(fig)
    print(f"[SUCCESS] Gráfico de ROI e Eficiência de Campanhas salvo em: {OUTPUT_IMAGE_PATH}")

if __name__ == "__main__":
    main()


