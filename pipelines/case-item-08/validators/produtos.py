"""
Validador Declarativo e Funcional: Entidade 'produtos' (Item 8 - Dadosfera)
Contém funções de validação puras e a tupla declarativa de regras.
"""

from typing import Final
import pandas as pd
from core.types import ValidationResult, ValidationRule


def validate_produto_id_not_null(df: pd.DataFrame) -> ValidationResult:
    """Verifica se o identificador do produto é não-nulo."""
    nulls = int(df["produto_id"].isna().sum()) if "produto_id" in df.columns else len(df)
    return ValidationResult(
        rule_code="ERR_PROD_001",
        rule_name="produto_id_not_null",
        entity_name="produtos",
        column_name="produto_id",
        passed=(nulls == 0),
        total_records=len(df),
        affected_count=nulls,
        severity="CRITICAL",
        description="Identificador único do produto (PK) não pode ser nulo.",
    )


def validate_positive_price(df: pd.DataFrame) -> ValidationResult:
    """Garante que o preço atual seja estritamente maior que zero."""
    if "preco_atual" not in df.columns:
        invalid = len(df)
    else:
        invalid = int((df["preco_atual"] <= 0).sum())

    return ValidationResult(
        rule_code="ERR_PROD_002",
        rule_name="positive_price",
        entity_name="produtos",
        column_name="preco_atual",
        passed=(invalid == 0),
        total_records=len(df),
        affected_count=invalid,
        severity="CRITICAL",
        description="Preço comercial do produto deve ser estritamente positivo.",
    )


def validate_promotional_consistency(df: pd.DataFrame) -> ValidationResult:
    """Detecta promoção invertida (preco_atual > preco_original)."""
    if "preco_atual" not in df.columns or "preco_original" not in df.columns:
        invalid = 0
    else:
        invalid = int((df["preco_atual"] > df["preco_original"]).sum())

    return ValidationResult(
        rule_code="ERR_PROD_003",
        rule_name="promotional_consistency_check",
        entity_name="produtos",
        column_name="preco_atual",
        passed=(invalid == 0),
        total_records=len(df),
        affected_count=invalid,
        severity="WARNING",
        description="Preço promocional não pode ser superior ao preço original de tabela.",
    )


# =============================================================================
# 📋 Array Declarativo de Funções de Validação
# =============================================================================

VALIDATION_PRODUTOS: Final[tuple[ValidationRule, ...]] = (
    validate_produto_id_not_null,
    validate_positive_price,
    validate_promotional_consistency,
)
