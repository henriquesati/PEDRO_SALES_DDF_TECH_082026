#!/usr/bin/env python3
"""
master_generate_all_charts.py
Varre e executa todos os geradores de gráficos do projeto, garantindo que
100% dos artefatos visuais estejam atualizados e persistidos no workspace.
"""

import os
import sys
import runpy
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

SCRIPTS = [
    # Pitch & Arquitetura
    "presentation/pitch/roteiro/arquitetura-view/generate_l2r_charts.py",
    "presentation/pitch/views/caseitem06/generate_chart.py",
    "presentation/pitch/06_data_quality_e_quarentena/generate_chart.py",
    "presentation/pitch/07_arquitetura_dadosfera_vs_aws/generate_chart.py",
    "presentation/pitch/08_data_app_simulador_prescritivo_genai/generate_chart.py",
    
    # 01_descriptive
    "presentation/insights/01_descriptive/01_bi_recuperacao_carrinhos/generate_chart.py",
    "presentation/insights/01_descriptive/01_bi_recuperacao_carrinhos/generate_chart_sinuous_1week.py",
    "presentation/insights/01_descriptive/01_bi_recuperacao_carrinhos/generate_mini_tables.py",
    "presentation/insights/01_descriptive/02_motivos_abandono/generate_chart.py",
    "presentation/insights/01_descriptive/03_custo_recuperacao_roi/generate_chart.py",
    
    # 02_risk
    "presentation/insights/02_risk/01_segmentacao_risco/generate_chart.py",
    "presentation/insights/02_risk/02_ltv_vs_abandono/generate_chart.py",
    "presentation/insights/02_risk/03_viabilidade_recuperacao_carrinho/generate_chart.py",
    
    # 03_prescriptive
    "presentation/insights/03_prescriptive/01_estrategia_resgate_segmento/generate_chart.py",
    "presentation/insights/03_prescriptive/02_otimizacao_timing_envio/generate_chart.py",
    "presentation/insights/03_prescriptive/03_produtos_mais_abandonados/generate_chart.py",
    "presentation/insights/03_prescriptive/04_roi_campanhas_resgate/generate_chart.py",
    
    # Pipelines
    "pipelines/case-item-06/scripts/generate_chart.py",
    "pipelines/case-item-07/scripts/run_bi_analysis.py",
]

def main():
    print("=" * 80)
    print(" EXECUTANDO GERACAO CONSOLIDADA DE TODOS OS GRAFICOS DO WORKSPACE")
    print("=" * 80)
    
    success = 0
    errors = 0
    
    for rel_path in SCRIPTS:
        full_path = BASE_DIR / rel_path
        print(f"\n[RUNNING] {rel_path}...")
        if not full_path.exists():
            print(f"  [WARN] Arquivo nao encontrado: {full_path}")
            errors += 1
            continue
        try:
            # Executa o script no seu próprio contexto mantendo BASE_DIR no sys.path
            sys.path.insert(0, str(full_path.parent))
            sys.path.insert(0, str(BASE_DIR))
            runpy.run_path(str(full_path), run_name="__main__")
            print(f"  [OK] Sucesso: {rel_path}")
            success += 1
        except Exception as e:
            print(f"  [ERRO] Falha ao executar {rel_path}: {e}")
            errors += 1
            
    print("\n" + "=" * 80)
    print(f" CONCLUIDO! Sucesso: {success}/{len(SCRIPTS)} | Erros/Avisos: {errors}")
    print("=" * 80)

if __name__ == "__main__":
    main()
