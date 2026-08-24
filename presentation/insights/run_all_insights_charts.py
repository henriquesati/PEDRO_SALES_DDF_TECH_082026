"""
Orquestrador central de execução de todos os gráficos de Insights.
Executa sequencialmente cada gerador de módulo em presentation/insights/.
"""

import os
import sys
import subprocess

INSIGHTS_DIR: str = os.path.dirname(os.path.abspath(__file__))

MODULE_GENERATORS: list[str] = [
    os.path.join(INSIGHTS_DIR, "01_bi_recuperacao_carrinhos", "generate_chart.py"),
    os.path.join(INSIGHTS_DIR, "01_bi_recuperacao_carrinhos", "generate_chart_sinuous_1week.py"),
    os.path.join(INSIGHTS_DIR, "01_bi_recuperacao_carrinhos", "generate_mini_tables.py"),
    os.path.join(INSIGHTS_DIR, "02_motivos_abandono", "generate_chart.py"),
    os.path.join(INSIGHTS_DIR, "03_segmentacao_risco", "generate_chart.py"),
    os.path.join(INSIGHTS_DIR, "04_estrategia_resgate_segmento", "generate_chart.py"),
    os.path.join(INSIGHTS_DIR, "05_otimizacao_timing_envio", "generate_chart.py"),
]

def run_all_generators() -> int:
    """Executa todos os scripts geradores de gráficos de insights."""
    print("================================================================================")
    print(" INICIANDO GERAÇÃO DE GRÁFICOS DE INSIGHTS (PRESENTATION/INSIGHTS)")
    print("================================================================================")
    
    success_count = 0
    total_count = len(MODULE_GENERATORS)
    
    for script_path in MODULE_GENERATORS:
        module_name = os.path.basename(os.path.dirname(script_path))
        script_file = os.path.basename(script_path)
        print(f"\n[INSIGHTS] Executando: {module_name}/{script_file}...")
        
        result = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"[SUCCESS] {module_name}/{script_file}: Artefato gerado com sucesso!")
            if result.stdout:
                print(f"          {result.stdout.strip()}")
            success_count += 1
        else:
            print(f"[ERROR] {module_name}/{script_file}: Falha na geração!")
            print(result.stderr)
            
    print("\n================================================================================")
    print(f" FINALIZADO: {success_count}/{total_count} scripts de insights executados com sucesso.")
    print("================================================================================")
    
    return 0 if success_count == total_count else 1

if __name__ == "__main__":
    sys.exit(run_all_generators())
