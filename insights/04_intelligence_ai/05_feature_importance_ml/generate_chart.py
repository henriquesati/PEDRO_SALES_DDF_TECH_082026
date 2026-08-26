#!/usr/bin/env python3
"""
generate_chart.py
Módulo Canônico: insights/04_intelligence_ai/05_feature_importance_ml
Função: Renderização executiva do Gráfico de Feature Importance e Pesos do Modelo de Propensão de Resgate (Item 8).
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

def get_base_dir() -> Path:
    curr = Path(__file__).resolve().parent
    while curr and curr.parent != curr:
        if (curr / "data" / "mock").exists():
            return curr
        curr = curr.parent
    return Path(__file__).resolve().parents[4]

BASE_DIR: Final[Path] = get_base_dir()
OUTPUT_IMAGE_PATH: Final[Path] = Path(__file__).resolve().parent / "chart_feature_importance_ml.png"

# Paleta Semântica Corporativa Dadosfera (Fundo Branco Puro)
COLOR_PRIMARY: Final[str] = "#0F172A"       # Slate 900 (Títulos e Texto Forte)
COLOR_TEXT_MUTED: Final[str] = "#475569"    # Slate 600
COLOR_BLUE: Final[str] = "#2563EB"          # Blue 600 (Estrutural / Baseline)
COLOR_GREEN: Final[str] = "#059669"         # Emerald 600 (Alavanca Positiva de Resgate)
COLOR_CORAL: Final[str] = "#E11D48"         # Rose 600 (Fricção / Abandono)
COLOR_PURPLE: Final[str] = "#7C3AED"        # Violet 600 (Machine Learning / IA)
COLOR_AMBER: Final[str] = "#D97706"         # Amber 600 (Atenção / Telemetria)
COLOR_BG_CARD: Final[str] = "#F8FAFC"       # Slate 50 (Cards)
COLOR_BORDER: Final[str] = "#CBD5E1"        # Slate 300 (Bordas)

def load_feature_data() -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """Carrega dados estruturados de pesos de variáveis do modelo treinado (Item 8)."""
    feature_records = [
        {
            "feature_raw": "valor_carrinho_atribuido",
            "feature_label": "Ticket Total do Carrinho (R$)",
            "category": "Monetário",
            "weight_pct": 38.4,
            "direction": "positive",
            "description": "Maior esforço e engajamento em tickets altos (R$ > 500)"
        },
        {
            "feature_raw": "segmento_rfm_premium",
            "feature_label": "Segmento RFM VIP / Recorrente",
            "category": "Perfil Cliente",
            "weight_pct": 26.2,
            "direction": "positive",
            "description": "Alta lealdade histórica e propensão de resposta a contato"
        },
        {
            "feature_raw": "motivo_atrito_frete",
            "feature_label": "Sensibilidade ao Frete (vs Preço)",
            "category": "Causa Atrito",
            "weight_pct": 18.5,
            "direction": "positive",
            "description": "Elasticidade imediata a incentivos de frete grátis ou cupom"
        },
        {
            "feature_raw": "flag_clicado_mobile",
            "feature_label": "Engajamento Mobile (App/WhatsApp)",
            "category": "Canal",
            "weight_pct": 9.8,
            "direction": "positive",
            "description": "Agilidade de clique e conversão em mensageria instantânea"
        },
        {
            "feature_raw": "historico_frequencia_compras",
            "feature_label": "Frequência Histórica de Pedidos",
            "category": "Perfil Cliente",
            "weight_pct": 7.1,
            "direction": "positive",
            "description": "Compradores habituais retornam espontaneamente após lembrete"
        },
        {
            "feature_raw": "tempo_sessao_abandono",
            "feature_label": "Abandono Ultrarrápido (< 5 min)",
            "category": "Comportamento",
            "weight_pct": -12.3,
            "direction": "negative",
            "description": "Sessões superficiais sem pesquisa têm menor taxa de retorno"
        }
    ]
    df_features = pd.DataFrame(feature_records)
    
    meta_metrics = {
        "model_name": "Regularized Logistic Regression (L2)",
        "roc_auc": 0.9478,
        "accuracy": 99.53,
        "f1_score": 0.9950,
        "train_samples": 5142,
        "test_samples": 1285,
        "train_duration_ms": 111.71
    }
    return df_features, meta_metrics

def plot_feature_importance_panel(df_features: pd.DataFrame, meta_metrics: Dict[str, Any]) -> plt.Figure:
    """Renderiza painel executivo de Feature Importance em 16:9 widescreen."""
    plt.rcParams["font.sans-serif"] = ["Segoe UI", "DejaVu Sans", "Helvetica", "Arial", "sans-serif"]
    plt.rcParams["axes.edgecolor"] = COLOR_BORDER
    plt.rcParams["axes.linewidth"] = 1.1

    fig = plt.figure(figsize=(16.0, 9.0), facecolor="#FFFFFF")
    
    gs = fig.add_gridspec(
        3, 2,
        height_ratios=[0.14, 0.43, 0.43],
        width_ratios=[1.15, 1.05],
        hspace=0.38,
        wspace=0.28,
        left=0.06, right=0.95, top=0.91, bottom=0.08
    )

    # 0. HEADER & KPI CARDS (Topo)
    ax_banner = fig.add_subplot(gs[0, :])
    ax_banner.axis("off")

    kpis = [
        ("Mecanismo Stepsfera", "Snowpark ML / In-Database", "Zero Cold-Start de Cluster Glue", COLOR_PURPLE),
        ("Driver Preditor #1", "Ticket do Carrinho (+38.4%)", "Maior Alavanca Marginal de Resgate", COLOR_GREEN),
        ("Poder Discriminativo", f"ROC-AUC: {meta_metrics['roc_auc']:.4f}", "Separação Quase Perfeita de Classes", COLOR_BLUE),
        ("Acurácia no Teste", f"{meta_metrics['accuracy']:.2f}% (F1: 0.995)", f"Validado em {meta_metrics['test_samples']:,} Carrinhos", COLOR_AMBER),
    ]

    card_width = 0.235
    card_gap = 0.02
    for i, (title, main_val, sub_val, col) in enumerate(kpis):
        x0 = i * (card_width + card_gap)
        card_box = patches.FancyBboxPatch(
            (x0, 0.0), card_width, 0.95,
            boxstyle="round,pad=0.02,rounding_size=0.04",
            facecolor=COLOR_BG_CARD, edgecolor=col, linewidth=1.8,
            transform=ax_banner.transAxes
        )
        ax_banner.add_patch(card_box)
        ax_banner.text(x0 + 0.015, 0.72, title.upper(), transform=ax_banner.transAxes,
                       fontsize=9.0, fontweight="bold", color=COLOR_TEXT_MUTED)
        ax_banner.text(x0 + 0.015, 0.38, main_val, transform=ax_banner.transAxes,
                       fontsize=13.0, fontweight="bold", color=COLOR_PRIMARY)
        ax_banner.text(x0 + 0.015, 0.12, sub_val, transform=ax_banner.transAxes,
                       fontsize=8.5, fontweight="semibold", color=col)

    # 1. RANKING HORIZONTAL DE PESOS DAS FEATURES (Esquerda)
    ax_feat = fig.add_subplot(gs[1:, 0])
    ax_feat.set_facecolor("#FFFFFF")
    
    y_pos = np.arange(len(df_features))
    labels = df_features["feature_label"].tolist()
    weights = df_features["weight_pct"].to_numpy()
    bar_colors = [COLOR_GREEN if w > 0 else COLOR_CORAL for w in weights]
    
    bars = ax_feat.barh(y_pos, weights, color=bar_colors, height=0.55, edgecolor=COLOR_PRIMARY, linewidth=1.1, zorder=3)
    
    for bar, val in zip(bars, weights):
        if val >= 0:
            ax_feat.text(val + 1.2, bar.get_y() + bar.get_height() / 2, f"+{val:.1f}%",
                         va="center", ha="left", fontsize=9.5, fontweight="bold", color=COLOR_GREEN)
        else:
            ax_feat.text(val - 1.2, bar.get_y() + bar.get_height() / 2, f"{val:.1f}%",
                         va="center", ha="right", fontsize=9.5, fontweight="bold", color=COLOR_CORAL)
            
    ax_feat.axvline(0, color=COLOR_PRIMARY, linewidth=1.4, zorder=4)
    ax_feat.set_yticks(y_pos)
    ax_feat.set_yticklabels(labels, fontsize=10.0, fontweight="bold", color=COLOR_PRIMARY)
    ax_feat.set_xlim(-22, 48)
    ax_feat.set_xlabel("Impacto Marginal na Probabilidade de Conversão (%)", fontsize=10.5, fontweight="bold", color=COLOR_PRIMARY)
    ax_feat.set_title("Pesos das Features no Modelo Supervisionado de Propensão\n(Coeficientes Normalizados via Regressão Logística L2)", fontsize=12.0, fontweight="bold", color=COLOR_PRIMARY, pad=12)
    ax_feat.grid(axis="x", linestyle="--", alpha=0.45, color=COLOR_BORDER)
    ax_feat.spines["top"].set_visible(False)
    ax_feat.spines["right"].set_visible(False)
    ax_feat.invert_yaxis()

    # 2. DECOMPOSIÇÃO POR MACRO-CATEGORIA DE VARIÁVEL (Direita Topo)
    ax_cat = fig.add_subplot(gs[1, 1])
    ax_cat.set_facecolor("#FFFFFF")
    
    categories = ["Valor Monetário (Ticket)", "Perfil & Histórico do Cliente", "Causa-Raiz do Atrito", "Canal & Telemetria Mobile"]
    cat_impacts = [38.4, 33.3, 18.5, 9.8]
    cat_colors = [COLOR_GREEN, COLOR_BLUE, COLOR_PURPLE, COLOR_AMBER]
    
    y_cat = np.arange(len(categories))
    cat_bars = ax_cat.barh(y_cat, cat_impacts, color=cat_colors, height=0.52, edgecolor=COLOR_PRIMARY, linewidth=1.1, zorder=3)
    
    for bar, val in zip(cat_bars, cat_impacts):
        ax_cat.text(val + 1.0, bar.get_y() + bar.get_height() / 2, f"{val:.1f}%",
                    va="center", ha="left", fontsize=9.2, fontweight="bold", color=COLOR_PRIMARY)
        
    ax_cat.set_yticks(y_cat)
    ax_cat.set_yticklabels(categories, fontsize=9.5, fontweight="bold", color=COLOR_PRIMARY)
    ax_cat.set_xlim(0, 48)
    ax_cat.set_xlabel("Peso Agregado por Dimensão (%)", fontsize=9.8, fontweight="bold", color=COLOR_PRIMARY)
    ax_cat.set_title("Decomposição Dimensional dos Fatores de Resgate\n(Contribuição Relativa dos Pilares de Dados)", fontsize=11.5, fontweight="bold", color=COLOR_PRIMARY, pad=10)
    ax_cat.grid(axis="x", linestyle="--", alpha=0.45, color=COLOR_BORDER)
    ax_cat.spines["top"].set_visible(False)
    ax_cat.spines["right"].set_visible(False)
    ax_cat.invert_yaxis()

    # 3. MATRIZ DE REGRAS OPERACIONAIS & AÇÃO CRM (Direita Base)
    ax_rules = fig.add_subplot(gs[2, 1])
    ax_rules.axis("off")
    
    rules_box = patches.FancyBboxPatch(
        (0.0, 0.0), 1.0, 1.0,
        boxstyle="round,pad=0.03,rounding_size=0.03",
        facecolor=COLOR_BG_CARD, edgecolor=COLOR_BORDER, linewidth=1.2,
        transform=ax_rules.transAxes
    )
    ax_rules.add_patch(rules_box)
    
    ax_rules.text(0.04, 0.88, "DIRETRIZES PRESCRITIVAS BASEADAS NOS PESOS DO MODELO:",
                  fontsize=10.0, fontweight="bold", color=COLOR_BLUE, transform=ax_rules.transAxes)
    
    rules_content = [
        ("• Ticket Alto (R$ > 500 / +38.4%)", "Priorizar na Fila VIP de WhatsApp com atendimento consultivo humano."),
        ("• Segmento VIP (+26.2%)", "Oferecer garantia estendida ou suporte dedicado sem queima desnecessária de margem."),
        ("• Atrito Frete (+18.5%)", "Gatilho automático de Frete Grátis com validade de 2 horas (alta conversão)."),
        ("• Abandono Imediato (-12.3%)", "Não disparar canais caros; acionar apenas Push App com produto substituto.")
    ]
    
    y_text = 0.68
    for r_title, r_desc in rules_content:
        ax_rules.text(0.04, y_text, r_title, fontsize=9.2, fontweight="bold", color=COLOR_PRIMARY, transform=ax_rules.transAxes)
        ax_rules.text(0.04, y_text - 0.11, r_desc, fontsize=8.4, color=COLOR_TEXT_MUTED, transform=ax_rules.transAxes)
        y_text -= 0.22

    plt.suptitle("MÓDULO DE INTELIGÊNCIA: PESOS E IMPORTÂNCIA DE FEATURES (STEPSFERA / ML ITEM 8)",
                 fontsize=14.5, fontweight="bold", color=COLOR_PRIMARY, y=0.97)

    return fig

def generate_and_save(target_path: Path = OUTPUT_IMAGE_PATH) -> Path:
    """Gera o gráfico e persiste no caminho alvo."""
    df_features, meta_metrics = load_feature_data()
    fig = plot_feature_importance_panel(df_features, meta_metrics)
    target_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(target_path, dpi=300, bbox_inches="tight", facecolor="#FFFFFF")
    plt.close(fig)
    return target_path

def main() -> None:
    saved = generate_and_save(OUTPUT_IMAGE_PATH)
    print(f"[SUCCESS] Painel Canônico de Feature Importance gerado em: {saved}")

if __name__ == "__main__":
    main()
