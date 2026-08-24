"""
Orquestrador Consolidado de Gráficos de Insights de Negócio.
Executa sequencialmente cada gerador de módulo em presentation/insights/ organizado por categorias:
- 01_descriptive/ (Descritivos: BI de Recuperação, Motivos de Abandono, Custo por Recuperação & ROI)
- 02_risk/ (Diagnóstico de Risco: Matriz RFM de Abandono)
- 03_prescriptive/ (Prescritivos: Estratégia de Resgate por Canal, Otimização de Timing & Decaimento)
"""

from typing import Final, List
import os
import sys
import subprocess

INSIGHTS_ROOT: Final[str] = os.path.dirname(__file__)
BASE_DIR: Final[str] = os.path.abspath(os.path.join(INSIGHTS_ROOT, "..", ".."))

# Lista ordenada de scripts de geração por categoria
SCRIPTS: Final[List[str]] = [
    # 01_descriptive
    os.path.join("01_descriptive", "01_bi_recuperacao_carrinhos", "generate_chart.py"),
    os.path.join("01_descriptive", "01_bi_recuperacao_carrinhos", "generate_chart_sinuous_1week.py"),
    os.path.join("01_descriptive", "01_bi_recuperacao_carrinhos", "generate_mini_tables.py"),
    os.path.join("01_descriptive", "02_motivos_abandono", "generate_chart.py"),
    os.path.join("01_descriptive", "03_custo_recuperacao_roi", "generate_chart.py"),
    
    # 02_risk
    os.path.join("02_risk", "01_segmentacao_risco", "generate_chart.py"),
    
    # 03_prescriptive
    os.path.join("03_prescriptive", "01_estrategia_resgate_segmento", "generate_chart.py"),
    os.path.join("03_prescriptive", "02_otimizacao_timing_envio", "generate_chart.py")
]

def main() -> None:
    print("=" * 80)
    print(" INICIANDO GERAÇÃO DE GRÁFICOS DE INSIGHTS CATEGORIZADOS (PRESENTATION/INSIGHTS)")
    print("=" * 80)
    
    success_count = 0
    total_count = len(SCRIPTS)
    
    for rel_path in SCRIPTS:
        full_path = os.path.join(INSIGHTS_ROOT, rel_path)
        norm_rel = rel_path.replace("\\", "/")
        print(f"\n[INSIGHTS] Executando: {norm_rel}...")
        
        if not os.path.exists(full_path):
            print(f"[ERRO] Script não encontrado: {full_path}", file=sys.stderr)
            continue
            
        result = subprocess.run([sys.executable, full_path], cwd=BASE_DIR, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"[SUCCESS] {norm_rel}: Artefato gerado com sucesso!")
            if result.stdout.strip():
                for line in result.stdout.strip().splitlines():
                    print(f"          {line}")
            success_count += 1
        else:
            print(f"[FALHA] Erro ao executar {norm_rel}:", file=sys.stderr)
            print(result.stderr, file=sys.stderr)
            
    print("\n" + "=" * 80)
    print(f" FINALIZADO: {success_count}/{total_count} scripts de insights executados com sucesso.")
    print("=" * 80)

if __name__ == "__main__":
    main()
