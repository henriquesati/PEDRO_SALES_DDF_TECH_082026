"""Serviço de catálogo e leitura de especificações e gráficos do diretório insights/ (Padrão Funcional & Imutável)."""

import os
from typing import Final, Mapping
from types import MappingProxyType
from dataclasses import dataclass

@dataclass(frozen=True)
class InsightItem:
    """Modelo imutável de um item analítico de insight com spec e imagem de gráfico."""
    insight_id: str
    title: str
    category: str
    category_label: str
    category_badge_color: str
    directory_path: str
    spec_file_path: str
    chart_image_path: str
    key_kpis: tuple[tuple[str, str], ...]
    description: str
    architecture_notes: str


# =============================================================================
# 📊 CATÁLOGO COMPLETO DE INSIGHTS BASEADO NA ESTRUTURA DO DIRETÓRIO insights/
# =============================================================================

_INSIGHTS_DATA: Final[tuple[InsightItem, ...]] = (
    # -------------------------------------------------------------------------
    # 01. DESCRITIVO (01_descriptive)
    # -------------------------------------------------------------------------
    InsightItem(
        insight_id="desc_01_funil",
        title="Funil Semestral de Recuperação de Carrinhos",
        category="01_descriptive",
        category_label="01. Descritivo",
        category_badge_color="#2563EB",
        directory_path="insights/01_descriptive/01_bi_recuperacao_carrinhos/",
        spec_file_path="insights/01_descriptive/01_bi_recuperacao_carrinhos/spec.md",
        chart_image_path="insights/01_descriptive/01_bi_recuperacao_carrinhos/chart_bi_recuperacao_carrinhos.png",
        key_kpis=(
            ("Volume Semestral", "7.500 Carrinhos"),
            ("Taxa de Abandono", "69.7%"),
            ("Resgate Dadosfera", "+10.1% (+R$ 167,9k)"),
            ("CAC E-mail Unitário", "R$ 1,02"),
        ),
        description="Série temporal com 70% de abandono basal e 10.1% de taxa de recuperação através de réguas omnicanal Dadosfera (+50% de lift vs benchmark de mercado).",
        architecture_notes="Camada Silver Qualify • Visualização pareada com mini cards executivos de zonas de conversão."
    ),
    InsightItem(
        insight_id="desc_02_motivos",
        title="Decomposição de Motivos de Abandono & Faixa de Ticket",
        category="01_descriptive",
        category_label="01. Descritivo",
        category_badge_color="#2563EB",
        directory_path="insights/01_descriptive/02_motivos_abandono/",
        spec_file_path="insights/01_descriptive/motivos_abandono.md",
        chart_image_path="presentation/pitch/roteiro/views-04-insights/descritivos/motivosabandono/chart_02_motivos_abandono.png",
        key_kpis=(
            ("Frete Excessivo", "38.4%"),
            ("Preço Elevado", "21.2%"),
            ("Hesitação / Comparação", "18.5%"),
            ("Checkout Complexo", "12.8%"),
        ),
        description="Decomposição das 6 causas-raiz de abandono de carrinho e correlação direta com a concentração financeira de perda por faixa de ticket médio.",
        architecture_notes="Kimball dim_motivo_abandono • Relacionamento 1-Hop com fato_abandono."
    ),
    InsightItem(
        insight_id="desc_03_roi",
        title="Custo Unitário de Recuperação & ROI por Canal",
        category="01_descriptive",
        category_label="01. Descritivo",
        category_badge_color="#2563EB",
        directory_path="insights/01_descriptive/03_custo_recuperacao_roi/",
        spec_file_path="insights/01_descriptive/custo_recuperacao_roi.md",
        chart_image_path="presentation/pitch/roteiro/views-04-insights/descritivos/custorecuperacao/chart_03_custo_recuperacao_roi.png",
        key_kpis=(
            ("ROI Multiplicador", "45.2x"),
            ("E-mail CAC", "R$ 1,02 (85% vol)"),
            ("WhatsApp VIP CAC", "R$ 12,00 (12% vol)"),
            ("SMS Alerta CAC", "R$ 0,15 (2% vol)"),
        ),
        description="Eficiência financeira e custo unitário de acionamento por canal, garantindo o menor custo por real recuperado e ROI de 45x.",
        architecture_notes="Kimball dim_canal_resgate • Otimização orçamentária de alocação de disparos."
    ),

    # -------------------------------------------------------------------------
    # 02. RISCO (02_risk)
    # -------------------------------------------------------------------------
    InsightItem(
        insight_id="risk_01_segmentacao",
        title="Segmentação de Risco RFM & Matriz de Intervenção",
        category="02_risk",
        category_label="02. Risco",
        category_badge_color="#D97706",
        directory_path="insights/02_risk/01_segmentacao_risco/",
        spec_file_path="insights/02_risk/01_segmentacao_risco/spec.md",
        chart_image_path="insights/02_risk/01_segmentacao_risco/chart_03_segmentacao_risco.png",
        key_kpis=(
            ("Clientes Champions", "15.2% (Resgate VIP)"),
            ("Clientes At-Risk", "28.4% (Intervenção Imediata)"),
            ("Clientes Hibernating", "22.1% (Nutrição Gradual)"),
            ("Sensibilidade a Preço", "0.74 Correlação"),
        ),
        description="Matriz consolidada de risco de churn e abandono cruzando tempo de inatividade, histórico de compras e valor da cesta represada.",
        architecture_notes="Kimball dim_segmento_rfm • Segmentação comportamental sem fabricação de clusters."
    ),
    InsightItem(
        insight_id="risk_02_viabilidade",
        title="Matriz de Viabilidade Econômica de Resgate & ROI",
        category="02_risk",
        category_label="02. Risco",
        category_badge_color="#D97706",
        directory_path="insights/02_risk/03_viabilidade_recuperacao_carrinho/",
        spec_file_path="insights/02_risk/viabilidade_recuperacao_carrinho.md",
        chart_image_path="insights/02_risk/01_segmentacao_risco/chart_03_dashboard_03b_matriz_risk_roi.png",
        key_kpis=(
            ("Filtro Margem Líquida", ">= 28.5%"),
            ("Carrinhos Inviáveis", "14.2% (Eliminados)"),
            ("Economia de Budget", "R$ 42.800"),
            ("Margem Preservada", "100% Auditável"),
        ),
        description="Eliminação programática de resgates com margem negativa (carrinhos com ticket muito baixo ou frete inviável), preservando 28.5% de margem bruta.",
        architecture_notes="DEC-001 • Regra de corte financeiro automático por margem de contribuição."
    ),

    # -------------------------------------------------------------------------
    # 03. PRESCRITIVO (03_prescriptive)
    # -------------------------------------------------------------------------
    InsightItem(
        insight_id="presc_01_timing",
        title="Otimização da Janela Temporal de Disparo (+1h)",
        category="03_prescriptive",
        category_label="03. Prescritivo",
        category_badge_color="#059669",
        directory_path="insights/03_prescriptive/02_otimizacao_timing_envio/",
        spec_file_path="insights/03_prescriptive/otimizacao_timing_envio.md",
        chart_image_path="presentation/pitch/roteiro/views-04-insights/prescritivos/timingenvio/chart_05_otimizacao_timing_envio.png",
        key_kpis=(
            ("Janela de Ouro (+1h)", "86.4% das Conversões"),
            ("Janela Secundária (até 6h)", "11.2% das Conversões"),
            ("Queda após 24h", "-68% de Eficácia"),
            ("Spline k=3", "Curva Fiel sem Fabricação"),
        ),
        description="Curva de decaimento temporal comprovando que disparos no primeiro intervalo de 60 minutos capturam 86.4% do total de carrinhos recuperados.",
        architecture_notes="Série temporal com regressão Spline k=3 estritamente ancorada nos timestamps reais."
    ),
    InsightItem(
        insight_id="presc_02_rfm_preservacao",
        title="Estratégia RFM & Preservação de Margem sem Cupom",
        category="03_prescriptive",
        category_label="03. Prescritivo",
        category_badge_color="#059669",
        directory_path="insights/03_prescriptive/01_estrategia_resgate_segmento/",
        spec_file_path="insights/03_prescriptive/estrategia_resgate_segmento.md",
        chart_image_path="presentation/pitch/roteiro/views-04-insights/prescritivos/estrategiaresgate/chart_insights_prescritivos.png",
        key_kpis=(
            ("Cupom Desconto Tradicional", "20% (Queima R$ 779,80)"),
            ("WhatsApp VIP Dadosfera", "0% Cupom (18% Conversão)"),
            ("Margem Bruta Preservada", "28.5%"),
            ("Retorno Incremental", "+R$ 167.900"),
        ),
        description="Painel executivo de tomada de ação integrando a substituição da queima de descontos por abordagem consultiva assistida por IA.",
        architecture_notes="Políticas prescritivas por score RFM e regras de negócio formalizadas em DEC-001."
    ),
    InsightItem(
        insight_id="presc_03_produtos_criticos",
        title="Produtos Críticos de Abandono & Ações de Catálogo",
        category="03_prescriptive",
        category_label="03. Prescritivo",
        category_badge_color="#059669",
        directory_path="insights/03_prescriptive/03_produtos_mais_abandonados/",
        spec_file_path="insights/03_prescriptive/produtos_mais_abandonados.md",
        chart_image_path="presentation/pitch/roteiro/views-04-insights/prescritivos/produtosabandonados/chart_03_produtos_mais_abandonados.png",
        key_kpis=(
            ("Eletrônicos Críticos", "34% do Abandono Total"),
            ("Top 5 SKUs Críticos", "R$ 89.200 em Perda"),
            ("Intervenção de UX", "Revisão de Voltagem e Frete"),
            ("Substituição de SKU", "Lift +12.4% Conversão"),
        ),
        description="Matriz multidimensional de posicionamento de produtos e identificação de SKUs que demandam melhoria de especificações técnicas ou troca por similares.",
        architecture_notes="Cruzamento direto de TB_ITENS_CARRINHO com TB_PRODUTOS via Lakehouse."
    ),

    # -------------------------------------------------------------------------
    # 04. INTELIGÊNCIA & IA (04_intelligence_ai)
    # -------------------------------------------------------------------------
    InsightItem(
        insight_id="ia_01_master",
        title="Tríade de Inteligência & IA Master Dadosfera",
        category="04_intelligence_ai",
        category_label="04. Inteligência & IA",
        category_badge_color="#7C3AED",
        directory_path="insights/04_intelligence_ai/",
        spec_file_path="insights/04_intelligence_ai/spec.md",
        chart_image_path="presentation/pitch/roteiro/views-05-insights-ia/chart_insights_ia_master.png",
        key_kpis=(
            ("Machine Learning", "XGBoost Propensão (AUC 0.948)"),
            ("GenAI com LLMs", "Copies Pydantic (100% Schema)"),
            ("Busca Semântica", "Cosine Sim >= 0.85 (t-SNE 2D)"),
            ("Data Apps", "Streamlit Modular em 5 Camadas"),
        ),
        description="Painel de evolução da maturidade analítica: da engenharia de dados à inteligência preditiva e generativa unificada na plataforma Dadosfera.",
        architecture_notes="Integração Stepsfera ML + Snowflake + Streamlit SaaS."
    ),
    InsightItem(
        insight_id="ia_02_preditivo_ml",
        title="Scorecard de Validação do Classificador Preditivo (ML)",
        category="04_intelligence_ai",
        category_label="04. Inteligência & IA",
        category_badge_color="#7C3AED",
        directory_path="insights/04_intelligence_ai/01_modelos_preditivos_ml/",
        spec_file_path="pipelines/case-item-08/outputs/ml_model_evaluation.md",
        chart_image_path="presentation/pitch/roteiro/views-05-insights-ia/modelos-preditivos-ml/chart_modelos_preditivos_ml.png",
        key_kpis=(
            ("AUC-ROC", "0.9478"),
            ("Acurácia de Classificação", "99.53%"),
            ("Features Comportamentais", "14 Variáveis"),
            ("Falsos Positivos", "< 0.4%"),
        ),
        description="Avaliação de performance do modelo supervisionado de propensão de resgate treinado para direcionar os canais corretos em tempo real.",
        architecture_notes="Pipeline de Machine Learning executado no Snowpark com exportação do scorecard."
    ),
    InsightItem(
        insight_id="ia_03_genai_copies",
        title="Motor GenAI de Copies Contextuais com Validação Pydantic",
        category="04_intelligence_ai",
        category_label="04. Inteligência & IA",
        category_badge_color="#7C3AED",
        directory_path="insights/04_intelligence_ai/02_genai_extracao_copies/",
        spec_file_path="pipelines/case-item-05/outputs/genai_feature_extraction_report.md",
        chart_image_path="presentation/pitch/roteiro/views-05-insights-ia/genai-extracao-copies/chart_genai_extracao_copies.png",
        key_kpis=(
            ("Validação de Schema", "100% Pydantic JSON"),
            ("Alucinação de Modelo", "0.0%"),
            ("Lift em CTR", "+18% vs E-mails Genéricos"),
            ("Latência de Inferência", "< 2.5 ms"),
        ),
        description="Extração semântica de motivos de hesitação e geração instantânea de copies persuasivas e personalizadas para WhatsApp e E-mail.",
        architecture_notes="DEC-002 • Prompt Engineering estruturado com JSON Schema e Pydantic BaseModel."
    ),
    InsightItem(
        insight_id="ia_04_busca_vetorial",
        title="Projeção Vetorial 2D & Recomendação de SKUs Similares",
        category="04_intelligence_ai",
        category_label="04. Inteligência & IA",
        category_badge_color="#7C3AED",
        directory_path="insights/04_intelligence_ai/03_similaridade_produtos/",
        spec_file_path="insights/04_intelligence_ai/README.md",
        chart_image_path="presentation/pitch/roteiro/views-05-insights-ia/similaridade-produtos/chart_similaridade_produtos.png",
        key_kpis=(
            ("Catálogo Vetorizado", "300 SKUs"),
            ("Similaridade de Cosseno", ">= 0.85"),
            ("Recuperação Cruzada", "+12.4% GMV"),
            ("Projeção Dimensional", "t-SNE 2D Interativo"),
        ),
        description="Clusterização semântica do catálogo de produtos para recomendação automática de substitutos com maior margem em carrinhos abandonados.",
        architecture_notes="Embeddings multidimensionais projetados em 2D para visualização executiva."
    ),
)

_INSIGHTS_MAP: Final[Mapping[str, InsightItem]] = MappingProxyType({
    item.insight_id: item for item in _INSIGHTS_DATA
})


# =============================================================================
# 🚀 FUNÇÕES PURAS DE CONSULTA E ACESSO
# =============================================================================

def get_all_insights() -> tuple[InsightItem, ...]:
    """Retorna todos os itens do catálogo de insights."""
    return _INSIGHTS_DATA


def get_insights_by_category(category: str) -> tuple[InsightItem, ...]:
    """Retorna apenas os insights de uma determinada categoria."""
    return tuple(item for item in _INSIGHTS_DATA if item.category == category)


def get_insight_by_id(insight_id: str) -> InsightItem | None:
    """Retorna um item de insight por seu ID único."""
    return _INSIGHTS_MAP.get(insight_id)


def get_categories() -> tuple[tuple[str, str, str], ...]:
    """Retorna a lista de categorias canônicas (key, label, color)."""
    return (
        ("01_descriptive", "01. Descritivo", "#2563EB"),
        ("02_risk", "02. Risco", "#D97706"),
        ("03_prescriptive", "03. Prescritivo", "#059669"),
        ("04_intelligence_ai", "04. Inteligência & IA", "#7C3AED"),
    )
