#!/usr/bin/env python3
"""
generate_chart.py
Módulo: view-governanca (Ato 2 / Seção {3.1} - Governança, Dicionário de Dados & LGPD)
Função: Renderização executiva do Dicionário de Dados Vivo, Contrato Dual-Metadata e Matriz RBAC / LGPD.
Padrão Gráfico: Fundo Branco / Rich Semantic Colors Executive (16:9 Widescreen, 300 DPI, charts-maker standard).
"""

from typing import Final, Dict, Any, List, Tuple
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# ==============================================================================
# CONFIGURAÇÃO DE CONSTANTES E PALETA DE CORES ENRIQUECIDA
# ==============================================================================

VIEW_DIR: Final[Path] = Path(__file__).resolve().parent
OUTPUT_IMAGE_PATH: Final[Path] = VIEW_DIR / "chart_governanca_lgpd.png"

# Paleta Semântica Executiva Vibrante e Contrastada (Fundo Branco Puro)
COLORS: Final[Dict[str, str]] = {
    # Fundo e Superfícies
    "bg_canvas": "#FFFFFF",
    "bg_card": "#FFFFFF",
    "bg_subtle": "#F8FAFC",
    "border_light": "#E2E8F0",
    "border_card": "#CBD5E1",
    "border_dark": "#94A3B8",
    
    # Tipografia de Alto Contraste
    "text_primary": "#0F172A",      # Slate 900
    "text_secondary": "#334155",    # Slate 700
    "text_muted": "#64748B",        # Slate 500
    "text_subtle": "#94A3B8",       # Slate 400
    
    # Cores Semânticas Vivas
    "blue_main": "#1E40AF",         # Blue 800
    "blue_bright": "#2563EB",       # Blue 600
    "blue_soft": "#EFF6FF",         # Blue 50
    "blue_bdr": "#BFDBFE",          # Blue 200
    "blue_text": "#1E3A8A",         # Blue 900
    
    "green_main": "#047857",        # Emerald 700
    "green_bright": "#059669",      # Emerald 600
    "green_soft": "#ECFDF5",        # Emerald 50
    "green_bdr": "#A7F3D0",         # Emerald 200
    "green_text": "#064E3B",        # Emerald 900
    
    "purple_main": "#6D28D9",       # Violet 700
    "purple_bright": "#7C3AED",     # Violet 600
    "purple_soft": "#FAF5FF",       # Violet 50
    "purple_bdr": "#DDD6FE",        # Violet 200
    "purple_text": "#4C1D95",       # Violet 900
    
    "amber_main": "#B45309",        # Amber 700
    "amber_bright": "#D97706",      # Amber 600
    "amber_soft": "#FFFBEB",        # Amber 50
    "amber_bdr": "#FDE68A",         # Amber 200
    "amber_text": "#78350F",        # Amber 900
    
    "rose_main": "#BE123C",         # Rose 700
    "rose_bright": "#E11D48",       # Rose 600
    "rose_soft": "#FFF1F2",         # Rose 50
    "rose_bdr": "#FECDD3",          # Rose 200
    "rose_text": "#881337",         # Rose 900
    
    "teal_main": "#0F766E",         # Teal 700
    "teal_bright": "#0D9488",       # Teal 600
    "teal_soft": "#F0FDFA",         # Teal 50
    "teal_bdr": "#99F6E4",          # Teal 200
    "teal_text": "#134E4A",         # Teal 900
    
    "indigo_main": "#4338CA",       # Indigo 700
    "indigo_bright": "#4F46E5",     # Indigo 600
    "indigo_soft": "#EEF2FF",       # Indigo 50
    "indigo_bdr": "#C7D2FE",        # Indigo 200
    "indigo_text": "#312E81",       # Indigo 900
    
    "cyan_main": "#0369A1",         # Sky 700
    "cyan_bright": "#0284C7",       # Sky 600
    "cyan_soft": "#F0F9FF",         # Sky 50
    "cyan_bdr": "#BAE6FD",          # Sky 200
    "cyan_text": "#0C4A6E"          # Sky 900
}

# ==============================================================================
# FUNÇÕES DE DESENHO AUXILIARES
# ==============================================================================

def setup_canvas(width_in: float = 16.0, height_in: float = 9.0) -> Tuple[plt.Figure, plt.Axes]:
    """Inicializa a figura em proporção 16:9 widescreen com canvas 100% branco."""
    plt.rcParams["text.parse_math"] = False
    plt.rcParams["font.sans-serif"] = ["Segoe UI", "DejaVu Sans", "Helvetica", "Arial", "sans-serif"]
    
    fig, ax = plt.subplots(figsize=(width_in, height_in), dpi=300, facecolor=COLORS["bg_canvas"])
    ax.set_facecolor(COLORS["bg_canvas"])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    return fig, ax

def draw_card(
    ax: plt.Axes,
    x: float,
    y: float,
    w: float,
    h: float,
    bg_color: str = "#FFFFFF",
    bdr_color: str = "#CBD5E1",
    rounding: float = 0.012,
    linewidth: float = 1.0,
    zorder: int = 2
) -> patches.FancyBboxPatch:
    """Desenha um container retangular executivo com cantos arredondados e borda limpa."""
    card = patches.FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad=0.0,rounding_size={rounding}",
        facecolor=bg_color,
        edgecolor=bdr_color,
        linewidth=linewidth,
        zorder=zorder
    )
    ax.add_patch(card)
    return card

def draw_badge(
    ax: plt.Axes,
    x: float,
    y: float,
    w: float,
    h: float,
    text: str,
    bg_color: str,
    bdr_color: str,
    text_color: str,
    font_size: float = 6.8,
    rounding: float = 0.005,
    font_weight: str = "bold",
    zorder: int = 5
) -> None:
    """Desenha uma badge semântica de classificação com tipografia nítida."""
    badge = patches.FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad=0.0,rounding_size={rounding}",
        facecolor=bg_color,
        edgecolor=bdr_color,
        linewidth=0.9,
        zorder=zorder
    )
    ax.add_patch(badge)
    ax.text(
        x + w / 2.0, y + h / 2.0, text,
        ha="center", va="center", fontsize=font_size, fontweight=font_weight,
        color=text_color, zorder=zorder + 1
    )

# ==============================================================================
# 1. CABEÇALHO EXECUTIVO
# ==============================================================================

def render_header(ax: plt.Axes) -> None:
    """Renderiza a régua de cabeçalho executiva e títulos de impacto."""
    # Tag de Identificação da Seção
    tag_bg = patches.FancyBboxPatch(
        (0.040, 0.940), 0.330, 0.028,
        boxstyle="round,pad=0.0,rounding_size=0.006",
        facecolor=COLORS["blue_soft"],
        edgecolor=COLORS["blue_bdr"],
        linewidth=1.0,
        zorder=2
    )
    ax.add_patch(tag_bg)
    ax.text(
        0.050, 0.954, "[ ATO 2 / SEÇÃO {3.1} ]  GOVERNANÇA, CATÁLOGO & BLINDAGEM LGPD",
        ha="left", va="center", fontsize=8.2, fontweight="bold",
        color=COLORS["blue_main"], zorder=3
    )
    
    # Título Principal
    ax.text(
        0.040, 0.898, "Catálogo & Governança Ativa: Dicionário Vivo, RBAC Centralizado e Blindagem LGPD",
        ha="left", va="center", fontsize=15.5, fontweight="bold",
        color=COLORS["text_primary"], zorder=3
    )
    
    # Subtítulo com Proposta de Valor
    ax.text(
        0.040, 0.865,
        "Plataforma Dadosfera: Tagging PII automático, conformidade de opt-in mandatório (ANOM-03) e governança ágil self-service",
        ha="left", va="center", fontsize=9.2, fontweight="normal",
        color=COLORS["text_secondary"], zorder=3
    )

# ==============================================================================
# 2. TOP 3 KPI CARDS COLORIDOS E VIBRANTES
# ==============================================================================

def render_kpi_cards(ax: plt.Axes) -> None:
    """Renderiza 3 Mini-Cards de KPIs ricos em cores semânticas e profundidade visual."""
    kpi_configs = [
        {
            "x": 0.040, "w": 0.285, "h": 0.110, "y": 0.735,
            "title": "CATÁLOGO CANÔNICO & ATIVOS",
            "val": "7 Ativos Oficiais",
            "sub": "100% Linhagem Mapeada • Regra \"A é um B que C\"",
            "badge_text": "[ METADADOS VIVOS ]",
            "bg_color": COLORS["blue_soft"],
            "bdr_color": COLORS["blue_bdr"],
            "accent": COLORS["blue_bright"],
            "text_color": COLORS["blue_main"],
            "badge_bg": "#DBEAFE",
            "badge_col": COLORS["blue_main"]
        },
        {
            "x": 0.340, "w": 0.285, "h": 0.110, "y": 0.735,
            "title": "BLINDAGEM LGPD BY DESIGN",
            "val": "100% Proteção PII",
            "sub": "Opt-in Mandatório por Canal • Quarentena Ativa (ANOM-03)",
            "badge_text": "[ ZERO VAZAMENTO ]",
            "bg_color": COLORS["green_soft"],
            "bdr_color": COLORS["green_bdr"],
            "accent": COLORS["green_bright"],
            "text_color": COLORS["green_main"],
            "badge_bg": "#D1FAE5",
            "badge_col": COLORS["green_main"]
        },
        {
            "x": 0.640, "w": 0.320, "h": 0.110, "y": 0.735,
            "title": "GOVERNANÇA ÁGIL & RBAC",
            "val": "< 3 Dias Lead Time",
            "sub": "Self-Service Seguro • Fim dos Silos & Acesso Centralizado",
            "badge_text": "[ FIM DO SHADOW IT ]",
            "bg_color": COLORS["purple_soft"],
            "bdr_color": COLORS["purple_bdr"],
            "accent": COLORS["purple_bright"],
            "text_color": COLORS["purple_main"],
            "badge_bg": "#EDE9FE",
            "badge_col": COLORS["purple_main"]
        }
    ]
    
    for kpi in kpi_configs:
        # Fundo colorido suave do card
        draw_card(ax, kpi["x"], kpi["y"], kpi["w"], kpi["h"], bg_color=kpi["bg_color"], bdr_color=kpi["bdr_color"], rounding=0.012, linewidth=1.2)
        
        # Barra de destaque colorida no topo
        bar = patches.FancyBboxPatch(
            (kpi["x"], kpi["y"] + kpi["h"] - 0.014), kpi["w"], 0.014,
            boxstyle="round,pad=0.0,rounding_size=0.006",
            facecolor=kpi["accent"],
            edgecolor="none",
            zorder=3
        )
        ax.add_patch(bar)
        
        # Mini Badge no Canto Superior Direito do Card
        draw_badge(ax, kpi["x"] + kpi["w"] - 0.110, kpi["y"] + kpi["h"] - 0.034, 0.100, 0.016,
                   kpi["badge_text"], kpi["badge_bg"], kpi["bdr_color"], kpi["badge_col"], font_size=6.0)
        
        # Textos do KPI
        center_x = kpi["x"] + 0.018
        ax.text(
            center_x, kpi["y"] + 0.076, kpi["title"],
            ha="left", va="center", fontsize=7.8, fontweight="bold",
            color=kpi["text_color"], zorder=4
        )
        ax.text(
            center_x, kpi["y"] + 0.047, kpi["val"],
            ha="left", va="center", fontsize=15.5, fontweight="bold",
            color=kpi["accent"], zorder=4
        )
        ax.text(
            center_x, kpi["y"] + 0.018, kpi["sub"],
            ha="left", va="center", fontsize=7.2, fontweight="normal",
            color=COLORS["text_secondary"], zorder=4
        )

# ==============================================================================
# 3. PAINEL ESQUERDO: DICIONÁRIO VIVO & CATÁLOGO CANÔNICO
# ==============================================================================

def render_left_panel_dictionary(ax: plt.Axes) -> None:
    """Renderiza o Painel Esquerdo: Dicionário Vivo de Dados com Classificação LGPD colorida e Metadados."""
    x, y, w, h = 0.040, 0.115, 0.445, 0.605
    
    # Fundo do Card
    draw_card(ax, x, y, w, h, bg_color=COLORS["bg_card"], bdr_color=COLORS["border_dark"], rounding=0.014, linewidth=1.2)
    
    # Cabeçalho da Tabela de Dicionário
    ax.text(
        x + 0.016, y + h - 0.030, "CATÁLOGO: ENTIDADE CLIENTES",
        ha="left", va="center", fontsize=10.5, fontweight="bold",
        color=COLORS["blue_main"], zorder=3
    )
    
    # Badges do Cabeçalho Coloridas
    draw_badge(ax, x + w - 0.220, y + h - 0.038, 0.072, 0.018, "QUALIFY / SILVER", COLORS["cyan_soft"], COLORS["cyan_bdr"], COLORS["cyan_main"], font_size=6.2)
    draw_badge(ax, x + w - 0.144, y + h - 0.038, 0.070, 0.018, "ID: 0327fecc", COLORS["purple_soft"], COLORS["purple_bdr"], COLORS["purple_main"], font_size=6.2)
    draw_badge(ax, x + w - 0.070, y + h - 0.038, 0.060, 0.018, "SNOWFLAKE", COLORS["teal_soft"], COLORS["teal_bdr"], COLORS["teal_main"], font_size=6.2)
    
    ax.text(
        x + 0.016, y + h - 0.052, "Tabela Snowflake: CART_RECOVERY.CLIENTES  •  Asset ID: 0327fecc-f826-48fb-bb0a-1493fe18a32c",
        ha="left", va="center", fontsize=7.2, fontweight="bold",
        color=COLORS["text_muted"], zorder=3
    )
    
    # Caixa de Destaque: Regra Canônica "A é um B que C" com acento dourado vivo
    def_box_y = y + h - 0.115
    def_box = patches.FancyBboxPatch(
        (x + 0.014, def_box_y), w - 0.028, 0.052,
        boxstyle="round,pad=0.0,rounding_size=0.008",
        facecolor=COLORS["amber_soft"],
        edgecolor=COLORS["amber_bdr"],
        linewidth=1.2,
        zorder=3
    )
    ax.add_patch(def_box)
    
    # Barra lateral de acento na caixa de definição
    accent_strip = patches.FancyBboxPatch(
        (x + 0.014, def_box_y), 0.005, 0.052,
        boxstyle="round,pad=0.0,rounding_size=0.002",
        facecolor=COLORS["amber_bright"],
        edgecolor="none",
        zorder=4
    )
    ax.add_patch(accent_strip)
    
    ax.text(
        x + 0.026, def_box_y + 0.038, "DEFINIÇÃO CANÔNICA DE NEGÓCIO (Regra \"A é um B que C\"):",
        ha="left", va="center", fontsize=7.4, fontweight="bold",
        color=COLORS["amber_main"], zorder=5
    )
    ax.text(
        x + 0.026, def_box_y + 0.016,
        "\"Cliente é a pessoa física compradora que interage com o marketplace, cujos contatos cadastrais são\nestritamente regidos pela LGPD e exigem Opt-In ativo para disparos de réguas de resgate.\"",
        ha="left", va="center", fontsize=7.0, fontweight="normal", style="italic",
        color=COLORS["amber_text"], zorder=5
    )
    
    # Tabela de Atributos com Classificação LGPD
    table_top_y = def_box_y - 0.028
    
    # Cabeçalho das Colunas
    cols = [
        ("ATRIBUTO", x + 0.016, "left"),
        ("TIPO", x + 0.110, "left"),
        ("CLASSIFICAÇÃO LGPD", x + 0.220, "center"),
        ("GOVERNANÇA / REGRA", x + 0.290, "left")
    ]
    for cname, cx_pos, calign in cols:
        ax.text(cx_pos, table_top_y, cname, ha=calign, va="center", fontsize=7.4, fontweight="bold", color=COLORS["text_secondary"], zorder=3)
        
    ax.plot([x + 0.014, x + w - 0.014], [table_top_y - 0.012, table_top_y - 0.012], color=COLORS["border_light"], lw=1.0, zorder=3)
    
    # Linhas da Tabela Coloridas e Categorizadas
    rows_data = [
        {
            "name": "cliente_id", "type": "VARCHAR(36)",
            "badge_text": "[ PÚBLICO / PK ]", "badge_bg": COLORS["green_soft"], "badge_bdr": COLORS["green_bdr"], "badge_col": COLORS["green_bright"],
            "dot_color": COLORS["green_bright"],
            "rule": "Identificador único cadastral CRM"
        },
        {
            "name": "nome", "type": "VARCHAR(150)",
            "badge_text": "[ PII MASCARADO ]", "badge_bg": COLORS["rose_soft"], "badge_bdr": COLORS["rose_bdr"], "badge_col": COLORS["rose_bright"],
            "dot_color": COLORS["rose_bright"],
            "rule": "Anonimização SHA-256 no RBAC"
        },
        {
            "name": "email", "type": "VARCHAR(255)",
            "badge_text": "[ PII / OPT-IN ]", "badge_bg": COLORS["rose_soft"], "badge_bdr": COLORS["rose_bdr"], "badge_col": COLORS["rose_bright"],
            "dot_color": COLORS["rose_bright"],
            "rule": "Canal de resgate (Exige Opt-In)"
        },
        {
            "name": "telefone", "type": "VARCHAR(30)",
            "badge_text": "[ PII / WHATSAPP ]", "badge_bg": COLORS["rose_soft"], "badge_bdr": COLORS["rose_bdr"], "badge_col": COLORS["rose_bright"],
            "dot_color": COLORS["rose_bright"],
            "rule": "Disparos WhatsApp (Regra ANOM-03)"
        },
        {
            "name": "segmento", "type": "VARCHAR(50)",
            "badge_text": "[ RFM CLUSTER ]", "badge_bg": COLORS["indigo_soft"], "badge_bdr": COLORS["indigo_bdr"], "badge_col": COLORS["indigo_bright"],
            "dot_color": COLORS["indigo_bright"],
            "rule": "VIP, Regular, Novo, Dormant"
        },
        {
            "name": "ltv_estimado", "type": "FLOAT",
            "badge_text": "[ MÉTRICA GOLD ]", "badge_bg": COLORS["purple_soft"], "badge_bdr": COLORS["purple_bdr"], "badge_col": COLORS["purple_bright"],
            "dot_color": COLORS["purple_bright"],
            "rule": "Lifetime value preditivo da conta"
        },
    ]
    
    row_y_start = table_top_y - 0.030
    row_spacing = 0.045
    
    for i, row in enumerate(rows_data):
        ry = row_y_start - i * row_spacing
        
        # Fundo alternado sutil para legibilidade
        if i % 2 == 1:
            row_bg = patches.Rectangle((x + 0.014, ry - 0.016), w - 0.028, 0.034, facecolor=COLORS["bg_subtle"], edgecolor="none", zorder=2)
            ax.add_patch(row_bg)
            
        # Ponto colorido indicador da linha
        ax.add_patch(patches.Circle((x + 0.020, ry), 0.003, facecolor=row["dot_color"], edgecolor="none", zorder=4))
        
        ax.text(x + 0.028, ry, row["name"], ha="left", va="center", fontsize=7.6, fontweight="bold", fontfamily="monospace", color=COLORS["text_primary"], zorder=3)
        ax.text(x + 0.110, ry, row["type"], ha="left", va="center", fontsize=7.0, fontweight="normal", fontfamily="monospace", color=COLORS["text_muted"], zorder=3)
        
        # Badge de Classificação Colorida
        draw_badge(ax, x + 0.170, ry - 0.010, 0.100, 0.020, row["badge_text"], row["badge_bg"], row["badge_bdr"], row["badge_col"], font_size=6.6)
        
        ax.text(x + 0.290, ry, row["rule"], ha="left", va="center", fontsize=7.0, fontweight="normal", color=COLORS["text_secondary"], zorder=3)

    # Tags de Governança no Rodapé do Dicionário com 4 Cores Semânticas
    tags_y = y + 0.022
    ax.text(x + 0.016, tags_y, "Tags de Governança:", ha="left", va="center", fontsize=7.2, fontweight="bold", color=COLORS["text_muted"], zorder=3)
    
    draw_badge(ax, x + 0.115, tags_y - 0.009, 0.068, 0.018, "pii_sensivel", COLORS["rose_soft"], COLORS["rose_bdr"], COLORS["rose_bright"], font_size=6.2)
    draw_badge(ax, x + 0.188, tags_y - 0.009, 0.082, 0.018, "opt_in_mandatorio", COLORS["amber_soft"], COLORS["amber_bdr"], COLORS["amber_bright"], font_size=6.2)
    draw_badge(ax, x + 0.275, tags_y - 0.009, 0.075, 0.018, "rbac_governed", COLORS["purple_soft"], COLORS["purple_bdr"], COLORS["purple_bright"], font_size=6.2)
    draw_badge(ax, x + 0.355, tags_y - 0.009, 0.068, 0.018, "qualify_silver", COLORS["teal_soft"], COLORS["teal_bdr"], COLORS["teal_bright"], font_size=6.2)

# ==============================================================================
# 4. PAINEL DIREITO: CONTRATO EXECUTIVO DE METADADOS & MATRIZ RBAC COLORIDA
# ==============================================================================

def render_right_panel_contract(ax: plt.Axes) -> None:
    """Renderiza o Painel Direito: Card Executivo de Contrato Dual-Metadata e Matriz RBAC / Governança com mais cores."""
    x, y, w, h = 0.505, 0.115, 0.455, 0.605
    
    # Fundo do Card Principal Branco
    draw_card(ax, x, y, w, h, bg_color=COLORS["bg_card"], bdr_color=COLORS["border_dark"], rounding=0.014, linewidth=1.2)
    
    # Cabeçalho do Card
    ax.text(
        x + 0.016, y + h - 0.030, "CONTRATO EXECUTIVO: METADADOS & RBAC",
        ha="left", va="center", fontsize=10.0, fontweight="bold",
        color=COLORS["blue_main"], zorder=3
    )
    
    # Badge do Schema Version / Decisão
    draw_badge(ax, x + w - 0.130, y + h - 0.038, 0.115, 0.018, "DEC-006 DUAL-METADATA", COLORS["blue_soft"], COLORS["blue_bdr"], COLORS["blue_bright"], font_size=6.2)
    
    ax.text(
        x + 0.016, y + h - 0.052, "Especificação Canônica de Governança, Políticas de Acesso e Regras de Compliance",
        ha="left", va="center", fontsize=7.2, fontweight="bold",
        color=COLORS["text_muted"], zorder=3
    )
    
    # --------------------------------------------------------------------------
    # BLOCO 1: Identificação & Linhagem Ativa (Sky Blue Tint)
    # --------------------------------------------------------------------------
    b1_y = y + h - 0.176
    b1_h = 0.110
    b1_box = patches.FancyBboxPatch(
        (x + 0.014, b1_y), w - 0.028, b1_h,
        boxstyle="round,pad=0.0,rounding_size=0.008",
        facecolor=COLORS["cyan_soft"],
        edgecolor=COLORS["cyan_bdr"],
        linewidth=1.1,
        zorder=3
    )
    ax.add_patch(b1_box)
    
    ax.text(
        x + 0.024, b1_y + b1_h - 0.016, "1. IDENTIFICAÇÃO DO ATIVO & LINHAGEM ATIVA DADOSFERA",
        ha="left", va="center", fontsize=7.4, fontweight="bold",
        color=COLORS["cyan_main"], zorder=4
    )
    
    # Linha 1: Asset ID e Governança
    ax.text(x + 0.024, b1_y + 0.066, "Asset ID Oficial:", ha="left", va="center", fontsize=6.8, fontweight="bold", color=COLORS["text_secondary"], zorder=4)
    ax.text(x + 0.098, b1_y + 0.066, "0327fecc-f826-48fb-bb0a-1493fe18a32c", ha="left", va="center", fontsize=6.8, fontweight="bold", fontfamily="monospace", color=COLORS["purple_main"], zorder=4)
    
    ax.text(x + 0.315, b1_y + 0.066, "SLA / Tier:", ha="left", va="center", fontsize=6.8, fontweight="bold", color=COLORS["text_secondary"], zorder=4)
    ax.text(x + 0.365, b1_y + 0.066, "Tier 1 (< 15 min)", ha="left", va="center", fontsize=6.8, fontweight="bold", color=COLORS["green_main"], zorder=4)
    
    # Linha 2: Entidade e Tabela Snowflake
    ax.text(x + 0.024, b1_y + 0.040, "Entidade Canônica:", ha="left", va="center", fontsize=6.8, fontweight="bold", color=COLORS["text_secondary"], zorder=4)
    ax.text(x + 0.110, b1_y + 0.040, "clientes_qualify (Silver)", ha="left", va="center", fontsize=6.8, fontweight="bold", color=COLORS["blue_main"], zorder=4)
    
    ax.text(x + 0.235, b1_y + 0.040, "Tabela Snowflake:", ha="left", va="center", fontsize=6.8, fontweight="bold", color=COLORS["text_secondary"], zorder=4)
    ax.text(x + 0.320, b1_y + 0.040, "CART_RECOVERY.CLIENTES", ha="left", va="center", fontsize=6.8, fontweight="bold", fontfamily="monospace", color=COLORS["teal_main"], zorder=4)
    
    # Linha 3: Linhagem Mapeada com Pills Coloridas
    ax.text(x + 0.024, b1_y + 0.016, "Linhagem:", ha="left", va="center", fontsize=6.8, fontweight="bold", color=COLORS["text_secondary"], zorder=4)
    
    draw_badge(ax, x + 0.075, b1_y + 0.007, 0.078, 0.016, "Bronze S3 (Raw)", COLORS["amber_soft"], COLORS["amber_bdr"], COLORS["amber_bright"], font_size=5.8)
    ax.text(x + 0.160, b1_y + 0.016, "->", ha="center", va="center", fontsize=7.2, fontweight="bold", color=COLORS["text_muted"], zorder=4)
    draw_badge(ax, x + 0.168, b1_y + 0.007, 0.095, 0.016, "Silver (ANOM-03)", COLORS["teal_soft"], COLORS["teal_bdr"], COLORS["teal_bright"], font_size=5.8)
    ax.text(x + 0.270, b1_y + 0.016, "->", ha="center", va="center", fontsize=7.2, fontweight="bold", color=COLORS["text_muted"], zorder=4)
    draw_badge(ax, x + 0.278, b1_y + 0.007, 0.095, 0.016, "Gold Curated (Kimball)", COLORS["green_soft"], COLORS["green_bdr"], COLORS["green_bright"], font_size=5.8)
        
    # --------------------------------------------------------------------------
    # BLOCO 2: Matriz de Controle de Acesso Baseada em Papéis (RBAC - 3 Cores Distintas)
    # --------------------------------------------------------------------------
    b2_y = b1_y - 0.160
    b2_h = 0.146
    b2_box = patches.FancyBboxPatch(
        (x + 0.014, b2_y), w - 0.028, b2_h,
        boxstyle="round,pad=0.0,rounding_size=0.008",
        facecolor=COLORS["purple_soft"],
        edgecolor=COLORS["purple_bdr"],
        linewidth=1.1,
        zorder=3
    )
    ax.add_patch(b2_box)
    
    ax.text(
        x + 0.024, b2_y + b2_h - 0.016, "2. MATRIZ DE CONTROLE DE ACESSO POR PAPEL (RBAC CENTRALIZADO)",
        ha="left", va="center", fontsize=7.4, fontweight="bold",
        color=COLORS["purple_main"], zorder=4
    )
    
    rbac_rows = [
        ("CRM_OPS", "[ READ_MASKED ]", COLORS["indigo_soft"], COLORS["indigo_bdr"], COLORS["indigo_bright"], "Anonimização dinâmica SHA-256 de contatos"),
        ("MARKETING_ANALYTICS", "[ AGGREGATED_ONLY ]", COLORS["teal_soft"], COLORS["teal_bdr"], COLORS["teal_bright"], "Apenas métricas e clusters (Sem acesso a PII)"),
        ("DATA_ENGINEERING", "[ FULL_AUDITED ]", COLORS["green_soft"], COLORS["green_bdr"], COLORS["green_bright"], "Acesso técnico completo com auditoria ativa")
    ]
    
    r_start_y = b2_y + b2_h - 0.040
    r_spacing = 0.036
    for i, (role_name, perm_badge, p_bg, p_bdr, p_col, scope_desc) in enumerate(rbac_rows):
        ry = r_start_y - i * r_spacing
        
        # Mini Card para cada Role
        role_card = patches.FancyBboxPatch(
            (x + 0.022, ry - 0.013), w - 0.044, 0.027,
            boxstyle="round,pad=0.0,rounding_size=0.005",
            facecolor="#FFFFFF",
            edgecolor=p_bdr,
            linewidth=0.8,
            zorder=4
        )
        ax.add_patch(role_card)
        
        ax.add_patch(patches.Circle((x + 0.032, ry), 0.003, facecolor=p_col, edgecolor="none", zorder=5))
        ax.text(x + 0.040, ry, role_name, ha="left", va="center", fontsize=7.0, fontweight="bold", fontfamily="monospace", color=COLORS["text_primary"], zorder=5)
        
        draw_badge(ax, x + 0.170, ry - 0.009, 0.095, 0.018, perm_badge, p_bg, p_bdr, p_col, font_size=6.2)
        ax.text(x + 0.272, ry, scope_desc, ha="left", va="center", fontsize=6.7, fontweight="normal", color=COLORS["text_secondary"], zorder=5)

    # --------------------------------------------------------------------------
    # BLOCO 3: Políticas de Blindagem LGPD & Quarentena (Emerald & Rose Alerta)
    # --------------------------------------------------------------------------
    b3_y = y + 0.018
    b3_h = 0.126
    b3_box = patches.FancyBboxPatch(
        (x + 0.014, b3_y), w - 0.028, b3_h,
        boxstyle="round,pad=0.0,rounding_size=0.008",
        facecolor=COLORS["green_soft"],
        edgecolor=COLORS["green_bdr"],
        linewidth=1.1,
        zorder=3
    )
    ax.add_patch(b3_box)
    
    ax.text(
        x + 0.024, b3_y + b3_h - 0.016, "3. POLÍTICAS DE BLINDAGEM LGPD & QUARENTENA AUTOMATIZADA",
        ha="left", va="center", fontsize=7.4, fontweight="bold",
        color=COLORS["green_main"], zorder=4
    )
    
    lgpd_rules = [
        ("Opt-in Mandatório por Canal:", "Disparos bloqueados se opt-in = false (Regra ANOM-03)", COLORS["green_bright"], "[ STRICT ]", COLORS["green_soft"], COLORS["green_bdr"], COLORS["green_bright"]),
        ("Anonimização Dinâmica PII:", "Algoritmo SHA-256 com Salt para mascarar campos sensíveis", COLORS["blue_bright"], "[ SHA-256 ]", COLORS["blue_soft"], COLORS["blue_bdr"], COLORS["blue_bright"]),
        ("Ação em Não-Conformidade:", "ISOLATE_INTO_ANOMALIES_TABLE (Quarentena Ativa Silver)", COLORS["rose_bright"], "[ ANOM-03 ]", COLORS["rose_soft"], COLORS["rose_bdr"], COLORS["rose_bright"])
    ]
    
    g_start_y = b3_y + b3_h - 0.038
    g_spacing = 0.028
    for i, (rule_title, rule_text, dot_color, badge_lbl, b_bg, b_bdr, b_col) in enumerate(lgpd_rules):
        gy = g_start_y - i * g_spacing
        
        ax.add_patch(patches.Circle((x + 0.028, gy), 0.003, facecolor=dot_color, edgecolor="none", zorder=4))
        ax.text(x + 0.036, gy, rule_title, ha="left", va="center", fontsize=6.8, fontweight="bold", color=COLORS["text_primary"], zorder=4)
        ax.text(x + 0.170, gy, rule_text, ha="left", va="center", fontsize=6.7, fontweight="normal", color=COLORS["text_secondary"], zorder=4)
        draw_badge(ax, x + w - 0.080, gy - 0.008, 0.052, 0.016, badge_lbl, b_bg, b_bdr, b_col, font_size=5.8)

# ==============================================================================
# 5. BANNER INFERIOR: CICLO DE VIDA DA GOVERNANÇA ATIVA
# ==============================================================================

def render_footer_banner(ax: plt.Axes) -> None:
    """Renderiza a régua inferior com o fluxo de ponta a ponta e notas institucionais."""
    # Banner de Fluxo
    bx, by, bw, bh = 0.040, 0.038, 0.920, 0.052
    draw_card(ax, bx, by, bw, bh, bg_color=COLORS["bg_subtle"], bdr_color=COLORS["border_light"], rounding=0.008)
    
    # 5 Etapas do Fluxo de Governança com 5 Cores Semânticas Vivas
    steps = [
        ("1. Ingestão Bruta", "Bronze S3 (Raw)", COLORS["amber_bright"], COLORS["amber_soft"], COLORS["amber_bdr"]),
        ("2. Tagging PII", "Auto Classify", COLORS["blue_bright"], COLORS["blue_soft"], COLORS["blue_bdr"]),
        ("3. Validação Opt-In", "Regra ANOM-03", COLORS["rose_bright"], COLORS["rose_soft"], COLORS["rose_bdr"]),
        ("4. Quarentena Silver", "Isolamento Ativo", COLORS["purple_bright"], COLORS["purple_soft"], COLORS["purple_bdr"]),
        ("5. Data Views Seguras", "RBAC Centralizado", COLORS["green_bright"], COLORS["green_soft"], COLORS["green_bdr"])
    ]
    
    step_w = bw / 5.0
    for i, (stitle, ssub, scolor, sbg, sbdr) in enumerate(steps):
        sx = bx + i * step_w + 0.010
        sy = by + bh / 2.0
        
        # Pill container para a etapa
        step_box = patches.FancyBboxPatch(
            (sx, by + 0.006), step_w - 0.024, bh - 0.012,
            boxstyle="round,pad=0.0,rounding_size=0.006",
            facecolor=sbg,
            edgecolor=sbdr,
            linewidth=0.8,
            zorder=3
        )
        ax.add_patch(step_box)
        
        # Indicador de Ponto Colorido
        ax.add_patch(patches.Circle((sx + 0.010, sy + 0.005), 0.0035, facecolor=scolor, edgecolor="none", zorder=4))
        
        # Textos da Etapa
        ax.text(sx + 0.018, sy + 0.005, stitle, ha="left", va="center", fontsize=7.2, fontweight="bold", color=COLORS["text_primary"], zorder=4)
        ax.text(sx + 0.018, sy - 0.011, ssub, ha="left", va="center", fontsize=6.3, fontweight="normal", color=scolor, zorder=4)
        
        # Seta conectora entre etapas
        if i < 4:
            ax.text(sx + step_w - 0.012, sy, "->", ha="center", va="center", fontsize=7.8, fontweight="bold", color=COLORS["text_muted"], zorder=4)

    # Rodapé Técnico Canônico
    ax.text(
        0.040, 0.014,
        "Fonte: Catálogo & Governança Dadosfera | Framework Normativo LGPD & Dual-Metadata (DEC-006) | charts-maker 300 DPI",
        ha="left", va="center", fontsize=6.8, fontweight="normal", style="italic",
        color=COLORS["text_muted"], zorder=3
    )

# ==============================================================================
# FUNÇÃO PRINCIPAL DECLARATIVA
# ==============================================================================

def generate_governance_chart() -> plt.Figure:
    """Monta o painel completo de Governança, Dicionário e LGPD seguindo o padrão charts-maker."""
    fig, ax = setup_canvas(width_in=16.0, height_in=9.0)
    
    # 1. Cabeçalho Executivo
    render_header(ax)
    
    # 2. Mini-Cards de KPIs Superiores (Zero AWS Comparison, cores vibrantes)
    render_kpi_cards(ax)
    
    # 3. Painel Esquerdo: Dicionário Vivo de Dados & Regra Canônica
    render_left_panel_dictionary(ax)
    
    # 4. Painel Direito: Contrato Executivo de Metadados & Matriz RBAC Colorida
    render_right_panel_contract(ax)
    
    # 5. Banner Inferior de Fluxo e Rodapé Técnico
    render_footer_banner(ax)
    
    return fig

def main() -> None:
    """Executa a geração declarativa do gráfico e persiste em 300 DPI."""
    print(f"[RUNNING] Gerando painel executivo de Governança & LGPD em: {OUTPUT_IMAGE_PATH}...")
    fig = generate_governance_chart()
    fig.savefig(
        str(OUTPUT_IMAGE_PATH),
        dpi=300,
        bbox_inches="tight",
        facecolor=COLORS["bg_canvas"],
        edgecolor="none"
    )
    plt.close(fig)
    print(f"[SUCCESS] Painel de Governança & LGPD salvo com sucesso em: {OUTPUT_IMAGE_PATH}")

if __name__ == "__main__":
    main()
