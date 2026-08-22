"""
04_vincular/link_datasets_to_tables.py - FASE 4: Vincular Datasets às Tabelas
==============================================================================
Le os dataset_ids (fase 2) e table_ids (fase 3) e realiza a vinculacao
via POST /storage-explorer/tables/{tableId}/datasets.

FASE:   4 de 5
INPUT:  .state/uploaded_datasets.json + .state/created_tables.json
OUTPUT: .state/linked_datasets.json com confirmacao de cada vinculo
"""

import sys
import json
import time
from pathlib import Path

import requests

# ─── Import config
import importlib.util
_cfg_path = Path(__file__).resolve().parents[1] / "00_config.py"
_spec = importlib.util.spec_from_file_location("cfg", _cfg_path)
_cfg  = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_cfg)

_auth_path = Path(__file__).resolve().parents[1] / "01_auth" / "authenticate.py"
_aspec = importlib.util.spec_from_file_location("auth", _auth_path)
_auth  = importlib.util.module_from_spec(_aspec)
_aspec.loader.exec_module(_auth)

ENTITIES               = _cfg.ENTITIES
endpoint_link_dataset  = _cfg.endpoint_link_dataset
STATE_UPLOADS_FILE     = _cfg.STATE_UPLOADS_FILE
STATE_TABLES_FILE      = _cfg.STATE_TABLES_FILE
STATE_LINKS_FILE       = _cfg.STATE_LINKS_FILE
ensure_state_dir       = _cfg.ensure_state_dir
get_logger             = _cfg.get_logger
refresh_token_if_needed = _auth.refresh_token_if_needed

log = get_logger("fase4.vincular")


def load_state_file(path: Path, label: str) -> list[dict]:
    """Carrega um arquivo de estado JSON. Levanta erro descritivo se nao existir."""
    if not path.exists():
        raise FileNotFoundError(
            f"Arquivo de estado '{label}' nao encontrado em: {path}\n"
            f"Execute as fases anteriores primeiro."
        )
    return json.loads(path.read_text())


def link_dataset_to_table(token: str, table_id: str, dataset_id: str, entity: str) -> dict:
    """
    Vincula um dataset a uma tabela via POST /storage-explorer/tables/{tableId}/datasets.
    """
    endpoint = endpoint_link_dataset(table_id)
    headers  = {
        "Authorization": token,
        "Content-Type":  "application/json",
    }
    payload  = {"datasetId": dataset_id}

    log.info(f"  POST /tables/{table_id}/datasets → dataset={dataset_id}")
    resp = requests.post(endpoint, headers=headers, json=payload, timeout=60)

    if resp.status_code not in (200, 201, 204):
        log.error(f"  Erro ao vincular {entity}: {resp.status_code} - {resp.text[:500]}")
        return {
            "entity":     entity,
            "table_id":   table_id,
            "dataset_id": dataset_id,
            "status":     "error",
            "code":       resp.status_code,
            "detail":     resp.text[:500],
        }

    data = resp.json() if resp.content else {}
    log.info(f"  [OK] {entity} -> tabela vinculada ao dataset")
    return {
        "entity":     entity,
        "table_id":   table_id,
        "dataset_id": dataset_id,
        "status":     "success",
        "raw":        data,
    }


def link_all() -> list[dict]:
    """
    Carrega o estado das fases 2 e 3 e vincula cada dataset à sua tabela.
    """
    log.info("=== FASE 4: Vincular Datasets as Tabelas ===")

    uploads = load_state_file(STATE_UPLOADS_FILE, "uploaded_datasets")
    tables  = load_state_file(STATE_TABLES_FILE,  "created_tables")

    # Indexa por entidade
    uploads_by_entity = {u["entity"]: u for u in uploads}
    tables_by_entity  = {t["entity"]: t for t in tables}

    token   = refresh_token_if_needed()
    results = []

    for i, entity in enumerate(ENTITIES, 1):
        log.info(f"\n[{i}/{len(ENTITIES)}] {entity}")

        upload = uploads_by_entity.get(entity)
        table  = tables_by_entity.get(entity)

        if not upload or upload.get("status") != "success":
            log.warning(f"  SKIP: dataset de {entity} nao disponivel ou com erro na fase 2")
            results.append({"entity": entity, "status": "skipped_no_dataset"})
            continue

        if not table or table.get("status") != "success":
            log.warning(f"  SKIP: tabela de {entity} nao disponivel ou com erro na fase 3")
            results.append({"entity": entity, "status": "skipped_no_table"})
            continue

        table_id   = table["table_id"]
        dataset_id = upload["dataset_id"]

        if not table_id or not dataset_id:
            log.warning(f"  SKIP: table_id ou dataset_id nulo para {entity}")
            results.append({"entity": entity, "status": "skipped_null_ids",
                            "table_id": table_id, "dataset_id": dataset_id})
            continue

        result = link_dataset_to_table(token, table_id, dataset_id, entity)
        results.append(result)

        if i < len(ENTITIES):
            time.sleep(0.5)

    # Persiste estado
    ensure_state_dir()
    STATE_LINKS_FILE.write_text(json.dumps(results, indent=2, ensure_ascii=False))

    # Sumario
    success = [r for r in results if r.get("status") == "success"]
    errors  = [r for r in results if r.get("status") == "error"]
    skipped = [r for r in results if "skip" in r.get("status", "")]
    log.info(f"\n=== RESUMO FASE 4 ===")
    log.info(f"  [OK] Vinculos criados: {len(success)}/{len(ENTITIES)}")
    if skipped:
        log.warning(f"  [SKIP] Ignorados: {len(skipped)}")
    if errors:
        log.warning(f"  [ERRO] Erros: {len(errors)}")
    log.info(f"  Estado salvo em: {STATE_LINKS_FILE}")

    return results


if __name__ == "__main__":
    results = link_all()
    print(f"\n[OK] Fase 4 concluida: {sum(1 for r in results if r.get('status') == 'success')}/{len(ENTITIES)} vinculos criados")
