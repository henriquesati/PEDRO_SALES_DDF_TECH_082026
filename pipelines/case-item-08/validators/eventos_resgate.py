"""
Validador Declarativo e Funcional: Entidade 'eventos_resgate' (Item 8 - Dadosfera)
Contém funções de validação puras e a tupla declarativa de regras.
"""

from typing import Final
import pandas as pd
from core.types import ValidationResult, ValidationRule


def validate_resgate_id_not_null(df: pd.DataFrame) -> ValidationResult:
    """Verifica se a PK do disparo de resgate é não-nula."""
    nulls = int(df["resgate_id"].isna().sum()) if "resgate_id" in df.columns else len(df)
    return ValidationResult(
        rule_code="ERR_RES_001",
        rule_name="resgate_id_not_null",
        entity_name="eventos_resgate",
        column_name="resgate_id",
        passed=(nulls == 0),
        total_records=len(df),
        affected_count=nulls,
        severity="CRITICAL",
        description="Identificador único do evento de resgate (PK) não pode ser nulo.",
    )


def validate_carrinho_id_fk_not_null(df: pd.DataFrame) -> ValidationResult:
    """Verifica integridade de FK com o carrinho alvo."""
    nulls = int(df["carrinho_id"].isna().sum()) if "carrinho_id" in df.columns else len(df)
    return ValidationResult(
        rule_code="ERR_RES_002",
        rule_name="carrinho_id_fk_not_null",
        entity_name="eventos_resgate",
        column_name="carrinho_id",
        passed=(nulls == 0),
        total_records=len(df),
        affected_count=nulls,
        severity="CRITICAL",
        description="FK do carrinho alvo da recuperação não pode ser nula.",
    )


def validate_send_open_temporal_order(df: pd.DataFrame) -> ValidationResult:
    """Garante que a abertura do e-mail/SMS seja posterior ao envio."""
    if "data_envio" not in df.columns or "data_abertura" not in df.columns:
        invalid = 0
    else:
        valid_dates = df["data_envio"].notna() & df["data_abertura"].notna()
        df_sub = df.loc[valid_dates]
        invalid = int((df_sub["data_abertura"] < df_sub["data_envio"]).sum())

    return ValidationResult(
        rule_code="ERR_RES_003",
        rule_name="send_open_temporal_order",
        entity_name="eventos_resgate",
        column_name="data_abertura",
        passed=(invalid == 0),
        total_records=len(df),
        affected_count=invalid,
        severity="WARNING",
        description="Timestamp de abertura não pode ser anterior ao timestamp de envio.",
    )


def validate_channel_domain(df: pd.DataFrame) -> ValidationResult:
    """Valida se o canal de resgate pertence aos canais autorizados."""
    valid_channels = {"email", "sms", "whatsapp", "push_app"}
    if "canal" not in df.columns:
        invalid = len(df)
    else:
        invalid = int((~df["canal"].isin(valid_channels)).sum())

    return ValidationResult(
        rule_code="ERR_RES_004",
        rule_name="channel_domain_check",
        entity_name="eventos_resgate",
        column_name="canal",
        passed=(invalid == 0),
        total_records=len(df),
        affected_count=invalid,
        severity="WARNING",
        description="Canal de comunicação deve pertencer ao conjunto padronizado (email, sms, whatsapp, push_app).",
    )


# =============================================================================
# 📋 Array Declarativo de Funções de Validação
# =============================================================================

VALIDATION_EVENTOS_RESGATE: Final[tuple[ValidationRule, ...]] = (
    validate_resgate_id_not_null,
    validate_carrinho_id_fk_not_null,
    validate_send_open_temporal_order,
    validate_channel_domain,
)
