#!/usr/bin/env python3
"""
generate_chart.py (Wrapper do Roteiro - Padrão DRY)
Módulo: views-04-insights/descritivos/motivosabandono

Diretriz Arquitetural:
Este script NÃO implementa lógica própria de visualização.
Ele importa e executa estritamente o gerador canônico oficial da camada técnica:
`insights/01_descriptive/02_motivos_abandono/generate_chart.py`
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
CANONICAL_SCRIPT_PATH = BASE_DIR / "insights" / "01_descriptive/02_motivos_abandono/generate_chart.py"

def load_canonical_module():
    spec = importlib.util.spec_from_file_location("canonical_motivos_abandono", CANONICAL_SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise ImportError(f"Não foi possível carregar o módulo canônico em: {CANONICAL_SCRIPT_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def main() -> None:
    """Executa a rotina canônica unificada de geração e sincronização."""
    print("[WRAPPER] Acionando o gerador canônico: insights/01_descriptive/02_motivos_abandono/generate_chart.py...")
    canonical_module = load_canonical_module()
    canonical_module.main()

if __name__ == "__main__":
    main()
