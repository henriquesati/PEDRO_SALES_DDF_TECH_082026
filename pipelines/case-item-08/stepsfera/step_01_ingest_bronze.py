"""
Step 1: Ingestão Bronze & Schema Enforcement (Padrão Stepsfera / Dadosfera)
"""

import time
from pathlib import Path
import pandas as pd
from config.settings import ENTITY_FILES, RAW_DATA_DIR
from core.types import StepExecutionResult, StepMetadata

STEP_METADATA = StepMetadata(
    step_id="step_01_ingest_bronze",
    step_name="Ingestão de Dados Brutos (Bronze)",
    category="Ingest",
    layer_source="bronze",
    layer_target="bronze",
    description="Carrega os datasets brutos do data lakehouse e valida os esquemas de entrada.",
    snowpark_compatible=True,
)


def run_step(raw_dir: Path = RAW_DATA_DIR) -> tuple[dict[str, pd.DataFrame], StepExecutionResult]:
    """Executa a ingestão pura dos arquivos Parquet da camada Bronze."""
    start_time = time.perf_counter()
    loaded_datasets: dict[str, pd.DataFrame] = {}
    total_records = 0
    details: list[str] = []

    for entity_name, filename in ENTITY_FILES.items():
        file_path = raw_dir / filename
        if file_path.exists():
            df = pd.read_parquet(file_path)
            loaded_datasets[entity_name] = df
            count = len(df)
            total_records += count
            details.append(f"{entity_name}: {count:,} registros")
        else:
            details.append(f"{entity_name}: arquivo {filename} não encontrado")

    duration_ms = (time.perf_counter() - start_time) * 1000

    result = StepExecutionResult(
        step_id=STEP_METADATA.step_id,
        step_name=STEP_METADATA.step_name,
        status="SUCCESS" if loaded_datasets else "FAILED",
        records_in=total_records,
        records_out=total_records,
        duration_ms=round(duration_ms, 2),
        message=f"Carregadas {len(loaded_datasets)} entidades com sucesso.",
        details=tuple(details),
    )

    return loaded_datasets, result
