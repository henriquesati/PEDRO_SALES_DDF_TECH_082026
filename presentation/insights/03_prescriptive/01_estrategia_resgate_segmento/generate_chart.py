"""
Gerador da visualização: Estratégia Prescritiva de Resgate por Segmento RFM.
Atende à especificação de insights/03_prescriptive/estrategia_resgate_segmento.md.
Paradigma funcional e declarativo com tipagem estrita (Type Annotations).
"""

from typing import Final
import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR: Final[str] = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
OUTPUT_IMAGE_PATH: Final[str] = os.path.join(
    os.path.dirname(__file__), "chart_04_estrategia_resgate_segmento.png"
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

PARQUET_RESCUE_PATH: Final[str] = (
    os.path.join(BASE_DIR, "data", "mock", "output_cleaned", "parquet", "eventos_resgate.parquet")
    if os.path.exists(os.path.join(BASE_DIR, "data", "mock", "output_cleaned", "parquet", "eventos_resgate.parquet"))
    else os.path.join(BASE_DIR, "data", "mock", "output", "parquet", "eventos_resgate.parquet")
)

def load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Carrega carrinhos, clientes e telemetria de resgate."""
    df_carts = pd.read_parquet(PARQUET_CARTS_PATH)
    df_clients = pd.read_parquet(PARQUET_CLIENTS_PATH)
    
    df_merged = df_carts.merge(
        df_clients[["cliente_id", "segmento_rfm", "lifetime_value"]],
        on="cliente_id",
        how="left"
    )
    df_merged["segmento_rfm"] = df_merged["segmento_rfm"].fillna("novo")
    
    df_rescue = pd.read_parquet(PARQUET_RESCUE_PATH)
    return df_merged, df_rescue

def compute_viability_metrics(df_merged: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Calcula a viabilidade líquida por segmento e canal de comunicação."""
    # Médias de ticket e comportamento por segmento RFM
    seg_summary = df_merged.groupby("segmento_rfm").agg(
        ticket_medio=("valor_total", "mean"),
        total_carrinhos=("carrinho_id", "count")
    ).reindex(["premium", "regular", "dormant", "novo"]).reset_index()

    # Custos e taxas esperadas de conversão por canal
    channel_costs = {"WhatsApp": 0.30, "SMS": 0.15, "Email": 0.05, "Push": 0.02}
    
    # Conversões esperadas empíricas por segmento e canal
    conv_rates = {
        "premium": {"WhatsApp": 0.12, "SMS": 0.08, "Email": 0.09, "Push": 0.06},
        "regular": {"WhatsApp": 0.06, "SMS": 0.04, "Email": 0.05, "Push": 0.04},
        "dormant": {"WhatsApp": 0.02, "SMS": 0.015, "Email": 0.02, "Push": 0.015},
        "novo": {"WhatsApp": 0.025, "SMS": 0.018, "Email": 0.028, "Push": 0.02},
    }

    # Descontos médios prescritos por segmento
    discounts = {"premium": 0.0, "regular": 0.05, "dormant": 0.10, "novo": 0.10}

    records = []
    for _, row in seg_summary.iterrows():
        seg = row["segmento_rfm"]
        tkt = row["ticket_medio"]
        desc_rate = discounts[seg]
        
        for ch, cost in channel_costs.items():
            conv = conv_rates[seg][ch]
            # Fórmula: (Taxa Conv * Ticket) - (Custo Canal + (Conv * Ticket * % Desconto))
            rec_bruta = conv * tkt
            custo_desc = rec_bruta * desc_rate
            viab_liquida = rec_bruta - cost - custo_desc
            roi_mult = (viab_liquida / cost) if cost > 0 else 0
            
            records.append({
                "segmento": seg.capitalize(),
                "canal": ch,
                "ticket_medio": tkt,
                "conv_rate": conv * 100,
                "custo_canal": cost,
                "viab_liquida": viab_liquida,
                "roi_mult": roi_mult
            })
            
    df_viab = pd.DataFrame(records)
    return seg_summary, df_viab

def plot_prescriptive_strategy_chart(seg_summary: pd.DataFrame, df_viab: pd.DataFrame) -> plt.Figure:
    """Plota a visualização integrada de viabilidade e alocação prescritiva."""
    plt.rcParams["font.sans-serif"] = ["Segoe UI", "DejaVu Sans", "Helvetica", "Arial", "sans-serif"]
    plt.rcParams["axes.edgecolor"] = "#CBD5E1"
    plt.rcParams["axes.linewidth"] = 1.1

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14.0, 6.8), gridspec_kw={"width_ratios": [1.15, 1.05]})
    fig.patch.set_facecolor("#FFFFFF")

    # --- PAINEL 1: Viabilidade Econômica Líquida por Resgate (R$) ---
    ax1.set_facecolor("#FFFFFF")
    
    segments = ["Premium", "Regular", "Dormant", "Novo"]
    x = np.arange(len(segments))
    width = 0.18
    
    channel_colors = {
        "WhatsApp": "#059669",
        "SMS": "#F59E0B",
        "Email": "#2563EB",
        "Push": "#8B5CF6"
    }

    for i, ch in enumerate(["WhatsApp", "SMS", "Email", "Push"]):
        vals = [
            df_viab[(df_viab["segmento"] == seg) & (df_viab["canal"] == ch)]["viab_liquida"].values[0]
            for seg in segments
        ]
        offset = (i - 1.5) * width
        bars = ax1.bar(x + offset, vals, width=width, label=ch, color=channel_colors[ch], alpha=0.90, edgecolor="#334155")
        
        for bar, val in zip(bars, vals):
            y_text = bar.get_height() + (0.5 if val >= 0 else -1.2)
            ax1.text(bar.get_x() + bar.get_width()/2, y_text, f"R${val:.1f}",
                     ha="center", va="bottom" if val >= 0 else "top", fontsize=8.5, fontweight="bold", color="#0F172A")

    ax1.axhline(0, color="#64748B", linestyle="-", linewidth=1.0)
    ax1.set_xticks(x)
    ax1.set_xticklabels(segments, fontsize=11, fontweight="bold", color="#1E293B")
    ax1.set_ylabel("Ganho Líquido Esperado por Resgate (R$)", fontsize=11, fontweight="bold", color="#334155")
    ax1.set_title("Simulador de Viabilidade Líquida por Canal & Segmento", fontsize=13, fontweight="bold", color="#0F172A", pad=12)
    ax1.grid(axis="y", linestyle="--", alpha=0.5, color="#CBD5E1")
    ax1.legend(loc="upper right", frameon=True, facecolor="#F8FAFC", edgecolor="#CBD5E1", fontsize=9.5)
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)

    # --- PAINEL 2: Matriz Prescritiva de Ações Recomendadas ---
    ax2.set_facecolor("#FFFFFF")
    ax2.axis("off")
    
    table_data = [
        ["Segmento", "Timing 1º Toque", "Canal Primário", "Incentivo Prescrito", "Abordagem Copy"],
        ["PREMIUM\n(Ticket ~R$800)", "+1 hora\n(Lead Quente)", "WhatsApp / VIP\n(R$ 0,30)", "Sem Desconto\n(Reserva de Estoque)", "Atendimento VIP\ne Exclusividade"],
        ["REGULAR\n(Ticket ~R$360)", "+6h a +8h\n(Pós-Turno)", "Email + Push\n(R$ 0,05 / 0,02)", "Cupom 5%\n(Se > R$ 200)", "Lembrete Suave\nde Itens Salvos"],
        ["NOVO\n(Ticket ~R$250)", "+24 horas\n(D+1)", "Email Inbound\n(R$ 0,05)", "10% 1ª Compra\n(Margem protegida)", "Social Proof &\nGarantia de Compra"],
        ["DORMANT\n(Ticket ~R$200)", "+48 horas\n(Repescagem)", "Push App\n(R$ 0,02)", "Frete Fixo / 10%\n(Condicionado)", "Sentimos sua falta\n& Novidades"]
    ]

    table = ax2.table(
        cellText=table_data,
        cellLoc="center",
        loc="center",
        bbox=[0.0, 0.05, 1.0, 0.88]
    )
    table.auto_set_font_size(False)
    table.set_fontsize(9.5)

    for (row, col), cell in table.get_celld().items():
        cell.set_edgecolor("#CBD5E1")
        cell.set_linewidth(1.1)
        if row == 0:
            cell.set_facecolor("#0F172A")
            cell.set_text_props(weight="bold", color="#FFFFFF")
            cell.set_height(0.12)
        else:
            if row == 1:
                cell.set_facecolor("#EFF6FF")
            elif row == 2:
                cell.set_facecolor("#ECFDF5")
            elif row == 3:
                cell.set_facecolor("#FEF3C7")
            else:
                cell.set_facecolor("#F1F5F9")
            cell.set_text_props(weight="bold" if col == 0 else "normal", color="#0F172A")
            cell.set_height(0.19)

    ax2.set_title("Matriz de Políticas Prescritivas de Resgate", fontsize=13, fontweight="bold", color="#0F172A", pad=12)

    # Título Geral
    fig.suptitle("ESTRATÉGIA PRESCRITIVA DE RESGATE: VIABILIDADE LÍQUIDA & MATRIZ DE CANAIS (DADOSFERA)",
                 fontsize=15, fontweight="bold", color="#0F172A", y=0.98)

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    return fig

def main() -> None:
    df_merged, df_rescue = load_data()
    seg_summary, df_viab = compute_viability_metrics(df_merged)
    fig = plot_prescriptive_strategy_chart(seg_summary, df_viab)
    
    os.makedirs(os.path.dirname(OUTPUT_IMAGE_PATH), exist_ok=True)
    fig.savefig(OUTPUT_IMAGE_PATH, dpi=300, bbox_inches="tight", facecolor="#FFFFFF")
    plt.close(fig)
    print(f"[SUCCESS] Gráfico de Estratégia de Resgate salvo em: {OUTPUT_IMAGE_PATH}")

if __name__ == "__main__":
    main()
