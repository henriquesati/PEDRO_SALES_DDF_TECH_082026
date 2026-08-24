"""
Motor Declarativo de Injeção e Garantia de Anomalias (Dirty Data Engine).

Garante cotas declarativas com distribuições estatísticas naturais (percentuais quebrados)
em cada dataset gerado, registrando um relatório auditável de anomalias injetadas.
"""
from typing import Dict, List, Any, Optional, Set
import math
import numpy as np
import pandas as pd


class AnomalyAudit:
    """Registrador de auditoria de anomalias injetadas por entidade."""

    def __init__(self, entity_name: str):
        self.entity_name = entity_name
        self.records: List[Dict[str, Any]] = []

    def record(self, anomaly_name: str, target_min_pct: float, affected_rows: int, total_rows: int, description: str):
        actual_pct = (affected_rows / total_rows * 100.0) if total_rows > 0 else 0.0
        self.records.append({
            'entity': self.entity_name,
            'anomaly': anomaly_name,
            'target_min_pct': target_min_pct * 100.0,
            'affected_rows': affected_rows,
            'total_rows': total_rows,
            'actual_pct': actual_pct,
            'description': description,
        })

    def to_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame(self.records)


class AnomalyEngine:
    """Motor de seleção determinística e aplicação de anomalias com garantia de cotas."""

    @staticmethod
    def get_guaranteed_indices(
        total_rows: int,
        target_pct: float,
        seed: Optional[int] = None,
        exclude_indices: Optional[Set[int]] = None
    ) -> np.ndarray:
        """
        Garante a seleção de índices baseados no target_pct quebrado.
        
        Args:
            total_rows: Número total de linhas disponíveis.
            target_pct: Percentual desejado (ex: 0.0487 para 4.87%).
            seed: Seed opcional para reprodutibilidade.
            exclude_indices: Conjunto de índices que não devem ser selecionados.
            
        Returns:
            np.ndarray de índices selecionados garantindo a cota.
        """
        if total_rows <= 0 or target_pct <= 0:
            return np.array([], dtype=int)

        available_indices = np.arange(total_rows)
        if exclude_indices:
            mask = ~np.isin(available_indices, list(exclude_indices))
            available_indices = available_indices[mask]

        if len(available_indices) == 0:
            return np.array([], dtype=int)

        required_count = max(1, int(round(total_rows * target_pct)))
        actual_count = min(required_count, len(available_indices))

        rng = np.random.default_rng(seed)
        selected = rng.choice(available_indices, size=actual_count, replace=False)
        return selected
