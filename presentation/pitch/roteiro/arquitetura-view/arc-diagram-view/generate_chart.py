#!/usr/bin/env python3
"""
generate_chart.py — Wrapper de Importação da View de Diagrama de Arquitetura (arc-diagram-view)

Importa e executa o script central `generate_l2r_charts.py`, garantindo que todos os
diagramas L2R (Legado AWS DIY vs Dadosfera) sejam gerados e persistidos nesta view.
"""

from pathlib import Path
import sys
import shutil

# Forçar encoding UTF-8 no Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Diretórios
CURRENT_DIR = Path(__file__).resolve().parent
PARENT_DIR = CURRENT_DIR.parent
ASSETS_DIR = CURRENT_DIR / "assets"
ASSETS_DIR.mkdir(parents=True, exist_ok=True)

# Adiciona o diretório pai no path para importar o módulo original
if str(PARENT_DIR) not in sys.path:
    sys.path.insert(0, str(PARENT_DIR))

import generate_l2r_charts  # Importa o script original

def main():
    print("=" * 80)
    print(" [ARC-DIAGRAM-VIEW] EXECUTANDO GERADOR CENTRAL DE ARQUITETURA L2R...")
    print("=" * 80)
    
    # Executa o pipeline original de geração
    generate_l2r_charts.main()
    
    # Sincroniza os artefatos gerados para o diretório desta view
    parent_assets = PARENT_DIR / "assets"
    diagram_files = [
        "grafico-dadosfera-l2r.png",
        "grafico-legado-l2r.png",
        "grafico-legado-l2r-vazio.png",
        "grafico-dadosfera-l2r-vazio.png",
        "grafico-legado-l2r-populated.png"
    ]
    
    for filename in diagram_files:
        src = parent_assets / filename
        if src.exists():
            dst_local = CURRENT_DIR / filename
            dst_asset = ASSETS_DIR / filename
            shutil.copy2(src, dst_local)
            shutil.copy2(src, dst_asset)
            print(f"  [OK] Diagrama sincronizado em arc-diagram-view: {filename}")
            
    print("\n✅ [SUCCESS] Diagramas de arquitetura L2R gerados e sincronizados com sucesso!")

if __name__ == "__main__":
    main()
