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
    # Pitch & Arquitetura & Roteiro Views
    "presentation/pitch/roteiro/arquitetura-view/arc-diagram-view/generate_chart.py",
    "presentation/pitch/roteiro/problema-elasticidade/generate_chart.py",
    "presentation/pitch/roteiro/staff-pain-point/generate_chart.py",
    "presentation/pitch/roteiro/staff-pain-point/generate_cost_comparison_chart.py",
    "presentation/pitch/roteiro/view-03-dado-qualidades/view-lake-architecture/generate_chart.py",
    "presentation/pitch/roteiro/view-03-dado-qualidades/view-governanca/generate_chart.py",
    
    # 01_descriptive (Camada Canônica)
    "insights/01_descriptive/01_bi_recuperacao_carrinhos/generate_chart.py",
    "insights/01_descriptive/01_bi_recuperacao_carrinhos/generate_chart_sinuous_1week.py",
    "insights/01_descriptive/01_bi_recuperacao_carrinhos/generate_mini_tables.py",
    "insights/01_descriptive/02_motivos_abandono/generate_chart.py",
    "insights/01_descriptive/03_custo_recuperacao_roi/generate_chart.py",
    
    # 02_risk (Camada Canônica)
    "insights/02_risk/01_segmentacao_risco/generate_chart.py",
    "insights/02_risk/02_ltv_vs_abandono/generate_chart.py",
    "insights/02_risk/03_viabilidade_recuperacao_carrinho/generate_chart.py",
    
    # 03_prescriptive (Camada Canônica)
    "insights/03_prescriptive/01_estrategia_resgate_segmento/generate_chart.py",
    "insights/03_prescriptive/02_otimizacao_timing_envio/generate_chart.py",
    "insights/03_prescriptive/03_produtos_mais_abandonados/generate_chart.py",
    "insights/03_prescriptive/04_roi_campanhas_resgate/generate_chart.py",
    
    # 04_intelligence_ai (Camada Canônica)
    "insights/04_intelligence_ai/generate_chart.py",
    "insights/04_intelligence_ai/01_modelos_preditivos_ml/generate_chart.py",
    "insights/04_intelligence_ai/02_genai_extracao_copies/generate_chart.py",
    "insights/04_intelligence_ai/03_similaridade_produtos/generate_chart.py",
    "insights/04_intelligence_ai/04_data_app_simulador_roi/generate_chart.py",

    # Roteiro Views Wrappers (Validação de Acoplamento DRY)
    "presentation/pitch/roteiro/views-04-insights/descritivos/funilrecuperacao/generate_chart.py",
    "presentation/pitch/roteiro/views-04-insights/descritivos/motivosabandono/generate_chart.py",
    "presentation/pitch/roteiro/views-04-insights/descritivos/custorecuperacao/generate_chart.py",
    "presentation/pitch/roteiro/views-04-insights/prescritivos/timingenvio/generate_chart.py",
    "presentation/pitch/roteiro/views-04-insights/prescritivos/estrategiaresgate/generate_chart.py",
    "presentation/pitch/roteiro/views-04-insights/prescritivos/produtosabandonados/generate_chart.py",
    "presentation/pitch/roteiro/views-04-insights/prescritivos/roicampanhas/generate_chart.py",
    "presentation/pitch/roteiro/views-05-insights-ia/generate_chart.py",
]

def main():
    print("=" * 80)
    print(" EXECUTANDO GERAÇÃO CONSOLIDADA DE TODOS OS GRÁFICOS DO WORKSPACE")
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
