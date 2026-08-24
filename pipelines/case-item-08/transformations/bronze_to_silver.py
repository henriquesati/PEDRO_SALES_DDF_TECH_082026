"""
Transformações Funcionais: Bronze (RAW) -> Silver (Qualify & Anomalies)
Segue a decisão arquitetural DEC-006 (Dual-Artifact Pipeline).
"""

from typing import Final, Mapping
import numpy as np
import pandas as pd
from core.functional import pipe, split_qualify_and_anomalies
from core.types import TransformFn, ValidationResult, ValidationRule
from validators.registry import get_validators_for_entity

# =============================================================================
# 🧹 Funções Puras de Sanitização (Pure Sanitation Functions)
# =============================================================================

def strip_whitespace_from_strings(df: pd.DataFrame) -> pd.DataFrame:
    """Remove espaços em branco no início e fim de colunas do tipo texto."""
    str_cols = df.select_dtypes(include=["object", "string"]).columns
    if len(str_cols) == 0:
        return df.copy()
    
    transform_dict = {col: df[col].astype(str).str.strip() for col in str_cols}
    return df.assign(**transform_dict)


def normalize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Padroniza nomes de colunas em snake_case minúsculo."""
    new_columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
    new_df = df.copy()
    new_df.columns = new_columns
    return new_df


def sanitize_negative_numbers(df: pd.DataFrame, columns: tuple[str, ...]) -> pd.DataFrame:
    """Função pura que sanitiza números negativos para seus valores absolutos."""
    valid_cols = [c for c in columns if c in df.columns]
    if not valid_cols:
        return df.copy()
    
    updates = {c: df[c].abs() for c in valid_cols}
    return df.assign(**updates)


# =============================================================================
# ⚖️ Pipeline de Qualificação Declarativo
# =============================================================================

def identify_anomalous_indices(
    entity_name: str,
    df: pd.DataFrame,
) -> set[int | str]:
    """Identifica índices de registros com anomalias críticas e severas."""
    anomalous: set[int | str] = set()

    if entity_name == "carrinhos":
        if "carrinho_id" in df.columns:
            anomalous.update(df[df["carrinho_id"].isna()].index)
        if "cliente_id" in df.columns:
            anomalous.update(df[df["cliente_id"].isna()].index)
        if "valor_frete" in df.columns:
            anomalous.update(df[df["valor_frete"] < 0].index)
        if "valor_subtotal" in df.columns and "valor_desconto" in df.columns:
            anomalous.update(df[df["valor_desconto"] > df["valor_subtotal"]].index)
        if {"valor_total", "valor_subtotal", "valor_frete", "valor_desconto"}.issubset(df.columns):
            expected = df["valor_subtotal"] + df["valor_frete"] - df["valor_desconto"]
            anomalous.update(df[(df["valor_total"] - expected).abs() > 0.01].index)

    elif entity_name == "clientes":
        if "cliente_id" in df.columns:
            anomalous.update(df[df["cliente_id"].isna()].index)
        if "email" in df.columns:
            anomalous.update(df[df["email"].isna()].index)

    elif entity_name == "produtos":
        if "produto_id" in df.columns:
            anomalous.update(df[df["produto_id"].isna()].index)
        if "preco_atual" in df.columns:
            anomalous.update(df[df["preco_atual"] <= 0].index)

    elif entity_name == "itens_carrinho":
        if "item_id" in df.columns:
            anomalous.update(df[df["item_id"].isna()].index)
        if "quantidade" in df.columns:
            anomalous.update(df[df["quantidade"] <= 0].index)
        if "preco_unitario" in df.columns:
            anomalous.update(df[df["preco_unitario"] <= 0].index)

    elif entity_name == "eventos_resgate":
        if "resgate_id" in df.columns:
            anomalous.update(df[df["resgate_id"].isna()].index)
        if "carrinho_id" in df.columns:
            anomalous.update(df[df["carrinho_id"].isna()].index)

    return anomalous


def execute_bronze_to_silver_pipeline(
    entity_name: str,
    df_raw: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, tuple[ValidationResult, ...]]:
    """
    Executa a transformação pura de Bronze para Silver (Qualify e Anomalies).
    Retorna: (df_qualify, df_anomalies, validation_results)
    """
    df_sanitized = pipe(
        df_raw,
        normalize_column_names,
        strip_whitespace_from_strings,
    )

    validators = get_validators_for_entity(entity_name)
    validation_results = tuple(validator_fn(df_sanitized) for validator_fn in validators)

    anomalous_indices = identify_anomalous_indices(entity_name, df_sanitized)
    df_qualify, df_anomalies = split_qualify_and_anomalies(df_sanitized, anomalous_indices)

    return df_qualify, df_anomalies, validation_results
