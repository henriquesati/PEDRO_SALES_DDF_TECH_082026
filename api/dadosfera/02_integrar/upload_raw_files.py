"""
02_integrar/upload_raw_files.py - FASE 2: Upload de Arquivos para o Storage
============================================================================
Itera sobre os 7 CSVs gerados e faz upload para a zona /raw/ do Data Lake
da Dadosfera via POST /storage-explorer/storage/upload/batch.

FASE:   2 de 5
INPUT:  accessToken (de .state/auth_tokens.json) + CSVs em data/mock/output/csv/
OUTPUT: .state/uploaded_datasets.json com dataset_id de cada arquivo
"""

import sys
import json
import time
from pathlib import Path

import requests

# ─── Import config via importlib (compativel com execucao direta ou via orquestrador)
import importlib.util
_cfg_path = Path(__file__).resolve().parents[1] / "00_config.py"
_spec = importlib.util.spec_from_file_location("cfg", _cfg_path)
_cfg  = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_cfg)

_auth_path = Path(__file__).resolve().parents[1] / "01_auth" / "authenticate.py"
_aspec = importlib.util.spec_from_file_location("auth", _auth_path)
_auth  = importlib.util.module_from_spec(_aspec)
_aspec.loader.exec_module(_auth)

ENTITIES              = _cfg.ENTITIES
CSV_DIR               = _cfg.CSV_DIR
STORAGE_FOLDER_RAW    = _cfg.STORAGE_FOLDER_RAW
ENDPOINT_STORAGE_UPLOAD = _cfg.ENDPOINT_STORAGE_UPLOAD
STATE_UPLOADS_FILE    = _cfg.STATE_UPLOADS_FILE
ensure_state_dir      = _cfg.ensure_state_dir
get_logger            = _cfg.get_logger
load_token            = _auth.load_token
refresh_token_if_needed = _auth.refresh_token_if_needed

log = get_logger("fase2.upload")

# Mapeamento entidade → nome do arquivo CSV
CSV_FILES = {entity: CSV_DIR / f"{entity}.csv" for entity in ENTITIES}


def upload_file(token: str, entity: str, csv_path: Path) -> dict:
    """
    Faz upload de um arquivo CSV para o Storage da Dadosfera.
    Retorna o dict com informacoes do dataset criado.
    """
    size_mb = csv_path.stat().st_size / (1024 * 1024)
    log.info(f"  Uploading: {csv_path.name} ({size_mb:.2f} MB)")

    headers = {"Authorization": token}

    # Parametros de destino no storage
    params = {
        "folderPath": STORAGE_FOLDER_RAW,
    }

    with open(csv_path, "rb") as f:
        files = {"file": (csv_path.name, f, "text/csv")}
        resp = requests.post(
            ENDPOINT_STORAGE_UPLOAD,
            headers=headers,
            params=params,
            files=files,
            timeout=120,
        )

    if resp.status_code not in (200, 201):
        log.error(f"  Erro no upload de {entity}: {resp.status_code} - {resp.text[:500]}")
        return {
            "entity": entity,
            "file":   str(csv_path),
            "status": "error",
            "code":   resp.status_code,
            "detail": resp.text[:500],
        }

    data = resp.json()
    dataset_id = (
        data.get("datasetId")
        or data.get("dataset_id")
        or data.get("id")
        or data.get("fileId")
        or data.get("file_id")
    )

    log.info(f"  [OK] {entity} -> dataset_id={dataset_id}")
    return {
        "entity":     entity,
        "file":       csv_path.name,
        "dataset_id": dataset_id,
        "folder":     STORAGE_FOLDER_RAW,
        "size_bytes": csv_path.stat().st_size,
        "status":     "success",
        "raw":        data,
    }


def upload_all() -> list[dict]:
    """
    Executa o upload de todos os 7 CSVs e persiste o estado.
    Retorna lista de resultados por entidade.
    """
    log.info("=== FASE 2: Upload de Arquivos para o Storage ===")
    log.info(f"Destino no Data Lake: {STORAGE_FOLDER_RAW}")
    log.info(f"Total de entidades: {len(ENTITIES)}")

    token = refresh_token_if_needed()
    results = []

    for i, entity in enumerate(ENTITIES, 1):
        csv_path = CSV_FILES[entity]
        log.info(f"\n[{i}/{len(ENTITIES)}] {entity}")

        if not csv_path.exists():
            log.warning(f"  AVISO: Arquivo nao encontrado: {csv_path}")
            results.append({"entity": entity, "status": "file_not_found", "file": str(csv_path)})
            continue

        result = upload_file(token, entity, csv_path)
        results.append(result)

        # Pequena pausa entre uploads para nao sobrecarregar a API
        if i < len(ENTITIES):
            time.sleep(1)

    # Persiste estado para proximas fases
    ensure_state_dir()
    STATE_UPLOADS_FILE.write_text(json.dumps(results, indent=2, ensure_ascii=False))

    # Sumario
    success = [r for r in results if r.get("status") == "success"]
    errors  = [r for r in results if r.get("status") != "success"]
    log.info(f"\n=== RESUMO FASE 2 ===")
    log.info(f"  [OK] Uploads com sucesso: {len(success)}/{len(ENTITIES)}")
    if errors:
        log.warning(f"  [ERRO] Falhas: {len(errors)}")
        for e in errors:
            log.warning(f"    - {e['entity']}: {e.get('detail', e.get('status'))}")
    log.info(f"  Estado salvo em: {STATE_UPLOADS_FILE}")

    return results


if __name__ == "__main__":
    results = upload_all()
    print(f"\n[OK] Fase 2 concluida: {sum(1 for r in results if r.get('status') == 'success')}/{len(ENTITIES)} uploads com sucesso")
