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

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

def task_notebook_gen(chart_name: str | None = None) -> None:
    """Gera os artefatos de gráficos e views analíticas de insights e BI."""
    script_path = os.path.join(BASE_DIR, "presentation", "insights", "run_all_insights_charts.py")
    print(f"\n[TASK: notebook-gen] Executando gerador de imagens de BI e Insights...")
    res = subprocess.run([sys.executable, script_path], cwd=BASE_DIR)
    if res.returncode == 0:
        print("[TASK: notebook-gen] Imagens geradas com sucesso em insights/!\n")
    else:
        print("[ERRO] Falha na geração das imagens.", file=sys.stderr)
        sys.exit(res.returncode)

def task_list_charts() -> None:
    """Lista as categorias e módulos de gráficos de insights disponíveis."""
    print("""
📊 Catálogo de Gráficos de Insights Disponíveis:
  - 01_descriptive/ (BI de Recuperação, Motivos de Abandono, Custo & ROI)
  - 02_risk/ (Segmentação de Risco, LTV vs Abandono, Viabilidade de Recuperação)
  - 03_prescriptive/ (Estratégia de Resgate, Otimização de Timing, Produtos Abandonados, ROI de Campanhas)
""")

def task_mock_gen(profile: str = "standard") -> None:
    """Executa a geração modular de datasets sintéticos."""
    script_path = os.path.join(BASE_DIR, "data", "mock", "generators", "parquet", "run_all.py")
    cmd = [sys.executable, script_path, "--profile", profile]
    print(f"\n[TASK: mock-gen] Gerando base sintetica (Perfil: {profile})...")
    subprocess.run(cmd, cwd=BASE_DIR)

def task_quality_eval() -> None:
    """Executa a validação e relatório de Data Quality (Item 4)."""
    script_path = os.path.join(BASE_DIR, "pipelines", "case-item-04", "scripts", "run_quality_pipeline.py")
    print("\n[TASK: quality-eval] Executando pipeline de Data Quality & Anomalias (Item 4)...")
    subprocess.run([sys.executable, script_path], cwd=BASE_DIR)
    print("[TASK: quality-eval] Relatório e imagens gerados em: pipelines/case-item-04/outputs/\n")

def task_genai_extract() -> None:
    """Executa o pipeline de extração de features com GenAI & LLMs (Item 5)."""
    script_path = os.path.join(BASE_DIR, "pipelines", "case-item-05", "scripts", "run_genai_pipeline.py")
    print("\n[TASK: genai-extract] Executando pipeline de GenAI & LLMs (Item 5)...")
    subprocess.run([sys.executable, script_path], cwd=BASE_DIR)
    print("[TASK: genai-extract] Artefatos e relatório gerados em: pipelines/case-item-05/outputs/\n")

def task_pitch_charts() -> None:
    """Executa o orquestrador consolidado de gráficos do Pitch (Item 10)."""
    script_path = os.path.join(BASE_DIR, "presentation", "pitch", "run_all_pitch_charts.py")
    print("\n[TASK: pitch-charts] Gerando os gráficos e painéis visuais do Pitch...")
    subprocess.run([sys.executable, script_path], cwd=BASE_DIR)

def task_insights_charts() -> None:
    """Executa o orquestrador consolidado de gráficos de Insights."""
    script_path = os.path.join(BASE_DIR, "presentation", "insights", "run_all_insights_charts.py")
    print("\n[TASK: insights-charts] Gerando gráficos de Insights...")
    subprocess.run([sys.executable, script_path], cwd=BASE_DIR)

def task_push_read(commit_msg: str | None = None) -> None:
    """Faz commit e push exclusivamente do arquivo README.md."""
    msg = commit_msg or "docs: update README.md"
    readme_path = "README.md"
    
    print("\n[TASK: push-read] Adicionando exclusivamente o README.md ao staging...")
    res_add = subprocess.run(["git", "add", readme_path], cwd=BASE_DIR)
    if res_add.returncode != 0:
        print("[ERRO] Falha ao adicionar README.md ao git.", file=sys.stderr)
        sys.exit(res_add.returncode)

    print(f"[TASK: push-read] Criando commit: '{msg}'...")
    res_commit = subprocess.run(["git", "commit", "-m", msg], cwd=BASE_DIR)
    if res_commit.returncode != 0:
        print("[AVISO] Nenhuma alteração pendente no README.md para commitar.")
        return

    print("[TASK: push-read] Enviando alterações ao repositório remoto (git push)...")
    res_push = subprocess.run(["git", "push"], cwd=BASE_DIR)
    if res_push.returncode == 0:
        print("\n[OK] [TASK: push-read] README.md commitado e enviado com sucesso ao GitHub!\n")
    else:
        print("[ERRO] Falha no git push.", file=sys.stderr)
        sys.exit(res_push.returncode)

def task_data_app() -> None:
    """Inicia a aplicação interativa do Data App em Streamlit (Item 9 & Bônus)."""
    script_path = os.path.join(BASE_DIR, "pipelines", "case-item-09", "scripts", "run_app_locally.py")
    print("\n[TASK: data-app] Iniciando Data App Streamlit (Item 9 & Bônus)...")
    subprocess.run([sys.executable, script_path], cwd=BASE_DIR)

def task_data_app_assets() -> None:
    """Gera os gráficos e imagens em 300 DPI do Data App (Item 9)."""
    script_path = os.path.join(BASE_DIR, "pipelines", "case-item-09", "scripts", "export_app_assets.py")
    print("\n[TASK: data-app-assets] Gerando assets visuais do Data App...")
    subprocess.run([sys.executable, script_path], cwd=BASE_DIR)

def task_data_modeling() -> None:
    """Gera o dashboard e arquitetura da Modelagem Dimensional Kimball (Item 6)."""
    script_path = os.path.join(BASE_DIR, "pipelines", "case-item-06", "scripts", "generate_chart.py")
    print("\n[TASK: data-modeling] Gerando artefatos dimensionais Kimball (Item 6)...")
    subprocess.run([sys.executable, script_path], cwd=BASE_DIR)

def task_pipeline_run() -> None:
    """Executa o pipeline modular de dados e machine learning (Item 8)."""
    script_path = os.path.join(BASE_DIR, "pipelines", "case-item-08", "scripts", "run_silver_gold_pipeline.py")
    print("\n[TASK: pipeline-run] Executando pipeline Medallion, Stepsfera e ML (Item 8)...")
    subprocess.run([sys.executable, script_path], cwd=BASE_DIR)

def task_bi_analysis() -> None:
    """Executa a geração das visualizações de BI e métricas do Item 7."""
    script_path = os.path.join(BASE_DIR, "pipelines", "case-item-07", "scripts", "run_bi_analysis.py")
    print("\n[TASK: bi-analysis] Executando gerador de BI e métricas (Item 7)...")
    subprocess.run([sys.executable, script_path], cwd=BASE_DIR)

def print_help() -> None:
    print("""
=============================================================================
🛠️  MAKEFILE EM PYTHON - CASE RECUPERAÇÃO DE CARRINHO (DADOSFERA)
=============================================================================
Comandos disponíveis:

  python make.py data-app                   Inicia o Data App Streamlit (Item 9 & Bônus)
  python make.py data-app-assets            Gera as imagens em 300 DPI do Data App
  python make.py push-read [MSG]            Commita e envia EXCLUSIVAMENTE o README.md
  python make.py pipeline-run               Executa o pipeline modular & ML (Item 8)
  python make.py data-modeling              Gera a modelagem Kimball Gold DW (Item 6)
  python make.py bi-analysis                Gera as 6 visualizações e métricas de BI (Item 7)
  python make.py pitch-charts               Gera todos os 8 gráficos do Pitch (Item 10)
  python make.py insights-charts            Gera os gráficos de Insights (insights/)
  python make.py notebook-gen               Gera todas as 6 imagens de BI (Item 7)
  python make.py notebook-gen [CHART]       Gera apenas o gráfico especificado
  python make.py chart [CHART]              Atalho para gerar um gráfico específico
  python make.py list-charts                Lista todos os IDs e chaves de gráficos
  python make.py mock-gen                   Gera os 115k+ registros sintéticos
  python make.py quality-eval               Executa a suíte de Data Quality (Item 4)
  python make.py genai-extract              Executa o pipeline de GenAI & LLMs (Item 5)
  python make.py help                       Exibe este menu de ajuda

Atalhos diretos no Windows CLI:
  .\\push-read                               (commita e sobe o README.md)
  .\\push-read "mensagem personalizada"      (com mensagem de commit customizada)
  .\\make push-read                         (executa via make wrapper)
  .\\notebook-gen                            (executa notebook-gen diretamente)
=============================================================================
""")

def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("help", "-h", "--help"):
        print_help()
        return

    command = sys.argv[1].lower().replace("-", "_")
    arg = sys.argv[2] if len(sys.argv) > 2 else None

    if command in ("data_app", "dataapp", "app", "streamlit"):
        task_data_app()
    elif command in ("data_app_assets", "dataapp_assets", "app_assets"):
        task_data_app_assets()
    elif command in ("push_read", "pushread", "push_readme", "pushreadme"):
        task_push_read(arg)
    elif command in ("pipeline_run", "pipeline", "pipelinerun", "pipe", "pipeline_eval"):
        task_pipeline_run()
    elif command in ("data_modeling", "datamodeling", "kimball", "modeling", "case6", "case06"):
        task_data_modeling()
    elif command in ("bi_analysis", "bianalysis", "bi", "case7", "case07"):
        task_bi_analysis()
    elif command in ("pitch_charts", "pitch", "pitch_gen"):
        task_pitch_charts()
    elif command in ("insights_charts", "insights", "insight_charts"):
        task_insights_charts()
    elif command in ("notebook_gen", "notebookgen", "charts"):
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
    elif command in ("genai_extract", "genai", "llm", "llms"):
        task_genai_extract()
    else:
        print(f"[ERRO] Comando desconhecido: '{sys.argv[1]}'")
        print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()

