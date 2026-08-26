#!/usr/bin/env python3
"""
generate_dictionary_chart.py
Módulo: view-lake-architecture (Ato 2 / Seção [3] - Arquitetura Lakehouse Medallion & Dicionário de Dados)
Função: Renderização declarativa da representação visual do Dicionário de Dados e Catálogo
         de Governança nas 4 zonas do Medallion (Bronze/Raw, Silver/Qualify, Silver/Anomaly, Gold/Curated).

Padrão Gráfico: charts-maker Standard (Fundo Branco #FFFFFF, 16:9 Widescreen, 300 DPI).
Paradigma: declarative-functional-coding (Tipagem estrita, imutabilidade, funções puras).
"""

from typing import Final, Dict, Any, List, Tuple, Sequence
from dataclasses import dataclass
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# ==============================================================================
# CONFIGURAÇÃO DE CONSTANTES E PALETA SEMÂNTICA
# ==============================================================================

VIEW_DIR: Final[Path] = Path(__file__).resolve().parent
BASE_DIR: Final[Path] = VIEW_DIR.parents[4]  # Raiz do repositório wheels
OUTPUT_IMAGE_PATH: Final[Path] = VIEW_DIR / "chart_dicionario_medallion.png"

# Paleta Semântica Executiva (Padrão White Background)
COLORS: Final[Dict[str, str]] = {
    "bg": "#FFFFFF",
    "card_bg": "#F8FAFC",
    "card_border": "#CBD5E1",
    "card_border_dark": "#94A3B8",
    "text_dark": "#0F172A",
    "text_body": "#1E293B",
    "text_muted": "#475569",
    "text_subtle": "#64748B",
    
    # Camadas Medallion
    "bronze": "#B45309",        # Bronze / Raw (Âmbar escuro)
    "bronze_bg": "#FFFBEB",
    "bronze_bdr": "#FDE68A",
    
    "silver": "#0284C7",        # Silver / Qualify (Azul Oceano)
    "silver_bg": "#F0F9FF",
    "silver_bdr": "#BAE6FD",
    
    "anomaly": "#EF4444",       # Silver / Quarentena Anomalias (Coral / Vermelho)
    "anomaly_bg": "#FEF2F2",
    "anomaly_bdr": "#FECACA",
    
    "gold": "#7C3AED",          # Gold / Curated DW Kimball (Roxo / Púrpura)
    "gold_bg": "#F5F3FF",
    "gold_bdr": "#DDD6FE",
    
    "accent_green": "#10B981",  # Sucesso / Opt-in Ativo
    "accent_green_bg": "#ECFDF5",
    "accent_green_bdr": "#A7F3D0",
    
    "accent_blue": "#2563EB",   # Snowflake / Dadosfera Core
    "accent_amber": "#D97706",  # Alerta de Governança
    "tag_pii": "#DC2626",       # Tag PII LGPD
    "tag_pii_bg": "#FEE2E2",
    "tag_pub": "#059669",       # Tag Pública
    "tag_pub_bg": "#D1FAE5",
    "grid": "#E2E8F0"
}

# ==============================================================================
# ESTRUTURAS DE DADOS IMUTÁVEIS DO CATÁLOGO DE GOVERNANÇA
# ==============================================================================

@dataclass(frozen=True)
class CatalogEntity:
    name: str
    display_name: str
    asset_id: str
    zone: str
    storage_table: str
    records: str
    classification: str
    definition: str
    key_type: str
    is_pii: bool
    dq_summary: str

# Mapeamento Canônico dos Ativos de Dados (Ground Truth dos output-mappers e dicionários)
RAW_ENTITIES: Final[Tuple[Dict[str, str], ...]] = (
    {"name": "clientes.parquet", "vol": "2.000 reg", "desc": "Ingestão bruta cadastral do CRM corporativo", "pii": "Sim (AES-256)", "fmt": "Parquet / S3"},
    {"name": "produtos.parquet", "vol": "500 reg", "desc": "Catálogo de SKUs, categorias e preços do PIM", "pii": "Não", "fmt": "Parquet / S3"},
    {"name": "carrinhos.parquet", "vol": "15.000 reg", "desc": "Sessões e intenções de compra de Web & App", "pii": "Não", "fmt": "Parquet / S3"},
    {"name": "itens_carrinho.parquet", "vol": "22.500 reg", "desc": "Detalhes e mercadorias adicionadas na cesta", "pii": "Não", "fmt": "Parquet / S3"},
    {"name": "eventos_carrinho.parquet", "vol": "72.026 reg", "desc": "Telemetria contínua de clickstream e checkout", "pii": "Não", "fmt": "Parquet / S3"},
    {"name": "eventos_resgate.parquet", "vol": "2.500 reg", "desc": "Disparos e telemetria de réguas de marketing", "pii": "Não", "fmt": "Parquet / S3"},
    {"name": "pedidos.parquet", "vol": "2.000 reg", "desc": "Ordens liquidadas e faturamento do ERP", "pii": "Não", "fmt": "Parquet / S3"},
)

QUALIFY_ENTITIES: Final[Tuple[CatalogEntity, ...]] = (
    CatalogEntity(
        name="CLIENTES",
        display_name="clientes_qualify",
        asset_id="0327fecc-f826-48fb-bb0a-1493fe18a32c",
        zone="Silver / Qualify",
        storage_table="CART_RECOVERY.CLIENTES",
        records="2.000 (94.2% conf)",
        classification="Confidencial (PII / LGPD)",
        definition="A entidade clientes consolida os dados cadastrais e scores RFM dos usuários.",
        key_type="PK: cliente_id (UUID)",
        is_pii=True,
        dq_summary="Regex de E-mail • Opt-in mandatório • Unicidade PK"
    ),
    CatalogEntity(
        name="PRODUTOS",
        display_name="produtos_qualify",
        asset_id="65fcfa25-a6f3-4cb8-a444-7fd23df3fa84",
        zone="Silver / Qualify",
        storage_table="CART_RECOVERY.PRODUTOS",
        records="500 (100% conf)",
        classification="Público / Catálogo",
        definition="A entidade produtos consolida os SKUs, faixas de preço e categorias de produto.",
        key_type="PK: produto_id (UUID)",
        is_pii=False,
        dq_summary="Preço >= 0 • Preço atual <= Preço original"
    ),
    CatalogEntity(
        name="CARRINHOS",
        display_name="carrinhos_qualify",
        asset_id="e2d3b1bb-bf22-456e-bc66-4ac843deec82",
        zone="Silver / Qualify",
        storage_table="CART_RECOVERY.CARRINHOS",
        records="15.000 (94.2% conf)",
        classification="Interno / Transacional",
        definition="A entidade carrinhos registra o ciclo de vida das sessões de compra.",
        key_type="PK: carrinho_id | FK: cliente_id",
        is_pii=False,
        dq_summary="Equação Financeira Fechada • Frete >= 0"
    ),
    CatalogEntity(
        name="ITENS_CARRINHO",
        display_name="itens_carrinho_qualify",
        asset_id="7649755a-c6e8-4b56-a092-be9eefde1dab",
        zone="Silver / Qualify",
        storage_table="CART_RECOVERY.ITENS_CARRINHO",
        records="22.500 (94.2% conf)",
        classification="Interno / Detalhe",
        definition="A entidade itens_carrinho detalha mercadorias e quantidades por sessão.",
        key_type="PK: item_id | FK: carrinho_id, produto_id",
        is_pii=False,
        dq_summary="Quantidade > 0 • Preço Unitário > 0"
    ),
    CatalogEntity(
        name="EVENTOS_CARRINHO",
        display_name="eventos_carrinho_qualify",
        asset_id="397c3ebc-15cb-42d2-a717-a3b5d150c3ea",
        zone="Silver / Qualify",
        storage_table="CART_RECOVERY.EVENTOS_CARRINHO",
        records="72.026 (94.2% conf)",
        classification="Interno / Telemetria",
        definition="A entidade eventos_carrinho monitora clickstream e interações de checkout.",
        key_type="PK: evento_id | FK: carrinho_id",
        is_pii=False,
        dq_summary="Sequência temporal de etapas sem sobreposição"
    ),
    CatalogEntity(
        name="EVENTOS_RESGATE",
        display_name="eventos_resgate_qualify",
        asset_id="04739f6d-e8c3-4d6f-80b7-0f98c12a5798",
        zone="Silver / Qualify",
        storage_table="CART_RECOVERY.EVENTOS_RESGATE",
        records="2.500 (94.2% conf)",
        classification="Interno / Marketing",
        definition="A entidade eventos_resgate mede a eficácia de réguas de acionamento.",
        key_type="PK: resgate_id | FK: carrinho_id",
        is_pii=False,
        dq_summary="Monotonicidade: Enviado >= Aberto >= Convertido"
    ),
    CatalogEntity(
        name="PEDIDOS",
        display_name="pedidos_qualify",
        asset_id="7f82a988-8e68-416a-b6fa-5007c4789d1a",
        zone="Silver / Qualify",
        storage_table="CART_RECOVERY.PEDIDOS",
        records="2.000 (94.2% conf)",
        classification="Interno / Faturamento",
        definition="A entidade pedidos registra transações finalizadas e liquidação de vendas.",
        key_type="PK: pedido_id | FK: carrinho_id, cliente_id",
        is_pii=False,
        dq_summary="Valor Total > 0 • Integridade de Atribuição"
    )
)

ANOMALY_RULES: Final[Tuple[Dict[str, str], ...]] = (
    {"code": "ANOM-01", "name": "Frete Negativo / Divergência", "table": "carrinhos_anomalies", "sev": "ALTA", "act": "Isola payload bruto p/ auditoria contábil"},
    {"code": "ANOM-02", "name": "Subtotal Zerado / Incoerente", "table": "carrinhos_anomalies", "sev": "ALTA", "act": "Segrega da Silver Qualify sem quebrar pipeline"},
    {"code": "ANOM-03", "name": "Opt-in Ausente / E-mail Inválido", "table": "clientes_anomalies", "sev": "CRÍTICA", "act": "Bloqueia disparo de régua (Blindagem LGPD)"},
    {"code": "ANOM-04", "name": "Preço Promocional Invertido", "table": "produtos_anomalies", "sev": "MÉDIA", "act": "Alerta catálogo: preço atual > preço original"},
    {"code": "ANOM-05", "name": "Quebra de Monotonicidade", "table": "eventos_resgate_anomalies", "sev": "MÉDIA", "act": "Isola cliques sem registro de abertura prévia"},
)

GOLD_MODELS: Final[Tuple[Dict[str, str], ...]] = (
    {"type": "DIMENSÃO", "name": "dim_cliente", "grain": "1 linha por cliente único", "sk": "cliente_sk (PK)", "purpose": "Segmentação RFM e LTV"},
    {"type": "DIMENSÃO", "name": "dim_produto", "grain": "1 linha por SKU de produto", "sk": "produto_sk (PK)", "purpose": "Atrito e categoria de preço"},
    {"type": "DIMENSÃO", "name": "dim_tempo", "grain": "1 linha por data/hora (calendário)", "sk": "tempo_sk (PK)", "purpose": "Sazonalidade e janelas (+1h)"},
    {"type": "DIMENSÃO", "name": "dim_dispositivo", "grain": "1 linha por plataforma (Mobile/Web)", "sk": "dispositivo_sk (PK)", "purpose": "Análise de usabilidade"},
    {"type": "DIMENSÃO", "name": "dim_canal_resgate", "grain": "1 linha por canal (WhatsApp/Email)", "sk": "canal_sk (PK)", "purpose": "Custo unitário e ROI"},
    {"type": "FATO CENTRAL", "name": "fato_abandono", "grain": "1 linha por evento de abandono", "sk": "abandono_id (PK) + 5 FKs", "purpose": "Métricas aditivas de perda"},
    {"type": "FATO DERIVADO", "name": "fato_resgate", "grain": "1 linha por disparo de campanha", "sk": "resgate_id (PK) + 4 FKs", "purpose": "Conversão e ROI de 45x"},
    {"type": "VIEW ANALÍTICA", "name": "v_abandonment_summary", "grain": "Agregação por categoria e canal", "sk": "Visão Curada Metabase", "purpose": "Dashboard Executivo Direto"},
    {"type": "VIEW ANALÍTICA", "name": "v_recovery_roi_by_channel", "grain": "Agregação financeira de canais", "sk": "Visão Curada Streamlit", "purpose": "Simulador Prescritivo ROI"},
)

# ==============================================================================
# FUNÇÕES DE DESENHO VETORIAL DECLARATIVAS
# ==============================================================================

def draw_top_kpi_card(
    ax: plt.Axes,
    x: float,
    y: float,
    w: float,
    h: float,
    zone_name: str,
    metric_val: str,
    sub_text: str,
    accent_color: str,
    bg_color: str,
    bdr_color: str
) -> None:
    """Desenha um KPI Card superior temático com o padrão visual corporativo."""
    card = patches.FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.0,rounding_size=0.025",
        facecolor=bg_color,
        edgecolor=bdr_color,
        linewidth=1.4,
        zorder=2
    )
    ax.add_patch(card)
    
    # Tag superior colorida
    tag_h = 0.028
    tag = patches.FancyBboxPatch(
        (x, y + h - tag_h), w, tag_h,
        boxstyle="round,pad=0.0,rounding_size=0.015",
        facecolor=accent_color,
        edgecolor="none",
        zorder=3
    )
    ax.add_patch(tag)
    
    ax.text(
        x + w / 2.0, y + h - tag_h / 2.0, zone_name.upper(),
        ha="center", va="center", fontsize=8.2, fontweight="bold",
        color="#FFFFFF", zorder=4
    )
    ax.text(
        x + w / 2.0, y + h / 2.0 + 0.006, metric_val,
        ha="center", va="center", fontsize=14.5, fontweight="bold",
        color=accent_color, zorder=4
    )
    ax.text(
        x + w / 2.0, y + 0.022, sub_text,
        ha="center", va="bottom", fontsize=7.6,
        color=COLORS["text_dark"], zorder=4
    )

def draw_column_container(
    ax: plt.Axes,
    x: float,
    y: float,
    w: float,
    h: float,
    col_tag: str,
    col_title: str,
    col_subtitle: str,
    accent_color: str,
    bg_color: str,
    border_color: str
) -> None:
    """Desenha a caixa container de cada coluna temático do Medallion."""
    box = patches.FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.0,rounding_size=0.025",
        facecolor=bg_color,
        edgecolor=border_color,
        linewidth=1.3,
        zorder=2
    )
    ax.add_patch(box)
    
    # Cabeçalho da coluna
    header_h = 0.080
    header_box = patches.FancyBboxPatch(
        (x, y + h - header_h), w, header_h,
        boxstyle="round,pad=0.0,rounding_size=0.018",
        facecolor=accent_color,
        edgecolor="none",
        zorder=3
    )
    ax.add_patch(header_box)
    
    ax.text(
        x + 0.010, y + h - header_h / 2.0 + 0.014, col_tag.upper(),
        ha="left", va="center", fontsize=8.0, fontweight="bold",
        color="#FFFFFF", zorder=4
    )
    ax.text(
        x + 0.010, y + h - header_h / 2.0 - 0.005, col_title,
        ha="left", va="center", fontsize=9.6, fontweight="bold",
        color="#FFFFFF", zorder=4
    )
    ax.text(
        x + 0.010, y + h - header_h / 2.0 - 0.024, col_subtitle,
        ha="left", va="center", fontsize=7.2,
        color="#F8FAFC", zorder=4
    )

def render_raw_column(ax: plt.Axes, x: float, y: float, w: float, h: float) -> None:
    """Renderiza a coluna de entidades brutas da Zona Bronze."""
    draw_column_container(
        ax, x, y, w, h,
        col_tag="Zona 1: Bronze (Raw)",
        col_title="INGESTÃO BRUTA AS-IS",
        col_subtitle="7 Datasets • 115.777+ Registros S3 • Imutável",
        accent_color=COLORS["bronze"],
        bg_color=COLORS["bronze_bg"],
        border_color=COLORS["bronze_bdr"]
    )
    
    # Lista de arquivos brutos
    curr_y = y + h - 0.100
    card_h = 0.068
    gap = 0.012
    
    for item in RAW_ENTITIES:
        # Card individual da entidade bruta
        item_box = patches.FancyBboxPatch(
            (x + 0.008, curr_y - card_h), w - 0.016, card_h,
            boxstyle="round,pad=0.0,rounding_size=0.012",
            facecolor="#FFFFFF",
            edgecolor=COLORS["bronze_bdr"],
            linewidth=1.0,
            zorder=3
        )
        ax.add_patch(item_box)
        
        # Nome do arquivo e volume
        ax.text(
            x + 0.015, curr_y - 0.018, item["name"],
            ha="left", va="center", fontsize=7.8, fontweight="bold",
            color=COLORS["text_dark"], zorder=4
        )
        ax.text(
            x + w - 0.015, curr_y - 0.018, item["vol"],
            ha="right", va="center", fontsize=7.4, fontweight="bold",
            color=COLORS["bronze"], zorder=4
        )
        
        # Descrição de negócio resumida
        ax.text(
            x + 0.015, curr_y - 0.038, item["desc"],
            ha="left", va="center", fontsize=6.8,
            color=COLORS["text_muted"], zorder=4
        )
        
        # Tag de formato e PII
        pii_color = COLORS["tag_pii"] if "Sim" in item["pii"] else COLORS["text_subtle"]
        ax.text(
            x + 0.015, curr_y - 0.054, f"[{item['fmt']}] • PII: {item['pii']}",
            ha="left", va="center", fontsize=6.4, fontweight="bold",
            color=pii_color, zorder=4
        )
        
        curr_y -= (card_h + gap)

def render_qualify_column(ax: plt.Axes, x: float, y: float, w: float, h: float) -> None:
    """Renderiza a coluna de Dicionário Canônico e Catálogo da Zona Silver Qualify."""
    draw_column_container(
        ax, x, y, w, h,
        col_tag="Zona 2A: Silver (Qualify)",
        col_title="CATÁLOGO & DICIONÁRIO DE DADOS",
        col_subtitle="94.2% Conformidade • Snowflake • 18 Regras DQ",
        accent_color=COLORS["silver"],
        bg_color=COLORS["silver_bg"],
        border_color=COLORS["silver_bdr"]
    )
    
    curr_y = y + h - 0.100
    card_h = 0.068
    gap = 0.012
    
    for entity in QUALIFY_ENTITIES:
        # Card individual da entidade qualificada
        item_box = patches.FancyBboxPatch(
            (x + 0.008, curr_y - card_h), w - 0.016, card_h,
            boxstyle="round,pad=0.0,rounding_size=0.012",
            facecolor="#FFFFFF",
            edgecolor=COLORS["silver_bdr"],
            linewidth=1.0,
            zorder=3
        )
        ax.add_patch(item_box)
        
        # Tabela Snowflake e Badge PII/Status
        ax.text(
            x + 0.015, curr_y - 0.018, entity.name,
            ha="left", va="center", fontsize=8.0, fontweight="bold",
            color=COLORS["accent_blue"], zorder=4
        )
        
        # Badge de PII / Classificação
        badge_text = "🔒 PII / LGPD" if entity.is_pii else "PÚBLICO" if "Público" in entity.classification else "INTERNO"
        badge_color = COLORS["tag_pii"] if entity.is_pii else COLORS["tag_pub"] if "Público" in entity.classification else COLORS["text_muted"]
        badge_bg = COLORS["tag_pii_bg"] if entity.is_pii else COLORS["tag_pub_bg"] if "Público" in entity.classification else "#F1F5F9"
        
        badge_w = 0.062
        badge_h = 0.018
        badge_patch = patches.FancyBboxPatch(
            (x + w - badge_w - 0.015, curr_y - 0.026), badge_w, badge_h,
            boxstyle="round,pad=0.0,rounding_size=0.006",
            facecolor=badge_bg,
            edgecolor=badge_color,
            linewidth=0.8,
            zorder=4
        )
        ax.add_patch(badge_patch)
        ax.text(
            x + w - badge_w / 2.0 - 0.015, curr_y - 0.017, badge_text,
            ha="center", va="center", fontsize=6.2, fontweight="bold",
            color=badge_color, zorder=5
        )
        
        # Definição formal "A é um B que C"
        ax.text(
            x + 0.015, curr_y - 0.038, entity.definition,
            ha="left", va="center", fontsize=6.6,
            color=COLORS["text_dark"], zorder=4
        )
        
        # Chaves e Regra DQ
        ax.text(
            x + 0.015, curr_y - 0.054, f"{entity.key_type} | Asset: {entity.asset_id[:8]}...",
            ha="left", va="center", fontsize=6.2, fontweight="bold",
            color=COLORS["text_subtle"], zorder=4
        )
        
        curr_y -= (card_h + gap)

def render_anomaly_column(ax: plt.Axes, x: float, y: float, w: float, h: float) -> None:
    """Renderiza a coluna de Quarentena e Diagnóstico da Zona Silver Anomaly."""
    draw_column_container(
        ax, x, y, w, h,
        col_tag="Zona 2B: Silver (Quarentena)",
        col_title="QUARENTENA ATIVA & DIAGNÓSTICO",
        col_subtitle="5.8% Desvios • DEC-006 • Payload Bruto Retido",
        accent_color=COLORS["anomaly"],
        bg_color=COLORS["anomaly_bg"],
        border_color=COLORS["anomaly_bdr"]
    )
    
    # Bloco explicativo da Quarentena
    info_h = 0.075
    info_box = patches.FancyBboxPatch(
        (x + 0.008, y + h - 0.100 - info_h), w - 0.016, info_h,
        boxstyle="round,pad=0.0,rounding_size=0.012",
        facecolor="#FFFFFF",
        edgecolor=COLORS["anomaly_bdr"],
        linewidth=1.0,
        zorder=3
    )
    ax.add_patch(info_box)
    
    ax.text(
        x + 0.015, y + h - 0.118, "MECANISMO DUAL-ARTIFACT (DEC-006)",
        ha="left", va="center", fontsize=7.6, fontweight="bold",
        color=COLORS["anomaly"], zorder=4
    )
    ax.text(
        x + 0.015, y + h - 0.138, "Isola registros com falhas de integridade sem parar\no pipeline, registrando código de erro e severidade.",
        ha="left", va="center", fontsize=6.7,
        color=COLORS["text_muted"], zorder=4
    )
    ax.text(
        x + 0.015, y + h - 0.160, "Schema de Destino: CART_RECOVERY_ANOMALIES.*",
        ha="left", va="center", fontsize=6.4, fontweight="bold",
        color=COLORS["text_dark"], zorder=4
    )
    
    # Lista de Regras de Quarentena
    curr_y = y + h - 0.100 - info_h - 0.014
    card_h = 0.082
    gap = 0.012
    
    for rule in ANOMALY_RULES:
        rule_box = patches.FancyBboxPatch(
            (x + 0.008, curr_y - card_h), w - 0.016, card_h,
            boxstyle="round,pad=0.0,rounding_size=0.012",
            facecolor="#FFFFFF",
            edgecolor=COLORS["anomaly_bdr"],
            linewidth=1.0,
            zorder=3
        )
        ax.add_patch(rule_box)
        
        # Código e Severidade
        ax.text(
            x + 0.015, curr_y - 0.018, f"[{rule['code']}] {rule['name']}",
            ha="left", va="center", fontsize=7.6, fontweight="bold",
            color=COLORS["text_dark"], zorder=4
        )
        
        sev_col = COLORS["anomaly"] if rule["sev"] == "CRÍTICA" else COLORS["accent_amber"] if rule["sev"] == "ALTA" else COLORS["silver"]
        ax.text(
            x + w - 0.015, curr_y - 0.018, rule["sev"],
            ha="right", va="center", fontsize=7.2, fontweight="bold",
            color=sev_col, zorder=4
        )
        
        ax.text(
            x + 0.015, curr_y - 0.040, f"Tabela: {rule['table']}",
            ha="left", va="center", fontsize=6.8, fontweight="bold",
            color=COLORS["accent_blue"], zorder=4
        )
        ax.text(
            x + 0.015, curr_y - 0.060, f"Ação: {rule['act']}",
            ha="left", va="center", fontsize=6.5,
            color=COLORS["text_muted"], zorder=4
        )
        
        curr_y -= (card_h + gap)

def render_gold_column(ax: plt.Axes, x: float, y: float, w: float, h: float) -> None:
    """Renderiza a coluna de Modelagem Kimball e Data Views da Zona Gold Curated."""
    draw_column_container(
        ax, x, y, w, h,
        col_tag="Zona 3: Gold (Curated)",
        col_title="KIMBALL STAR SCHEMA & VIEWS",
        col_subtitle="6 Dimensões • 2 Fatos • 1-Hop JOINs • DEC-008",
        accent_color=COLORS["gold"],
        bg_color=COLORS["gold_bg"],
        border_color=COLORS["gold_bdr"]
    )
    
    curr_y = y + h - 0.100
    card_h = 0.053
    gap = 0.008
    
    for model in GOLD_MODELS:
        model_box = patches.FancyBboxPatch(
            (x + 0.008, curr_y - card_h), w - 0.016, card_h,
            boxstyle="round,pad=0.0,rounding_size=0.010",
            facecolor="#FFFFFF",
            edgecolor=COLORS["gold_bdr"],
            linewidth=1.0,
            zorder=3
        )
        ax.add_patch(model_box)
        
        # Tipo e Nome
        type_col = COLORS["gold"] if "DIMENSÃO" in model["type"] else COLORS["accent_blue"] if "FATO" in model["type"] else COLORS["accent_green"]
        ax.text(
            x + 0.015, curr_y - 0.016, f"[{model['type']}] {model['name']}",
            ha="left", va="center", fontsize=7.6, fontweight="bold",
            color=type_col, zorder=4
        )
        
        # Granularidade e Chave
        ax.text(
            x + 0.015, curr_y - 0.034, f"{model['sk']} • {model['grain']}",
            ha="left", va="center", fontsize=6.6,
            color=COLORS["text_dark"], zorder=4
        )
        
        curr_y -= (card_h + gap)

# ==============================================================================
# FUNÇÃO PRINCIPAL DE RENDERIZAÇÃO
# ==============================================================================

def plot_dictionary_medallion() -> plt.Figure:
    """Gera o painel executivo de Dicionário de Dados e Governança Medallion (16:9, 300 DPI)."""
    plt.rcParams["font.sans-serif"] = ["Segoe UI", "DejaVu Sans", "Helvetica", "Arial", "sans-serif"]
    
    fig = plt.figure(figsize=(16.0, 9.0), facecolor=COLORS["bg"], dpi=300)
    
    # --------------------------------------------------------------------------
    # 1. CABEÇALHO DO PAINEL EXECUTIVO
    # --------------------------------------------------------------------------
    ax_header = fig.add_axes([0.04, 0.89, 0.92, 0.09])
    ax_header.set_xlim(0, 1)
    ax_header.set_ylim(0, 1)
    ax_header.axis("off")
    
    ax_header.text(
        0.00, 0.82, "CATÁLOGO & DICIONÁRIO DE DADOS MEDALLION — GOVERNANÇA E METADADOS DADOSFERA",
        ha="left", va="center", fontsize=13.5, fontweight="bold",
        color=COLORS["text_dark"]
    )
    ax_header.text(
        0.00, 0.28, "Mapeamento Canônico por Zona: Bronze (Raw) ➔ Silver (Qualify / Quarentena) ➔ Gold (Curated DW) • IDs Oficiais Maestro API • Blindagem LGPD / PII",
        ha="left", va="center", fontsize=8.8,
        color=COLORS["text_muted"]
    )
    
    # --------------------------------------------------------------------------
    # 2. TOP EXECUTIVE KPI CARDS (4 Zonas Medallion)
    # --------------------------------------------------------------------------
    ax_kpi = fig.add_axes([0.04, 0.75, 0.92, 0.12])
    ax_kpi.set_xlim(0, 1)
    ax_kpi.set_ylim(0, 1)
    ax_kpi.axis("off")
    
    kpis_config = [
        ("Zona Bronze (Raw)", "7 Datasets Brutos", "115.777+ Registros • S3 Landing Imutável", COLORS["bronze"], COLORS["bronze_bg"], COLORS["bronze_bdr"]),
        ("Zona Silver (Qualify)", "94.2% Conforme", "7 Tabelas Relacionais • 18 Regras DQ", COLORS["silver"], COLORS["silver_bg"], COLORS["silver_bdr"]),
        ("Quarentena (Anomaly)", "5.8% Isolado", "7 Tabelas Anomalias • Diagnóstico ANOM-01..03", COLORS["anomaly"], COLORS["anomaly_bg"], COLORS["anomaly_bdr"]),
        ("Zona Gold (Curated)", "Star Schema Kimball", "6 Dimensões + 2 Fatos • 1-Hop Snowflake DW", COLORS["gold"], COLORS["gold_bg"], COLORS["gold_bdr"])
    ]
    
    card_w = 0.235
    gap_kpi = (1.0 - (4 * card_w)) / 3.0
    for i, (z_name, m_val, s_txt, col, bg, bdr) in enumerate(kpis_config):
        cx = i * (card_w + gap_kpi)
        draw_top_kpi_card(ax_kpi, cx, 0.05, card_w, 0.90, z_name, m_val, s_txt, col, bg, bdr)
        
    # --------------------------------------------------------------------------
    # 3. PAINEL DE 4 COLUNAS TEMÁTICAS MEDALLION
    # --------------------------------------------------------------------------
    ax_cols = fig.add_axes([0.04, 0.08, 0.92, 0.65])
    ax_cols.set_xlim(0, 1)
    ax_cols.set_ylim(0, 1)
    ax_cols.axis("off")
    
    col_w = 0.235
    gap_col = (1.0 - (4 * col_w)) / 3.0
    
    # [Coluna 1: Bronze Raw]
    render_raw_column(ax_cols, x=0.00 * (col_w + gap_col), y=0.00, w=col_w, h=1.00)
    
    # [Coluna 2: Silver Qualify]
    render_qualify_column(ax_cols, x=1.00 * (col_w + gap_col), y=0.00, w=col_w, h=1.00)
    
    # [Coluna 3: Silver Anomaly]
    render_anomaly_column(ax_cols, x=2.00 * (col_w + gap_col), y=0.00, w=col_w, h=1.00)
    
    # [Coluna 4: Gold Curated]
    render_gold_column(ax_cols, x=3.00 * (col_w + gap_col), y=0.00, w=col_w, h=1.00)
    
    # --------------------------------------------------------------------------
    # 4. RODAPÉ EXECUTIVO DE GOVERNANÇA E NORMAS
    # --------------------------------------------------------------------------
    fonte_texto = "Padrão Dual-Metadata (metadata.md + metadata.json) • Catálogo Maestro API (https://maestro.dadosfera.ai) • Frameworks DEC-006 & DEC-008 • Blindagem LGPD Opt-In (ANOM-03)"
    fig.text(0.04, 0.035, fonte_texto, fontsize=8.2, color=COLORS["text_subtle"], style="italic")
    
    return fig

# ==============================================================================
# EXECUÇÃO PRINCIPAL DECLARATIVA
# ==============================================================================

def main() -> None:
    """Função principal declarativa que renderiza e salva a visualização do catálogo."""
    print(f"[RUNNING] Gerando representação visual do Dicionário de Dados Medallion em: {OUTPUT_IMAGE_PATH}...")
    fig = plot_dictionary_medallion()
    fig.savefig(str(OUTPUT_IMAGE_PATH), dpi=300, bbox_inches="tight", facecolor=COLORS["bg"])
    plt.close(fig)
    print(f"[SUCCESS] Dicionário de Dados Medallion gerado com sucesso em: {OUTPUT_IMAGE_PATH}")

if __name__ == "__main__":
    main()
