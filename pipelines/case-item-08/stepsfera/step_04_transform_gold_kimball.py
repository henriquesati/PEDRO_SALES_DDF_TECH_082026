"""
Step 4: Modelagem Dimensional Gold (Kimball Star Schema) (Padrão Stepsfera / Dadosfera)
"""

import time
from pathlib import Path
import pandas as pd
from config.settings import CURATED_DIR
from core.types import StepExecutionResult, StepMetadata
from transformations.silver_to_gold import (
    build_dim_clientes,
    build_dim_tempo,
    build_dim_dispositivo,
    build_dim_canal_resgate,
    build_fato_abandono,
    build_fato_resgate,
    build_view_abandonment_summary,
    build_view_recovery_roi_by_channel,
)

STEP_METADATA = StepMetadata(
    step_id="step_04_transform_gold_kimball",
    step_name="Modelagem Dimensional Gold (Kimball)",
    category="Kimball",
    layer_source="silver_qualify",
    layer_target="gold_curated",
    description="Constrói dimensões conformadas, fatos granulares e Data Views para o Metabase.",
    snowpark_compatible=True,
)


def run_step(
    qualify_datasets: dict[str, pd.DataFrame],
    curated_dir: Path = CURATED_DIR,
) -> tuple[dict[str, pd.DataFrame], StepExecutionResult]:
    """Constrói a camada dimensional Gold e persiste os modelos em Parquet."""
    start_time = time.perf_counter()
    curated_dir.mkdir(parents=True, exist_ok=True)
    
    df_clientes = qualify_datasets["clientes"]
    df_carrinhos = qualify_datasets["carrinhos"]
    df_resgates = qualify_datasets["eventos_resgate"]

    # 1. Dimensões conformadas
    dim_clientes = build_dim_clientes(df_clientes)
    dim_tempo = build_dim_tempo(df_carrinhos)
    dim_dispositivo = build_dim_dispositivo(df_carrinhos)
    dim_canal = build_dim_canal_resgate(df_resgates)

    # 2. Fatos granulares
    fato_abandono = build_fato_abandono(df_carrinhos, dim_clientes, dim_dispositivo)
    fato_resgate = build_fato_resgate(df_resgates, df_carrinhos, dim_canal)

    # 3. Visões analíticas
    view_abandono = build_view_abandonment_summary(fato_abandono, dim_clientes)
    view_roi = build_view_recovery_roi_by_channel(fato_resgate)

    gold_models = {
        "dim_clientes": dim_clientes,
        "dim_tempo": dim_tempo,
        "dim_dispositivo": dim_dispositivo,
        "dim_canal_resgate": dim_canal,
        "fato_abandono": fato_abandono,
        "fato_resgate": fato_resgate,
        "v_abandonment_summary": view_abandono,
        "v_recovery_roi_by_channel": view_roi,
    }

    # Persistência
    for model_name, df_model in gold_models.items():
        df_model.to_parquet(curated_dir / f"{model_name}.parquet", index=False)

    duration_ms = (time.perf_counter() - start_time) * 1000
    total_records_out = sum(len(df) for df in gold_models.values())

    result = StepExecutionResult(
        step_id=STEP_METADATA.step_id,
        step_name=STEP_METADATA.step_name,
        status="SUCCESS",
        records_in=len(df_carrinhos) + len(df_clientes) + len(df_resgates),
        records_out=total_records_out,
        duration_ms=round(duration_ms, 2),
        message=f"Modelagem Gold concluída com 4 Dimensões, 2 Fatos e 2 Data Views.",
        details=(
            f"fato_abandono: {len(fato_abandono):,} linhas",
            f"fato_resgate: {len(fato_resgate):,} linhas",
            f"v_abandonment_summary: {len(view_abandono)} registros",
            f"v_recovery_roi_by_channel: {len(view_roi)} registros",
        ),
    )

    return gold_models, result
