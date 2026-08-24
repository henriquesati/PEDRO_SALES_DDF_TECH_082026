"""
Validador Declarativo e Funcional: Entidade 'itens_carrinho' (Item 8 - Dadosfera)
Contém funções de validação puras e a tupla declarativa de regras.
"""

from typing import Final
import pandas as pd
from core.types import ValidationResult, ValidationRule


def validate_item_id_not_null(df: pd.DataFrame) -> ValidationResult:
    """Verifica se o identificador do item é não-nulo."""
    nulls = int(df["item_id"].isna().sum()) if "item_id" in df.columns else len(df)
    return ValidationResult(
        rule_code="ERR_ITM_001",
        rule_name="item_id_not_null",
        entity_name="itens_carrinho",
        column_name="item_id",
        passed=(nulls == 0),
        total_records=len(df),
        affected_count=nulls,
        severity="CRITICAL",
        description="Identificador único do item no carrinho não pode ser nulo.",
    )


def validate_carrinho_id_fk_not_null(df: pd.DataFrame) -> ValidationResult:
    """Verifica se a FK de carrinho está presente."""
    nulls = int(df["carrinho_id"].isna().sum()) if "carrinho_id" in df.columns else len(df)
    return ValidationResult(
        rule_code="ERR_ITM_002",
        rule_name="carrinho_id_fk_not_null",
        entity_name="itens_carrinho",
        column_name="carrinho_id",
        passed=(nulls == 0),
        total_records=len(df),
        affected_count=nulls,
        severity="CRITICAL",
        description="FK do carrinho de origem não pode ser nula.",
    )


def validate_positive_quantity(df: pd.DataFrame) -> ValidationResult:
    """Garante quantidade estritamente positiva."""
    if "quantidade" not in df.columns:
        invalid = len(df)
    else:
        invalid = int((df["quantidade"] <= 0).sum())

    return ValidationResult(
        rule_code="ERR_ITM_003",
        rule_name="positive_quantity",
        entity_name="itens_carrinho",
        column_name="quantidade",
        passed=(invalid == 0),
        total_records=len(df),
        affected_count=invalid,
        severity="CRITICAL",
        description="Quantidade do item no carrinho deve ser superior a zero.",
    )


def validate_positive_unit_price(df: pd.DataFrame) -> ValidationResult:
    """Garante preço unitário positivo."""
    if "preco_unitario" not in df.columns:
        invalid = len(df)
    else:
        invalid = int((df["preco_unitario"] <= 0).sum())

    return ValidationResult(
        rule_code="ERR_ITM_004",
        rule_name="positive_unit_price",
        entity_name="itens_carrinho",
        column_name="preco_unitario",
        passed=(invalid == 0),
        total_records=len(df),
        affected_count=invalid,
        severity="CRITICAL",
        description="Preço unitário do item adicionado deve ser maior que zero.",
    )


# =============================================================================
# 📋 Array Declarativo de Funções de Validação
# =============================================================================

VALIDATION_ITENS_CARRINHO: Final[tuple[ValidationRule, ...]] = (
    validate_item_id_not_null,
    validate_carrinho_id_fk_not_null,
    validate_positive_quantity,
    validate_positive_unit_price,
)
