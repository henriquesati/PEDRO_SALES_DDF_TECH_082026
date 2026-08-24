"""
Utilitários de Programação Funcional Pura (Item 8 - Dadosfera)
Garante imutabilidade, composição limpa e ausência de efeitos colaterais.
"""

from functools import reduce
from typing import Any, Callable, Mapping, Sequence, TypeVar
import pandas as pd
from core.types import TransformFn, ValidationResult, ValidationRule

T = TypeVar("T")
U = TypeVar("U")


def pipe(data: pd.DataFrame, *steps: TransformFn) -> pd.DataFrame:
    """
    Composição funcional para DataFrames: f_n(...f_2(f_1(data))).
    Executa cada função de transformação sequencialmente sem mutação in-place.
    """
    return reduce(lambda current_df, step_fn: step_fn(current_df), steps, data)


def compose(*functions: Callable[[Any], Any]) -> Callable[[Any], Any]:
    """Composição matemática tradicional: (f ∘ g)(x) = f(g(x))."""
    return reduce(lambda f, g: lambda x: f(g(x)), functions, lambda x: x)


def run_validation_suite(
    df: pd.DataFrame,
    rules: Sequence[ValidationRule],
) -> tuple[ValidationResult, ...]:
    """
    Executa uma suíte de validações de forma declarativa e pura,
    retornando uma tupla imutável de ValidationResult.
    """
    return tuple(rule(df) for rule in rules)


def split_qualify_and_anomalies(
    df_raw: pd.DataFrame,
    failed_indices: set[int | str],
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Bifurcação funcional pura entre dados conformes (Qualify) e anomalias (DEC-006).
    Retorna dois novos DataFrames sem modificar o original.
    """
    is_anomaly = df_raw.index.isin(failed_indices)
    df_qualify = df_raw.loc[~is_anomaly].copy()
    df_anomaly = df_raw.loc[is_anomaly].copy()
    return df_qualify, df_anomaly


def safe_assign(df: pd.DataFrame, **kwargs: Any) -> pd.DataFrame:
    """Atribuição pura de novas colunas retornando uma nova cópia do DataFrame."""
    return df.assign(**kwargs)


def dispatch_handler(
    key: str,
    dispatch_table: Mapping[str, Callable[[pd.DataFrame], pd.DataFrame]],
    default_handler: Callable[[pd.DataFrame], pd.DataFrame] = lambda df: df,
) -> Callable[[pd.DataFrame], pd.DataFrame]:
    """Retorna o handler funcional a partir de uma tabela de despacho declarativa."""
    return dispatch_table.get(key, default_handler)
