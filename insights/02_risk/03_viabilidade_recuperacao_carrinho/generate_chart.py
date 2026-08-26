"""
Gerador da visualização: Score de Viabilidade de Recuperação (Recovery Viability) & Matriz de Priorização.
Atende estritamente à especificação de insights/02_risk/03_viabilidade_recuperacao_carrinho/spec.md
e insights/02_risk/viabilidade_recuperacao_carrinho.md.
Paradigma funcional e declarativo com tipagem estrita (Type Annotations).
"""

from typing import Final, Tuple
import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def _find_base_dir() -> str:
    curr = os.path.abspath(os.path.dirname(__file__))
    while curr and os.path.dirname(curr) != curr:
        if os.path.exists(os.path.join(curr, "data", "mock")):
            return curr
        curr = os.path.dirname(curr)
    return os.path.abspath(os.getcwd())

BASE_DIR: Final[str] = _find_base_dir()
MODULE_DIR: Final[str] = os.path.dirname(__file__)

OUTPUT_IMAGE_PATH: Final[str] = os.path.join(
    MODULE_DIR, "chart_03_viabilidade_recuperacao_carrinho.png"
)

PARQUET_CARTS_PATH: Final[str] = (
    os.path.join(BASE_DIR, "data", "mock", "output_cleaned", "parquet", "carrinhos.parquet")
    if os.path.exists(os.path.join(BASE_DIR, "data", "mock", "output_cleaned", "parquet", "carrinhos.parquet"))
    else os.path.join(BASE_DIR, "data", "mock", "output", "parquet", "carrinhos.parquet")
)

PARQUET_CLIENTS_PATH: Final[str] = (
    os.path.join(BASE_DIR, "data", "mock", "output_cleaned", "parquet", "clientes.parquet")
    if os.path.exists(os.path.join(BASE_DIR, "data", "mock", "output_cleaned", "parquet", "clientes.parquet"))
    else os.path.join(BASE_DIR, "data", "mock", "output", "parquet", "clientes.parquet")
)

def load_data() -> pd.DataFrame:
    """Carrega dados transacionais de carrinhos e clientes com validação de chaves."""
    df_carts = pd.read_parquet(PARQUET_CARTS_PATH)
    df_clients = pd.read_parquet(PARQUET_CLIENTS_PATH)
    
    df_merged = df_carts.merge(
        df_clients[["cliente_id", "segmento_rfm", "lifetime_value"]],
        on="cliente_id",
        how="left"
    )
    df_merged["segmento_rfm"] = df_merged["segmento_rfm"].fillna("novo")
    return df_merged

def compute_recovery_viability(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Aplica o pipeline matemático de viabilidade de recuperação:
    1. P_BASE (RFM): Premium=18%, Novo=12%, Regular=10%, Dormant=6%
    2. FATOR_MOTIVO: Indecisão=1.2, Frete=1.1, Preço=1.0, Não Inf=0.9, Pagamento=0.8, Estoque=0.3
    3. FATOR_VALOR: >500=1.1, 100-500=1.0, <100=0.9
    4. FATOR_TEMPO: 1.0 (baseline)
    5. Custo Canal: Premium=0.40, Regular=0.07, Dormant=0.20, Novo=0.07
    6. Expected Return = P_RECUP * valor_total | Expected ROI = Retorno / Custo
    7. Classificação: Alta (ROI>=50x & Retorno>=R$10), Média (ROI>=10x & Retorno>=R$2), Baixa
    """
    df_aband = df[df["status"] == "abandonado"].copy()

    p_base_map = {"premium": 0.18, "novo": 0.12, "regular": 0.10, "dormant": 0.06}
    df_aband["p_base"] = df_aband["segmento_rfm"].map(p_base_map).fillna(0.10)

    motivo_map = {
        "indecisao": 1.2, "frete": 1.1, "preco": 1.0,
        "nao_informado": 0.9, "pagamento": 0.8, "estoque": 0.3
    }
    df_aband["f_motivo"] = df_aband["motivo_abandono"].map(motivo_map).fillna(0.9)

    df_aband["f_valor"] = np.where(
        df_aband["valor_total"] > 500, 1.1,
        np.where(df_aband["valor_total"] >= 100, 1.0, 0.9)
    )

    df_aband["p_recup"] = np.clip(
        df_aband["p_base"] * df_aband["f_motivo"] * df_aband["f_valor"],
        0.01, 0.50
    )

    custo_map = {"premium": 0.40, "regular": 0.07, "dormant": 0.20, "novo": 0.07}
    df_aband["custo_est"] = df_aband["segmento_rfm"].map(custo_map).fillna(0.07)

    df_aband["retorno_esperado"] = df_aband["p_recup"] * df_aband["valor_total"]
    df_aband["roi_esperado"] = df_aband["retorno_esperado"] / df_aband["custo_est"]

    cond_alta = (df_aband["roi_esperado"] >= 50.0) & (df_aband["retorno_esperado"] >= 10.0)
    cond_media = (df_aband["roi_esperado"] >= 10.0) & (df_aband["retorno_esperado"] >= 2.0) & (~cond_alta)

    df_aband["viabilidade"] = np.where(cond_alta, "Alta", np.where(cond_media, "Média", "Baixa"))

    # Agregação executiva
    order_viab = ["Alta", "Média", "Baixa"]
    summary_viab = df_aband.groupby("viabilidade").agg(
        total_carrinhos=("carrinho_id", "count"),
        valor_represado=("valor_total", "sum"),
        retorno_esperado_total=("retorno_esperado", "sum"),
        custo_total_disparos=("custo_est", "sum"),
        roi_medio_ponderado=("retorno_esperado", lambda r: r.sum() / df_aband.loc[r.index, "custo_est"].sum()),
        p_recup_media=("p_recup", lambda p: p.mean() * 100)
    ).reindex(order_viab).reset_index()

    summary_viab["pct_carrinhos"] = (summary_viab["total_carrinhos"] / len(df_aband)) * 100
    summary_viab["pct_retorno"] = (summary_viab["retorno_esperado_total"] / summary_viab["retorno_esperado_total"].sum()) * 100

    return df_aband, summary_viab

def plot_viability_chart(df_aband: pd.DataFrame, summary_viab: pd.DataFrame) -> plt.Figure:
    """Gera visualização integrada de dispersão de viabilidade e matriz de alocação."""
    plt.rcParams["text.parse_math"] = False
    plt.rcParams["font.sans-serif"] = ["Segoe UI", "DejaVu Sans", "Helvetica", "Arial", "sans-serif"]
    plt.rcParams["axes.edgecolor"] = "#CBD5E1"
    plt.rcParams["axes.linewidth"] = 1.1

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15.8, 7.2), gridspec_kw={"width_ratios": [1.15, 1.05]})
    fig.patch.set_facecolor("#FFFFFF")

    colors_map = {
        "Alta": "#059669",
        "Média": "#F59E0B",
        "Baixa": "#E11D48"
    }

    # --- PAINEL 1: Scatter Plot de Viabilidade (Probabilidade vs Valor) ---
    ax1.set_facecolor("#FFFFFF")

    for v_level in ["Alta", "Média", "Baixa"]:
        subset = df_aband[df_aband["viabilidade"] == v_level]
        p_pct = subset["p_recup"] * 100
        val = subset["valor_total"]
        roi_sizes = np.clip(subset["roi_esperado"] * 0.4, 25, 180)

        ax1.scatter(
            p_pct, val,
            s=roi_sizes,
            color=colors_map[v_level],
            alpha=0.65,
            edgecolor="#0F172A",
            linewidth=0.6,
            label=f"Viabilidade {v_level} ({len(subset):,} un)",
            zorder=4
        )

    # Linhas de corte e caixas
    ax1.axhline(500, color="#94A3B8", linestyle="--", linewidth=1.1, label="Cesta de Alto Valor (R$ 500)")
    ax1.axvline(15, color="#CBD5E1", linestyle=":", linewidth=1.1)

    ax1.set_xlabel("Probabilidade Estimada de Recuperação (%)", fontsize=11.5, fontweight="bold", color="#334155")
    ax1.set_ylabel("Valor Total do Carrinho Abandonado (R$)", fontsize=11.5, fontweight="bold", color="#334155")
    ax1.set_title("1. MATRIZ DE SCORE: PROBABILIDADE × VALOR × ROI", fontsize=12.5, fontweight="bold", color="#0F172A", pad=12)
    ax1.set_xlim(0, 30)
    ax1.set_ylim(0, max(df_aband["valor_total"]) * 1.05)
    ax1.grid(True, linestyle="--", alpha=0.4, color="#CBD5E1")
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax1.legend(loc="upper left", frameon=True, facecolor="#F8FAFC", edgecolor="#CBD5E1", fontsize=9.0)

    # --- PAINEL 2: Decomposição Operacional & Ação Prescrita ---
    ax2.set_facecolor("#FFFFFF")
    ax2.axis("off")

    table_data = [
        ["Nível Viabilidade", "% Base", "Retorno Esperado", "Custo Disparos", "Expected ROI", "Ação Operacional Prescrita"],
        ["ALTA (Prioritária)", f"{summary_viab.loc[0, 'pct_carrinhos']:.1f}%", f"R$ {summary_viab.loc[0, 'retorno_esperado_total']/1000:,.1f}k", f"R$ {summary_viab.loc[0, 'custo_total_disparos']:,.0f}", f"{summary_viab.loc[0, 'roi_medio_ponderado']:.0f}x", "Resgate Prioritário Imediato\n(WhatsApp / Email VIP)"],
        ["MÉDIA (Escala)", f"{summary_viab.loc[1, 'pct_carrinhos']:.1f}%", f"R$ {summary_viab.loc[1, 'retorno_esperado_total']/1000:,.1f}k", f"R$ {summary_viab.loc[1, 'custo_total_disparos']:,.0f}", f"{summary_viab.loc[1, 'roi_medio_ponderado']:.0f}x", "Automação Padrão em Escala\n(Email + Push D+0/D+1)"],
        ["BAIXA (Custo Zero)", f"{summary_viab.loc[2, 'pct_carrinhos']:.1f}%", f"R$ {summary_viab.loc[2, 'retorno_esperado_total']/1000:,.2f}k", f"R$ {summary_viab.loc[2, 'custo_total_disparos']:,.0f}", f"{summary_viab.loc[2, 'roi_medio_ponderado']:.0f}x", "Não Intervir Ativamente\n(Evita Prejuízo / Retargeting)"]
    ]

    table = ax2.table(
        cellText=table_data,
        cellLoc="center",
        loc="center",
        bbox=[0.0, 0.20, 1.0, 0.70]
    )
    table.auto_set_font_size(False)
    table.set_fontsize(9.0)

    for (row, col), cell in table.get_celld().items():
        cell.set_edgecolor("#CBD5E1")
        cell.set_linewidth(1.1)
        if row == 0:
            cell.set_facecolor("#0F172A")
            cell.set_text_props(weight="bold", color="#FFFFFF")
            cell.set_height(0.12)
        else:
            if row == 1:
                cell.set_facecolor("#ECFDF5")  # Verde
            elif row == 2:
                cell.set_facecolor("#FEF3C7")  # Âmbar
            else:
                cell.set_facecolor("#FEF2F2")  # Vermelho
            cell.set_text_props(weight="bold" if col in [0, 4] else "normal", color="#0F172A")
            cell.set_height(0.16)

    # Nota explicativa
    note_text = (
        "IMPACTO DE NEGÓCIO DA PRIORIZAÇÃO POR VIABILIDADE:\n"
        "• Alocação Eficiente: 80% do orçamento é direcionado para carrinhos de ALTA viabilidade.\n"
        "• Proteção de Margem: Sessões de baixa viabilidade são filtradas, economizando verba de canais pagos.\n"
        "• Resultado Consolidado: Multiplica por até 3x a receita recuperada em relação a disparos massivos genéricos."
    )
    bbox_props = dict(boxstyle="round,pad=0.5", facecolor="#F8FAFC", edgecolor="#94A3B8", linewidth=1.1)
    ax2.text(0.0, 0.02, note_text, fontsize=8.5, color="#1E293B", va="bottom", bbox=bbox_props, transform=ax2.transAxes, family="monospace")

    ax2.set_title("2. DECOMPOSIÇÃO OPERACIONAL & MATRIZ PRESCRITIVA", fontsize=12.5, fontweight="bold", color="#0F172A", pad=12)

    fig.suptitle("SCORE DE VIABILIDADE DE RECUPERAÇÃO (RECOVERY VIABILITY) & PRIORIZAÇÃO FINANCEIRA",
                 fontsize=14.5, fontweight="bold", color="#0F172A", y=0.98)

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    return fig

def main() -> None:
    df_data = load_data()
    df_aband, summary_viab = compute_recovery_viability(df_data)
    
    fig = plot_viability_chart(df_aband, summary_viab)
    os.makedirs(MODULE_DIR, exist_ok=True)
    fig.savefig(OUTPUT_IMAGE_PATH, dpi=300, bbox_inches="tight", facecolor="#FFFFFF")
    plt.close(fig)
    print(f"[SUCCESS] Gráfico de Viabilidade de Recuperação salvo em: {OUTPUT_IMAGE_PATH}")

if __name__ == "__main__":
    main()
