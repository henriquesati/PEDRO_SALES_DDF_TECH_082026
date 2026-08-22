"""
run_pipeline.py - Orquestrador do Pipeline Dadosfera API
=========================================================
Executa as 5 fases do pipeline em sequencia com logging unificado.
Pode ser interrompido apos qualquer fase com --stop-after <fase>.

USO:
    python api/dadosfera/run_pipeline.py              # todas as fases
    python api/dadosfera/run_pipeline.py --stop-after 2  # para apos upload
    python api/dadosfera/run_pipeline.py --fase 3     # apenas fase 3
"""

import sys
import argparse
import importlib.util
import traceback
from pathlib import Path
from datetime import datetime, timezone

# ─── Logger simples antes de carregar config
import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
)
log = logging.getLogger("pipeline")

BASE_DIR = Path(__file__).resolve().parent


def load_module(name: str, path: Path):
    """Carrega um modulo Python a partir do caminho absoluto."""
    spec = importlib.util.spec_from_file_location(name, path)
    mod  = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


PHASES = {
    1: {
        "name":   "Autenticacao",
        "desc":   "Login + obtencao do token de acesso",
        "path":   BASE_DIR / "01_auth" / "authenticate.py",
        "func":   "authenticate",
    },
    2: {
        "name":   "Integracao (Upload)",
        "desc":   "Upload dos 7 CSVs para /raw/recuperacao_carrinho/",
        "path":   BASE_DIR / "02_integrar" / "upload_raw_files.py",
        "func":   "upload_all",
    },
    3: {
        "name":   "Criacao de Tabelas",
        "desc":   "Cria as 7 tabelas no Snowflake com schemas tipados",
        "path":   BASE_DIR / "03_criar_tabelas" / "create_snowflake_tables.py",
        "func":   "create_all_tables",
    },
    4: {
        "name":   "Vinculacao",
        "desc":   "Vincula datasets → tabelas (materializacao)",
        "path":   BASE_DIR / "04_vincular" / "link_datasets_to_tables.py",
        "func":   "link_all",
    },
    5: {
        "name":   "Catalogacao",
        "desc":   "Busca ativos no catalogo e gera relatorio",
        "path":   BASE_DIR / "05_catalogar" / "catalog_assets.py",
        "func":   "catalog_assets",
    },
}


def run_phase(phase_num: int) -> bool:
    """
    Executa uma unica fase. Retorna True se sucesso, False se erro.
    """
    phase  = PHASES[phase_num]
    banner = f"{'=' * 60}\n  FASE {phase_num}: {phase['name'].upper()}\n  {phase['desc']}\n{'=' * 60}"
    log.info(f"\n{banner}")

    try:
        mod  = load_module(f"fase{phase_num}", phase["path"])
        func = getattr(mod, phase["func"])
        result = func()
        log.info(f"[OK] Fase {phase_num} concluida com sucesso.\n")
        return True
    except FileNotFoundError as e:
        log.error(f"[ERRO] Fase {phase_num} falhou — arquivo nao encontrado:\n  {e}\n")
        return False
    except Exception as e:
        log.error(f"[ERRO] Fase {phase_num} falhou:\n  {type(e).__name__}: {e}\n")
        log.debug(traceback.format_exc())
        return False


def run_pipeline(phases_to_run: list[int], stop_on_error: bool = True) -> dict:
    """
    Executa as fases especificadas em sequencia.
    """
    start_time = datetime.now(timezone.utc)
    log.info(f"""
+==============================================================+
|   PIPELINE DADOSFERA -- CASE RECUPERACAO DE CARRINHO         |
|   Inicio: {start_time.strftime('%Y-%m-%d %H:%M:%S UTC')}                       |
|   Fases:  {phases_to_run}                                           |
+==============================================================+
""")

    results = {}
    for phase_num in sorted(phases_to_run):
        if phase_num not in PHASES:
            log.warning(f"Fase {phase_num} nao existe. Pulando.")
            continue

        success = run_phase(phase_num)
        results[phase_num] = success

        if not success and stop_on_error:
            log.error(f"Pipeline interrompido na Fase {phase_num} (--stop-on-error ativo).")
            break

    # Sumario final
    end_time  = datetime.now(timezone.utc)
    duration  = (end_time - start_time).total_seconds()
    succeeded = [p for p, ok in results.items() if ok]
    failed    = [p for p, ok in results.items() if not ok]

    log.info(f"""
+==============================================================+
|   SUMARIO FINAL DO PIPELINE                                  |
+==============================================================+
|   Duracao:    {duration:.1f}s                                        |
|   Sucesso:    Fases {succeeded}                                    |
|   Falhas:     Fases {failed}                                      |
+==============================================================+
""")

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Orquestrador do pipeline de API Dadosfera"
    )
    parser.add_argument(
        "--fases", nargs="+", type=int, default=list(PHASES.keys()),
        metavar="N",
        help="Fases a executar (default: todas). Ex: --fases 1 2 3"
    )
    parser.add_argument(
        "--stop-after", type=int, metavar="N",
        help="Para apos a fase N (inclusive)"
    )
    parser.add_argument(
        "--fase", type=int, metavar="N",
        help="Executa apenas a fase N"
    )
    parser.add_argument(
        "--continuar-em-erros", action="store_true",
        help="Nao para o pipeline em caso de erro em uma fase"
    )
    args = parser.parse_args()

    # Determina quais fases rodar
    if args.fase:
        phases = [args.fase]
    elif args.stop_after:
        phases = [p for p in args.fases if p <= args.stop_after]
    else:
        phases = args.fases

    results = run_pipeline(phases, stop_on_error=not args.continuar_em_erros)

    # Exit code = 0 se todas as fases executadas tiveram sucesso
    all_ok = all(results.values())
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
