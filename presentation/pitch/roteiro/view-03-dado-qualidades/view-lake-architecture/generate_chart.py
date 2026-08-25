#!/usr/bin/env python3
"""
generate_chart.py
Módulo: view-lake-architecture (Ato 2 / Seção [3] - Arquitetura Lakehouse Medallion & Data Quality)
Padrão Gráfico: Fundo Branco Puro (#FFFFFF), 16:9 Widescreen, 300 DPI, Tipografia Sem Serifa Moderna.
Estilização: Padrão Executivo charts-maker com grandes cilindros 3D de banco de dados,
             sem caixas/quadrados envolventes, padronização tipográfica estrita e painel inferior de métricas.
"""

from typing import Final, Dict, Any, List, Tuple
import os
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# ==============================================================================
# CONFIGURAÇÃO DE DIRETÓRIOS & CONSTANTES
# ==============================================================================

VIEW_DIR: Final[Path] = Path(__file__).resolve().parent
BASE_DIR: Final[Path] = VIEW_DIR.parents[4]  # Raiz do repositório wheels
OUTPUT_IMAGE_PATH: Final[Path] = VIEW_DIR / "chart_lake_architecture.png"
OUTPUT_POWERPOINT_PATH: Final[Path] = VIEW_DIR / "chart_powerpoint_medallion.png"

# Paleta Semântica Executiva de Alto Contraste (Padrão White Background)
COLORS: Final[Dict[str, str]] = {
    "bg": "#FFFFFF",
    "card_bg": "#F8FAFC",
    "card_border": "#94A3B8",
    "card_border_subtle": "#CBD5E1",
    
    # Tipografia de Alto Contraste Padronizada
    "text_dark": "#0F172A",          # Quase preto / Navy profundo para títulos e valores principais
    "text_title": "#0F172A",         # Títulos de seções com peso máximo
    "text_body": "#1E293B",          # Texto de leitura padrão (Slate 800 - alta legibilidade)
    "text_muted": "#334155",         # Subtítulos escuros e rótulos de categoria (Slate 700)
    "text_subtle": "#475569",        # Metadados e rodapé (Slate 600)
    
    # Camada Bronze (Âmbar / Cobre Metálico)
    "bronze_title": "#B45309",
    "bronze_light": "#FEF3C7",
    "bronze_mid": "#F59E0B",
    "bronze_dark": "#B45309",
    "bronze_border": "#78350F",
    "bronze_pill": "#FFFBEB",
    "bronze_pill_bdr": "#F59E0B",
    
    # Camada Silver (Azul Oceano / Prata Metálico)
    "silver_title": "#0369A1",
    "silver_light": "#E0F2FE",
    "silver_mid": "#38BDF8",
    "silver_dark": "#0284C7",
    "silver_border": "#0369A1",
    "silver_pill": "#F0F9FF",
    "silver_pill_bdr": "#0284C7",
    
    # Camada Gold (Púrpura / Dourado DW Metálico)
    "gold_title": "#6D28D9",
    "gold_light": "#F3E8FF",
    "gold_mid": "#A855F7",
    "gold_dark": "#7C3AED",
    "gold_border": "#5B21B6",
    "gold_pill": "#FAF5FF",
    "gold_pill_bdr": "#7C3AED",
    
    # Camada Consumo (Azul Royal Metálico)
    "consumo_title": "#1D4ED8",
    "consumo_light": "#DBEAFE",
    "consumo_mid": "#60A5FA",
    "consumo_dark": "#2563EB",
    "consumo_border": "#1D4ED8",
    "consumo_pill": "#EFF6FF",
    "consumo_pill_bdr": "#2563EB",
    
    # Quarentena & Destaques de Sucesso
    "anomaly": "#DC2626",
    "anomaly_bg": "#FEF2F2",
    "anomaly_border": "#F87171",
    
    "accent_green": "#047857",
    "accent_green_bg": "#ECFDF5",
    "accent_green_bdr": "#10B981",
}

# ==============================================================================
# FUNÇÃO DE DESENHO VETORIAL 3D DOS GRANDES CILINDROS DE BANCO DE DADOS
# ==============================================================================

def draw_grand_3d_cylinder(
    ax: plt.Axes,
    cx: float,
    cy: float,
    w: float = 0.120,
    h: float = 0.220,
    c_light: str = "#E0F2FE",
    c_mid: str = "#38BDF8",
    c_dark: str = "#0284C7",
    c_border: str = "#0369A1",
    num_disks: int = 3,
    zorder_base: int = 5
) -> None:
    """
    Desenha um cilindro de banco de dados 3D imponente e de alta definição,
    com sombreamento volumétrico realista, reflexo especular e elipses precisas.
    """
    disk_h = h / num_disks
    ry = disk_h * 0.28
    
    # 0. Sombra suave na base do cilindro
    shadow = patches.Ellipse(
        (cx, cy - h / 2.0 - 0.005), w * 1.12, ry * 2.0,
        facecolor="#CBD5E1",
        edgecolor="none",
        alpha=0.5,
        zorder=zorder_base - 1
    )
    ax.add_patch(shadow)
    
    # Cores gradientes por disco (de baixo para cima)
    disks_colors = [
        (c_dark, c_mid),
        (c_mid, c_light),
        (c_light, "#FFFFFF")
    ]
    
    for i in range(num_disks):
        base_y = cy - h / 2.0 + i * disk_h
        body_col, cap_col = disks_colors[i] if i < len(disks_colors) else (c_mid, c_light)
        
        # 1. Corpo cilíndrico do disco com sombreamento curvo
        num_slices = 24
        slice_w = w / num_slices
        for s in range(num_slices):
            sx = (cx - w / 2.0) + s * slice_w
            norm_pos = s / (num_slices - 1)
            
            if norm_pos < 0.25:
                intensity = 0.70 + (norm_pos / 0.25) * 0.30
            else:
                intensity = 1.00 - ((norm_pos - 0.25) / 0.75) * 0.45
                
            slice_rect = patches.Rectangle(
                (sx, base_y), slice_w + 0.0005, disk_h,
                facecolor=body_col,
                edgecolor="none",
                alpha=max(0.35, min(1.0, intensity)),
                zorder=zorder_base + i * 4
            )
            ax.add_patch(slice_rect)
            
        # 2. Contorno lateral do disco
        ax.plot([cx - w / 2.0, cx - w / 2.0], [base_y, base_y + disk_h], color=c_border, linewidth=1.6, zorder=zorder_base + i * 4 + 1)
        ax.plot([cx + w / 2.0, cx + w / 2.0], [base_y, base_y + disk_h], color=c_border, linewidth=1.6, zorder=zorder_base + i * 4 + 1)
        
        # 3. Arco inferior de profundidade (3D curved base)
        arc_bot = patches.Arc(
            (cx, base_y), w, ry * 2.0,
            angle=0, theta1=180, theta2=360,
            color=c_border,
            linewidth=1.5,
            zorder=zorder_base + i * 4 + 2
        )
        ax.add_patch(arc_bot)
        
        # 4. Elipse superior do disco (topo visível)
        ellipse_top = patches.Ellipse(
            (cx, base_y + disk_h), w, ry * 2.0,
            facecolor=cap_col,
            edgecolor=c_border,
            linewidth=1.5,
            zorder=zorder_base + i * 4 + 3
        )
        ax.add_patch(ellipse_top)
        
        # 5. Linha de brilho especular vertical
        spec_x = cx - w / 2.0 + w * 0.22
        ax.plot(
            [spec_x, spec_x],
            [base_y + disk_h * 0.12, base_y + disk_h * 0.88],
            color="#FFFFFF",
            alpha=0.85,
            linewidth=1.6,
            zorder=zorder_base + i * 4 + 4
        )

# ==============================================================================
# FUNÇÕES DE DESENHO AUXILIARES (ESTILO CHARTS-MAKER)
# ==============================================================================

def draw_top_kpi_card_compact(
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
    """Desenha um KPI Card compacto no topo com espaçamento interno reduzido e alto contraste."""
    card = patches.FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.0,rounding_size=0.018",
        facecolor=badge_bg,
        edgecolor=COLORS["card_border_subtle"],
        linewidth=1.1,
        zorder=2
    )
    ax.add_patch(card)
    
    # Barra de destaque horizontal superior esbelta
    bar_h = 0.020
    top_bar = patches.FancyBboxPatch(
        (x, y + h - bar_h), w, bar_h,
        boxstyle="round,pad=0.0,rounding_size=0.006",
        facecolor=accent_color,
        edgecolor="none",
        zorder=3
    )
    ax.add_patch(top_bar)
    
    # Rótulo de Categoria (Padronizado em negrito e cor nítida)
    ax.text(
        x + w / 2.0, y + h - 0.038, title.upper(),
        ha="center", va="top", fontsize=8.8, fontweight="bold",
        color=COLORS["text_muted"], zorder=4
    )
    
    # Valor Principal do KPI (Fonte grande e expressiva em negrito)
    ax.text(
        x + w / 2.0, y + h / 2.0 - 0.002, value,
        ha="center", va="center", fontsize=19.5, fontweight="bold",
        color=accent_color, zorder=4
    )
    
    # Subtítulo Descritivo (Texto normal bem legível em alto contraste)
    ax.text(
        x + w / 2.0, y + 0.024, subtitle,
        ha="center", va="bottom", fontsize=8.4, fontweight="normal",
        color=COLORS["text_dark"], zorder=4
    )


def draw_pillar_column(
    ax: plt.Axes,
    cx: float,
    title: str,
    data_type: str,
    cylinder_colors: Tuple[str, str, str, str],  # light, mid, dark, border
    bullets: List[str],
    pill_label: str,
    accent_color: str,
    pill_bg: str,
    pill_border: str,
    badge_callout: str = ""
) -> None:
    """
    Desenha uma coluna de camada arquitetural fluida e perfeitamente equilibrada,
    com cilindro 3D central, cabeçalho limpo, bullets formulados e pill padronizado.
    """
    # 1. TÍTULO PRINCIPAL DA CAMADA (Sem número, em negrito e cor temática)
    ax.text(
        cx, 0.948, title,
        ha="center", va="top", fontsize=15.5, fontweight="bold",
        color=accent_color, zorder=3
    )
    
    # 2. TIPO DE DADO (Diretamente abaixo do título em negrito de alto contraste)
    ax.text(
        cx, 0.892, data_type,
        ha="center", va="top", fontsize=9.2, fontweight="bold",
        color=COLORS["text_dark"], zorder=3
    )
    
    # Badge Callout Opcional (e.g. "Qualify" ou "Star Schema DW")
    if badge_callout:
        b_w = 0.095
        b_h = 0.036
        b_x = cx - b_w / 2.0
        b_y = 0.826
        badge_box = patches.FancyBboxPatch(
            (b_x, b_y), b_w, b_h,
            boxstyle="round,pad=0.0,rounding_size=0.010",
            facecolor=pill_bg,
            edgecolor=pill_border,
            linewidth=1.1,
            zorder=3
        )
        ax.add_patch(badge_box)
        ax.text(
            cx, b_y + b_h / 2.0, badge_callout,
            ha="center", va="center", fontsize=8.0, fontweight="bold",
            color=accent_color, zorder=4
        )
    
    # 3. GRANDE CILINDRO 3D (Elemento Hero Central)
    cyl_cy = 0.620
    cyl_w = 0.120
    cyl_h = 0.220
    draw_grand_3d_cylinder(
        ax,
        cx=cx,
        cy=cyl_cy,
        w=cyl_w,
        h=cyl_h,
        c_light=cylinder_colors[0],
        c_mid=cylinder_colors[1],
        c_dark=cylinder_colors[2],
        c_border=cylinder_colors[3],
        num_disks=3,
        zorder_base=5
    )
    
    # 4. BULLETS DESCRITIVOS (Padronização estrita: texto regular com alto contraste)
    start_y = 0.460
    line_spacing = 0.046
    for i, bullet in enumerate(bullets):
        ax.text(
            cx, start_y - i * line_spacing, bullet,
            ha="center", va="top", fontsize=8.6, fontweight="normal",
            color=COLORS["text_body"], zorder=3
        )
        
    # 5. PILL BADGE DE INFRAESTRUTURA / PLATAFORMA (Padronizado em negrito)
    pill_w = 0.160
    pill_h = 0.042
    pill_x = cx - pill_w / 2.0
    pill_y = 0.165
    pill_patch = patches.FancyBboxPatch(
        (pill_x, pill_y), pill_w, pill_h,
        boxstyle="round,pad=0.0,rounding_size=0.012",
        facecolor=pill_bg,
        edgecolor=pill_border,
        linewidth=1.2,
        zorder=3
    )
    ax.add_patch(pill_patch)
    ax.text(
        cx, pill_y + pill_h / 2.0, pill_label,
        ha="center", va="center", fontsize=8.2, fontweight="bold",
        color=accent_color, zorder=4
    )


def draw_arrow_flow(
    ax: plt.Axes,
    start_x: float,
    end_x: float,
    y: float,
    color: str,
    label: str = ""
) -> None:
    """Desenha seta de transição elegante entre os cilindros."""
    ax.annotate(
        "",
        xy=(end_x, y),
        xytext=(start_x, y),
        arrowprops=dict(
            arrowstyle="-|>",
            color=color,
            linewidth=2.2,
            mutation_scale=16.0
        ),
        zorder=6
    )
    if label:
        mid_x = (start_x + end_x) / 2.0
        ax.text(
            mid_x, y + 0.038, label,
            ha="center", va="center", fontsize=8.2, fontweight="bold",
            color=color,
            bbox=dict(boxstyle="round,pad=0.25", facecolor="#FFFFFF", edgecolor=color, linewidth=1.1),
            zorder=7
        )


def draw_layer_ground_truth_card(
    ax: plt.Axes,
    x: float,
    y: float,
    w: float,
    h: float,
    layer_title: str,
    metric_label: str,
    metric_value: str,
    detail_lines: List[str],
    accent_color: str,
    bg_color: str
) -> None:
    """
    Desenha um card analítico inferior alinhado verticalmente à sua coluna correspondente,
    com tipografia ampliada e padronização rigorosa de negritos nos títulos e métricas.
    """
    box = patches.FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.0,rounding_size=0.018",
        facecolor="#FFFFFF",
        edgecolor=COLORS["card_border_subtle"],
        linewidth=1.1,
        zorder=2
    )
    ax.add_patch(box)
    
    # Barra lateral de identificação de cor da camada
    bar_w = 0.008
    side_bar = patches.FancyBboxPatch(
        (x, y), bar_w, h,
        boxstyle="round,pad=0.0,rounding_size=0.004",
        facecolor=accent_color,
        edgecolor="none",
        zorder=3
    )
    ax.add_patch(side_bar)
    
    content_x = x + 0.016
    
    # Cabeçalho do Card (Nome da Camada em negrito e Métrica Principal em negrito)
    ax.text(
        content_x, y + h - 0.110, layer_title.upper(),
        ha="left", va="top", fontsize=8.8, fontweight="bold",
        color=accent_color, zorder=3
    )
    ax.text(
        x + w - 0.012, y + h - 0.110, metric_value,
        ha="right", va="top", fontsize=9.6, fontweight="bold",
        color=COLORS["text_dark"], zorder=3
    )
    
    # Linha divisória sutil
    ax.plot([content_x, x + w - 0.012], [y + h - 0.240, y + h - 0.240], color=COLORS["card_border_subtle"], linewidth=0.8, zorder=3)
    
    # Linhas de Detalhe Técnico (Fonte aumentada para 8.4pt, texto regular bem legível)
    for i, line in enumerate(detail_lines):
        line_y = y + h - 0.430 - i * 0.225
        ax.text(
            content_x, line_y, line,
            ha="left", va="center", fontsize=8.4, fontweight="normal",
            color=COLORS["text_body"], zorder=3
        )

# ==============================================================================
# FUNÇÃO PRINCIPAL DE PLOTAGEM EXECUTIVA UNIFICADA
# ==============================================================================

def plot_lake_architecture() -> plt.Figure:
    """Gera o painel executivo da Arquitetura Medallion com Grandes Cilindros 3D (16:9, 300 DPI)."""
    plt.rcParams["font.sans-serif"] = ["Segoe UI", "DejaVu Sans", "Helvetica", "Arial", "sans-serif"]
    
    fig = plt.figure(figsize=(16.0, 9.0), facecolor=COLORS["bg"], dpi=300)
    
    # --------------------------------------------------------------------------
    # 1. CABEÇALHO DA VIEW (TÍTULO LIMPO E FORTE)
    # --------------------------------------------------------------------------
    fig.text(
        0.050, 0.942,
        "Arquitetura Medallion Lakehouse & Qualidade de Dados",
        fontsize=20.0, fontweight="bold", color=COLORS["text_dark"]
    )
    
    # --------------------------------------------------------------------------
    # 2. TOP EXECUTIVE KPI CARDS (ESPAÇAMENTO REDUZIDO E COMPACTO)
    # --------------------------------------------------------------------------
    ax_top = fig.add_axes([0.050, 0.785, 0.900, 0.120])
    ax_top.set_xlim(0, 1)
    ax_top.set_ylim(0, 1)
    ax_top.axis("off")
    
    kpis = [
        ("Conformidade Silver Qualify", "94.2%", "Registros higienizados e aprovados para Gold DW", COLORS["accent_green"], COLORS["accent_green_bg"]),
        ("Anomalias em Quarentena", "5.8%", "Anomalias interceptadas antes do consumo analítico", COLORS["anomaly"], COLORS["anomaly_bg"]),
        ("Suíte Great Expectations", "18 Regras", "Validação sintática, integridade referencial & LGPD", COLORS["silver_dark"], COLORS["silver_pill"]),
    ]
    
    card_w = 0.290
    gap_kpi = (1.0 - (3 * card_w)) / 2.0
    for i, (title, val, sub, col, bg_col) in enumerate(kpis):
        cx = i * (card_w + gap_kpi)
        draw_top_kpi_card_compact(ax_top, cx, 0.02, card_w, 0.96, title, val, sub, col, bg_col)
        
    # --------------------------------------------------------------------------
    # 3. PAINEL PRINCIPAL: FLUXO MEDALLION COM GRANDES CILINDROS 3D
    # --------------------------------------------------------------------------
    ax_flow = fig.add_axes([0.050, 0.235, 0.900, 0.525])
    ax_flow.set_xlim(0, 1)
    ax_flow.set_ylim(0, 1)
    ax_flow.axis("off")
    
    # Fundo sutil para toda a área de fluxo (Clean Canvas aberto)
    bg_canvas = patches.FancyBboxPatch(
        (0.00, 0.08), 1.00, 0.90,
        boxstyle="round,pad=0.0,rounding_size=0.024",
        facecolor=COLORS["card_bg"],
        edgecolor=COLORS["card_border_subtle"],
        linewidth=1.2,
        zorder=1
    )
    ax_flow.add_patch(bg_canvas)
    
    # Centros X das 4 Colunas Principais
    col_x = [0.125, 0.375, 0.625, 0.875]
    
    # [PILAR 1: BRONZE]
    draw_pillar_column(
        ax_flow,
        cx=col_x[0],
        title="BRONZE",
        data_type="Dados em Estado Original (Raw)",
        cylinder_colors=(COLORS["bronze_light"], COLORS["bronze_mid"], COLORS["bronze_dark"], COLORS["bronze_border"]),
        bullets=[
            "• Ingestão contínua bruta (As-Is)",
            "• 115.777 eventos transacionais",
            "• 7 entidades originais preservadas",
            "• Imutabilidade e auditoria total"
        ],
        pill_label="Amazon S3 Storage",
        accent_color=COLORS["bronze_title"],
        pill_bg=COLORS["bronze_pill"],
        pill_border=COLORS["bronze_pill_bdr"],
        badge_callout="Raw Ingestion"
    )
    
    # [PILAR 2: SILVER] (Sem o '94.2%' no badge, documentado de forma padronizada)
    draw_pillar_column(
        ax_flow,
        cx=col_x[1],
        title="SILVER",
        data_type="Dados Validados & Higienizados",
        cylinder_colors=(COLORS["silver_light"], COLORS["silver_mid"], COLORS["silver_dark"], COLORS["silver_border"]),
        bullets=[
            "• 18 regras de Data Quality ativas",
            "• 94.2% aprovados e higienizados",
            "• 5.8% anomalias em quarentena",
            "• Anonimização e proteção LGPD"
        ],
        pill_label="Snowflake Lakehouse",
        accent_color=COLORS["silver_title"],
        pill_bg=COLORS["silver_pill"],
        pill_border=COLORS["silver_pill_bdr"],
        badge_callout="Qualify"
    )
    
    # [PILAR 3: GOLD]
    draw_pillar_column(
        ax_flow,
        cx=col_x[2],
        title="GOLD",
        data_type="Dados Estruturados Kimball DW",
        cylinder_colors=(COLORS["gold_light"], COLORS["gold_mid"], COLORS["gold_dark"], COLORS["gold_border"]),
        bullets=[
            "• Modelagem Star Schema Kimball",
            "• 6 dimensões com chaves surrogate",
            "• 2 tabelas fato de eventos e resgate",
            "• Consultas em 1-Hop sem cascata"
        ],
        pill_label="Snowflake Data Warehouse",
        accent_color=COLORS["gold_title"],
        pill_bg=COLORS["gold_pill"],
        pill_border=COLORS["gold_pill_bdr"],
        badge_callout="Star Schema DW"
    )
    
    # [PILAR 4: CONSUMO]
    draw_pillar_column(
        ax_flow,
        cx=col_x[3],
        title="CONSUMO",
        data_type="Dados para Decisão, BI & IA",
        cylinder_colors=(COLORS["consumo_light"], COLORS["consumo_mid"], COLORS["consumo_dark"], COLORS["consumo_border"]),
        bullets=[
            "• Data Views analíticas prontas",
            "• Dashboards executivos Metabase",
            "• Simulador preditivo Streamlit",
            "• Ações automatizadas com ROI 45x"
        ],
        pill_label="Metabase & Streamlit Apps",
        accent_color=COLORS["consumo_title"],
        pill_bg=COLORS["consumo_pill"],
        pill_border=COLORS["consumo_pill_bdr"],
        badge_callout="Ação & Decisão"
    )
    
    # Conectores de Fluxo com Badges Elegantes entre os Cilindros
    arrow_y = 0.620
    cyl_rad = 0.065
    
    draw_arrow_flow(ax_flow, col_x[0] + cyl_rad + 0.008, col_x[1] - cyl_rad - 0.008, arrow_y, COLORS["accent_green"], label="DQ & Limpeza")
    draw_arrow_flow(ax_flow, col_x[1] + cyl_rad + 0.008, col_x[2] - cyl_rad - 0.008, arrow_y, COLORS["gold_title"], label="Modelagem DW")
    draw_arrow_flow(ax_flow, col_x[2] + cyl_rad + 0.008, col_x[3] - cyl_rad - 0.008, arrow_y, COLORS["consumo_title"], label="Serviço SQL")
    
    # --------------------------------------------------------------------------
    # 4. PAINEL INFERIOR: ARTEFATOS & MÉTRICAS GROUND TRUTH DAS 4 CAMADAS
    # (Alinhado verticalmente com cada pilar correspondente)
    # --------------------------------------------------------------------------
    ax_cards = fig.add_axes([0.050, 0.048, 0.900, 0.165])
    ax_cards.set_xlim(0, 1)
    ax_cards.set_ylim(0, 1)
    ax_cards.axis("off")
    
    # Fundo do container analítico
    bg_cards = patches.FancyBboxPatch(
        (0.00, 0.00), 1.00, 1.00,
        boxstyle="round,pad=0.0,rounding_size=0.020",
        facecolor=COLORS["card_bg"],
        edgecolor=COLORS["card_border_subtle"],
        linewidth=1.2,
        zorder=1
    )
    ax_cards.add_patch(bg_cards)
    
    # Dados Reais do Case (Ground Truth) para cada coluna
    ground_truth_data = [
        {
            "layer": "Bronze Ingestion",
            "val": "115.777 Eventos",
            "lines": ["• 7 tabelas brutas no S3 Lake", "• Ingestão de logs e checkout", "• Histórico completo preservado"],
            "color": COLORS["bronze_title"],
            "bg": COLORS["bronze_pill"]
        },
        {
            "layer": "Silver Quality",
            "val": "109.062 Dados Limpos",
            "lines": ["• 94.2% conformidade aprovada", "• 6.715 anomalias em quarentena", "• 100% opt-in e PII mascarado"],
            "color": COLORS["silver_title"],
            "bg": COLORS["silver_pill"]
        },
        {
            "layer": "Gold Dimensional DW",
            "val": "1-Hop JOINs",
            "lines": ["• 6 Dimensões + 2 Tabelas Fato", "• Chaves surrogate (_sk) únicas", "• Latência < 50ms no Snowflake"],
            "color": COLORS["gold_title"],
            "bg": COLORS["gold_pill"]
        },
        {
            "layer": "Consumo & Conversão",
            "val": "R$ 1,27M Resgatado",
            "lines": ["• 10.1% de taxa de conversão", "• 45x ROI das réguas de resgate", "• Data Views: v_recovery_roi"],
            "color": COLORS["consumo_title"],
            "bg": COLORS["consumo_pill"]
        },
    ]
    
    card_bottom_w = 0.228
    gap_bottom = (0.960 - (4 * card_bottom_w)) / 3.0
    for i, data in enumerate(ground_truth_data):
        cx = 0.020 + i * (card_bottom_w + gap_bottom)
        draw_layer_ground_truth_card(
            ax_cards, cx, 0.08, card_bottom_w, 0.84,
            data["layer"], "", data["val"], data["lines"],
            data["color"], data["bg"]
        )
        
    # --------------------------------------------------------------------------
    # 5. RODAPÉ EXECUTIVO
    # --------------------------------------------------------------------------
    fonte_texto = "Fonte: Plataforma Dadosfera | Pipelines Datalakes | Frameworks DEC-006 (Qualidade & Quarentena) e DEC-008 (Modelagem Kimball) | Ground Truth Parquet"
    fig.text(0.050, 0.020, fonte_texto, fontsize=8.0, color=COLORS["text_subtle"], style="italic")
    
    return fig

# ==============================================================================
# EXECUÇÃO PRINCIPAL
# ==============================================================================

def main() -> None:
    """Execução declarativa que salva os artefatos de imagem de alta resolução."""
    print(f"[RUNNING] Gerando visualização executiva da Arquitetura Medallion com grandes cilindros 3D...")
    
    # 1. Gera o gráfico principal integrado
    fig_main = plot_lake_architecture()
    fig_main.savefig(str(OUTPUT_IMAGE_PATH), dpi=300, bbox_inches="tight", facecolor=COLORS["bg"])
    # Salva também como chart_powerpoint_medallion.png para sincronização total
    fig_main.savefig(str(OUTPUT_POWERPOINT_PATH), dpi=300, bbox_inches="tight", facecolor=COLORS["bg"])
    plt.close(fig_main)
    print(f"[SUCCESS] Gráfico principal salvo em: {OUTPUT_IMAGE_PATH}")
    print(f"[SUCCESS] Gráfico PowerPoint sincronizado em: {OUTPUT_POWERPOINT_PATH}")

if __name__ == "__main__":
    main()
