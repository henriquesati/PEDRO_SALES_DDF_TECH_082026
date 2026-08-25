"""
Gerador das visualizações oficiais do Módulo 02: Motivos de Abandono de Carrinho.
1. Treemap Hierárquico: Decomposição Proporcional de Volume por Causa-Raiz (Rótulos humanizados, sem poluição financeira).
2. Gráfico Lado a Lado de Perda Financeira por Faixa de Ticket:
   - Painel 1: Perda Financeira Bruta Represada por Faixa de Ticket (Unicolor Rose).
   - Painel 2: Impacto do Resgate Dadosfera (Montante Recuperado em Verde Esmeralda vs Residual em Rose).
Atende estritamente à especificação de presentation/insights/02_motivos_abandono/spec.md.
Paradigma funcional e declarativo com tipagem estrita (Type Annotations).
"""

from typing import Final
import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches

BASE_DIR: Final[str] = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
MODULE_DIR: Final[str] = os.path.dirname(__file__)

OUTPUT_TREEMAP_PATH: Final[str] = os.path.join(
    MODULE_DIR, "chart_02_treemap_motivos_abandono.png"
)
OUTPUT_OFFICIAL_PATH: Final[str] = os.path.join(
    MODULE_DIR, "chart_02_motivos_abandono.png"
)
OUTPUT_FINANCIAL_PATH: Final[str] = os.path.join(
    MODULE_DIR, "chart_02_perda_financeira_motivos.png"
)

PARQUET_CARTS_PATH: Final[str] = (
    os.path.join(BASE_DIR, "data", "mock", "output_cleaned", "parquet", "carrinhos.parquet")
    if os.path.exists(os.path.join(BASE_DIR, "data", "mock", "output_cleaned", "parquet", "carrinhos.parquet"))
    else os.path.join(BASE_DIR, "data", "mock", "output", "parquet", "carrinhos.parquet")
)

PARQUET_ORDERS_PATH: Final[str] = (
    os.path.join(BASE_DIR, "data", "mock", "output_cleaned", "parquet", "pedidos.parquet")
    if os.path.exists(os.path.join(BASE_DIR, "data", "mock", "output_cleaned", "parquet", "pedidos.parquet"))
    else os.path.join(BASE_DIR, "data", "mock", "output", "parquet", "pedidos.parquet")
)

def load_data() -> pd.DataFrame:
    """Carrega dados transacionais de carrinhos abandonados cruzados com pedidos recuperados (Ground Truth)."""
    df_carts = pd.read_parquet(PARQUET_CARTS_PATH)
    df_orders = pd.read_parquet(PARQUET_ORDERS_PATH)
    
    recup_cart_ids = set(df_orders[df_orders["origem_recuperacao"] == True]["carrinho_id"])
    df_carts["is_recuperado"] = df_carts["carrinho_id"].isin(recup_cart_ids)
    
    df_aband = df_carts[df_carts["motivo_abandono"].notna() & (df_carts["motivo_abandono"] != "")].copy()
    
    label_map = {
        "preco": "Preço Alto",
        "frete": "Frete Caro",
        "indecisao": "Indecisão / Dúvida",
        "pagamento": "Erro no Pagamento",
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
    return df_aband

def prepare_aggregations(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Calcula agregados consolidados por motivo e por faixa de ticket."""
    order_motivos = [
        "Preço Alto", "Frete Caro", "Indecisão / Dúvida",
        "Erro no Pagamento", "Não Informado", "Estoque Indisponível"
    ]
    
    agg_motivos = df.groupby("motivo_label").agg(
        volume=("carrinho_id", "count"),
        receita_represada=("valor_total", "sum"),
        ticket_medio=("valor_total", "mean")
    ).reindex(order_motivos).reset_index()
    
    total_vol = agg_motivos["volume"].sum()
    agg_motivos["pct_volume"] = (agg_motivos["volume"] / total_vol) * 100
    
    order_faixas = [
        "Ticket Baixo (< R$ 100)",
        "Ticket Médio-Baixo (R$ 100–250)",
        "Ticket Médio-Alto (R$ 250–500)",
        "Ticket Alto (> R$ 500)"
    ]
    
    agg_tickets = df.groupby("faixa_ticket").agg(
        volume_total=("carrinho_id", "count"),
        valor_total=("valor_total", "sum"),
        ticket_medio=("valor_total", "mean"),
        vol_recuperado=("is_recuperado", lambda s: s.sum()),
        valor_recuperado=("valor_total", lambda v: v[df.loc[v.index, "is_recuperado"]].sum())
    ).reindex(order_faixas).reset_index()
    
    agg_tickets["valor_residual"] = agg_tickets["valor_total"] - agg_tickets["valor_recuperado"]
    agg_tickets["pct_valor_total"] = (agg_tickets["valor_total"] / agg_tickets["valor_total"].sum()) * 100
    agg_tickets["pct_recuperado_val"] = (agg_tickets["valor_recuperado"] / agg_tickets["valor_total"]) * 100
    agg_tickets["pct_recuperado_vol"] = (agg_tickets["vol_recuperado"] / agg_tickets["volume_total"]) * 100
    
    return agg_motivos, agg_tickets

def plot_treemap_chart(agg_motivos: pd.DataFrame) -> plt.Figure:
    """Gera o Treemap Hierárquico Proporcional ao volume, sem cifras financeiras."""
    plt.rcParams["font.sans-serif"] = ["Segoe UI", "DejaVu Sans", "Helvetica", "Arial", "sans-serif"]
    
    fig, ax = plt.subplots(figsize=(13.5, 7.2))
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")
    ax.axis("off")
    
    # Blocos com paleta harmonizada com a identidade visual Dadosfera
    # As descrições e percentuais são obtidos dinamicamente de agg_motivos (Ground Truth)
    motivo_stats = agg_motivos.set_index("motivo_label")
    total_vol = agg_motivos["volume"].sum()
    
    rect_configs = [
        {"name": "Preço Alto", "desc_base": "carrinhos abandonados por preços elevados", "bbox": [0.0, 0.50, 0.50, 0.50], "color": "#1E3A8A", "text_col": "#FFFFFF"},
        {"name": "Frete Caro", "desc_base": "carrinhos abandonados por frete muito caro", "bbox": [0.50, 0.50, 0.50, 0.50], "color": "#2563EB", "text_col": "#FFFFFF"},
        {"name": "Indecisão / Dúvida", "desc_base": "carrinhos abandonados por indecisão ou dúvida", "bbox": [0.0, 0.0, 0.40, 0.50], "color": "#059669", "text_col": "#FFFFFF"},
        {"name": "Erro no Pagamento", "desc_base": "carrinhos abandonados por falhas no pagamento", "bbox": [0.40, 0.0, 0.35, 0.50], "color": "#D97706", "text_col": "#FFFFFF"},
        {"name": "Não Informado", "desc_base": "carrinhos abandonados sem motivo declarado", "bbox": [0.75, 0.22, 0.25, 0.28], "color": "#64748B", "text_col": "#FFFFFF"},
        {"name": "Estoque Indisponível", "desc_base": "carrinhos abandonados por falta de estoque", "bbox": [0.75, 0.0, 0.25, 0.22], "color": "#94A3B8", "text_col": "#0F172A"}
    ]
    
    for r in rect_configs:
        x, y, w, h = r["bbox"]
        name = r["name"]
        
        # Recupera valores reais dinamicamente
        vol = int(motivo_stats.loc[name, "volume"]) if name in motivo_stats.index else 0
        pct = float(motivo_stats.loc[name, "pct_volume"]) if name in motivo_stats.index else 0.0
        desc = f"{vol:,.0f} {r['desc_base']}".replace(",", ".")
        
        rect_patch = patches.Rectangle((x, y), w, h, facecolor=r["color"], edgecolor="#FFFFFF", linewidth=3.5)
        ax.add_patch(rect_patch)
        
        cx, cy = x + w / 2, y + h / 2
        ax.text(cx, cy + h * 0.12, name, ha="center", va="center", color=r["text_col"], fontsize=12.5, fontweight="bold")
        ax.text(cx, cy - h * 0.04, f"{pct:.1f}% do abandono", ha="center", va="center", color=r["text_col"], fontsize=11, fontweight="bold")
        ax.text(cx, cy - h * 0.20, desc, ha="center", va="center", color=r["text_col"], fontsize=9.5, fontweight="normal", alpha=0.92)

    ax.set_xlim(-0.01, 1.01)
    ax.set_ylim(-0.01, 1.06)
    ax.set_title(f"DECOMPOSIÇÃO DE VOLUME: CAUSAS-RAIZ DE ABANDONO DE CARRINHO ({total_vol:,.0f} UN)".replace(",", "."),
                 fontsize=14.5, fontweight="bold", color="#0F172A", pad=15)
                 
    plt.tight_layout()
    return fig

def plot_side_by_side_financial_loss_chart(agg_tickets: pd.DataFrame) -> plt.Figure:
    """Gera o Gráfico Lado a Lado de Perda Financeira por Faixa de Ticket e Impacto do Resgate."""
    plt.rcParams["font.sans-serif"] = ["Segoe UI", "DejaVu Sans", "Helvetica", "Arial", "sans-serif"]
    plt.rcParams["axes.edgecolor"] = "#CBD5E1"
    plt.rcParams["axes.linewidth"] = 1.1

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15.0, 6.8), gridspec_kw={"width_ratios": [1.0, 1.18]})
    fig.patch.set_facecolor("#FFFFFF")

    faixas = agg_tickets["faixa_ticket"].tolist()
    y_pos = np.arange(len(agg_tickets))
    val_total_k = agg_tickets["valor_total"].to_numpy() / 1000.0
    val_rec_k = agg_tickets["valor_recuperado"].to_numpy() / 1000.0
    val_res_k = agg_tickets["valor_residual"].to_numpy() / 1000.0
    pcts_tot = agg_tickets["pct_valor_total"].to_numpy()
    pcts_rec = agg_tickets["pct_recuperado_val"].to_numpy()
    vols = agg_tickets["volume_total"].to_numpy()
    vols_rec = agg_tickets["vol_recuperado"].to_numpy()
    
    total_represado_k = val_total_k.sum()
    total_rec_k = val_rec_k.sum()
    
    bar_height = 0.52

    # --- PAINEL 1: Perda Financeira Bruta por Faixa de Ticket (Unicolor Rose Dadosfera) ---
    ax1.set_facecolor("#FFFFFF")
    bars1 = ax1.barh(y_pos, val_total_k, height=bar_height, color="#E11D48", alpha=0.88, edgecolor="#9F1239", linewidth=1.2)

    for i, (val, pct, vol) in enumerate(zip(val_total_k, pcts_tot, vols)):
        ax1.text(
            val + 15, i,
            f"R$ {val:,.1f}k ({pct:.1f}% da perda)\n{vol:,.0f} carrinhos abandonados",
            va="center", ha="left", fontsize=9.5, fontweight="bold", color="#0F172A"
        )

    ax1.set_yticks(y_pos)
    ax1.set_yticklabels(faixas, fontsize=10.5, fontweight="bold", color="#1E293B")
    ax1.set_xlabel("Perda Financeira Represada (R$ Milhares)", fontsize=11, fontweight="bold", color="#334155")
    ax1.set_title("1. PERDA FINANCEIRA BRUTA POR TICKET", fontsize=12.5, fontweight="bold", color="#0F172A", pad=12)
    ax1.set_xlim(0, max(val_total_k) * 1.38)
    ax1.grid(axis="x", linestyle="--", alpha=0.5, color="#CBD5E1")
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)

    # --- PAINEL 2: Impacto do Resgate Dadosfera (Recuperado em Verde vs Residual em Rose) ---
    ax2.set_facecolor("#FFFFFF")
    
    # Barra Residual (Rose suave com borda)
    bars_res = ax2.barh(y_pos, val_res_k, height=bar_height, color="#E11D48", alpha=0.75,
                        label="Perda Residual Não Recuperada", edgecolor="#9F1239", linewidth=1.2)
    # Barra Recuperada (Verde Esmeralda harmonizado com o BI de Resgate)
    bars_rec = ax2.barh(y_pos, val_rec_k, height=bar_height, left=val_res_k, color="#059669", alpha=0.95,
                        label="Montante Recuperado (Dadosfera)", edgecolor="#022C22", linewidth=2.0)

    for i, (total, rec, res, pct_r, v_rec) in enumerate(zip(val_total_k, val_rec_k, val_res_k, pcts_rec, vols_rec)):
        ax2.text(
            total + 15, i,
            f"Resgate: +R$ {rec:,.1f}k ({pct_r:.1f}%)\n{v_rec} carrinhos convertidos",
            va="center", ha="left", fontsize=9.5, fontweight="bold", color="#065F46"
        )

    ax2.set_yticks(y_pos)
    ax2.set_yticklabels([])
    ax2.set_xlabel("Receita em Risco vs Recuperada (R$ Milhares)", fontsize=11, fontweight="bold", color="#334155")
    ax2.set_title("2. IMPACTO DO RESGATE: RECUPERADO vs RESIDUAL", fontsize=12.5, fontweight="bold", color="#0F172A", pad=12)
    ax2.set_xlim(0, max(val_total_k) * 1.45)
    ax2.grid(axis="x", linestyle="--", alpha=0.5, color="#CBD5E1")
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.legend(loc="lower right", frameon=True, facecolor="#F8FAFC", edgecolor="#CBD5E1", fontsize=9.5)

    # Título Consolidado
    fig.suptitle(f"IMPACTO FINANCEIRO POR FAIXA DE TICKET: PERDA BRUTA vs RESGATE DADOSFERA (TOTAL: R$ {total_represado_k:,.1f}k | RESGATE: R$ {total_rec_k:,.1f}k)",
                 fontsize=14, fontweight="bold", color="#0F172A", y=0.98)

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    return fig

def main() -> None:
    df_data = load_data()
    agg_motivos, agg_tickets = prepare_aggregations(df_data)

    # 1. Gráfico de Treemap de Volume por Causa-Raiz
    fig_tree = plot_treemap_chart(agg_motivos)
    fig_tree.savefig(OUTPUT_TREEMAP_PATH, dpi=300, bbox_inches="tight", facecolor="#FFFFFF")
    fig_tree.savefig(OUTPUT_OFFICIAL_PATH, dpi=300, bbox_inches="tight", facecolor="#FFFFFF")
    plt.close(fig_tree)
    print(f"[SUCCESS] Treemap de Motivos salvo em: {OUTPUT_TREEMAP_PATH}")

    # 2. Gráfico Lado a Lado de Perda Financeira por Faixa de Ticket
    fig_fin = plot_side_by_side_financial_loss_chart(agg_tickets)
    fig_fin.savefig(OUTPUT_FINANCIAL_PATH, dpi=300, bbox_inches="tight", facecolor="#FFFFFF")
    plt.close(fig_fin)
    print(f"[SUCCESS] Gráfico de Perda Financeira por Ticket salvo em: {OUTPUT_FINANCIAL_PATH}")

if __name__ == "__main__":
    main()
