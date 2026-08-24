"""
Classe Base Declarativa para Geradores de Dados Mock — Cart Recovery.
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from pathlib import Path
import pandas as pd
import numpy as np

try:
    from config.settings import GeneratorSettings
    from core.anomaly_engine import AnomalyAudit, AnomalyEngine
except (ImportError, ValueError):
    from ..config.settings import GeneratorSettings
    from .anomaly_engine import AnomalyAudit, AnomalyEngine


class BaseGenerator(ABC):
    """Classe base abstrata para todos os geradores de entidades."""

    name: str = "base_entity"
    dependencies: List[str] = []

    def __init__(self, settings: GeneratorSettings):
        self.settings = settings
        self.seed = settings.seed
        self.audit = AnomalyAudit(self.name)
        self.engine = AnomalyEngine()

    @abstractmethod
    def generate_raw(self, **context) -> pd.DataFrame:
        """Gera o DataFrame base com dados sintéticos aderentes ao domínio."""
        pass

    def apply_anomalies(self, df: pd.DataFrame) -> pd.DataFrame:
        """Aplica perturbações e anomalias de negócio garantindo cotas mínimas."""
        return df

    def validate_schema(self, df: pd.DataFrame) -> bool:
        """Valida que colunas obrigatórias existem e tipos mínimos estão presentes."""
        return len(df) > 0

    def clean_internal_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Remove colunas de controle interno (prefixadas por _) antes de salvar."""
        cols_to_drop = [c for c in df.columns if c.startswith('_')]
        return df.drop(columns=cols_to_drop) if cols_to_drop else df

    def run(self, **context) -> pd.DataFrame:
        """Ciclo de execução completo: generate -> apply_anomalies -> validate."""
        np.random.seed(self.seed)
        df = self.generate_raw(**context)
        df = self.apply_anomalies(df)
        self.validate_schema(df)
        return df

    def save(self, df: pd.DataFrame, parquet_dir: Optional[Path] = None, csv_dir: Optional[Path] = None) -> Dict[str, Path]:
        """Exporta o DataFrame para Parquet e CSV nos diretórios configurados."""
        parquet_dir = parquet_dir or self.settings.parquet_dir
        csv_dir = csv_dir or self.settings.csv_dir

        parquet_dir.mkdir(parents=True, exist_ok=True)
        csv_dir.mkdir(parents=True, exist_ok=True)

        clean_df = self.clean_internal_columns(df)

        parquet_path = parquet_dir / f"{self.name}.parquet"
        csv_path = csv_dir / f"{self.name}.csv"

        clean_df.to_parquet(parquet_path, index=False, engine='pyarrow')
        clean_df.to_csv(csv_path, index=False, encoding='utf-8')

        return {'parquet': parquet_path, 'csv': csv_path}
