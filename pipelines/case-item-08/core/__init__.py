"""Módulo core funcional do Item 8."""
from .types import ValidationResult, ValidationRule, StepMetadata, StepExecutionResult, MLModelMetrics, PipelineExecutionSummary
from .functional import pipe, compose, run_validation_suite, split_qualify_and_anomalies, safe_assign, dispatch_handler
