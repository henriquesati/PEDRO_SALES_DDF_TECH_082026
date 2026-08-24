"""
Validador Declarativo e Funcional: Entidade 'clientes' (Item 8 - Dadosfera)
Contém funções de validação puras e a tupla declarativa de regras.
"""

import re
from typing import Final
import pandas as pd
from core.types import ValidationResult, ValidationRule

EMAIL_REGEX: Final[re.Pattern] = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def validate_cliente_id_not_null(df: pd.DataFrame) -> ValidationResult:
    """Verifica se a chave primária de clientes é não-nula."""
    nulls = int(df["cliente_id"].isna().sum()) if "cliente_id" in df.columns else len(df)
    return ValidationResult(
        rule_code="ERR_CLI_001",
        rule_name="cliente_id_not_null",
        entity_name="clientes",
        column_name="cliente_id",
        passed=(nulls == 0),
        total_records=len(df),
        affected_count=nulls,
        severity="CRITICAL",
        description="Identificador único do cliente (PK) não pode ser nulo.",
    )


def validate_email_not_null(df: pd.DataFrame) -> ValidationResult:
    """Verifica se o e-mail do cliente está presente."""
    nulls = int(df["email"].isna().sum()) if "email" in df.columns else len(df)
    return ValidationResult(
        rule_code="ERR_CLI_002",
        rule_name="email_not_null",
        entity_name="clientes",
        column_name="email",
        passed=(nulls == 0),
        total_records=len(df),
        affected_count=nulls,
        severity="CRITICAL",
        description="E-mail do cliente é obrigatório para réguas de recuperação.",
    )


def validate_email_format(df: pd.DataFrame) -> ValidationResult:
    """Valida a conformidade sintática do e-mail com expressão regular."""
    if "email" not in df.columns:
        invalid = len(df)
    else:
        emails = df["email"].dropna().astype(str)
        invalid = int((~emails.str.match(EMAIL_REGEX.pattern)).sum())

    return ValidationResult(
        rule_code="ERR_CLI_003",
        rule_name="email_format_regex",
        entity_name="clientes",
        column_name="email",
        passed=(invalid == 0),
        total_records=len(df),
        affected_count=invalid,
        severity="WARNING",
        description="Formato sintático de e-mail deve respeitar o padrão RFC.",
    )


def validate_rfm_score_range(df: pd.DataFrame) -> ValidationResult:
    """Garante que o score RFM esteja dentro da faixa esperada."""
    if "rfm_score" not in df.columns:
        invalid = 0
    else:
        scores = df["rfm_score"].dropna()
        invalid = int(((scores < 111) | (scores > 555)).sum())

    return ValidationResult(
        rule_code="ERR_CLI_004",
        rule_name="rfm_score_range",
        entity_name="clientes",
        column_name="rfm_score",
        passed=(invalid == 0),
        total_records=len(df),
        affected_count=invalid,
        severity="INFO",
        description="Score RFM composto deve estar contido no intervalo de 111 a 555.",
    )


# =============================================================================
# 📋 Array Declarativo de Funções de Validação
# =============================================================================

VALIDATION_CLIENTES: Final[tuple[ValidationRule, ...]] = (
    validate_cliente_id_not_null,
    validate_email_not_null,
    validate_email_format,
    validate_rfm_score_range,
)
