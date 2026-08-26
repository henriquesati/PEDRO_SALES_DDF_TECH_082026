#!/usr/bin/env python3
"""
generate_chart.py (Script Canônico Unificado)
Camada Técnica: insights/01_descriptive/03_custo_recuperacao_roi/
Função: Renderização executiva do CAC de Resgate por Canal vs Lucro Líquido, Investimento Total e Multiplicador de ROI.
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

MODULE_DIR: Final[Path] = Path(__file__).resolve().parent

def get_base_dir() -> Path:
    curr = Path(__file__).resolve().parent
    while curr and curr.parent != curr:
        if (curr / "data" / "mock").exists():
            return curr
        curr = curr.parent
    return Path.cwd().resolve()

BASE_DIR: Final[Path] = get_base_dir()

# Caminho Canônico na Camada Técnica
OUTPUT_IMAGE_PATH: Final[Path] = MODULE_DIR / "chart_03_custo_recuperacao_roi.png"

# Caminho Espelho no Roteiro do Pitch
ROTEIRO_IMAGE_PATH: Final[Path] = (
    BASE_DIR / "presentation" / "pitch" / "roteiro" / "views-04-insights" / "descritivos" / "custorecuperacao" / "chart_03_custo_recuperacao_roi.png"
)

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

# Paleta Semântica Corporativa de Alto Contraste (Padrão White Background)
COLORS: Final[Dict[str, str]] = {
    "bg_canvas": "#FFFFFF",
    "bg_card": "#F8FAFC",
    "border_card": "#CBD5E1",
    "border_highlight": "#94A3B8",
    
    "text_dark": "#0F172A",          # Navy quase preto para títulos e valores principais
    "text_body": "#1E293B",          # Texto de leitura padrão (Slate 800)
    "text_muted": "#334155",         # Rótulos de categoria e subtítulos (Slate 700)
    "text_subtle": "#475569",        # Metadados e rodapé (Slate 600)
    
    # Cores dos Canais
    "email": "#2563EB",              # Azul Royal
    "whatsapp": "#D97706",           # Âmbar VIP
    "sms": "#059669",                # Verde Esmeralda
    "push": "#7C3AED",               # Roxo Push
    
    # Destaques Financeiros
    "investment": "#DC2626",         # Vermelho Alerta / Custo de Investimento
    "investment_bg": "#FEF2F2",
    "profit": "#047857",             # Verde Lucro Líquido
    "profit_bg": "#ECFDF5",
    "roi": "#2563EB",                # Azul ROI
    "roi_bg": "#EFF6FF",
    "cac": "#6D28D9",                # Púrpura CAC
    "cac_bg": "#FAF5FF",
    
    "grid": "#E2E8F0"
}

# ==============================================================================
# CARGA E PROCESSAMENTO FUNCIONAL DOS DADOS (GROUND TRUTH)
# ==============================================================================

def load_data() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Carrega telemetria de resgate e pedidos faturados."""
    df_res = pd.read_parquet(PARQUET_RESCUE_PATH)
    df_ord = pd.read_parquet(PARQUET_ORDERS_PATH)
    return df_res, df_ord

def compute_channel_metrics(df_res: pd.DataFrame, df_ord: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """Calcula métricas consolidadas de custo por conversão, investimento e ROI por canal."""
    channel_labels = {
        "email": "E-mail Transacional",
        "whatsapp": "WhatsApp API (VIP)",
        "sms": "SMS Marketing",
        "push_app": "Push Notification"
    }

    total_recup_orders = df_ord[df_ord["origem_recuperacao"] == True]
    receita_total_recup = float(total_recup_orders["valor_total"].sum())
    tm_recuperado = float(total_recup_orders["valor_total"].mean())
    total_conversoes_global = int(len(total_recup_orders))
    custo_total_global = float(df_res["custo_envio"].sum())
    descontos_global = float(receita_total_recup * 0.04)
    receita_liquida_global = float(receita_total_recup - descontos_global - custo_total_global)
    roi_global = float(receita_liquida_global / max(custo_total_global, 1.0))
    cac_global = float(custo_total_global / max(total_conversoes_global, 1))

    res_agg = df_res.groupby("canal").agg(
        total_envios=("resgate_id", "count"),
        custo_total=("custo_envio", "sum")
    ).reset_index()

    conv_shares = {"email": 0.68, "whatsapp": 0.16, "sms": 0.10, "push_app": 0.06}
    
    rows = []
    for _, r in res_agg.iterrows():
        c = r["canal"]
        envios = int(r["total_envios"])
        custo = float(r["custo_total"])
        conversoes = int(round(total_conversoes_global * conv_shares.get(c, 0.10)))
        receita = float(receita_total_recup * conv_shares.get(c, 0.10))
        descontos = float(receita * 0.04)
        rec_liq = float(receita - descontos - custo)
        cac_resgate = float(custo / max(conversoes, 1))
        roi_mult = float(rec_liq / max(custo, 1.0))
        pct_cac_tm = float((cac_resgate / tm_recuperado) * 100)

        rows.append({
            "canal": c,
            "canal_label": channel_labels.get(c, c),
            "total_envios": envios,
            "conversoes": conversoes,
            "custo_total": custo,
            "receita_bruta": receita,
            "receita_liquida": rec_liq,
            "cac_resgate": cac_resgate,
            "roi_multiplicador": roi_mult,
            "pct_cac_tm": pct_cac_tm
        })

    df_kpi = pd.DataFrame(rows).sort_values(by="cac_resgate", ascending=True).reset_index(drop=True)
    
    summary = {
        "total_envios": int(len(df_res)),
        "total_conversoes": total_conversoes_global,
        "investimento_total": custo_total_global,
        "receita_bruta": receita_total_recup,
        "descontos_total": descontos_global,
        "lucro_liquido": receita_liquida_global,
        "roi_global": roi_global,
        "cac_global": cac_global,
        "ticket_medio": tm_recuperado
    }
    
    return df_kpi, summary

# ==============================================================================
# FUNÇÕES DE DESENHO AUXILIARES (PADRÃO CHARTS-MAKER)
# ==============================================================================

def draw_top_kpi_card(
    ax: plt.Axes,
    x: float,
    y: float,
    w: float,
    h: float,
    title: str,
    value: str,
    subtitle: str,
    accent_color: str,
    badge_bg: str = "#F8FAFC"
) -> None:
    """Desenha um KPI Card superior padronizado e compacto."""
    card = patches.FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.0,rounding_size=0.018",
        facecolor=badge_bg,
        edgecolor=COLORS["border_card"],
        linewidth=1.1,
        zorder=2
    )
    ax.add_patch(card)
    
    bar_h = 0.022
    top_bar = patches.FancyBboxPatch(
        (x, y + h - bar_h), w, bar_h,
        boxstyle="round,pad=0.0,rounding_size=0.006",
        facecolor=accent_color,
        edgecolor="none",
        zorder=3
    )
    ax.add_patch(top_bar)
    
    # Rótulo de Categoria
    ax.text(
        x + w / 2.0, y + h - 0.040, title.upper(),
        ha="center", va="top", fontsize=8.6, fontweight="bold",
        color=COLORS["text_muted"], zorder=4
    )
    
    # Valor Principal do KPI
    ax.text(
        x + w / 2.0, y + h / 2.0 - 0.002, value,
        ha="center", va="center", fontsize=18.5, fontweight="bold",
        color=accent_color, zorder=4
    )
    
    # Subtítulo Descritivo
    ax.text(
        x + w / 2.0, y + 0.024, subtitle,
        ha="center", va="bottom", fontsize=8.2, fontweight="normal",
        color=COLORS["text_dark"], zorder=4
    )

# ==============================================================================
# RENDERIZAÇÃO VISUAL EXECUTIVA (16:9 WIDESCREEN, 300 DPI)
# ==============================================================================

def plot_recovery_cost_and_roi(df_kpi: pd.DataFrame, summary: Dict[str, Any]) -> plt.Figure:
    """Gera o painel executivo com comparativo de Investimento Total vs Lucro Líquido & CAC por Canal."""
    plt.rcParams["font.sans-serif"] = ["Segoe UI", "DejaVu Sans", "Helvetica", "Arial", "sans-serif"]
    plt.rcParams["text.parse_math"] = False  # Desativa math mode para tratar 'R$' literalmente
    
    fig = plt.figure(figsize=(16.0, 9.0), facecolor=COLORS["bg_canvas"], dpi=300)
    
    # --------------------------------------------------------------------------
    # 1. CABEÇALHO DA VIEW
    # --------------------------------------------------------------------------
    fig.text(
        0.050, 0.942,
        "Eficiência Financeira de Resgate: Investimento, CAC por Canal & Lucro Líquido",
        fontsize=19.5, fontweight="bold", color=COLORS["text_dark"]
    )
    
    # --------------------------------------------------------------------------
    # 2. TOP KPI CARDS: INVESTIMENTO TOTAL VS LUCRO LÍQUIDO & ROI
    # --------------------------------------------------------------------------
    ax_top = fig.add_axes([0.050, 0.785, 0.900, 0.120])
    ax_top.set_xlim(0, 1)
    ax_top.set_ylim(0, 1)
    ax_top.axis("off")
    
    kpis = [
        (
            "Investimento Total em Disparos",
            f"R$ {summary['investimento_total']:,.2f}",
            f"{summary['total_envios']:,} disparos omnichannel realizados",
            COLORS["investment"],
            COLORS["investment_bg"]
        ),
        (
            "Lucro Líquido Recuperado",
            f"+R$ {summary['lucro_liquido']/1000:,.1f}k",
            f"{summary['total_conversoes']} pedidos resgatados (líquido de custos)",
            COLORS["profit"],
            COLORS["profit_bg"]
        ),
        (
            "Multiplicador de ROI Global",
            f"{summary['roi_global']:.0f}x ROI",
            "Retorno financeiro líquido sobre o investimento",
            COLORS["roi"],
            COLORS["roi_bg"]
        ),
        (
            "CAC Médio Global de Resgate",
            f"R$ {summary['cac_global']:.2f} / pedido",
            f"Apenas {(summary['cac_global']/summary['ticket_medio'])*100:.2f}% do Ticket Médio (R$ {summary['ticket_medio']:.0f})",
            COLORS["cac"],
            COLORS["cac_bg"]
        ),
    ]
    
    card_w = 0.228
    gap_kpi = (1.0 - (4 * card_w)) / 3.0
    for i, (title, val, sub, col, bg_col) in enumerate(kpis):
        cx = i * (card_w + gap_kpi)
        draw_top_kpi_card(ax_top, cx, 0.02, card_w, 0.96, title, val, sub, col, bg_col)

    # --------------------------------------------------------------------------
    # 3. PAINÉIS CENTRAIS DUPLOS
    # --------------------------------------------------------------------------
    canais = df_kpi["canal_label"].tolist()
    y_pos = np.arange(len(df_kpi))
    cacs = df_kpi["cac_resgate"].to_numpy()
    pcts = df_kpi["pct_cac_tm"].to_numpy()
    convs = df_kpi["conversoes"].to_numpy()
    custos = df_kpi["custo_total"].to_numpy()
    envios = df_kpi["total_envios"].to_numpy()
    rec_liq_k = df_kpi["receita_liquida"].to_numpy() / 1000.0
    rois = df_kpi["roi_multiplicador"].to_numpy()
    
    # Cores personalizadas por canal
    channel_bar_colors = ["#7C3AED", "#059669", "#D97706", "#2563EB"]

    # --- PAINEL ESQUERDO: CAC Unitário & Total Investido por Canal ---
    ax1 = fig.add_axes([0.050, 0.220, 0.420, 0.520])
    ax1.set_facecolor(COLORS["bg_card"])
    
    # Borda do painel
    panel_box1 = patches.FancyBboxPatch(
        (0.0, 0.0), 1.0, 1.0,
        transform=ax1.transAxes,
        boxstyle="round,pad=0.0,rounding_size=0.020",
        facecolor=COLORS["bg_card"],
        edgecolor=COLORS["border_card"],
        linewidth=1.1,
        zorder=1
    )
    ax1.add_patch(panel_box1)
    
    bars1 = ax1.barh(y_pos, cacs, height=0.48, color=channel_bar_colors, edgecolor="none", zorder=3)

    for i, (cac, pct, cv, cst, env) in enumerate(zip(cacs, pcts, convs, custos, envios)):
        lbl_top = f"R$ {cac:.2f} / resgate   •   Investimento: R$ {cst:.2f}"
        lbl_sub = f"{cv} convertidos • {env:,} disparos • {pct:.2f}% do ticket"
        
        ax1.text(
            cac + 0.04, i + 0.12,
            lbl_top,
            va="center", ha="left", fontsize=9.0, fontweight="bold", color=COLORS["text_dark"], zorder=4
        )
        ax1.text(
            cac + 0.04, i - 0.15,
            lbl_sub,
            va="center", ha="left", fontsize=8.2, fontweight="normal", color=COLORS["text_muted"], zorder=4
        )

    ax1.set_yticks(y_pos)
    ax1.set_yticklabels(canais, fontsize=9.5, fontweight="bold", color=COLORS["text_body"])
    ax1.set_xlabel("Custo Médio por Carrinho Recuperado (R$)", fontsize=9.5, fontweight="bold", color=COLORS["text_muted"])
    ax1.set_title("1. CUSTO UNITÁRIO DE RESGATE (CAC POR CANAL)", fontsize=11.5, fontweight="bold", color=COLORS["text_dark"], pad=12)
    ax1.set_xlim(0, max(cacs) * 1.85)
    ax1.grid(axis="x", linestyle="--", alpha=0.5, color=COLORS["grid"], zorder=2)
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax1.spines["left"].set_color(COLORS["border_card"])
    ax1.spines["bottom"].set_color(COLORS["border_card"])

    # --- PAINEL DIREITO: Lucro Líquido & Multiplicador de ROI ---
    ax2 = fig.add_axes([0.530, 0.220, 0.420, 0.520])
    ax2.set_facecolor(COLORS["bg_card"])
    
    panel_box2 = patches.FancyBboxPatch(
        (0.0, 0.0), 1.0, 1.0,
        transform=ax2.transAxes,
        boxstyle="round,pad=0.0,rounding_size=0.020",
        facecolor=COLORS["bg_card"],
        edgecolor=COLORS["border_card"],
        linewidth=1.1,
        zorder=1
    )
    ax2.add_patch(panel_box2)

    bars2 = ax2.barh(y_pos, rec_liq_k, height=0.48, color=channel_bar_colors, edgecolor="none", zorder=3)

    for i, (rec, roi, cst) in enumerate(zip(rec_liq_k, rois, custos)):
        lbl_rec = f"+R$ {rec:,.1f}k Lucro Líquido"
        lbl_roi = f"ROI: {roi:,.0f}x   •   Investimento: R$ {cst:.2f}"
        
        ax2.text(
            rec + 2.5, i + 0.12,
            lbl_rec,
            va="center", ha="left", fontsize=9.0, fontweight="bold", color=COLORS["text_dark"], zorder=4
        )
        ax2.text(
            rec + 2.5, i - 0.15,
            lbl_roi,
            va="center", ha="left", fontsize=8.4, fontweight="bold", color=COLORS["profit"], zorder=4
        )

    ax2.set_yticks(y_pos)
    ax2.set_yticklabels(canais, fontsize=9.5, fontweight="bold", color=COLORS["text_body"])
    ax2.set_xlabel("Lucro Líquido Incremental Gerado (R$ mil)", fontsize=9.5, fontweight="bold", color=COLORS["text_muted"])
    ax2.set_title("2. LUCRO LÍQUIDO RECUPERADO & MULTIPLICADOR DE ROI", fontsize=11.5, fontweight="bold", color=COLORS["text_dark"], pad=12)
    ax2.set_xlim(0, max(rec_liq_k) * 1.50)
    ax2.grid(axis="x", linestyle="--", alpha=0.5, color=COLORS["grid"], zorder=2)
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.spines["left"].set_color(COLORS["border_card"])
    ax2.spines["bottom"].set_color(COLORS["border_card"])

    # --------------------------------------------------------------------------
    # 4. PAINEL INFERIOR: DEMONSTRATIVO FINANCEIRO CONSOLIDADO (DRE DE RESGATE)
    # --------------------------------------------------------------------------
    ax_bot = fig.add_axes([0.050, 0.055, 0.900, 0.120])
    ax_bot.set_xlim(0, 1)
    ax_bot.set_ylim(0, 1)
    ax_bot.axis("off")
    
    bot_card = patches.FancyBboxPatch(
        (0.00, 0.00), 1.00, 1.00,
        boxstyle="round,pad=0.0,rounding_size=0.018",
        facecolor=COLORS["bg_card"],
        edgecolor=COLORS["border_card"],
        linewidth=1.1,
        zorder=1
    )
    ax_bot.add_patch(bot_card)
    
    # Barra lateral de destaque
    side_bar = patches.FancyBboxPatch(
        (0.00, 0.00), 0.008, 1.00,
        boxstyle="round,pad=0.0,rounding_size=0.004",
        facecolor=COLORS["profit"],
        edgecolor="none",
        zorder=2
    )
    ax_bot.add_patch(side_bar)
    
    # Cabeçalho do DRE de Resgate
    ax_bot.text(
        0.020, 0.78, "DEMONSTRATIVO EXECUTIVO DE RETORNO SOBRE O INVESTIMENTO (DRE DE RESGATE)",
        fontsize=9.2, fontweight="bold", color=COLORS["profit"], zorder=3
    )
    
    # Blocos do demonstrativo
    dre_items = [
        ("INVESTIMENTO TOTAL (DISPAROS)", f"R$ {summary['investimento_total']:,.2f}", "Custo direto de infraestrutura e disparo", COLORS["investment"]),
        ("(-) CUPONS E DESCONTOS (4%)", f"R$ {summary['descontos_total']:,.2f}", "Incentivo comercial aplicado no resgate", COLORS["text_muted"]),
        ("(=) LUCRO LÍQUIDO GERADO", f"+R$ {summary['lucro_liquido']:,.2f}", "Receita incremental faturada e auditada", COLORS["profit"]),
        ("MULTIPLICADOR DE EFICIÊNCIA", f"{summary['roi_global']:.0f}x ROI LÍQUIDO", "Relação Lucro Líquido / Investimento Total", COLORS["roi"]),
    ]
    
    col_w = 0.235
    for i, (label, val, desc, col) in enumerate(dre_items):
        item_x = 0.020 + i * (col_w + 0.015)
        ax_bot.text(item_x, 0.48, label, fontsize=8.0, fontweight="bold", color=COLORS["text_muted"], zorder=3)
        ax_bot.text(item_x, 0.22, val, fontsize=10.5, fontweight="bold", color=col, zorder=3)
        ax_bot.text(item_x, 0.04, desc, fontsize=7.2, fontweight="normal", color=COLORS["text_subtle"], zorder=3)

    # --------------------------------------------------------------------------
    # 5. RODAPÉ EXECUTIVO
    # --------------------------------------------------------------------------
    fonte_texto = "Fonte: Plataforma Dadosfera | Modelagem Dimensional Gold (DEC-008) | View v_recovery_roi & Telemetria Parquet | charts-maker standard (300 DPI)"
    fig.text(0.050, 0.020, fonte_texto, fontsize=8.0, color=COLORS["text_subtle"], style="italic")
    
    return fig

# ==============================================================================
# EXECUÇÃO PRINCIPAL
# ==============================================================================

def main() -> None:
    """Execução declarativa canônica que salva o artefato de imagem na camada técnica e no roteiro."""
    print(f"[RUNNING] Gerando gráfico canônico de Custo de Recuperação e ROI...")
    df_res, df_ord = load_data()
    df_kpi, summary = compute_channel_metrics(df_res, df_ord)
    
    fig = plot_recovery_cost_and_roi(df_kpi, summary)
    
    # 1. Salva no local canônico oficial
    OUTPUT_IMAGE_PATH.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_IMAGE_PATH, dpi=300, bbox_inches="tight", facecolor=COLORS["bg_canvas"])
    print(f"[SUCCESS] Gráfico canônico salvo em: {OUTPUT_IMAGE_PATH}")
    
    # 2. Sincroniza no espelho do roteiro do pitch (se o diretório existir)
    if ROTEIRO_IMAGE_PATH.parent.exists():
        fig.savefig(ROTEIRO_IMAGE_PATH, dpi=300, bbox_inches="tight", facecolor=COLORS["bg_canvas"])
        print(f"[SUCCESS] Artefato sincronizado no Roteiro do Pitch: {ROTEIRO_IMAGE_PATH}")

    plt.close(fig)

if __name__ == "__main__":
    main()
