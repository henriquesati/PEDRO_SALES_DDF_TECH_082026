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

VoiceTone: TypeAlias = Literal["Urgência", "Suporte", "Prova Social"]

RecommendationStrategy: TypeAlias = Literal["Substituto", "Cross-sell", "Acessório"]

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
    preserved_margin_pct: float
    channel_breakdown: tuple[ChannelSimulationResult, ...]

@dataclass(frozen=True)
class ProductSimilarityMatch:
    """Produto similar retornado pela busca vetorial por cosseno."""
    product_id: str
    title: str
    category: str
    price: float
    price_delta_pct: float
    similarity_score: float
    strategy_badge: RecommendationStrategy
    price_sensitivity: str
    urgency_level: str
    friction_risk: str

@dataclass(frozen=True)
class MLFeatureDriver:
    """Impacto marginal de feature no modelo de Machine Learning."""
    feature_name: str
    importance_pct: float
    impact_type: Literal["Positivo", "Negativo"]
    description: str

@dataclass(frozen=True)
class MLModelSummary:
    """Métricas consolidadas do modelo supervisionado de propensão."""
    model_name: str
    accuracy: float
    roc_auc: float
    f1_score: float
    precision: float
    recall: float
    train_records: int
    test_records: int
    top_drivers: tuple[MLFeatureDriver, ...]

@dataclass(frozen=True)
class GeneratedCopy:
    """Cópia estruturada gerada para abordagem de resgate."""
    channel: ChannelType
    segment: RFMSegment
    reason: AbandonmentReason
    tone: VoiceTone
    subject_or_headline: str
    body_text: str
    call_to_action: str
    persuasion_trigger: str
    json_schema_payload: str

@dataclass(frozen=True)
class ShowcasePresentation:
    """Estrutura da apresentação visual e multimodal do produto (Item Bônus GenAI)."""
    title: str
    value_proposition: str
    key_pillars: str
    visual_prompt_reference: str
    sales_pitch_hook: str
    audio_transcript: str


# =============================================================================
# 🥋 CONTRATOS DO ROSTER DE AGENTES & SKILLS (STREET FIGHTER ARCADE SPEC)
# =============================================================================

AgentMode: TypeAlias = Literal["Autonomous", "Specialist", "Subagent", "Read-Only"]
AgentCategory: TypeAlias = Literal[
    "01_strategy_governance",
    "02_lakehouse_engineering",
    "03_analytics_insights"
]

AgentArchetype: TypeAlias = Literal[
    "Master Strategist",
    "Repository Architect",
    "Analytics Mastermind",
    "Platform Guardian",
    "Lineage Chronicler",
    "Pure Logic Sage",
    "Visual Virtuoso",
    "Senior Consultant",
    "Synthetic World Builder",
    "Code Explorer"
]

@dataclass(frozen=True)
class AgentPowerStats:
    """Atributos numéricos e medidores técnicos do agente (0-100)."""
    autonomy: int
    analytical_rigor: int
    execution_speed: int
    platform_mastery: int
    data_quality: int

@dataclass(frozen=True)
class SpecialMove:
    """Capacidade técnica / especialidade única do agente."""
    name: str
    input_command: str
    description: str
    impact_area: str

@dataclass(frozen=True)
class AgentCombo:
    """Sinergia colaborativa com outro agente do ecossistema."""
    partner_agent: str
    combo_name: str
    workflow_description: str

@dataclass(frozen=True)
class SkillProfile:
    """Perfil completo e imutável de uma Skill."""
    skill_id: str
    display_name: str
    archetype: str
    category: AgentCategory
    avatar_emoji: str
    file_path: str
    description: str
    tools_available: tuple[str, ...]
    artifacts_managed: tuple[str, ...]
    constraints: tuple[str, ...]
    case_items_covered: tuple[str, ...]

    def to_yaml_spec(self) -> str:
        """Gera a especificação YAML limpa da Skill (sem kind)."""
        tools_yaml = "\n".join(f"    - {t}" for t in self.tools_available)
        artifacts_yaml = "\n".join(f"    - {a}" for a in self.artifacts_managed)
        items_yaml = "\n".join(f"    - {item}" for item in self.case_items_covered)
        constraints_yaml = "\n".join(f"    - {c}" for c in self.constraints)

        return f"""apiVersion: dadosfera.ai/v1alpha1
metadata:
  name: {self.skill_id}
  displayName: "{self.display_name}"
  archetype: "{self.archetype}"
  category: {self.category}
  sourceFile: "{self.file_path}"
  status: Active
spec:
  description: "{self.description}"
  tools:
{tools_yaml}
  artifactsManaged:
{artifacts_yaml}
  caseItemsCovered:
{items_yaml}
  constraints:
{constraints_yaml}
status:
  compliance: 100% Ground Truth
  sqlLocalForbidden: true
"""

@dataclass(frozen=True)
class AgentProfile:
    """Perfil completo e imutável do agente para o catálogo e console."""
    slot_number: str
    agent_id: str
    display_name: str
    arcade_title: str
    archetype: AgentArchetype
    category: AgentCategory
    avatar_emoji: str
    card_color_hex: str
    accent_color_hex: str
    mode: AgentMode
    soundbite: str
    mission: str
    role_in_case: str
    case_items_covered: tuple[str, ...]
    skills_equipped: tuple[str, ...]
    tools_available: tuple[str, ...]
    artifacts_managed: tuple[str, ...]
    direct_output: tuple[str, ...]
    constraints: tuple[str, ...]
    power_stats: AgentPowerStats
    special_moves: tuple[SpecialMove, ...]
    synergies: tuple[AgentCombo, ...]
    system_prompt_excerpt: str
    full_system_prompt: str
    file_path: str
    sample_queries: tuple[str, ...]

    def to_yaml_manifest(self) -> str:
        """Gera a especificação YAML limpa do Agente (sem kind)."""
        items_yaml = "\n".join(f"    - {item}" for item in self.case_items_covered)
        skills_yaml = "\n".join(f"    - {skill}" for skill in self.skills_equipped)
        tools_yaml = "\n".join(f"    - {tool}" for tool in self.tools_available)
        artifacts_yaml = "\n".join(f"    - {art}" for art in self.artifacts_managed)
        outputs_yaml = "\n".join(f"    - {out}" for out in self.direct_output)
        constraints_yaml = "\n".join(f"    - {c}" for c in self.constraints)
        moves_yaml = "\n".join(
            f"    - name: {m.name}\n      command: \"{m.input_command}\"\n      impact: {m.impact_area}"
            for m in self.special_moves
        )

        return f"""apiVersion: dadosfera.ai/v1alpha1
metadata:
  name: {self.agent_id}
  displayName: "{self.display_name}"
  archetype: "{self.arcade_title}"
  category: {self.category}
  sourceFile: "{self.file_path}"
  status: Active
spec:
  mode: {self.mode}
  mission: "{self.mission}"
  roleInCase: "{self.role_in_case}"
  caseItemsCovered:
{items_yaml}
  skillsEquipped:
{skills_yaml}
  tools:
{tools_yaml}
  artifactsManaged:
{artifacts_yaml}
  directOutputs:
{outputs_yaml}
  constraints:
{constraints_yaml}
  capabilities:
{moves_yaml}
status:
  telemetry:
    autonomy: {self.power_stats.autonomy}%
    analyticalRigor: {self.power_stats.analytical_rigor}%
    executionSpeed: {self.power_stats.execution_speed}%
    platformMastery: {self.power_stats.platform_mastery}%
    dataQualityScore: {self.power_stats.data_quality}%
  groundTruthCompliance: 100%
  sqlLocalForbidden: true
"""




