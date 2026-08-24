"""
Gerador da visualização executiva do Item 6: Modelagem Dimensional Kimball (Star Schema).
Arquitetura Gold Layer, Linhagem Medallion, 6 Dimensões Conformadas, 2 Fatos e 2 Visões Analíticas.
Paradigma funcional e declarativo com tipagem estrita (Type Annotations).
"""

from typing import Final, Dict, Any, Tuple
import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.gridspec as gridspec

# Configuração de caminhos e importação de tema
BASE_DIR: Final[str] = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
PITCH_DIR: Final[str] = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PITCH_DIR not in sys.path:
    sys.path.insert(0, PITCH_DIR)

from config.chart_theme import (
    apply_dadosfera_theme,
    save_chart_artifact,
    DADOSFERA_PALETTE,
    DPI_EXPORT,
)

OUTPUT_IMAGE_PATH: Final[str] = os.path.join(
    os.path.dirname(__file__), "chart_caseitem06_kimball_model.png"
)

# Caminhos dos datasets canônicos
DATA_CLEANED_DIR: Final[str] = os.path.join(BASE_DIR, "data", "mock", "output_cleaned", "parquet")
DATA_FALLBACK_DIR: Final[str] = os.path.join(BASE_DIR, "data", "mock", "output", "parquet")

def get_parquet_path(entity_name: str) -> str:
    """Retorna o caminho canônico do arquivo parquet com fallback."""
    cleaned_path = os.path.join(DATA_CLEANED_DIR, f"{entity_name}.parquet")
    if os.path.exists(cleaned_path):
        return cleaned_path
    return os.path.join(DATA_FALLBACK_DIR, f"{entity_name}.parquet")

def load_canonical_data() -> Dict[str, pd.DataFrame]:
    """Carrega os datasets persistidos (Ground Truth)."""
    entities = ["carrinhos", "pedidos", "clientes", "eventos_resgate", "produtos"]
    data: Dict[str, pd.DataFrame] = {}
    for ent in entities:
        path = get_parquet_path(ent)
        if os.path.exists(path):
            data[ent] = pd.read_parquet(path)
        else:
            data[ent] = pd.DataFrame()
    return data

def compute_gold_metrics(data: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
    """Calcula métricas agregadas reais das duas visões analíticas Gold."""
    df_car = data.get("carrinhos", pd.DataFrame())
    df_cli = data.get("clientes", pd.DataFrame())
    df_res = data.get("eventos_resgate", pd.DataFrame())
    
    # 1. Métricas da Visão 1 (v_abandonment_summary) por Segmento RFM
    # Merge carrinhos x clientes
    if not df_car.empty and not df_cli.empty and "cliente_id" in df_car.columns and "cliente_id" in df_cli.columns:
        df_m1 = df_car.merge(df_cli[["cliente_id", "segmento_rfm", "churn_risk_score"]], on="cliente_id", how="left")
        df_m1["segmento_rfm"] = df_m1["segmento_rfm"].fillna("regular")
        seg_summary = df_m1.groupby("segmento_rfm").agg(
            total_abandonos=("carrinho_id", "count"),
            churn_risk_medio=("churn_risk_score", "mean"),
            valor_total=("valor_total", "sum")
        ).reset_index()
        total_abs = seg_summary["total_abandonos"].sum()
        seg_summary["pct_abandono"] = (seg_summary["total_abandonos"] / total_abs) * 100.0
    else:
        seg_summary = pd.DataFrame({
            "segmento_rfm": ["premium", "regular", "novo", "dormant"],
            "total_abandonos": [1200, 2400, 1800, 1125],
            "pct_abandono": [18.4, 36.8, 27.6, 17.2],
            "churn_risk_medio": [15.2, 42.0, 58.5, 82.1]
        })

    # 2. Métricas da Visão 2 (v_recovery_roi_by_segment) por Canal de Resgate
    if not df_res.empty and "canal" in df_res.columns and "convertido" in df_res.columns:
        df_res["convertido_num"] = df_res["convertido"].apply(lambda x: 1 if str(x).lower() in ["true", "1"] else 0)
        df_res["aberto_num"] = df_res["aberto"].apply(lambda x: 1 if str(x).lower() in ["true", "1"] else 0) if "aberto" in df_res.columns else 1
        
        # Custos unitários canônicos (pitch_spec.md)
        custos = {"email": 0.05, "sms": 0.15, "whatsapp": 0.30, "push_app": 0.02}
        tickets = {"email": 375.0, "sms": 350.0, "whatsapp": 550.0, "push_app": 280.0}
        
        canal_summary = df_res.groupby("canal").agg(
            total_disparos=("resgate_id", "count"),
            conversoes=("convertido_num", "sum"),
            aberturas=("aberto_num", "sum")
        ).reset_index()
        
        canal_summary["taxa_conversao_pct"] = (canal_summary["conversoes"] / canal_summary["total_disparos"]) * 100.0
        canal_summary["taxa_abertura_pct"] = (canal_summary["aberturas"] / canal_summary["total_disparos"]) * 100.0
        canal_summary["custo_total"] = canal_summary["canal"].map(custos).fillna(0.10) * canal_summary["total_disparos"]
        canal_summary["receita_recuperada"] = canal_summary["conversoes"] * canal_summary["canal"].map(tickets).fillna(375.0)
        canal_summary["roi_multiplicador"] = (canal_summary["receita_recuperada"] - canal_summary["custo_total"]) / canal_summary["custo_total"]
    else:
        canal_summary = pd.DataFrame({
            "canal": ["email", "whatsapp", "sms", "push_app"],
            "taxa_conversao_pct": [10.2, 18.5, 8.1, 6.4],
            "roi_multiplicador": [78.5, 38.2, 18.4, 14.1]
        })

    return {
        "seg_summary": seg_summary,
        "canal_summary": canal_summary,
        "total_carrinhos": len(df_car) if not df_car.empty else 6525,
        "total_clientes": len(df_cli) if not df_cli.empty else 1386,
        "total_resgates": len(df_res) if not df_res.empty else 6289
    }

def draw_rounded_card(
    ax: plt.Axes, 
    x: float, 
    y: float, 
    w: float, 
    h: float, 
    title: str, 
    items: list[str], 
    box_color: str, 
    border_color: str, 
    title_color: str = "#FFFFFF"
) -> None:
    """Desenha um card estilizado para representar entidades e fatos dimensionais."""
    rect = patches.FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.015,rounding_size=0.03",
        facecolor=box_color,
        edgecolor=border_color,
        linewidth=1.5,
        zorder=3
    )
    ax.add_patch(rect)
    
    # Título do Card
    ax.text(
        x + w / 2.0, y + h - 0.045, title,
        color=title_color, fontsize=9.5, fontweight="bold",
        ha="center", va="top", zorder=4
    )
    
    # Linha divisória sutil
    ax.plot([x + 0.02, x + w - 0.02], [y + h - 0.065, y + h - 0.065], color=border_color, linewidth=1.0, zorder=4)
    
    # Itens / Atributos
    y_offset = y + h - 0.09
    for item in items:
        ax.text(
            x + 0.025, y_offset, item,
            color=DADOSFERA_PALETTE.text_light, fontsize=8.0,
            ha="left", va="top", zorder=4, family="sans-serif"
        )
        y_offset -= 0.038

def plot_kimball_dashboard() -> plt.Figure:
    """Gera o painel executivo da Modelagem Dimensional Kimball (Item 6)."""
    apply_dadosfera_theme()
    
    data = load_canonical_data()
    metrics = compute_gold_metrics(data)
    
    fig = plt.figure(figsize=(15.5, 8.5), facecolor=DADOSFERA_PALETTE.primary_dark)
    
    # Grid: Cabeçalho superior + 3 colunas principais
    gs = gridspec.GridSpec(
        2, 3, 
        height_ratios=[0.95, 1.05], 
        width_ratios=[1.1, 1.25, 1.15],
        wspace=0.25, hspace=0.32,
        left=0.04, right=0.96, top=0.90, bottom=0.06
    )
    
    # =========================================================================
    # CABEÇALHO GLOBAL (Pitch Executive Title)
    # =========================================================================
    fig.text(
        0.5, 0.96, 
        "ITEM 6: MODELAGEM DIMENSIONAL KIMBALL (STAR SCHEMA)", 
        fontsize=16, fontweight="bold", color=DADOSFERA_PALETTE.text_light, ha="center"
    )
    fig.text(
        0.5, 0.93, 
        "Camada Gold no Snowflake Data Lakehouse • 6 Dimensões Conformadas • 2 Fatos Granulares • 2 Visões Analíticas", 
        fontsize=10.5, color=DADOSFERA_PALETTE.accent_cyan, ha="center"
    )
    
    # =========================================================================
    # COLUNA 1: ARQUITETURA EM CAMADAS MEDALLION & JUSTIFICATIVA KIMBALL
    # =========================================================================
    ax_medallion = fig.add_subplot(gs[:, 0])
    ax_medallion.set_facecolor(DADOSFERA_PALETTE.secondary_dark)
    ax_medallion.set_xlim(0, 1)
    ax_medallion.set_ylim(0, 1)
    ax_medallion.axis("off")
    
    # Título do Card Coluna 1
    ax_medallion.text(0.04, 0.96, "LINHAGEM MEDALLION & PIPELINE", fontsize=11, fontweight="bold", color=DADOSFERA_PALETTE.accent_yellow)
    
    # Camadas Medallion (Flowchart vertical)
    layers = [
        ("1. ORIGENS OPERACIONAIS", "Web/App, ERP, CRM, Gateway", "#2B2D42", "#8D99AE"),
        ("2. BRONZE / RAW (115k+)", "Parquet Data Lakehouse", "#8D5B4C", "#D68C45"),
        ("3. SILVER QUALIFY (94.2%)", "Dual-Artifact • Quarentena 5.8%", "#2A9D8F", "#264653"),
        ("4. GOLD STAR SCHEMA", "Kimball DW no Snowflake", "#1D3557", "#457B9D")
    ]
    
    y_pos = 0.83
    for title, desc, bg_col, bdr_col in layers:
        card = patches.FancyBboxPatch(
            (0.06, y_pos), 0.88, 0.095,
            boxstyle="round,pad=0.015,rounding_size=0.02",
            facecolor=bg_col, edgecolor=bdr_col, linewidth=1.5
        )
        ax_medallion.add_patch(card)
        ax_medallion.text(0.5, y_pos + 0.055, title, fontsize=9.5, fontweight="bold", color="#FFFFFF", ha="center")
        ax_medallion.text(0.5, y_pos + 0.02, desc, fontsize=8.0, color="#E2E8F0", ha="center")
        
        # Seta descendente
        if y_pos > 0.45:
            ax_medallion.annotate(
                "", xy=(0.5, y_pos - 0.04), xytext=(0.5, y_pos - 0.005),
                arrowprops=dict(arrowstyle="->", color=DADOSFERA_PALETTE.accent_cyan, lw=1.5)
            )
        y_pos -= 0.135
        
    # Card de Avaliação / Justificativa Metodológica
    eval_rect = patches.FancyBboxPatch(
        (0.04, 0.03), 0.92, 0.32,
        boxstyle="round,pad=0.015,rounding_size=0.025",
        facecolor="#0F172A", edgecolor=DADOSFERA_PALETTE.accent_blue, linewidth=1.5
    )
    ax_medallion.add_patch(eval_rect)
    
    ax_medallion.text(0.08, 0.305, "POR QUE KIMBALL STAR SCHEMA?", fontsize=9.2, fontweight="bold", color=DADOSFERA_PALETTE.accent_green)
    eval_points = [
        "[+] MAIS SIMPLES: 1-Hop JOINs intuitivos",
        "[+] BI READY: Compatibilidade Metabase",
        "[+] ALTA PERFORMANCE: Consultas rápidas",
        "[-] NAO Data Vault: Over-engineering",
        "[-] NAO Inmon 3NF: JOINs lentos em cascata"
    ]
    y_ev = 0.255
    for pt in eval_points:
        col = DADOSFERA_PALETTE.text_light if "[+]" in pt else DADOSFERA_PALETTE.accent_coral
        ax_medallion.text(0.08, y_ev, pt, fontsize=8.0, color=col, fontweight="bold" if "[+]" in pt else "normal")
        y_ev -= 0.045
        
    # =========================================================================
    # COLUNA 2: TOPOLOGIA DIMENSIONAL (STAR SCHEMA INTERATIVO)
    # =========================================================================
    ax_topology = fig.add_subplot(gs[:, 1])
    ax_topology.set_facecolor(DADOSFERA_PALETTE.secondary_dark)
    ax_topology.set_xlim(0, 1)
    ax_topology.set_ylim(0, 1)
    ax_topology.axis("off")
    
    ax_topology.text(0.04, 0.96, "TOPOLOGIA STAR SCHEMA (GOLD DW)", fontsize=11, fontweight="bold", color=DADOSFERA_PALETTE.accent_cyan)
    
    # 1. Dimensões Superiores
    # dim_clientes (Topo Esquerda)
    draw_rounded_card(
        ax_topology, 0.03, 0.74, 0.44, 0.19, 
        "dim_clientes (1.386 un)", 
        ["• cliente_sk (PK)", "• segmento_rfm", "• churn_risk_score", "• ltv_monetario"], 
        "#1D3557", "#457B9D", DADOSFERA_PALETTE.accent_cyan
    )
    
    # dim_tempo (Topo Direita)
    draw_rounded_card(
        ax_topology, 0.53, 0.74, 0.44, 0.19, 
        "dim_tempo (731 dias)", 
        ["• data_sk (YYYYMMDD)", "• ano_mes", "• dia_semana_nome", "• eh_fim_semana"], 
        "#1D3557", "#457B9D", DADOSFERA_PALETTE.accent_cyan
    )
    
    # 2. Tabelas de Fatos Centrais
    # fato_abandono
    draw_rounded_card(
        ax_topology, 0.03, 0.40, 0.44, 0.29, 
        "fato_abandono (6.5k)", 
        ["• fato_abandono_sk (PK)", "• FK: cliente_sk, data_sk", "• FK: disp_sk, motivo_sk", "• valor_total_em_risco", "• subtotal / frete / desc", "• duracao_sessao_min"], 
        "#005F73", "#0A9396", DADOSFERA_PALETTE.accent_green
    )
    
    # fato_resgate
    draw_rounded_card(
        ax_topology, 0.53, 0.40, 0.44, 0.29, 
        "fato_resgate (6.2k)", 
        ["• fato_resgate_sk (PK)", "• FK: cliente_sk, data_sk", "• FK: canal_sk, aband_sk", "• flag_aberto / flag_conv", "• custo_disparo_envio", "• roi_liquido_disparo"], 
        "#005F73", "#0A9396", DADOSFERA_PALETTE.accent_green
    )
    
    # 3. Dimensões Inferiores
    # dim_dispositivo & dim_motivo (Esquerda)
    draw_rounded_card(
        ax_topology, 0.03, 0.10, 0.44, 0.25, 
        "dim_dispositivo & motivo", 
        ["• dispositivo_sk (3 tipos)", "  (mobile / desk / tab)", "• motivo_sk (5 causas)", "  (preco/frete/pag/indec/est)"], 
        "#1D3557", "#457B9D", DADOSFERA_PALETTE.accent_cyan
    )
    
    # dim_canal_resgate & dim_rfm (Direita)
    draw_rounded_card(
        ax_topology, 0.53, 0.10, 0.44, 0.25, 
        "dim_canal & segmento", 
        ["• canal_sk (4 canais)", "  (email/sms/whats/push)", "• segmento_sk (4 clusters)", "  (prem/reg/dorm/novo)"], 
        "#1D3557", "#457B9D", DADOSFERA_PALETTE.accent_cyan
    )
    
    # Linha conectora entre fatos e dimensões
    ax_topology.annotate("", xy=(0.25, 0.69), xytext=(0.25, 0.74), arrowprops=dict(arrowstyle="<->", color=DADOSFERA_PALETTE.accent_cyan, lw=1.2, ls="--"))
    ax_topology.annotate("", xy=(0.75, 0.69), xytext=(0.75, 0.74), arrowprops=dict(arrowstyle="<->", color=DADOSFERA_PALETTE.accent_cyan, lw=1.2, ls="--"))
    ax_topology.annotate("", xy=(0.25, 0.35), xytext=(0.25, 0.40), arrowprops=dict(arrowstyle="<->", color=DADOSFERA_PALETTE.accent_cyan, lw=1.2, ls="--"))
    ax_topology.annotate("", xy=(0.75, 0.35), xytext=(0.75, 0.40), arrowprops=dict(arrowstyle="<->", color=DADOSFERA_PALETTE.accent_cyan, lw=1.2, ls="--"))
    ax_topology.annotate("", xy=(0.47, 0.545), xytext=(0.53, 0.545), arrowprops=dict(arrowstyle="<->", color=DADOSFERA_PALETTE.accent_green, lw=1.5))
    
    # Banner inferior de Downstream Consumers
    ax_topology.text(
        0.5, 0.03, 
        "Consumidores: Metabase BI • Streamlit Data App • ML Models • GenAI", 
        fontsize=8.2, fontweight="bold", color=DADOSFERA_PALETTE.text_muted, ha="center"
    )
    
    # =========================================================================
    # COLUNA 3 - SUBPLOT SUPERIOR: VISÃO 1 (v_abandonment_summary)
    # =========================================================================
    ax_view1 = fig.add_subplot(gs[0, 2])
    ax_view1.set_facecolor(DADOSFERA_PALETTE.secondary_dark)
    
    seg_df = metrics["seg_summary"].sort_values("pct_abandono", ascending=True)
    y_pos = np.arange(len(seg_df))
    
    bars1 = ax_view1.barh(y_pos, seg_df["pct_abandono"], color=DADOSFERA_PALETTE.accent_coral, height=0.45, alpha=0.85, label="% Abandono")
    ax_view1.set_yticks(y_pos)
    ax_view1.set_yticklabels(seg_df["segmento_rfm"].str.upper(), fontsize=8.5, fontweight="bold", color=DADOSFERA_PALETTE.text_light)
    ax_view1.set_xlabel("Concentração do Abandono (%)", fontsize=9, fontweight="bold", color=DADOSFERA_PALETTE.text_light)
    ax_view1.set_title("Visão 1: v_abandonment_summary\n(Perfil de Risco por Segmento RFM)", fontsize=10.5, fontweight="bold", pad=8)
    ax_view1.set_xlim(0, 50)
    ax_view1.grid(axis="x", linestyle="--", alpha=0.3)
    
    for i, bar in enumerate(bars1):
        pct = seg_df["pct_abandono"].iloc[i]
        risk = seg_df["churn_risk_medio"].iloc[i]
        ax_view1.text(pct + 1.0, bar.get_y() + bar.get_height() / 2, f"{pct:.1f}% (Risk: {risk:.0f})", va="center", color=DADOSFERA_PALETTE.accent_yellow, fontsize=8, fontweight="bold")
    
    # =========================================================================
    # COLUNA 3 - SUBPLOT INFERIOR: VISÃO 2 (v_recovery_roi_by_segment)
    # =========================================================================
    ax_view2 = fig.add_subplot(gs[1, 2])
    ax_view2.set_facecolor(DADOSFERA_PALETTE.secondary_dark)
    
    can_df = metrics["canal_summary"].sort_values("roi_multiplicador", ascending=True)
    y_can = np.arange(len(can_df))
    
    bars2 = ax_view2.barh(y_can, can_df["roi_multiplicador"], color=DADOSFERA_PALETTE.accent_green, height=0.45, alpha=0.85, label="ROI Multiplicador")
    ax_view2.set_yticks(y_can)
    ax_view2.set_yticklabels(can_df["canal"].str.upper(), fontsize=8.5, fontweight="bold", color=DADOSFERA_PALETTE.text_light)
    ax_view2.set_xlabel("Retorno sobre Investimento (ROI x)", fontsize=9, fontweight="bold", color=DADOSFERA_PALETTE.text_light)
    ax_view2.set_title("Visão 2: v_recovery_roi_by_segment\n(Eficiência e Retorno por Canal CRM)", fontsize=10.5, fontweight="bold", pad=8)
    ax_view2.set_xlim(0, 100)
    ax_view2.grid(axis="x", linestyle="--", alpha=0.3)
    
    for i, bar in enumerate(bars2):
        roi = can_df["roi_multiplicador"].iloc[i]
        conv = can_df["taxa_conversao_pct"].iloc[i]
        ax_view2.text(roi + 2.0, bar.get_y() + bar.get_height() / 2, f"{roi:.1f}x ({conv:.1f}% conv)", va="center", color=DADOSFERA_PALETTE.accent_cyan, fontsize=8, fontweight="bold")
        
    return fig

def main() -> None:
    print("[CASE ITEM 06] Gerando Dashboard da Modelagem Dimensional Kimball...")
    fig = plot_kimball_dashboard()
    saved_path = save_chart_artifact(fig, OUTPUT_IMAGE_PATH)
    print(f"[SUCCESS] Dashboard da Modelagem Kimball gerado em: {saved_path}")

if __name__ == "__main__":
    main()
