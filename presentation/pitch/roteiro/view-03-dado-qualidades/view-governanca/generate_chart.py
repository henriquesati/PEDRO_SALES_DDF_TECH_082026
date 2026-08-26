#!/usr/bin/env python3
"""
generate_chart.py
Módulo: view-governanca (Ato 2 / Seção {3.1} - Governança, Dicionário de Dados & LGPD)
Função: Renderização executiva do Dicionário de Dados Vivo, Contrato Dual-Metadata e Matriz RBAC / LGPD.
Padrão Gráfico: Fundo Branco / Clean Executive (16:9 Widescreen, 300 DPI).
"""

from typing import Final, Dict, Any, List, Tuple
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# ==============================================================================
# CONFIGURAÇÃO DE CONSTANTES E PALETA DE CORES
# ==============================================================================

VIEW_DIR: Final[Path] = Path(__file__).resolve().parent
OUTPUT_IMAGE_PATH: Final[Path] = VIEW_DIR / "chart_governanca_lgpd.png"

# Paleta Semântica Executiva de Alto Padrão (Clean White Background)
COLORS: Final[Dict[str, str]] = {
    # Fundo e Superfícies
    "bg_canvas": "#FFFFFF",
    "bg_card": "#FFFFFF",
    "bg_subtle": "#F8FAFC",
    "border_light": "#E2E8F0",
    "border_card": "#CBD5E1",
    "border_dark": "#94A3B8",
    
    # Tipografia de Alto Contraste
    "text_primary": "#0F172A",      # Navy Profundo / Títulos
    "text_secondary": "#334155",    # Slate Escuro / Corpo Principal
    "text_muted": "#64748B",        # Slate Médio / Subtítulos
    "text_subtle": "#94A3B8",       # Slate Claro / Metadados
    
    # Cores Institucionais & Acentos Executivos
    "brand_blue": "#1E40AF",        # Azul Real Dadosfera
    "accent_blue": "#2563EB",
    "blue_light_bg": "#EFF6FF",
    "blue_light_bdr": "#BFDBFE",
    
    "accent_green": "#047857",      # Verde Compliance & Sucesso
    "green_light_bg": "#ECFDF5",
    "green_light_bdr": "#A7F3D0",
    
    "accent_purple": "#6D28D9",     # Púrpura Curadoria & Métricas
    "purple_light_bg": "#F5F3FF",
    "purple_light_bdr": "#DDD6FE",
    
    "accent_amber": "#B45309",      # Âmbar Definição Canônica
    "amber_light_bg": "#FFFBEB",
    "amber_light_bdr": "#FDE68A",
    
    "accent_coral": "#991B1B",      # Coral / PII & Quarentena
    "coral_light_bg": "#FEF2F2",
    "coral_light_bdr": "#FECACA",
    
    "accent_cyan": "#0369A1",       # Ciano / Snowflake & Lakehouse
    "cyan_light_bg": "#F0F9FF",
    "cyan_light_bdr": "#BAE6FD"
}

# ==============================================================================
# FUNÇÕES DE DESENHO AUXILIARES
# ==============================================================================

def setup_canvas(width_in: float = 16.0, height_in: float = 9.0) -> Tuple[plt.Figure, plt.Axes]:
    """Inicializa a figura em proporção 16:9 widescreen com canvas 100% branco."""
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
        linewidth=0.8,
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
        (0.040, 0.940), 0.315, 0.028,
        boxstyle="round,pad=0.0,rounding_size=0.006",
        facecolor=COLORS["blue_light_bg"],
        edgecolor=COLORS["blue_light_bdr"],
        linewidth=0.8,
        zorder=2
    )
    ax.add_patch(tag_bg)
    ax.text(
        0.050, 0.954, "[ ATO 2 / SEÇÃO {3.1} ]  GOVERNANÇA, CATÁLOGO & LGPD",
        ha="left", va="center", fontsize=8.2, fontweight="bold",
        color=COLORS["brand_blue"], zorder=3
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
# 2. MINI-CARDS DE KPIS SUPERIORES (SEM COMPARAÇÃO COM AWS)
# ==============================================================================

def render_kpi_cards(ax: plt.Axes) -> None:
    """Renderiza 3 Mini-Cards de KPIs focados 100% em valor de governança e conformidade."""
    kpi_configs = [
        {
            "x": 0.040, "w": 0.285, "h": 0.110, "y": 0.735,
            "title": "CATÁLOGO CANÔNICO",
            "val": "7 Ativos Integrados",
            "sub": "100% Linhagem Mapeada • Regra \"A é um B que C\" + Asset IDs",
            "accent": COLORS["brand_blue"], "light_bg": COLORS["blue_light_bg"], "border": COLORS["blue_light_bdr"]
        },
        {
            "x": 0.340, "w": 0.285, "h": 0.110, "y": 0.735,
            "title": "BLINDAGEM LGPD BY DESIGN",
            "val": "100% Proteção PII",
            "sub": "Opt-in Mandatório por Canal • Quarentena Ativa (ANOM-03)",
            "accent": COLORS["accent_green"], "light_bg": COLORS["green_light_bg"], "border": COLORS["green_light_bdr"]
        },
        {
            "x": 0.640, "w": 0.320, "h": 0.110, "y": 0.735,
            "title": "GOVERNANÇA ÁGIL & RBAC",
            "val": "< 3 Dias Lead Time",
            "sub": "Self-Service Seguro • Fim dos Silos de Dados & Acesso por Papel",
            "accent": COLORS["accent_purple"], "light_bg": COLORS["purple_light_bg"], "border": COLORS["purple_light_bdr"]
        }
    ]
    
    for kpi in kpi_configs:
        draw_card(ax, kpi["x"], kpi["y"], kpi["w"], kpi["h"], bg_color=COLORS["bg_card"], bdr_color=kpi["border"], rounding=0.012)
        
        # Barra de Acento Superior do Card
        bar = patches.FancyBboxPatch(
            (kpi["x"], kpi["y"] + kpi["h"] - 0.014), kpi["w"], 0.014,
            boxstyle="round,pad=0.0,rounding_size=0.006",
            facecolor=kpi["accent"],
            edgecolor="none",
            zorder=3
        )
        ax.add_patch(bar)
        
        # Textos do KPI
        center_x = kpi["x"] + kpi["w"] / 2.0
        ax.text(
            center_x, kpi["y"] + 0.076, kpi["title"],
            ha="center", va="center", fontsize=7.8, fontweight="bold",
            color=COLORS["text_secondary"], zorder=4
        )
        ax.text(
            center_x, kpi["y"] + 0.047, kpi["val"],
            ha="center", va="center", fontsize=15.0, fontweight="bold",
            color=kpi["accent"], zorder=4
        )
        ax.text(
            center_x, kpi["y"] + 0.018, kpi["sub"],
            ha="center", va="center", fontsize=7.1, fontweight="normal",
            color=COLORS["text_muted"], zorder=4
        )

# ==============================================================================
# 3. PAINEL ESQUERDO: DICIONÁRIO VIVO & CATÁLOGO CANÔNICO
# ==============================================================================

def render_left_panel_dictionary(ax: plt.Axes) -> None:
    """Renderiza o Painel Esquerdo: Dicionário Vivo de Dados com Classificação LGPD e Metadados Canônicos."""
    x, y, w, h = 0.040, 0.115, 0.445, 0.605
    
    # Fundo do Card
    draw_card(ax, x, y, w, h, bg_color=COLORS["bg_card"], bdr_color=COLORS["border_card"], rounding=0.014, linewidth=1.2)
    
    # Cabeçalho da Tabela de Dicionário
    ax.text(
        x + 0.016, y + h - 0.030, "CATÁLOGO: ENTIDADE CLIENTES",
        ha="left", va="center", fontsize=10.5, fontweight="bold",
        color=COLORS["brand_blue"], zorder=3
    )
    
    # Badges do Cabeçalho
    draw_badge(ax, x + w - 0.180, y + h - 0.038, 0.082, 0.018, "QUALIFY / SILVER", COLORS["blue_light_bg"], COLORS["blue_light_bdr"], COLORS["brand_blue"], font_size=6.5)
    draw_badge(ax, x + w - 0.092, y + h - 0.038, 0.078, 0.018, "ID: 0327fecc", COLORS["bg_subtle"], COLORS["border_light"], COLORS["text_secondary"], font_size=6.5)
    
    ax.text(
        x + 0.016, y + h - 0.052, "Tabela Snowflake: CART_RECOVERY.CLIENTES  •  Asset ID: 0327fecc-f826-48fb-bb0a-1493fe18a32c",
        ha="left", va="center", fontsize=7.2, fontweight="bold",
        color=COLORS["text_muted"], zorder=3
    )
    
    # Caixa de Destaque: Regra Canônica "A é um B que C"
    def_box_y = y + h - 0.115
    def_box = patches.FancyBboxPatch(
        (x + 0.014, def_box_y), w - 0.028, 0.052,
        boxstyle="round,pad=0.0,rounding_size=0.008",
        facecolor=COLORS["amber_light_bg"],
        edgecolor=COLORS["amber_light_bdr"],
        linewidth=1.0,
        zorder=3
    )
    ax.add_patch(def_box)
    
    ax.text(
        x + 0.024, def_box_y + 0.038, "DEFINIÇÃO CANÔNICA DE NEGÓCIO (Regra \"A é um B que C\"):",
        ha="left", va="center", fontsize=7.4, fontweight="bold",
        color=COLORS["accent_amber"], zorder=4
    )
    ax.text(
        x + 0.024, def_box_y + 0.016,
        "\"Cliente é a pessoa física compradora que interage com o marketplace, cujos contatos cadastrais são\nestritamente regidos pela LGPD e exigem Opt-In ativo para disparos de réguas de resgate.\"",
        ha="left", va="center", fontsize=7.0, fontweight="normal", style="italic",
        color="#78350F", zorder=4
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
    
    # Linhas da Tabela
    rows_data = [
        {
            "name": "cliente_id", "type": "VARCHAR(36)",
            "badge_text": "[ Público / PK ]", "badge_bg": COLORS["green_light_bg"], "badge_bdr": COLORS["green_light_bdr"], "badge_col": COLORS["accent_green"],
            "rule": "Identificador único cadastral CRM"
        },
        {
            "name": "nome", "type": "VARCHAR(150)",
            "badge_text": "[ PII Mascarado ]", "badge_bg": COLORS["coral_light_bg"], "badge_bdr": COLORS["coral_light_bdr"], "badge_col": COLORS["accent_coral"],
            "rule": "Anonimização SHA-256 no RBAC"
        },
        {
            "name": "email", "type": "VARCHAR(255)",
            "badge_text": "[ PII / Opt-In ]", "badge_bg": COLORS["coral_light_bg"], "badge_bdr": COLORS["coral_light_bdr"], "badge_col": COLORS["accent_coral"],
            "rule": "Canal de resgate (Exige Opt-In)"
        },
        {
            "name": "telefone", "type": "VARCHAR(30)",
            "badge_text": "[ PII / Opt-In ]", "badge_bg": COLORS["coral_light_bg"], "badge_bdr": COLORS["coral_light_bdr"], "badge_col": COLORS["accent_coral"],
            "rule": "Disparos WhatsApp (Regra ANOM-03)"
        },
        {
            "name": "segmento", "type": "VARCHAR(50)",
            "badge_text": "[ RFM Cluster ]", "badge_bg": COLORS["blue_light_bg"], "badge_bdr": COLORS["blue_light_bdr"], "badge_col": COLORS["brand_blue"],
            "rule": "VIP, Frequente, Em Risco, Bronze"
        },
        {
            "name": "ltv_estimado", "type": "FLOAT",
            "badge_text": "[ Métrica Gold ]", "badge_bg": COLORS["purple_light_bg"], "badge_bdr": COLORS["purple_light_bdr"], "badge_col": COLORS["accent_purple"],
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
            
        ax.text(x + 0.016, ry, row["name"], ha="left", va="center", fontsize=7.6, fontweight="bold", fontfamily="monospace", color=COLORS["text_primary"], zorder=3)
        ax.text(x + 0.110, ry, row["type"], ha="left", va="center", fontsize=7.0, fontweight="normal", fontfamily="monospace", color=COLORS["text_muted"], zorder=3)
        
        # Badge de Classificação
        draw_badge(ax, x + 0.170, ry - 0.010, 0.100, 0.020, row["badge_text"], row["badge_bg"], row["badge_bdr"], row["badge_col"], font_size=6.6)
        
        ax.text(x + 0.290, ry, row["rule"], ha="left", va="center", fontsize=7.0, fontweight="normal", color=COLORS["text_secondary"], zorder=3)

    # Tags de Governança no Rodapé do Dicionário
    tags_y = y + 0.022
    ax.text(x + 0.016, tags_y, "Tags de Governança:", ha="left", va="center", fontsize=7.2, fontweight="bold", color=COLORS["text_muted"], zorder=3)
    
    draw_badge(ax, x + 0.115, tags_y - 0.009, 0.068, 0.018, "pii_sensivel", COLORS["coral_light_bg"], COLORS["coral_light_bdr"], COLORS["accent_coral"], font_size=6.2)
    draw_badge(ax, x + 0.188, tags_y - 0.009, 0.082, 0.018, "opt_in_mandatorio", COLORS["amber_light_bg"], COLORS["amber_light_bdr"], COLORS["accent_amber"], font_size=6.2)
    draw_badge(ax, x + 0.275, tags_y - 0.009, 0.075, 0.018, "rbac_governed", COLORS["purple_light_bg"], COLORS["purple_light_bdr"], COLORS["accent_purple"], font_size=6.2)
    draw_badge(ax, x + 0.355, tags_y - 0.009, 0.068, 0.018, "qualify_silver", COLORS["blue_light_bg"], COLORS["blue_light_bdr"], COLORS["brand_blue"], font_size=6.2)

# ==============================================================================
# 4. PAINEL DIREITO: CONTRATO EXECUTIVO DE METADADOS & MATRIZ RBAC (NO-TERMINAL)
# ==============================================================================

def render_right_panel_contract(ax: plt.Axes) -> None:
    """Renderiza o Painel Direito: Card Executivo de Contrato Dual-Metadata e Matriz RBAC / Governança."""
    x, y, w, h = 0.505, 0.115, 0.455, 0.605
    
    # Fundo do Card Principal Branco
    draw_card(ax, x, y, w, h, bg_color=COLORS["bg_card"], bdr_color=COLORS["border_card"], rounding=0.014, linewidth=1.2)
    
    # Cabeçalho do Card
    ax.text(
        x + 0.016, y + h - 0.030, "CONTRATO EXECUTIVO: METADADOS & RBAC",
        ha="left", va="center", fontsize=10.0, fontweight="bold",
        color=COLORS["brand_blue"], zorder=3
    )
    
    # Badge do Schema Version / Decisão
    draw_badge(ax, x + w - 0.125, y + h - 0.038, 0.110, 0.018, "DEC-006 DUAL-METADATA", COLORS["blue_light_bg"], COLORS["blue_light_bdr"], COLORS["brand_blue"], font_size=6.2)
    
    ax.text(
        x + 0.016, y + h - 0.052, "Especificação Canônica de Governança, Políticas de Acesso e Regras de Compliance",
        ha="left", va="center", fontsize=7.2, fontweight="bold",
        color=COLORS["text_muted"], zorder=3
    )
    
    # --------------------------------------------------------------------------
    # BLOCO 1: Identificação & Linhagem Ativa
    # --------------------------------------------------------------------------
    b1_y = y + h - 0.176
    b1_h = 0.110
    b1_box = patches.FancyBboxPatch(
        (x + 0.014, b1_y), w - 0.028, b1_h,
        boxstyle="round,pad=0.0,rounding_size=0.008",
        facecolor=COLORS["cyan_light_bg"],
        edgecolor=COLORS["cyan_light_bdr"],
        linewidth=1.0,
        zorder=3
    )
    ax.add_patch(b1_box)
    
    ax.text(
        x + 0.024, b1_y + b1_h - 0.016, "1. IDENTIFICAÇÃO DO ATIVO & LINHAGEM ATIVA DADOSFERA",
        ha="left", va="center", fontsize=7.4, fontweight="bold",
        color=COLORS["accent_cyan"], zorder=4
    )
    
    # Linha 1: Asset ID e Governança
    ax.text(x + 0.024, b1_y + 0.066, "Asset ID Oficial:", ha="left", va="center", fontsize=6.8, fontweight="bold", color=COLORS["text_secondary"], zorder=4)
    ax.text(x + 0.098, b1_y + 0.066, "0327fecc-f826-48fb-bb0a-1493fe18a32c", ha="left", va="center", fontsize=6.8, fontweight="normal", fontfamily="monospace", color=COLORS["text_primary"], zorder=4)
    
    ax.text(x + 0.315, b1_y + 0.066, "SLA / Tier:", ha="left", va="center", fontsize=6.8, fontweight="bold", color=COLORS["text_secondary"], zorder=4)
    ax.text(x + 0.365, b1_y + 0.066, "Tier 1 (< 15 min)", ha="left", va="center", fontsize=6.8, fontweight="normal", color=COLORS["text_primary"], zorder=4)
    
    # Linha 2: Entidade e Tabela Snowflake
    ax.text(x + 0.024, b1_y + 0.040, "Entidade Canônica:", ha="left", va="center", fontsize=6.8, fontweight="bold", color=COLORS["text_secondary"], zorder=4)
    ax.text(x + 0.110, b1_y + 0.040, "clientes_qualify (Silver)", ha="left", va="center", fontsize=6.8, fontweight="bold", color=COLORS["brand_blue"], zorder=4)
    
    ax.text(x + 0.235, b1_y + 0.040, "Tabela Snowflake:", ha="left", va="center", fontsize=6.8, fontweight="bold", color=COLORS["text_secondary"], zorder=4)
    ax.text(x + 0.320, b1_y + 0.040, "CART_RECOVERY.CLIENTES", ha="left", va="center", fontsize=6.8, fontweight="normal", fontfamily="monospace", color=COLORS["text_primary"], zorder=4)
    
    # Linha 3: Linhagem Mapeada
    ax.text(x + 0.024, b1_y + 0.016, "Linhagem Mapeada:", ha="left", va="center", fontsize=6.8, fontweight="bold", color=COLORS["text_secondary"], zorder=4)
    ax.text(x + 0.114, b1_y + 0.016, "Bronze S3 (Raw)  ➔  Silver Qualify (ANOM-03)  ➔  Gold Curated (Kimball)", ha="left", va="center", fontsize=6.7, fontweight="normal", color=COLORS["accent_green"], zorder=4)
        
    # --------------------------------------------------------------------------
    # BLOCO 2: Matriz de Controle de Acesso Baseada em Papéis (RBAC)
    # --------------------------------------------------------------------------
    b2_y = b1_y - 0.160
    b2_h = 0.146
    b2_box = patches.FancyBboxPatch(
        (x + 0.014, b2_y), w - 0.028, b2_h,
        boxstyle="round,pad=0.0,rounding_size=0.008",
        facecolor=COLORS["purple_light_bg"],
        edgecolor=COLORS["purple_light_bdr"],
        linewidth=1.0,
        zorder=3
    )
    ax.add_patch(b2_box)
    
    ax.text(
        x + 0.024, b2_y + b2_h - 0.016, "2. MATRIZ DE CONTROLE DE ACESSO POR PAPEL (RBAC CENTRALIZADO)",
        ha="left", va="center", fontsize=7.4, fontweight="bold",
        color=COLORS["accent_purple"], zorder=4
    )
    
    rbac_rows = [
        ("CRM_OPS", "[ READ_MASKED ]", COLORS["blue_light_bg"], COLORS["blue_light_bdr"], COLORS["brand_blue"], "Anonimização dinâmica SHA-256 de contatos"),
        ("MARKETING_ANALYTICS", "[ AGGREGATED_ONLY ]", COLORS["purple_light_bg"], COLORS["purple_light_bdr"], COLORS["accent_purple"], "Apenas métricas e clusters (Sem acesso a PII)"),
        ("DATA_ENGINEERING", "[ FULL_AUDITED ]", COLORS["green_light_bg"], COLORS["green_light_bdr"], COLORS["accent_green"], "Acesso técnico completo com auditoria ativa")
    ]
    
    r_start_y = b2_y + b2_h - 0.040
    r_spacing = 0.036
    for i, (role_name, perm_badge, p_bg, p_bdr, p_col, scope_desc) in enumerate(rbac_rows):
        ry = r_start_y - i * r_spacing
        
        ax.add_patch(patches.Circle((x + 0.028, ry), 0.003, facecolor=COLORS["accent_purple"], edgecolor="none", zorder=4))
        ax.text(x + 0.036, ry, role_name, ha="left", va="center", fontsize=7.0, fontweight="bold", fontfamily="monospace", color=COLORS["text_primary"], zorder=4)
        
        draw_badge(ax, x + 0.170, ry - 0.009, 0.095, 0.018, perm_badge, p_bg, p_bdr, p_col, font_size=6.2)
        ax.text(x + 0.272, ry, scope_desc, ha="left", va="center", fontsize=6.7, fontweight="normal", color=COLORS["text_secondary"], zorder=4)

    # --------------------------------------------------------------------------
    # BLOCO 3: Políticas de Blindagem LGPD & Quarentena
    # --------------------------------------------------------------------------
    b3_y = y + 0.018
    b3_h = 0.126
    b3_box = patches.FancyBboxPatch(
        (x + 0.014, b3_y), w - 0.028, b3_h,
        boxstyle="round,pad=0.0,rounding_size=0.008",
        facecolor=COLORS["green_light_bg"],
        edgecolor=COLORS["green_light_bdr"],
        linewidth=1.0,
        zorder=3
    )
    ax.add_patch(b3_box)
    
    ax.text(
        x + 0.024, b3_y + b3_h - 0.016, "3. POLÍTICAS DE BLINDAGEM LGPD & QUARENTENA AUTOMATIZADA",
        ha="left", va="center", fontsize=7.4, fontweight="bold",
        color=COLORS["accent_green"], zorder=4
    )
    
    lgpd_rules = [
        ("Opt-in Mandatório por Canal:", "Disparos bloqueados se opt-in = false (Regra ANOM-03)", COLORS["accent_green"]),
        ("Anonimização Dinâmica PII:", "Algoritmo SHA-256 com Salt para mascarar campos sensíveis", COLORS["accent_green"]),
        ("Ação em Não-Conformidade:", "ISOLATE_INTO_ANOMALIES_TABLE (Quarentena Ativa Silver)", COLORS["accent_coral"])
    ]
    
    g_start_y = b3_y + b3_h - 0.038
    g_spacing = 0.028
    for i, (rule_title, rule_text, dot_color) in enumerate(lgpd_rules):
        gy = g_start_y - i * g_spacing
        
        ax.add_patch(patches.Circle((x + 0.028, gy), 0.003, facecolor=dot_color, edgecolor="none", zorder=4))
        ax.text(x + 0.036, gy, rule_title, ha="left", va="center", fontsize=6.8, fontweight="bold", color=COLORS["text_primary"], zorder=4)
        ax.text(x + 0.170, gy, rule_text, ha="left", va="center", fontsize=6.7, fontweight="normal", color=COLORS["text_secondary"], zorder=4)

# ==============================================================================
# 5. BANNER INFERIOR: CICLO DE VIDA DA GOVERNANÇA ATIVA
# ==============================================================================

def render_footer_banner(ax: plt.Axes) -> None:
    """Renderiza a régua inferior com o fluxo de ponta a ponta e notas institucionais."""
    # Banner de Fluxo
    bx, by, bw, bh = 0.040, 0.038, 0.920, 0.052
    draw_card(ax, bx, by, bw, bh, bg_color=COLORS["bg_subtle"], bdr_color=COLORS["border_light"], rounding=0.008)
    
    # 5 Etapas do Fluxo de Governança
    steps = [
        ("1. Ingestão Bruta", "Bronze S3 (Raw)", COLORS["accent_amber"]),
        ("2. Tagging PII", "Auto Classify", COLORS["brand_blue"]),
        ("3. Validação Opt-In", "Regra ANOM-03", COLORS["accent_coral"]),
        ("4. Quarentena Silver", "Isolamento Ativo", COLORS["accent_purple"]),
        ("5. Data Views Seguras", "RBAC Centralizado", COLORS["accent_green"])
    ]
    
    step_w = bw / 5.0
    for i, (stitle, ssub, scolor) in enumerate(steps):
        sx = bx + i * step_w + 0.015
        sy = by + bh / 2.0
        
        # Indicador de Ponto Colorido
        ax.add_patch(patches.Circle((sx, sy + 0.005), 0.004, facecolor=scolor, edgecolor="none", zorder=3))
        
        # Textos da Etapa
        ax.text(sx + 0.010, sy + 0.005, stitle, ha="left", va="center", fontsize=7.4, fontweight="bold", color=COLORS["text_primary"], zorder=3)
        ax.text(sx + 0.010, sy - 0.012, ssub, ha="left", va="center", fontsize=6.5, fontweight="normal", color=COLORS["text_muted"], zorder=3)
        
        # Seta conectora entre etapas
        if i < 4:
            ax.text(sx + step_w - 0.010, sy, "➔", ha="center", va="center", fontsize=8.0, fontweight="bold", color=COLORS["text_subtle"], zorder=3)

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
    
    # 2. Mini-Cards de KPIs Superiores (Zero AWS Comparison)
    render_kpi_cards(ax)
    
    # 3. Painel Esquerdo: Dicionário Vivo de Dados & Regra Canônica
    render_left_panel_dictionary(ax)
    
    # 4. Painel Direito: Contrato Executivo de Metadados & Matriz RBAC (Sem visual de código IDE)
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
