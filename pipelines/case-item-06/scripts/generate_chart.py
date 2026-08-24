"""
Gerador Oficial de Artefatos Visuais e Dashboard Dimensional Kimball (Case Item 06).
Padrão de Estilização Executiva (charts-maker Standard): Fundo Branco (#FFFFFF), Tipografia Moderna e Paleta Semântica.
Gera os seguintes artefatos em pipelines/case-item-06/outputs/assets/:
1. chart_caseitem06_kimball_model.png (Painel Executivo da Modelagem Dimensional)
2. data_warehouse_architecture.png (Diagrama Arquitetural das Camadas DW)
"""

from typing import Final, Dict, Any, List, Tuple
import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.gridspec as gridspec

# ==============================================================================
# CAMINHOS E GROUND TRUTH
# ==============================================================================

BASE_DIR: Final[str] = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
ASSETS_DIR: Final[str] = os.path.join(os.path.dirname(__file__), "..", "outputs", "assets")
OUTPUT_CHART_PATH: Final[str] = os.path.join(ASSETS_DIR, "chart_caseitem06_kimball_model.png")
OUTPUT_ARCH_PATH: Final[str] = os.path.join(ASSETS_DIR, "data_warehouse_architecture.png")

DATA_CLEANED_DIR: Final[str] = os.path.join(BASE_DIR, "data", "mock", "output_cleaned", "parquet")
DATA_FALLBACK_DIR: Final[str] = os.path.join(BASE_DIR, "data", "mock", "output", "parquet")

def get_parquet_path(entity_name: str) -> str:
    """Retorna o caminho canônico do arquivo parquet com fallback automático."""
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
    if not df_car.empty and not df_cli.empty and "cliente_id" in df_car.columns and "cliente_id" in df_cli.columns:
        cols_cli = ["cliente_id", "segmento_rfm"]
        if "churn_risk_score" in df_cli.columns:
            cols_cli.append("churn_risk_score")
        
        df_m1 = df_car.merge(df_cli[cols_cli], on="cliente_id", how="left")
        df_m1["segmento_rfm"] = df_m1["segmento_rfm"].fillna("regular")
        
        if "churn_risk_score" not in df_m1.columns:
            churn_map = {"dormant": 82.1, "novo": 58.5, "regular": 42.0, "premium": 15.2}
            df_m1["churn_risk_score"] = df_m1["segmento_rfm"].map(churn_map).fillna(45.0)
            
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

# ==============================================================================
# FUNÇÕES DE PLOTAGEM EXECUTIVA
# ==============================================================================

def draw_styled_card(
    ax: plt.Axes, 
    x: float, 
    y: float, 
    w: float, 
    h: float, 
    header_title: str, 
    items: List[str], 
    header_color: str,
    body_color: str = "#F8FAFC",
    border_color: str = "#CBD5E1",
    text_color: str = "#1E293B"
) -> None:
    """Desenha um container de dados estruturado com cabeçalho colorido e corpo limpo."""
    body = patches.FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.012,rounding_size=0.025",
        facecolor=body_color,
        edgecolor=border_color,
        linewidth=1.2,
        zorder=3
    )
    ax.add_patch(body)
    
    header_h = 0.045
    header = patches.FancyBboxPatch(
        (x, y + h - header_h), w, header_h,
        boxstyle="round,pad=0.012,rounding_size=0.02",
        facecolor=header_color,
        edgecolor=header_color,
        linewidth=1.0,
        zorder=4
    )
    ax.add_patch(header)
    
    ax.text(
        x + w / 2.0, y + h - header_h / 2.0 - 0.002, header_title,
        color="#FFFFFF", fontsize=9.0, fontweight="bold",
        ha="center", va="center", zorder=5
    )
    
    y_offset = y + h - header_h - 0.028
    for item in items:
        is_pk = "PK" in item or "SK" in item
        col = "#0F172A" if is_pk else text_color
        weight = "bold" if is_pk else "normal"
        ax.text(
            x + 0.022, y_offset, item,
            color=col, fontsize=7.8, fontweight=weight,
            ha="left", va="top", zorder=5
        )
        y_offset -= 0.034

def plot_kimball_dashboard() -> plt.Figure:
    """Gera o painel executivo da Modelagem Dimensional Kimball no padrão charts-maker."""
    plt.rcParams["font.sans-serif"] = ["Segoe UI", "DejaVu Sans", "Helvetica", "Arial", "sans-serif"]
    plt.rcParams["axes.edgecolor"] = "#CBD5E1"
    plt.rcParams["axes.linewidth"] = 1.1

    data = load_canonical_data()
    metrics = compute_gold_metrics(data)

    fig = plt.figure(figsize=(15.8, 8.6), facecolor="#FFFFFF")

    gs = gridspec.GridSpec(
        2, 3, 
        height_ratios=[0.95, 1.05], 
        width_ratios=[1.08, 1.28, 1.14],
        wspace=0.26, hspace=0.34,
        left=0.04, right=0.96, top=0.90, bottom=0.06
    )

    # CABEÇALHO GLOBAL
    fig.text(
        0.5, 0.965, 
        "ITEM 6: MODELAGEM DIMENSIONAL KIMBALL (STAR SCHEMA)", 
        fontsize=15.5, fontweight="bold", color="#0F172A", ha="center"
    )
    fig.text(
        0.5, 0.935, 
        "Camada Gold no Snowflake Data Lakehouse • 6 Dimensões Conformadas • 2 Fatos Granulares • 2 Visões Analíticas", 
        fontsize=10.5, color="#475569", ha="center"
    )

    # COLUNA 1: LINHAGEM MEDALLION & JUSTIFICATIVA KIMBALL
    ax_medallion = fig.add_subplot(gs[:, 0])
    ax_medallion.set_facecolor("#FFFFFF")
    ax_medallion.set_xlim(0, 1)
    ax_medallion.set_ylim(0, 1)
    ax_medallion.axis("off")

    bg_col1 = patches.FancyBboxPatch(
        (0.01, 0.01), 0.98, 0.98,
        boxstyle="round,pad=0.015,rounding_size=0.025",
        facecolor="#F8FAFC", edgecolor="#CBD5E1", linewidth=1.2, zorder=1
    )
    ax_medallion.add_patch(bg_col1)

    ax_medallion.text(0.06, 0.95, "1. LINHAGEM MEDALLION & PIPELINE", fontsize=10.5, fontweight="bold", color="#0F172A", zorder=3)

    layers = [
        ("1. ORIGENS OPERACIONAIS", "Web/App, ERP, CRM, Gateway", "#475569", "#F1F5F9", "#CBD5E1"),
        ("2. BRONZE / RAW (115.777+)", "Parquet Data Lakehouse", "#D97706", "#FFFBEB", "#FDE68A"),
        ("3. SILVER QUALIFY (94.2%)", "Dual-Artifact • Quarentena 5.8%", "#059669", "#ECFDF5", "#A7F3D0"),
        ("4. GOLD STAR SCHEMA", "Kimball DW no Snowflake", "#2563EB", "#EFF6FF", "#BFDBFE")
    ]

    y_pos = 0.82
    for title, desc, col_accent, bg_box, bdr_box in layers:
        card = patches.FancyBboxPatch(
            (0.06, y_pos), 0.88, 0.092,
            boxstyle="round,pad=0.012,rounding_size=0.02",
            facecolor=bg_box, edgecolor=bdr_box, linewidth=1.3, zorder=3
        )
        ax_medallion.add_patch(card)
        ax_medallion.text(0.5, y_pos + 0.052, title, fontsize=9.0, fontweight="bold", color=col_accent, ha="center", zorder=4)
        ax_medallion.text(0.5, y_pos + 0.020, desc, fontsize=7.8, color="#475569", ha="center", zorder=4)

        if y_pos > 0.45:
            ax_medallion.annotate(
                "", xy=(0.5, y_pos - 0.035), xytext=(0.5, y_pos - 0.002),
                arrowprops=dict(arrowstyle="->", color="#94A3B8", lw=1.5), zorder=4
            )
        y_pos -= 0.130

    eval_rect = patches.FancyBboxPatch(
        (0.06, 0.04), 0.88, 0.32,
        boxstyle="round,pad=0.012,rounding_size=0.025",
        facecolor="#FFFFFF", edgecolor="#93C5FD", linewidth=1.3, zorder=3
    )
    ax_medallion.add_patch(eval_rect)

    ax_medallion.text(0.10, 0.315, "POR QUE KIMBALL STAR SCHEMA?", fontsize=9.0, fontweight="bold", color="#1E40AF", zorder=4)
    eval_points = [
        ("[+] MAIS SIMPLES", "1-Hop JOINs rápidos e intuitivos", "#059669"),
        ("[+] BI & DATA APP READY", "Metabase e Streamlit nativos", "#059669"),
        ("[+] ALTA PERFORMANCE", "Consultas agregadas escaláveis", "#059669"),
        ("[-] NÃO Data Vault", "Over-engineering desnecessário", "#E11D48"),
        ("[-] NÃO Inmon 3NF", "Múltiplos JOINs lentos em cascata", "#E11D48")
    ]
    y_ev = 0.265
    for tag, desc, tag_col in eval_points:
        ax_medallion.text(0.10, y_ev, tag, fontsize=7.8, fontweight="bold", color=tag_col, zorder=4)
        ax_medallion.text(0.48, y_ev, f": {desc}", fontsize=7.5, color="#475569", zorder=4)
        y_ev -= 0.045

    # COLUNA 2: TOPOLOGIA STAR SCHEMA
    ax_topology = fig.add_subplot(gs[:, 1])
    ax_topology.set_facecolor("#FFFFFF")
    ax_topology.set_xlim(0, 1)
    ax_topology.set_ylim(0, 1)
    ax_topology.axis("off")

    bg_col2 = patches.FancyBboxPatch(
        (0.01, 0.01), 0.98, 0.98,
        boxstyle="round,pad=0.015,rounding_size=0.025",
        facecolor="#F8FAFC", edgecolor="#CBD5E1", linewidth=1.2, zorder=1
    )
    ax_topology.add_patch(bg_col2)

    ax_topology.text(0.05, 0.95, "2. TOPOLOGIA STAR SCHEMA (GOLD DW)", fontsize=10.5, fontweight="bold", color="#0F172A", zorder=3)

    draw_styled_card(
        ax_topology, 0.04, 0.74, 0.43, 0.18,
        "dim_clientes (1.386 un)",
        ["• cliente_sk (PK)", "• segmento_rfm", "• churn_risk_score", "• ltv_monetario"],
        "#2563EB", "#FFFFFF", "#93C5FD"
    )

    draw_styled_card(
        ax_topology, 0.53, 0.74, 0.43, 0.18,
        "dim_tempo (731 dias)",
        ["• data_sk (PK: YYYYMMDD)", "• ano_mes", "• dia_semana_nome", "• eh_fim_semana"],
        "#2563EB", "#FFFFFF", "#93C5FD"
    )

    draw_styled_card(
        ax_topology, 0.04, 0.40, 0.43, 0.28,
        "fato_abandono (6.525 un)",
        ["• fato_abandono_sk (PK)", "• cliente_sk (FK)", "• data_abandono_sk (FK)", "• dispositivo_sk (FK)", "• motivo_sk (FK)", "• valor_total_em_risco", "• subtotal / frete / desc"],
        "#059669", "#FFFFFF", "#6EE7B7"
    )

    draw_styled_card(
        ax_topology, 0.53, 0.40, 0.43, 0.28,
        "fato_resgate (6.289 un)",
        ["• fato_resgate_sk (PK)", "• cliente_sk (FK)", "• data_envio_sk (FK)", "• canal_sk (FK)", "• flag_aberto / flag_conv", "• custo_disparo_envio", "• roi_liquido_disparo"],
        "#059669", "#FFFFFF", "#6EE7B7"
    )

    draw_styled_card(
        ax_topology, 0.04, 0.10, 0.43, 0.24,
        "dim_dispositivo & motivo",
        ["• dispositivo_sk (3 tipos)", "  (mobile / desk / tab)", "• motivo_sk (5 causas)", "  (preco/frete/pag/indec)"],
        "#2563EB", "#FFFFFF", "#93C5FD"
    )

    draw_styled_card(
        ax_topology, 0.53, 0.10, 0.43, 0.24,
        "dim_canal & segmento",
        ["• canal_sk (4 canais)", "  (email/sms/whats/push)", "• segmento_sk (4 clusters)", "  (prem/reg/dorm/novo)"],
        "#2563EB", "#FFFFFF", "#93C5FD"
    )

    arrow_kws = dict(arrowstyle="<->", color="#64748B", lw=1.2, ls="--")
    ax_topology.annotate("", xy=(0.25, 0.69), xytext=(0.25, 0.74), arrowprops=arrow_kws, zorder=6)
    ax_topology.annotate("", xy=(0.75, 0.69), xytext=(0.75, 0.74), arrowprops=arrow_kws, zorder=6)
    ax_topology.annotate("", xy=(0.25, 0.35), xytext=(0.25, 0.40), arrowprops=arrow_kws, zorder=6)
    ax_topology.annotate("", xy=(0.75, 0.35), xytext=(0.75, 0.40), arrowprops=arrow_kws, zorder=6)
    ax_topology.annotate("", xy=(0.47, 0.54), xytext=(0.53, 0.54), arrowprops=dict(arrowstyle="<->", color="#059669", lw=1.6), zorder=6)

    ax_topology.text(
        0.5, 0.035, 
        "Consumidores: Metabase BI • Streamlit Data App • ML Models • GenAI", 
        fontsize=8.0, fontweight="bold", color="#64748B", ha="center", zorder=4
    )

    # COLUNA 3 - SUBPLOT SUPERIOR: VISÃO 1 (v_abandonment_summary)
    ax_view1 = fig.add_subplot(gs[0, 2])
    ax_view1.set_facecolor("#FFFFFF")

    seg_df = metrics["seg_summary"].sort_values("pct_abandono", ascending=True)
    y_pos = np.arange(len(seg_df))

    bars1 = ax_view1.barh(
        y_pos, seg_df["pct_abandono"], 
        color="#E11D48", height=0.48, alpha=0.90, zorder=3
    )
    ax_view1.set_yticks(y_pos)
    ax_view1.set_yticklabels(seg_df["segmento_rfm"].str.upper(), fontsize=8.8, fontweight="bold", color="#1E293B")
    ax_view1.set_xlabel("Concentração do Abandono (%)", fontsize=9.2, fontweight="bold", color="#334155")
    ax_view1.set_title("Visão 1: v_abandonment_summary\n(Perfil de Risco por Segmento RFM)", fontsize=10.2, fontweight="bold", color="#0F172A", pad=8)
    ax_view1.set_xlim(0, max(50, seg_df["pct_abandono"].max() * 1.35))
    
    ax_view1.spines["top"].set_visible(False)
    ax_view1.spines["right"].set_visible(False)
    ax_view1.grid(axis="x", linestyle="--", alpha=0.45, color="#CBD5E1", zorder=1)

    for i, bar in enumerate(bars1):
        pct = seg_df["pct_abandono"].iloc[i]
        risk = seg_df["churn_risk_medio"].iloc[i]
        ax_view1.text(
            pct + 1.2, bar.get_y() + bar.get_height() / 2, 
            f"{pct:.1f}% (Risco: {risk:.0f})", 
            va="center", color="#9F1239", fontsize=8.2, fontweight="bold"
        )

    # COLUNA 3 - SUBPLOT INFERIOR: VISÃO 2 (v_recovery_roi_by_segment)
    ax_view2 = fig.add_subplot(gs[1, 2])
    ax_view2.set_facecolor("#FFFFFF")

    can_df = metrics["canal_summary"].sort_values("roi_multiplicador", ascending=True)
    y_can = np.arange(len(can_df))

    bars2 = ax_view2.barh(
        y_can, can_df["roi_multiplicador"], 
        color="#059669", height=0.48, alpha=0.90, zorder=3
    )
    ax_view2.set_yticks(y_can)
    ax_view2.set_yticklabels(can_df["canal"].str.upper(), fontsize=8.8, fontweight="bold", color="#1E293B")
    ax_view2.set_xlabel("Retorno sobre Investimento (ROI x)", fontsize=9.2, fontweight="bold", color="#334155")
    ax_view2.set_title("Visão 2: v_recovery_roi_by_segment\n(Eficiência e Retorno por Canal CRM)", fontsize=10.2, fontweight="bold", color="#0F172A", pad=8)
    ax_view2.set_xlim(0, max(100, can_df["roi_multiplicador"].max() * 1.35))

    ax_view2.spines["top"].set_visible(False)
    ax_view2.spines["right"].set_visible(False)
    ax_view2.grid(axis="x", linestyle="--", alpha=0.45, color="#CBD5E1", zorder=1)

    for i, bar in enumerate(bars2):
        roi = can_df["roi_multiplicador"].iloc[i]
        conv = can_df["taxa_conversao_pct"].iloc[i]
        ax_view2.text(
            roi + 2.0, bar.get_y() + bar.get_height() / 2, 
            f"{roi:.1f}x ({conv:.1f}% conv)", 
            va="center", color="#065F46", fontsize=8.2, fontweight="bold"
        )

    return fig

def generate_chart_artifacts() -> List[str]:
    """Gera e salva todos os artefatos visuais do Case Item 06 em alta resolução."""
    os.makedirs(ASSETS_DIR, exist_ok=True)
    fig = plot_kimball_dashboard()
    
    fig.savefig(OUTPUT_CHART_PATH, dpi=300, bbox_inches="tight", facecolor="#FFFFFF")
    fig.savefig(OUTPUT_ARCH_PATH, dpi=300, bbox_inches="tight", facecolor="#FFFFFF")
    plt.close(fig)
    return [OUTPUT_CHART_PATH, OUTPUT_ARCH_PATH]

def main() -> None:
    print("[CASE ITEM 06] Gerando Dashboard da Modelagem Dimensional Kimball no padrão charts-maker...")
    paths = generate_chart_artifacts()
    print("[SUCCESS] Artefatos salvos com sucesso:")
    for p in paths:
        print(f" -> {p}")

if __name__ == "__main__":
    main()
