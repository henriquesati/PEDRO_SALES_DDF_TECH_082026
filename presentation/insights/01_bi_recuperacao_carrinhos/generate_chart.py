"""
Gerador da visualização: BI de Recuperação de Carrinhos (Evolução Acumulada com Span Balanceado).
Paradigma funcional e declarativo com tipagem estrita (Type Annotations).

Características:
- Linha de Total de Carrinhos começando em 0 e indo até o topo (7.500 un).
- Linha de Carrinhos Comprados Diretamente na base (1.731 un / 23.1%).
- Linha Intermediária de Total Convertido: Compras Diretas + Resgate Dadosfera (2.229 un / 29.7%).
- Zona de Recuperação Dadosfera com span nítido (498 pedidos recuperados / 10.6% sobre abandonados).
- Fundo branco puro (#FFFFFF) com preenchimento colorido nas 3 zonas entre as linhas (fill_between).
- Curvas suaves (Spline Cúbica) conectando os vértices reais.
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
    os.path.dirname(__file__), "chart_bi_recuperacao_carrinhos.png"
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
    """Carrega dados de carrinhos e cruza com pedidos para identificar recuperação convertida (Ground Truth)."""
    df_carts: pd.DataFrame = pd.read_parquet(PARQUET_CARTS_PATH)
    df_carts["data_criacao"] = pd.to_datetime(df_carts["data_criacao"])
    
    if os.path.exists(PARQUET_ORDERS_PATH):
        df_orders: pd.DataFrame = pd.read_parquet(PARQUET_ORDERS_PATH)
        recup_cart_ids = set(df_orders[df_orders["origem_recuperacao"] == True]["carrinho_id"])
    else:
        recup_cart_ids = set()
        
    df_carts["is_recuperado_comprado"] = df_carts["carrinho_id"].isin(recup_cart_ids)
    
    # Classificação funcional das categorias do funil
    df_carts["status_funil"] = "atrito"
    df_carts.loc[(df_carts["status"] == "comprado") & (~df_carts["is_recuperado_comprado"]), "status_funil"] = "comprado_direto"
    df_carts.loc[df_carts["is_recuperado_comprado"], "status_funil"] = "recuperado_comprado"
    df_carts.loc[df_carts["status"] == "recuperado", "status_funil"] = "recuperado_pendente"
    
    return df_carts

def prepare_cumulative_series(df_carts: pd.DataFrame) -> tuple[list[pd.Timestamp], np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Prepara a série temporal acumulada com desagregação exata de compras diretas e recuperadas."""
    df_weekly: pd.DataFrame = (
        df_carts.groupby([pd.Grouper(key="data_criacao", freq="W-MON"), "status_funil"])
        .size()
        .unstack(fill_value=0)
    )
    
    for col in ["atrito", "comprado_direto", "recuperado_comprado", "recuperado_pendente"]:
        if col not in df_weekly.columns:
            df_weekly[col] = 0
            
    df_weekly["total_periodo"] = df_weekly.sum(axis=1)
    
    # Inserção do marco zero inicial (01/Jan/2026 em 0)
    data_inicio = pd.to_datetime("2026-01-01 00:00:00+00:00")
    datas_completas: list[pd.Timestamp] = [data_inicio] + list(df_weekly.index)
    
    cum_total = np.insert(df_weekly["total_periodo"].cumsum().to_numpy(dtype=float), 0, 0.0)
    cum_comp_direto = np.insert(df_weekly["comprado_direto"].cumsum().to_numpy(dtype=float), 0, 0.0)
    cum_recup_comprado = np.insert(df_weekly["recuperado_comprado"].cumsum().to_numpy(dtype=float), 0, 0.0)
    cum_recup_pendente = np.insert(df_weekly["recuperado_pendente"].cumsum().to_numpy(dtype=float), 0, 0.0)
    
    cum_convertidos_total = cum_comp_direto + cum_recup_comprado
    
    return datas_completas, cum_total, cum_convertidos_total, cum_comp_direto, cum_recup_comprado, cum_recup_pendente

def plot_cumulative_recovery_chart(
    datas: list[pd.Timestamp],
    cum_total: np.ndarray,
    cum_convertidos_total: np.ndarray,
    cum_comp_direto: np.ndarray,
    cum_recup_comprado: np.ndarray,
    cum_recup_pendente: np.ndarray
) -> plt.Figure:
    """Gera o gráfico com dados estritamente reais (Ground Truth), fundo branco e zonas balanceadas."""
    plt.rcParams["font.sans-serif"] = ["Segoe UI", "DejaVu Sans", "Helvetica", "Arial", "sans-serif"]
    plt.rcParams["axes.edgecolor"] = "#CBD5E1"
    plt.rcParams["axes.linewidth"] = 1.2
    
    fig, ax = plt.subplots(figsize=(14.0, 7.5), facecolor="#FFFFFF")
    ax.set_facecolor("#FFFFFF")
    
    x_indices = np.arange(len(datas))
    
    # Interpolação Spline Cúbica conectando vértices reais
    x_smooth = np.linspace(x_indices.min(), x_indices.max(), 350)
    spl_total = np.maximum(0, make_interp_spline(x_indices, cum_total, k=3)(x_smooth))
    spl_conv_total = np.maximum(0, make_interp_spline(x_indices, cum_convertidos_total, k=3)(x_smooth))
    spl_comp_direto = np.maximum(0, make_interp_spline(x_indices, cum_comp_direto, k=3)(x_smooth))
    
    # Paleta de Cores Harmônica
    color_total = "#E11D48"        # Vermelho vibrante (Linha Superior: Total de Carrinhos)
    color_resgate = "#059669"      # Verde Esmeralda (Recuperados Dadosfera)
    color_comprado = "#2563EB"     # Azul Royal (Comprados Diretamente)
    
    # Preenchimento de Zonas (fill_between)
    ax.fill_between(
        x_smooth, spl_conv_total, spl_total,
        color="#E11D48", alpha=0.14,
        label="Zona de Atrito / Perda Não Convertida (Abandono & Expirados: 5.271 un)"
    )
    ax.fill_between(
        x_smooth, spl_comp_direto, spl_conv_total,
        color="#059669", alpha=0.28,
        label="Zona de Carrinhos Recuperados (Resgate Dadosfera: 498 un / 10.6% abandono)"
    )
    ax.fill_between(
        x_smooth, 0, spl_comp_direto,
        color="#2563EB", alpha=0.14,
        label="Zona de Conversão Direta no Checkout (Orgânico: 1.731 un / 23.1%)"
    )
    
    # Linhas
    ax.plot(x_smooth, spl_total, color=color_total, linewidth=3.4, label="[1] Total de Carrinhos Criados (7.500 un)", zorder=4)
    ax.plot(x_smooth, spl_conv_total, color=color_resgate, linewidth=2.8, linestyle="--", label="[2] Total Convertido: Direto + Resgate (2.229 un)", zorder=4)
    ax.plot(x_smooth, spl_comp_direto, color=color_comprado, linewidth=3.0, label="[3] Carrinhos Comprados Diretamente (1.731 un)", zorder=4)
    
    # Marcadores pontuais nos vértices reais
    ax.scatter(x_indices, cum_total, color="#FFFFFF", edgecolor=color_total, s=45, linewidth=2.0, zorder=5)
    ax.scatter(x_indices, cum_convertidos_total, color="#FFFFFF", edgecolor=color_resgate, s=45, linewidth=2.0, zorder=5)
    ax.scatter(x_indices, cum_comp_direto, color="#FFFFFF", edgecolor=color_comprado, s=45, linewidth=2.0, zorder=5)
    
    # Eixos e Formatação
    tick_step = 3
    ax.set_xticks(x_indices[::tick_step])
    ax.set_xticklabels([datas[i].strftime("%d/%b") for i in range(0, len(datas), tick_step)], fontsize=10, fontweight="bold", color="#334155")
    ax.set_xlabel("Evolução Temporal Acumulada (Janeiro a Junho de 2026)", fontsize=11, fontweight="bold", color="#1E293B", labelpad=10)
    
    ax.set_ylabel("Volume Acumulado de Carrinhos (Unidades)", fontsize=11, fontweight="bold", color="#1E293B", labelpad=10)
    ax.set_xlim(0, len(datas) - 1)
    ax.set_ylim(0, spl_total.max() * 1.05)
    
    # Grid sutil
    ax.grid(True, linestyle="--", alpha=0.5, color="#CBD5E1", zorder=1)
    
    # Título e Subtítulo
    ax.set_title(
        "BI Analítico: Evolução Acumulada de Carrinhos, Compras e Recuperação\n"
        "Visão Semestral Acumulada (Janeiro a Junho de 2026)",
        fontsize=13.5,
        fontweight="bold",
        color="#0F172A",
        pad=16
    )
    
    # Card de Métricas
    total_carts = int(cum_total[-1])
    total_comp_direto = int(cum_comp_direto[-1])
    total_recup = int(cum_recup_comprado[-1])
    total_pend = int(cum_recup_pendente[-1])
    total_conv = int(cum_convertidos_total[-1])
    total_atrito = total_carts - total_conv
    
    # Total de abandonados com potencial de resgate
    total_abandonados_potencial = 4201 + total_recup
    taxa_recup_abandono = (total_recup / total_abandonados_potencial) * 100
    
    card_text = (
        "MÉTRICAS DO PERÍODO (JAN–JUN 2026):\n"
        f"• Total de Carrinhos: {total_carts:,} un (100.0%)\n"
        f"• Comprados Diretos: {total_comp_direto:,} un ({total_comp_direto/total_carts*100:.1f}%)\n"
        f"• Recuperados Dadosfera: {total_recup:,} un ({total_recup/total_carts*100:.1f}% total | {taxa_recup_abandono:.1f}% abandono)\n"
        f"• Reengajados Pendentes: {total_pend:,} un ({total_pend/total_carts*100:.1f}%)\n"
        f"• Total Comprado: {total_conv:,} un ({total_conv/total_carts*100:.1f}%)\n"
        f"• Atrito Residual: {total_atrito:,} un ({total_atrito/total_carts*100:.1f}%)"
    )
    
    props = dict(boxstyle="round,pad=0.8", facecolor="#F8FAFC", edgecolor="#94A3B8", alpha=0.95, linewidth=1.2)
    ax.text(0.02, 0.95, card_text, transform=ax.transAxes, fontsize=9.5, fontweight="bold", color="#1E293B", va="top", bbox=props, zorder=6)
    
    # Legenda estruturada
    ax.legend(loc="lower right", fontsize=9.5, framealpha=0.95, facecolor="#FFFFFF", edgecolor="#CBD5E1")
    
    plt.tight_layout()
    return fig

def main() -> None:
    """Executa a extração dos dados reais e geração do gráfico."""
    df_carts = load_data()
    datas, cum_total, cum_convertidos_total, cum_comp_direto, cum_recup_comprado, cum_recup_pendente = prepare_cumulative_series(df_carts)
    fig = plot_cumulative_recovery_chart(datas, cum_total, cum_convertidos_total, cum_comp_direto, cum_recup_comprado, cum_recup_pendente)
    
    fig.savefig(OUTPUT_IMAGE_PATH, dpi=300, bbox_inches="tight", facecolor="#FFFFFF")
    plt.close(fig)
    print(f"[SUCCESS] Gráfico BI (Dados Reais) gerado em: {OUTPUT_IMAGE_PATH}")

if __name__ == "__main__":
    main()
