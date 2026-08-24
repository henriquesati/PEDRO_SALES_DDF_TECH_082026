"""
Snowpark / PySpark Compatible Transformation Engine (Item 8 Bônus - Dadosfera)
Demonstra a equivalência declarativa entre a API do Snowpark Python (Snowflake In-Database)
e o processamento funcional de DataFrames.
"""

from typing import Any, Final
import pandas as pd
import numpy as np


class SnowparkDataFrameSimulator:
    """
    Simulador funcional que espelha rigorosamente a API de DataFrame do Snowpark Python
    e do Apache PySpark (df.filter, df.with_column, df.group_by, df.agg, df.join),
    permitindo execução local idêntica à que roda nos Virtual Warehouses do Snowflake.
    """

    def __init__(self, data: pd.DataFrame):
        self._df = data.copy()

    @property
    def raw_data(self) -> pd.DataFrame:
        """Retorna uma cópia imutável dos dados subjacentes."""
        return self._df.copy()

    def count(self) -> int:
        return len(self._df)

    def filter(self, condition: Any) -> "SnowparkDataFrameSimulator":
        """Equivalente a df.filter(col('status') == 'abandonado')."""
        if callable(condition):
            mask = condition(self._df)
        elif isinstance(condition, str):
            mask = self._df.eval(condition)
        else:
            mask = condition
        return SnowparkDataFrameSimulator(self._df.loc[mask].copy())

    def with_column(self, col_name: str, expression: Any) -> "SnowparkDataFrameSimulator":
        """Equivalente a df.withColumn('gmv_em_risco', col('valor_subtotal') + col('valor_frete'))."""
        new_df = self._df.copy()
        if callable(expression):
            new_df[col_name] = expression(new_df)
        else:
            new_df[col_name] = expression
        return SnowparkDataFrameSimulator(new_df)

    def select(self, *cols: str) -> "SnowparkDataFrameSimulator":
        """Equivalente a df.select('carrinho_id', 'cliente_id', 'valor_total')."""
        existing_cols = [c for c in cols if c in self._df.columns]
        return SnowparkDataFrameSimulator(self._df[existing_cols].copy())

    def group_by(self, *group_cols: str) -> "SnowparkGroupedDataSimulator":
        """Equivalente a df.groupBy('motivo_abandono')."""
        return SnowparkGroupedDataSimulator(self._df, list(group_cols))

    def join(
        self,
        other: "SnowparkDataFrameSimulator",
        on: str | list[str],
        how: str = "inner",
    ) -> "SnowparkDataFrameSimulator":
        """Equivalente a df.join(df_clientes, on='cliente_id', how='left')."""
        merged = self._df.merge(other._df, on=on, how=how)
        return SnowparkDataFrameSimulator(merged)

    def to_pandas(self) -> pd.DataFrame:
        """Equivalente a df.to_pandas() do Snowpark."""
        return self._df.copy()


class SnowparkGroupedDataSimulator:
    """Simulador de agregações agrupadas do Snowpark/PySpark."""

    def __init__(self, df: pd.DataFrame, group_cols: list[str]):
        self._df = df
        self._group_cols = group_cols

    def agg(self, agg_dict: dict[str, str | tuple[str, str]]) -> SnowparkDataFrameSimulator:
        """
        Equivalente a df.groupBy('canal').agg(count('id').alias('total'), sum('rec').alias('rec_tot')).
        """
        # Suporta mapeamento simples de agregações pandas
        pandas_agg = {}
        for col_alias, col_expr in agg_dict.items():
            if isinstance(col_expr, tuple):
                col, func = col_expr
                pandas_agg[col_alias] = (col, func)
            else:
                pandas_agg[col_alias] = (col_alias, col_expr)

        grouped = self._df.groupby(self._group_cols).agg(**pandas_agg).reset_index()
        return SnowparkDataFrameSimulator(grouped)


# =============================================================================
# 🚀 Snowpark Pipeline Logic (Declarative Pure Function)
# =============================================================================

def run_snowpark_abandonment_transformation(
    raw_carrinhos_df: pd.DataFrame,
    raw_clientes_df: pd.DataFrame,
) -> SnowparkDataFrameSimulator:
    """
    Executa o pipeline de transformação de carrinhos abandonados utilizando a sintaxe
    estrita da API do Snowpark Python. Na Dadosfera, este código roda diretamente
    no Virtual Warehouse do Snowflake sem movimentação de dados.
    """
    # 1. Converte para abstração de DataFrame Snowpark
    df_carrinhos = SnowparkDataFrameSimulator(raw_carrinhos_df)
    df_clientes = SnowparkDataFrameSimulator(raw_clientes_df)

    # 2. Filtragem de carrinhos abandonados (Pushdown predicate)
    df_abandonados = df_carrinhos.filter(lambda df: df["status"].isin(["abandonado", "expirado"]))

    # 3. Enriquecimento de colunas (withColumn)
    df_enriquecido = (
        df_abandonados
        .with_column("ticket_liquido_em_risco", lambda df: df["valor_subtotal"] - df["valor_desconto"])
        .with_column("flag_alto_valor", lambda df: df["valor_total"] > 1000.0)
    )

    # 4. JOIN com dimensão de clientes
    df_consolidado = df_enriquecido.join(
        df_clientes.select("cliente_id", "email", "segmento_rfm", "churn_risk_score"),
        on="cliente_id",
        how="left",
    )

    return df_consolidado
