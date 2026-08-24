"""Contratos de dados e modelos tipados para a aplicação Streamlit (Padrão TypeScript / Data Contracts)."""

from dataclasses import dataclass
from typing import Final, Literal, Mapping, Sequence, TypeAlias

RFMSegment: TypeAlias = Literal[
    "Campeões", "Clientes Leais", "Potenciais Leais", "Promissores",
    "Precisam de Atenção", "Quase Hibernando", "Em Risco", "Hibernando"
]

ChannelType: TypeAlias = Literal["WhatsApp", "Email", "SMS", "Push"]

AbandonmentReason: TypeAlias = Literal[
    "Frete Abusivo", "Preço Elevado", "Dúvida Técnica", "Checkout Complexo", "Indecisão"
]

@dataclass(frozen=True)
class ChannelAllocation:
    """Alocação percentual e volumétrica por canal de resgate."""
    channel: ChannelType
    share_pct: float
    dispatches_count: int
    cost_per_dispatch: float
    base_conversion_rate: float

@dataclass(frozen=True)
class SimulationInput:
    """Parâmetros de entrada para a simulação financeira de resgate."""
    total_abandoned_carts: int
    average_ticket: float
    discount_pct: float
    conversion_elasticity: float
    channel_allocations: tuple[ChannelAllocation, ...]

@dataclass(frozen=True)
class ChannelSimulationResult:
    """Resultado detalhado por canal de comunicação."""
    channel: ChannelType
    dispatches: int
    recovered_carts: int
    conversion_rate_pct: float
    gross_recovered_revenue: float
    communication_cost: float
    discount_cost: float
    net_recovered_revenue: float
    roi_multiplier: float

@dataclass(frozen=True)
class SimulationOutput:
    """Resultado financeiro consolidado da campanha."""
    total_dispatches: int
    total_recovered_carts: int
    blended_conversion_rate_pct: float
    total_gross_revenue: float
    total_communication_cost: float
    total_discount_cost: float
    total_net_revenue: float
    overall_roi_multiplier: float
    channel_breakdown: tuple[ChannelSimulationResult, ...]

@dataclass(frozen=True)
class ProductSimilarityMatch:
    """Produto similar retornado pela busca vetorial por cosseno."""
    product_id: str
    title: str
    category: str
    price: float
    similarity_score: float
    price_sensitivity: str
    urgency_level: str
    friction_risk: str

@dataclass(frozen=True)
class GeneratedCopy:
    """Cópia estruturada gerada para abordagem de resgate."""
    channel: ChannelType
    segment: RFMSegment
    reason: AbandonmentReason
    subject_or_headline: str
    body_text: str
    call_to_action: str
    persuasion_trigger: str

@dataclass(frozen=True)
class ShowcasePresentation:
    """Estrutura da apresentação visual do produto (Item Bônus)."""
    title: str
    value_proposition: str
    key_pillars: str
    visual_prompt_reference: str
    sales_pitch_hook: str
