#!/usr/bin/env python
"""
Task Runner / Makefile em Python Puro para o Case Dadosfera
Compatível com Windows, Linux e macOS.

Uso:
    python make.py notebook-gen           -> Gera todos os gráficos e imagens de BI
    python make.py chart [nome]          -> Gera um gráfico específico por chave string
    python make.py list-charts           -> Lista todos os gráficos disponíveis
    python make.py mock-gen              -> Executa a geração dos datasets sintéticos (115k+)
    python make.py quality-eval          -> Executa a suite de Data Quality do Item 4
    python make.py help                  -> Exibe este menu de ajuda
"""

import sys
import os
import argparse
import subprocess

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

def task_notebook_gen(chart_name: str | None = None) -> None:
    """Gera os artefatos de gráficos e views de BI."""
    script_path = os.path.join(BASE_DIR, "notebooks", "pipelines", "serving", "generate_bi_charts.py")
    cmd = [sys.executable, script_path]
    
    if chart_name:
        cmd.extend(["--chart", chart_name])
    else:
        cmd.append("--all")
        
    print(f"\n[TASK: notebook-gen] Executando gerador de imagens de BI...")
    res = subprocess.run(cmd, cwd=BASE_DIR)
    if res.returncode == 0:
        print("[TASK: notebook-gen] Imagens geradas com sucesso em dashboards/assets/ e docs/assets/charts/!\n")
    else:
        print("[ERRO] Falha na geracao das imagens.", file=sys.stderr)
        sys.exit(res.returncode)

def task_list_charts() -> None:
    """Lista as especificações de gráficos disponíveis."""
    script_path = os.path.join(BASE_DIR, "notebooks", "pipelines", "serving", "generate_bi_charts.py")
    subprocess.run([sys.executable, script_path, "--list"], cwd=BASE_DIR)

def task_mock_gen(profile: str = "standard") -> None:
    """Executa a geração modular de datasets sintéticos."""
    script_path = os.path.join(BASE_DIR, "data", "mock", "generators", "parquet", "run_all.py")
    cmd = [sys.executable, script_path, "--profile", profile]
    print(f"\n[TASK: mock-gen] Gerando base sintetica (Perfil: {profile})...")
    subprocess.run(cmd, cwd=BASE_DIR)

def task_quality_eval() -> None:
    """Executa a validação e relatório de Data Quality."""
    script_path = os.path.join(BASE_DIR, "notebooks", "pipelines", "quality_report", "run_quality_pipeline.py")
    print("\n[TASK: quality-eval] Executando pipeline de Data Quality & Anomalias...")
    subprocess.run([sys.executable, script_path], cwd=BASE_DIR)
    print("[TASK: quality-eval] Relatório e imagens gerados em: notebooks/pipelines/quality_report/outputs/\n")

def print_help() -> None:
    print("""
=============================================================================
🛠️  MAKEFILE EM PYTHON - CASE RECUPERAÇÃO DE CARRINHO (DADOSFERA)
=============================================================================
Comandos disponíveis:

  python make.py notebook-gen               Gera todas as 6 imagens de BI
  python make.py notebook-gen [CHART]       Gera apenas o gráfico especificado
  python make.py chart [CHART]              Atalho para gerar um gráfico específico
  python make.py list-charts                Lista todos os IDs e chaves de gráficos
  python make.py mock-gen                   Gera os 115k+ registros sintéticos
  python make.py quality-eval               Executa a suíte de Data Quality (Item 4)
  python make.py help                       Exibe este menu de ajuda

Atalhos diretos no Windows CLI:
  .\\notebook-gen                            (executa notebook-gen diretamente)
  .\\notebook-gen categories                 (gera gráfico específico)
  .\\make notebook-gen                       (executa via wrapper make)
=============================================================================
""")

def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("help", "-h", "--help"):
        print_help()
        return

    command = sys.argv[1].lower().replace("-", "_")
    arg = sys.argv[2] if len(sys.argv) > 2 else None

    if command in ("notebook_gen", "notebookgen", "charts"):
        task_notebook_gen(arg)
    elif command in ("chart", "view"):
        if not arg:
            print("[ERRO] Especifique o nome do chart (ex: python make.py chart time_series)")
            task_list_charts()
            sys.exit(1)
        task_notebook_gen(arg)
    elif command in ("list_charts", "list", "catalog"):
        task_list_charts()
    elif command in ("mock_gen", "mock", "datagen"):
        task_mock_gen(arg or "standard")
    elif command in ("quality_eval", "quality", "dq"):
        task_quality_eval()
    else:
        print(f"[ERRO] Comando desconhecido: '{sys.argv[1]}'")
        print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
