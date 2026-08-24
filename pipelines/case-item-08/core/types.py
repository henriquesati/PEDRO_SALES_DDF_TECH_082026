"""
Tipos Imutáveis e Contratos de Tipagem (Item 8 - Dadosfera)
Seguindo o paradigma funcional declarativo estrito.
"""

from dataclasses import dataclass
from typing import Callable, Literal, NamedTuple, Protocol, Sequence, TypeAlias
import pandas as pd

# =============================================================================
# 🏷️ Type Aliases Fundamentais
# =============================================================================

Severity: TypeAlias = Literal["INFO", "WARNING", "CRITICAL"]
LayerName: TypeAlias = Literal["bronze", "silver_qualify", "silver_anomaly", "gold_curated"]
StepStatus: TypeAlias = Literal["SUCCESS", "FAILED", "SKIPPED"]

# Funções de pipeline funcional
TransformFn: TypeAlias = Callable[[pd.DataFrame], pd.DataFrame]


# =============================================================================
# 📦 Estruturas de Dados Imutáveis (Frozen Dataclasses & NamedTuples)
# =============================================================================

@dataclass(frozen=True)
class ValidationResult:
    """Resultado imutável de uma regra de validação declarativa."""
    rule_code: str
    rule_name: str
    entity_name: str
    column_name: str | None
    passed: bool
    total_records: int
    affected_count: int
    severity: Severity
    description: str


ValidationRule: TypeAlias = Callable[[pd.DataFrame], ValidationResult]


@dataclass(frozen=True)
class StepMetadata:
    """Metadados descritivos de um Step no padrão Stepsfera."""
    step_id: str
    step_name: str
    category: Literal["Ingest", "Quality", "GenAI", "Kimball", "ML"]
    layer_source: LayerName
    layer_target: LayerName
    description: str
    snowpark_compatible: bool = True


@dataclass(frozen=True)
class StepExecutionResult:
    """Resultado da execução de um Step individual."""
    step_id: str
    step_name: str
    status: StepStatus
    records_in: int
    records_out: int
    duration_ms: float
    message: str
    details: tuple[str, ...] = ()


@dataclass(frozen=True)
class MLModelMetrics:
    """Métricas de avaliação do modelo de Machine Learning treinado."""
    model_name: str
    target_variable: str
    train_records: int
    test_records: int
    accuracy: float
    roc_auc: float
    f1_score: float
    precision: float
    recall: float
    feature_importances: tuple[tuple[str, float], ...]


@dataclass(frozen=True)
class PipelineExecutionSummary:
    """Sumário consolidado imutável da execução de todo o pipeline."""
    execution_id: str
    profile_used: str
    started_at: str
    completed_at: str
    total_duration_ms: float
    total_raw_records: int
    total_qualify_records: int
    total_anomaly_records: int
    total_gold_records: int
    steps_executed: tuple[StepExecutionResult, ...]
    validation_results: tuple[ValidationResult, ...]
    ml_metrics: MLModelMetrics | None = None
