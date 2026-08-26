#!/usr/bin/env python3
"""
generate_chart.py
Módulo: presentation/pitch/roteiro/views-05-insights-ia/feature-importance-ml
Função: Importa e executa o gerador canônico de Feature Importance e Pesos do Modelo de ML a partir da raiz de insights.
Origem Canônica: insights/04_intelligence_ai/05_feature_importance_ml/generate_chart.py
"""

from typing import Final
import os
import sys
import importlib.util
from pathlib import Path

def get_base_dir() -> Path:
    curr = Path(__file__).resolve().parent
    while curr and curr.parent != curr:
        if (curr / "data" / "mock").exists():
            return curr
        curr = curr.parent
    return Path(__file__).resolve().parents[5]

BASE_DIR: Final[Path] = get_base_dir()
OUTPUT_IMAGE_PATH: Final[Path] = Path(__file__).resolve().parent / "chart_feature_importance_ml.png"
CANONICAL_SCRIPT_PATH: Final[Path] = (
    BASE_DIR / "insights" / "04_intelligence_ai" / "05_feature_importance_ml" / "generate_chart.py"
)

def load_canonical_module():
    spec = importlib.util.spec_from_file_location("canonical_feature_importance_chart", str(CANONICAL_SCRIPT_PATH))
    if spec is None or spec.loader is None:
        raise ImportError(f"Não foi possível carregar o módulo canônico em: {CANONICAL_SCRIPT_PATH}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def main() -> None:
    canonical_mod = load_canonical_module()
    saved_path = canonical_mod.generate_and_save(OUTPUT_IMAGE_PATH)
    print(f"[SUCCESS] Gráfico importado e gerado na view do roteiro a partir da raiz: {saved_path}")

if __name__ == "__main__":
    main()
