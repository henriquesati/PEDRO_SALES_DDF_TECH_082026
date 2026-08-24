"""
Validador Declarativo e Funcional: Entidade 'carrinhos' (Item 8 - Dadosfera)
Contém funções de validação puras e a tupla declarativa de regras.
"""

from typing import Final
import pandas as pd
from core.types import ValidationResult, ValidationRule

# =============================================================================
# 🔍 Funções de Validação Puras (Pure Validation Functions)
# =============================================================================

def validate_carrinho_id_not_null(df: pd.DataFrame) -> ValidationResult:
    """Verifica se o identificador do carrinho é não-nulo."""
    nulls = int(df["carrinho_id"].isna().sum()) if "carrinho_id" in df.columns else len(df)
    return ValidationResult(
        rule_code="ERR_CAR_001",
        rule_name="carrinho_id_not_null",
        entity_name="carrinhos",
        column_name="carrinho_id",
        passed=(nulls == 0),
        total_records=len(df),
        affected_count=nulls,
        severity="CRITICAL",
        description="Identificador único de sessão de carrinho não pode ser nulo.",
    )


def validate_cliente_id_not_null(df: pd.DataFrame) -> ValidationResult:
    """Verifica se a chave estrangeira do cliente está preenchida."""
    nulls = int(df["cliente_id"].isna().sum()) if "cliente_id" in df.columns else len(df)
    return ValidationResult(
        rule_code="ERR_CAR_002",
        rule_name="cliente_id_not_null",
        entity_name="carrinhos",
        column_name="cliente_id",
        passed=(nulls == 0),
        total_records=len(df),
        affected_count=nulls,
        severity="CRITICAL",
        description="Identificador do cliente associado ao carrinho não pode ser nulo.",
    )


def validate_status_domain(df: pd.DataFrame) -> ValidationResult:
    """Valida se o status pertence ao domínio permitido."""
    valid_statuses = {"comprado", "abandonado", "expirado", "ativo", "recuperado"}
    if "status" not in df.columns:
        invalid_count = len(df)
    else:
        invalid_count = int((~df["status"].isin(valid_statuses)).sum())

    return ValidationResult(
        rule_code="ERR_CAR_003",
        rule_name="status_domain_check",
        entity_name="carrinhos",
        column_name="status",
        passed=(invalid_count == 0),
        total_records=len(df),
        affected_count=invalid_count,
        severity="WARNING",
        description="Status do carrinho deve pertencer ao conjunto canônico de estados.",
    )


def validate_non_negative_shipping(df: pd.DataFrame) -> ValidationResult:
    """ANOM-01: Detecta cobranças de frete negativo."""
    if "valor_frete" not in df.columns:
        negatives = 0
    else:
        negatives = int((df["valor_frete"] < 0).sum())

    return ValidationResult(
        rule_code="ANOM_CAR_001",
        rule_name="non_negative_shipping",
        entity_name="carrinhos",
        column_name="valor_frete",
        passed=(negatives == 0),
        total_records=len(df),
        affected_count=negatives,
        severity="CRITICAL",
        description="Valor de frete não pode ser negativo (ANOM-01).",
    )


def validate_positive_subtotal(df: pd.DataFrame) -> ValidationResult:
    """ANOM-02: Detecta subtotal zerado ou negativo em carrinhos com itens."""
    if "valor_subtotal" not in df.columns:
        invalid = 0
    else:
        invalid = int((df["valor_subtotal"] <= 0).sum())

    return ValidationResult(
        rule_code="ANOM_CAR_002",
        rule_name="positive_subtotal",
        entity_name="carrinhos",
        column_name="valor_subtotal",
        passed=(invalid == 0),
        total_records=len(df),
        affected_count=invalid,
        severity="WARNING",
        description="Subtotal do carrinho com itens deve ser estritamente maior que zero (ANOM-02).",
    )


def validate_discount_ceiling(df: pd.DataFrame) -> ValidationResult:
    """ANOM-03: Garante que o desconto não exceda o subtotal."""
    if "valor_desconto" not in df.columns or "valor_subtotal" not in df.columns:
        invalid = 0
    else:
        invalid = int((df["valor_desconto"] > df["valor_subtotal"]).sum())

    return ValidationResult(
        rule_code="ANOM_CAR_003",
        rule_name="discount_ceiling_check",
        entity_name="carrinhos",
        column_name="valor_desconto",
        passed=(invalid == 0),
        total_records=len(df),
        affected_count=invalid,
        severity="CRITICAL",
        description="Desconto comercial não pode ultrapassar o subtotal do carrinho (ANOM-03).",
    )


def validate_accounting_equation(df: pd.DataFrame) -> ValidationResult:
    """ANOM-04: Confere a equação contábil: total = subtotal + frete - desconto."""
    required_cols = {"valor_total", "valor_subtotal", "valor_frete", "valor_desconto"}
    if not required_cols.issubset(df.columns):
        invalid = 0
    else:
        expected = df["valor_subtotal"] + df["valor_frete"] - df["valor_desconto"]
        diff = (df["valor_total"] - expected).abs()
        invalid = int((diff > 0.01).sum())

    return ValidationResult(
        rule_code="ANOM_CAR_004",
        rule_name="accounting_equation_consistency",
        entity_name="carrinhos",
        column_name="valor_total",
        passed=(invalid == 0),
        total_records=len(df),
        affected_count=invalid,
        severity="CRITICAL",
        description="Equação contábil do total do carrinho inconsistente (ANOM-04).",
    )


def validate_temporal_order(df: pd.DataFrame) -> ValidationResult:
    """ANOM-05: Confere se a data de abandono é posterior ou igual à data de criação."""
    if "data_criacao" not in df.columns or "data_abandono" not in df.columns:
        invalid = 0
    else:
        valid_dates = df["data_criacao"].notna() & df["data_abandono"].notna()
        df_sub = df.loc[valid_dates]
        invalid = int((df_sub["data_abandono"] < df_sub["data_criacao"]).sum())

    return ValidationResult(
        rule_code="ANOM_CAR_005",
        rule_name="temporal_creation_abandonment_order",
        entity_name="carrinhos",
        column_name="data_abandono",
        passed=(invalid == 0),
        total_records=len(df),
        affected_count=invalid,
        severity="WARNING",
        description="Data de abandono não pode ser cronologicamente anterior à criação (ANOM-05).",
    )


# =============================================================================
# 📋 Array Declarativo de Funções de Validação
# =============================================================================

VALIDATION_CARRINHOS: Final[tuple[ValidationRule, ...]] = (
    validate_carrinho_id_not_null,
    validate_cliente_id_not_null,
    validate_status_domain,
    validate_non_negative_shipping,
    validate_positive_subtotal,
    validate_discount_ceiling,
    validate_accounting_equation,
    validate_temporal_order,
)
