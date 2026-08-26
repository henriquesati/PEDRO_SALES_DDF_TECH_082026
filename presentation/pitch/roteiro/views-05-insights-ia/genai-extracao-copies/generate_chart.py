#!/usr/bin/env python3
"""
generate_chart.py (Wrapper do Roteiro - Padrão DRY)
Módulo: views-05-insights-ia/genai-extracao-copies

Diretriz Arquitetural:
Este script importa e executa estritamente o gerador canônico oficial da camada técnica:
`insights/04_intelligence_ai/02_genai_extracao_copies/generate_chart.py`
"""

import sys
import importlib.util
from pathlib import Path

def get_base_dir() -> Path:
    curr = Path(__file__).resolve().parent
    while curr and curr.parent != curr:
        if (curr / "data" / "mock").exists():
            return curr
        curr = curr.parent
    return Path.cwd().resolve()

BASE_DIR = get_base_dir()
OUTPUT_IMAGE_PATH = Path(__file__).resolve().parent / "chart_genai_extracao_copies.png"
CANONICAL_SCRIPT_PATH = BASE_DIR / "insights" / "04_intelligence_ai" / "02_genai_extracao_copies" / "generate_chart.py"

def load_canonical_module():
    spec = importlib.util.spec_from_file_location("canonical_genai_copies", str(CANONICAL_SCRIPT_PATH))
    if spec is None or spec.loader is None:
        raise ImportError(f"Não foi possível carregar o módulo canônico em: {CANONICAL_SCRIPT_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def main() -> None:
    """Executa a rotina canônica unificada de geração e sincronização."""
    print(f"[WRAPPER] Acionando o gerador canônico: {CANONICAL_SCRIPT_PATH}...")
    canonical_module = load_canonical_module()
    saved_path = canonical_module.generate_and_save(OUTPUT_IMAGE_PATH)
    print(f"[SUCCESS] Gráfico executivo salvo com sucesso em: {saved_path}")

if __name__ == "__main__":
    main()
