"""
Step 2: Qualificação, Data Quality & Quarentena de Anomalias (Padrão Stepsfera / Dadosfera)
"""

import time
from pathlib import Path
import pandas as pd
from config.settings import ANOMALIES_DIR, QUALIFY_DIR
from core.types import StepExecutionResult, StepMetadata, ValidationResult
from transformations.bronze_to_silver import execute_bronze_to_silver_pipeline

STEP_METADATA = StepMetadata(
    step_id="step_02_validate_qualify",
    step_name="Qualificação e Quarentena (Silver)",
    category="Quality",
    layer_source="bronze",
    layer_target="silver_qualify",
    description="Aplica suíte declarativa de Data Quality e bifurca em Qualify e Anomalies (DEC-006).",
    snowpark_compatible=True,
)


def run_step(
    raw_datasets: dict[str, pd.DataFrame],
    qualify_dir: Path = QUALIFY_DIR,
    anomalies_dir: Path = ANOMALIES_DIR,
) -> tuple[dict[str, pd.DataFrame], dict[str, pd.DataFrame], tuple[ValidationResult, ...], StepExecutionResult]:
    """Executa a qualificação declarativa e segregação em quarentena de todas as entidades."""
    start_time = time.perf_counter()
    qualify_datasets: dict[str, pd.DataFrame] = {}
    anomaly_datasets: dict[str, pd.DataFrame] = {}
    all_validation_results: list[ValidationResult] = []
    
    total_in = 0
    total_qualify = 0
    total_anomalies = 0
    details: list[str] = []

    qualify_dir.mkdir(parents=True, exist_ok=True)
    anomalies_dir.mkdir(parents=True, exist_ok=True)

    for entity_name, df_raw in raw_datasets.items():
        total_in += len(df_raw)
        df_q, df_a, val_res = execute_bronze_to_silver_pipeline(entity_name, df_raw)
        
        qualify_datasets[entity_name] = df_q
        anomaly_datasets[entity_name] = df_a
        all_validation_results.extend(val_res)
        
        q_count = len(df_q)
        a_count = len(df_a)
        total_qualify += q_count
        total_anomalies += a_count

        # Persistência em Parquet
        df_q.to_parquet(qualify_dir / f"{entity_name}.parquet", index=False)
        if a_count > 0:
            df_a.to_parquet(anomalies_dir / f"{entity_name}_anomalies.parquet", index=False)

        details.append(f"{entity_name}: {q_count:,} conformes | {a_count:,} anomalias")

    duration_ms = (time.perf_counter() - start_time) * 1000

    result = StepExecutionResult(
        step_id=STEP_METADATA.step_id,
        step_name=STEP_METADATA.step_name,
        status="SUCCESS",
        records_in=total_in,
        records_out=total_qualify,
        duration_ms=round(duration_ms, 2),
        message=f"Qualificação concluída: {total_qualify:,} conformes ({(total_qualify/max(total_in,1))*100:.1f}%) | {total_anomalies:,} isolados.",
        details=tuple(details),
    )

    return qualify_datasets, anomaly_datasets, tuple(all_validation_results), result
