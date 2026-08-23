"""
Orquestrador central de geração de todos os gráficos e painéis visuais do Pitch.
Executa os geradores de cada uma das 8 áreas temáticas do pitch.
"""

from typing import Final, Sequence
import os
import sys
import subprocess

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

PITCH_DIR: Final[str] = os.path.abspath(os.path.dirname(__file__))
BASE_DIR: Final[str] = os.path.abspath(os.path.join(PITCH_DIR, "..", ".."))

MODULES: Final[Sequence[str]] = (
    "01_abandono_vs_recuperacao_timeline",
    "02_performance_categorias_produtos",
    "03_roi_canais_e_comunicacao",
    "04_matriz_motivos_segmentos_rfm",
    "05_matriz_viabilidade_recuperacao",
    "06_data_quality_e_quarentena",
    "07_arquitetura_dadosfera_vs_aws",
    "08_data_app_simulador_prescritivo_genai",
)

def run_module(module_name: str) -> bool:
    """Executa o script generate_chart.py de um módulo específico."""
    script_path = os.path.join(PITCH_DIR, module_name, "generate_chart.py")
    if not os.path.exists(script_path):
        print(f"[ERRO] Script nao encontrado: {script_path}")
        return False
        
    print(f"-> Executando gerador em: {module_name}...")
    res = subprocess.run([sys.executable, script_path], cwd=BASE_DIR)
    return res.returncode == 0

def main() -> None:
    print("\n" + "="*75)
    print("[PITCH] GERADOR CONSOLIDADO DE GRAFICOS DO PITCH (DADOSFERA)")
    print("="*75)
    
    success_count = 0
    for mod in MODULES:
        ok = run_module(mod)
        if ok:
            success_count += 1
        else:
            print(f"[ALERTA] Falha ao processar modulo: {mod}")
            
    print("="*75)
    print(f"[PITCH] Concluido: {success_count}/{len(MODULES)} graficos gerados com sucesso!")
    print("Arquivos salvos em seus respectivos subdiretorios em presentation/pitch/\n")

if __name__ == "__main__":
    main()
