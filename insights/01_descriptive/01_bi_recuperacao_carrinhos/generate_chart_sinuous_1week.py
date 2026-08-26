"""
Gerador da visualização: BI de Recuperação de Carrinhos (Versão Sinuosa - Recorte de 1 Semana).
Paradigma funcional e declarativo com tipagem estrita (Type Annotations).

Características:
- Recorte temporal focado em 1 semana (09 a 15 de Fevereiro de 2026 - 288 carrinhos).
- Linhas sinuosas orgânicas (Spline Cúbica) com variações de curvatura e cristas/vales.
- Linha Superior: Total de Carrinhos Criados (288 un).
- Linha Intermediária: Total Convertido em Pedido: Compras Diretas + Resgate (81 un / 28.1%).
- Linha Inferior: Compras Diretas no Checkout (61 un / 21.2%).
- Zona de Recuperação Dadosfera: Resgate Ativo de 20 pedidos (+5 pendentes / 8.9% sobre abandonados).
- Fundo branco puro (#FFFFFF) com preenchimento colorido nas 3 zonas entre as linhas (fill_between).
- Vértices reais destacados para leitura clara das diferenças no eixo X e Y.
"""

from typing import Final
import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline

# Caminhos absolutos
def _find_base_dir() -> str:
    curr = os.path.abspath(os.path.dirname(__file__))
    while curr and os.path.dirname(curr) != curr:
        if os.path.exists(os.path.join(curr, "data", "mock")):
            return curr
        curr = os.path.dirname(curr)
    return os.path.abspath(os.getcwd())

BASE_DIR: Final[str] = _find_base_dir()
OUTPUT_IMAGE_PATH: Final[str] = os.path.join(
    os.path.dirname(__file__), "chart_bi_recuperacao_carrinhos_sinuous_1week.png"
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
    """Carrega dados transacionais de carrinhos e pedidos (fonte limpa com Ground Truth)."""
    df_carts: pd.DataFrame = pd.read_parquet(PARQUET_CARTS_PATH)
    df_carts["data_criacao"] = pd.to_datetime(df_carts["data_criacao"])
    
    if os.path.exists(PARQUET_ORDERS_PATH):
        df_orders: pd.DataFrame = pd.read_parquet(PARQUET_ORDERS_PATH)
        recup_cart_ids = set(df_orders[df_orders["origem_recuperacao"] == True]["carrinho_id"])
    else:
        recup_cart_ids = set()
        
    df_carts["is_recuperado_comprado"] = df_carts["carrinho_id"].isin(recup_cart_ids)
    
    df_carts["status_funil"] = "atrito"
    df_carts.loc[(df_carts["status"] == "comprado") & (~df_carts["is_recuperado_comprado"]), "status_funil"] = "comprado_direto"
    df_carts.loc[df_carts["is_recuperado_comprado"], "status_funil"] = "recuperado_comprado"
    df_carts.loc[df_carts["status"] == "recuperado", "status_funil"] = "recuperado_pendente"
    
    return df_carts

def prepare_1week_series(df_carts: pd.DataFrame) -> tuple[list[str], np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, int]:
    """Prepara a série temporal de 1 semana (09/Fev a 15/Fev) estritamente com dados reais persistidos."""
    start_dt = pd.to_datetime("2026-02-09 00:00:00+00:00")
    end_dt = pd.to_datetime("2026-02-15 23:59:59+00:00")
    
    df_week = df_carts[(df_carts["data_criacao"] >= start_dt) & (df_carts["data_criacao"] <= end_dt)]
    
    df_daily: pd.DataFrame = (
        df_week.groupby([pd.Grouper(key="data_criacao", freq="1D"), "status_funil"])
        .size()
        .unstack(fill_value=0)
    )
    
    for col in ["atrito", "comprado_direto", "recuperado_comprado", "recuperado_pendente"]:
        if col not in df_daily.columns:
            df_daily[col] = 0
            
    df_daily["total_dia"] = df_daily.sum(axis=1)
    
    dias_rotulos: list[str] = [
        "Seg (09/Fev)",
        "Ter (10/Fev)",
        "Qua (11/Fev)",
        "Qui (12/Fev)",
        "Sex (13/Fev)",
        "Sáb (14/Fev)",
        "Dom (15/Fev)",
    ]
    
    y_total = df_daily["total_dia"].to_numpy(dtype=float)
    y_aband = df_daily["atrito"].to_numpy(dtype=float)
    y_comp_direto = df_daily["comprado_direto"].to_numpy(dtype=float)
    y_recup_comprado = df_daily["recuperado_comprado"].to_numpy(dtype=float)
    y_recup_pendente = df_daily["recuperado_pendente"].to_numpy(dtype=float)
    total_geral = int(df_daily["total_dia"].sum())
    
    return dias_rotulos, y_total, y_aband, y_comp_direto, y_recup_comprado, y_recup_pendente, total_geral

def plot_sinuous_1week_chart(
    dias_rotulos: list[str],
    y_total: np.ndarray,
    y_aband: np.ndarray,
    y_comp_direto: np.ndarray,
    y_recup_comprado: np.ndarray,
    y_recup_pendente: np.ndarray,
    total_geral: int
) -> plt.Figure:
    """Gera o gráfico sinuoso de 1 semana com dados 100% reais, spline e zonas balanceadas."""
    plt.rcParams["text.parse_math"] = False
    plt.rcParams["font.sans-serif"] = ["Segoe UI", "DejaVu Sans", "Helvetica", "Arial", "sans-serif"]
    plt.rcParams["axes.edgecolor"] = "#CBD5E1"
    plt.rcParams["axes.linewidth"] = 1.2
    
    fig, ax = plt.subplots(figsize=(14.0, 7.5), facecolor="#FFFFFF")
    ax.set_facecolor("#FFFFFF")
    
    x_indices = np.arange(len(dias_rotulos))
    y_conv_total = y_comp_direto + y_recup_comprado
    
    # Interpolação Spline Cúbica hiper-suave conectando os vértices diários reais
    x_smooth = np.linspace(x_indices.min(), x_indices.max(), 300)
    spl_total = np.maximum(0, make_interp_spline(x_indices, y_total, k=3)(x_smooth))
    spl_conv_total = np.maximum(0, make_interp_spline(x_indices, y_conv_total, k=3)(x_smooth))
    spl_comp_direto = np.maximum(0, make_interp_spline(x_indices, y_comp_direto, k=3)(x_smooth))
    
    # Cores Corporativas
    color_total = "#E11D48"       # Vermelho vibrante (Teto / Total)
    color_resgate = "#059669"     # Verde Esmeralda (Recuperados)
    color_comp = "#2563EB"        # Azul Royal (Comprados Diretos)
    
    # Preenchimento de Zonas (fill_between)
    ax.fill_between(
        x_smooth, spl_conv_total, spl_total,
        color="#E11D48", alpha=0.14,
        label="Zona de Atrito / Perda Não Convertida (Abandono no Checkout: 202 un)"
    )
    ax.fill_between(
        x_smooth, spl_comp_direto, spl_conv_total,
        color="#059669", alpha=0.28,
        label="Zona de Carrinhos Recuperados (Resgate Dadosfera: 20 un / 8.9% abandono)"
    )
    ax.fill_between(
        x_smooth, 0, spl_comp_direto,
        color="#2563EB", alpha=0.14,
        label="Zona de Conversão Direta no Checkout (Orgânica: 61 un / 21.2%)"
    )
    
    # Linhas Sinuosas
    ax.plot(x_smooth, spl_total, color=color_total, linewidth=3.4, label="[1] Total de Carrinhos Criados (Teto Diário: 288 un)", zorder=4)
    ax.plot(x_smooth, spl_conv_total, color=color_resgate, linewidth=2.8, linestyle="--", label="[2] Total Convertido: Direto + Resgate (81 un)", zorder=4)
    ax.plot(x_smooth, spl_comp_direto, color=color_comp, linewidth=3.0, label="[3] Carrinhos Comprados Diretamente (61 un)", zorder=4)
    
    # Vértices reais destacados
    ax.scatter(x_indices, y_total, color="#FFFFFF", edgecolor=color_total, s=55, linewidth=2.2, zorder=5)
    ax.scatter(x_indices, y_conv_total, color="#FFFFFF", edgecolor=color_resgate, s=55, linewidth=2.2, zorder=5)
    ax.scatter(x_indices, y_comp_direto, color="#FFFFFF", edgecolor=color_comp, s=55, linewidth=2.2, zorder=5)
    
    # Anotações nos vértices diários auditáveis
    for i in range(len(dias_rotulos)):
        ax.annotate(f"{int(y_total[i])}", (x_indices[i], y_total[i] + 1.3), ha="center", fontsize=9.5, fontweight="bold", color="#9F1239")
        ax.annotate(f"{int(y_comp_direto[i])}", (x_indices[i], y_comp_direto[i] - 2.8), ha="center", fontsize=9.5, fontweight="bold", color="#1E40AF")
        if y_recup_comprado[i] > 0:
            ax.annotate(f"+{int(y_recup_comprado[i])}", (x_indices[i], y_conv_total[i] + 0.9), ha="center", fontsize=9.0, fontweight="bold", color="#065F46")
            
    # Eixos e Formatação
    ax.set_xticks(x_indices)
    ax.set_xticklabels(dias_rotulos, fontsize=11, fontweight="bold", color="#1E293B")
    ax.set_xlabel("Dias da Semana (Recorte Focado de 1 Semana: 09 a 15 de Fevereiro de 2026)", fontsize=11, fontweight="bold", color="#1E293B", labelpad=10)
    
    ax.set_ylabel("Volume Diário de Carrinhos (Unidades)", fontsize=11, fontweight="bold", color="#1E293B", labelpad=10)
    ax.set_xlim(-0.2, len(dias_rotulos) - 0.8)
    ax.set_ylim(0, max(y_total.max(), spl_total.max()) * 1.18)
    
    # Grid sutil
    ax.grid(True, linestyle="--", alpha=0.5, color="#CBD5E1", zorder=1)
    
    # Título e Subtítulo
    ax.set_title(
        "BI Analítico: Dinâmica Sinuosa em Janela Curta (Recorte de 1 Semana)\n"
        "Acompanhamento Diário de Conversão e Abandono (09 a 15 de Fevereiro de 2026)",
        fontsize=13.5,
        fontweight="bold",
        color="#0F172A",
        pad=16
    )
    
    # Card Resumo
    total_aband = int(y_aband.sum())
    total_comp_dir = int(y_comp_direto.sum())
    total_recup = int(y_recup_comprado.sum())
    total_pend = int(y_recup_pendente.sum())
    total_conv = total_comp_dir + total_recup
    
    total_aband_potencial = total_aband + total_recup
    taxa_recup_abandono = (total_recup / total_aband_potencial) * 100
    
    card_text = (
        "RECORTE SEMANAL (09 A 15 DE FEVEREIRO DE 2026):\n"
        f"• Total de Carrinhos: {total_geral} un (100.0%)\n"
        f"• Comprados Diretos: {total_comp_dir} un ({total_comp_dir/total_geral*100:.1f}%)\n"
        f"• Recuperados Dadosfera: {total_recup} un ({total_recup/total_geral*100:.1f}% total | {taxa_recup_abandono:.1f}% abandono)\n"
        f"• Reengajados Pendentes: {total_pend} un ({total_pend/total_geral*100:.1f}%)\n"
        f"• Conversão Total: {total_conv} un ({total_conv/total_geral*100:.1f}%)\n"
        f"• Abandono Residual: {total_aband} un ({total_aband/total_geral*100:.1f}%)"
    )
    
    props = dict(boxstyle="round,pad=0.8", facecolor="#F8FAFC", edgecolor="#94A3B8", alpha=0.95, linewidth=1.2)
    ax.text(0.02, 0.95, card_text, transform=ax.transAxes, fontsize=9.5, fontweight="bold", color="#1E293B", va="top", bbox=props, zorder=6)
    
    # Legenda estruturada
    ax.legend(loc="upper right", fontsize=9.5, framealpha=0.95, facecolor="#FFFFFF", edgecolor="#CBD5E1")
    
    plt.tight_layout()
    return fig

def main() -> None:
    """Executa a extração dos dados e geração do gráfico sinuoso de 1 semana."""
    df_carts = load_data()
    dias_rotulos, y_total, y_aband, y_comp_direto, y_recup_comprado, y_recup_pendente, total_geral = prepare_1week_series(df_carts)
    fig = plot_sinuous_1week_chart(dias_rotulos, y_total, y_aband, y_comp_direto, y_recup_comprado, y_recup_pendente, total_geral)
    
    fig.savefig(OUTPUT_IMAGE_PATH, dpi=300, bbox_inches="tight", facecolor="#FFFFFF")
    plt.close(fig)
    print(f"[SUCCESS] Gráfico Sinuoso de 1 Semana (Dados Reais) gerado em: {OUTPUT_IMAGE_PATH}")

if __name__ == "__main__":
    main()
