#!/usr/bin/env python
"""Script gerador de imagens e evidências visuais do Data App (Item 9 & Bônus).

Exporta gráficos analíticos em alta definição (300 DPI) para o relatório de entrega
e documentação do repositório.
"""

import os
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

CURRENT_DIR = Path(__file__).resolve().parent
ITEM_DIR = CURRENT_DIR.parent
BASE_DIR = ITEM_DIR.parent.parent
if str(ITEM_DIR) not in sys.path:
    sys.path.insert(0, str(ITEM_DIR))
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from config.settings import (
    COLOR_PRIMARY_NAVY,
    COLOR_PRIMARY_BLUE,
    COLOR_SUCCESS_GREEN,
    COLOR_WARNING_AMBER,
    COLOR_DANGER_RED,
    DATA_PATHS,
)
from core.similarity_engine import compute_2d_projection
from core.simulation_engine import (
    generate_discount_sensitivity_curve,
    run_simulation,
)
from core.types import ChannelAllocation, SimulationInput

OUTPUT_DIR = os.path.join(ITEM_DIR, "outputs", "assets")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_roi_simulation_chart() -> str:
    """Gera painel visual da simulação de ROI e curva de sensibilidade."""
    plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), dpi=300)
    
    # 1. Simulação
    allocs = (
        ChannelAllocation("WhatsApp", 0.40, 3000, 12.0, 0.145),
        ChannelAllocation("Email", 0.40, 3000, 1.02, 0.082),
        ChannelAllocation("SMS", 0.20, 1500, 3.00, 0.068),
    )
    sim_input = SimulationInput(7500, 348.80, 10.0, 1.5, allocs)
    sim_out = run_simulation(sim_input)
    
    # Waterfall Bar Chart
    labels = ["Rec. Bruta", "Custo Comun.", "Custo Desc.", "Rec. Líquida"]
    values = [
        sim_out.total_gross_revenue,
        -sim_out.total_communication_cost,
        -sim_out.total_discount_cost,
        sim_out.total_net_revenue
    ]
    colors = [COLOR_PRIMARY_BLUE, COLOR_DANGER_RED, COLOR_WARNING_AMBER, COLOR_SUCCESS_GREEN]
    
    bars = ax1.bar(labels, values, color=colors, width=0.55, edgecolor="#0F172A", linewidth=1.2)
    ax1.set_title("Decomposição Econômica da Ação de Resgate\n(Waterfall de Receita Líquida)", fontsize=12, fontweight="bold", pad=12)
    ax1.set_ylabel("R$ (Reais)", fontsize=10, fontweight="bold")
    ax1.axhline(0, color="black", linewidth=1)
    
    for bar, val in zip(bars, values):
        y_pos = bar.get_height() if val >= 0 else bar.get_height() - (abs(val) * 0.15)
        prefix = "+" if val > 0 else ""
        ax1.annotate(
            f"{prefix}R$ {abs(val):,.0f}",
            xy=(bar.get_x() + bar.get_width() / 2, y_pos),
            xytext=(0, 5 if val >= 0 else -15),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=9,
            fontweight="bold",
            color="#0F172A"
        )
    ax1.grid(axis="y", linestyle="--", alpha=0.5)

    # 2. Curva de Sensibilidade
    df_sens = generate_discount_sensitivity_curve(sim_input)
    ax2.plot(df_sens["Desconto (%)"], df_sens["ROI Multiplicador"], marker="o", color=COLOR_SUCCESS_GREEN, linewidth=2.5, markersize=8, label="ROI Projetado (x)")
    ax2.axvline(10.0, color=COLOR_WARNING_AMBER, linestyle="--", linewidth=1.8, label="Ponto Calibrado (10% OFF)")
    
    ax2.set_title("Curva de Sensibilidade de Desconto vs ROI\n(Elasticidade de Margem Líquida)", fontsize=12, fontweight="bold", pad=12)
    ax2.set_xlabel("Cupom de Desconto (%)", fontsize=10, fontweight="bold")
    ax2.set_ylabel("Multiplicador de ROI (x)", fontsize=10, fontweight="bold")
    ax2.legend(loc="upper right", frameon=True)
    ax2.grid(True, linestyle="--", alpha=0.5)
    
    for _, row in df_sens.iterrows():
        ax2.annotate(
            f"{row['ROI Multiplicador']:.1f}x",
            xy=(row["Desconto (%)"], row["ROI Multiplicador"]),
            xytext=(0, 8),
            textcoords="offset points",
            ha="center",
            fontsize=8.5,
            fontweight="bold"
        )

    plt.suptitle("Dadosfera | Data App Streamlit: Simulação Prescritiva de ROI (Item 9)", fontsize=14, fontweight="bold", y=0.98)
    plt.tight_layout()
    
    out_path = os.path.join(OUTPUT_DIR, "data_app_roi_simulation.png")
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"[OK] Gráfico de simulação salvo em: {out_path}")
    return out_path

def generate_product_similarity_chart() -> str:
    """Gera mapa de dispersão semântico 2D de produtos."""
    prod_path = DATA_PATHS["produtos_enriquecidos"]
    if not os.path.exists(prod_path):
        print(f"[AVISO] Dataset não encontrado: {prod_path}")
        return ""
        
    df_products = pd.read_parquet(prod_path)
    df_proj = compute_2d_projection(df_products, method="pca")
    
    plt.figure(figsize=(10, 6), dpi=300)
    
    categories = df_proj["categoria_normalizada"].unique()
    colors = [COLOR_PRIMARY_NAVY, COLOR_PRIMARY_BLUE, COLOR_SUCCESS_GREEN, COLOR_WARNING_AMBER, COLOR_DANGER_RED]
    
    for i, cat in enumerate(categories):
        subset = df_proj[df_proj["categoria_normalizada"] == cat]
        color = colors[i % len(colors)]
        plt.scatter(subset["dim_x"], subset["dim_y"], label=cat, color=color, s=90, alpha=0.85, edgecolors="#0F172A", linewidth=0.8)
        
        # Anotar alguns SKUs
        for _, r in subset.head(2).iterrows():
            plt.annotate(
                r["nome_bruto"][:22] + "...",
                xy=(r["dim_x"], r["dim_y"]),
                xytext=(5, 5),
                textcoords="offset points",
                fontsize=7.5,
                alpha=0.85
            )

    plt.title("Dadosfera | Mapa Semântico 2D de Produtos (Projeção PCA das Features GenAI)", fontsize=12, fontweight="bold", pad=12)
    plt.xlabel("Componente Principal 1 (PCA)", fontsize=10, fontweight="bold")
    plt.ylabel("Componente Principal 2 (PCA)", fontsize=10, fontweight="bold")
    plt.legend(title="Categorias", loc="best", frameon=True)
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.tight_layout()
    
    out_path = os.path.join(OUTPUT_DIR, "data_app_product_similarity_map.png")
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"[OK] Mapa semântico de produtos salvo em: {out_path}")
    return out_path

def main():
    print("[INIT] Exportando evidências visuais do Data App...")
    generate_roi_simulation_chart()
    generate_product_similarity_chart()
    print("[SUCESSO] Todos os assets do Data App gerados com sucesso em 300 DPI!")

if __name__ == "__main__":
    main()
