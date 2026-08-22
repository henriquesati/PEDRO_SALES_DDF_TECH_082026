"""
01_auth/authenticate.py - FASE 1: Autenticacao na Dadosfera
============================================================
Realiza login na API da Dadosfera e persiste os tokens em arquivo
local (.state/auth_tokens.json) para uso nas fases seguintes.

FASE:   1 de 5
INPUT:  credenciais em 00_config.py
OUTPUT: .state/auth_tokens.json com accessToken e refreshToken
"""

import sys
import json
import time
from pathlib import Path
from datetime import datetime, timezone

import requests

# ─── Import config via importlib (compativel com execucao direta ou via orquestrador)
import importlib.util
_cfg_path = Path(__file__).resolve().parents[1] / "00_config.py"
_spec = importlib.util.spec_from_file_location("cfg", _cfg_path)
_cfg  = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_cfg)

DADOSFERA_USERNAME      = _cfg.DADOSFERA_USERNAME
DADOSFERA_PASSWORD      = _cfg.DADOSFERA_PASSWORD
DADOSFERA_CUSTOMER_NAME = _cfg.DADOSFERA_CUSTOMER_NAME
ENDPOINT_AUTH_SIGNIN    = _cfg.ENDPOINT_AUTH_SIGNIN
ENDPOINT_AUTH_REFRESH   = _cfg.ENDPOINT_AUTH_REFRESH
STATE_TOKEN_FILE        = _cfg.STATE_TOKEN_FILE
ensure_state_dir        = _cfg.ensure_state_dir
get_logger              = _cfg.get_logger

log = get_logger("fase1.auth")


def authenticate() -> dict:
    """
    Realiza POST /auth/sign-in e salva tokens localmente.
    Retorna o dicionario com accessToken e refreshToken.
    """
    log.info("=== FASE 1: Autenticacao ===")
    log.info(f"Usuario: {DADOSFERA_USERNAME}")
    log.info(f"Customer: {DADOSFERA_CUSTOMER_NAME}")

    payload = {
        "username": DADOSFERA_USERNAME,
        "password": DADOSFERA_PASSWORD,
        "customerName": DADOSFERA_CUSTOMER_NAME,
    }

    log.info(f"POST {ENDPOINT_AUTH_SIGNIN}")
    resp = requests.post(ENDPOINT_AUTH_SIGNIN, json=payload, timeout=30)

    if resp.status_code != 200:
        log.error(f"Falha na autenticacao: {resp.status_code} - {resp.text}")
        resp.raise_for_status()

    data = resp.json()
    token_data = data.get("tokens", {})
    access_token  = token_data.get("accessToken") or data.get("accessToken") or data.get("access_token")
    refresh_token = token_data.get("refreshToken") or data.get("refreshToken") or data.get("refresh_token")

    if not access_token:
        log.error(f"Resposta inesperada da API: {json.dumps(data, indent=2)}")
        raise ValueError("accessToken nao encontrado na resposta")

    customer_info = data.get("customer", {})
    user_info = data.get("user", {})

    tokens = {
        "accessToken":  access_token,
        "refreshToken": refresh_token,
        "obtainedAt":   datetime.now(timezone.utc).isoformat(),
        "username":     DADOSFERA_USERNAME,
        "customerName": customer_info.get("name", DADOSFERA_CUSTOMER_NAME),
        "customerId":   customer_info.get("id"),
        "userId":       user_info.get("id"),
    }

    ensure_state_dir()
    STATE_TOKEN_FILE.write_text(json.dumps(tokens, indent=2, ensure_ascii=False))
    log.info(f"[OK] Token salvo em: {STATE_TOKEN_FILE}")
    log.info(f"  Customer: {customer_info.get('name') or DADOSFERA_CUSTOMER_NAME}")
    log.info(f"  accessToken[:25]: {access_token[:25]}...")

    return tokens


def load_token() -> str:
    """Carrega o accessToken salvo em disco. Levanta FileNotFoundError se nao existir."""
    if not STATE_TOKEN_FILE.exists():
        raise FileNotFoundError(
            f"Token nao encontrado em {STATE_TOKEN_FILE}. "
            "Execute a Fase 1 (authenticate.py) primeiro."
        )
    tokens = json.loads(STATE_TOKEN_FILE.read_text())
    return tokens["accessToken"]


def refresh_token_if_needed() -> str:
    """
    Verifica se o token ainda e valido. Se houver refreshToken disponivel,
    tenta renovar. Caso contrario, autentica novamente do zero.
    """
    if not STATE_TOKEN_FILE.exists():
        log.info("Nenhum token encontrado. Autenticando...")
        return authenticate()["accessToken"]

    tokens = json.loads(STATE_TOKEN_FILE.read_text())
    refresh_token = tokens.get("refreshToken")

    if not refresh_token:
        log.info("Sem refreshToken. Reautenticando...")
        return authenticate()["accessToken"]

    log.info(f"POST {ENDPOINT_AUTH_REFRESH}")
    resp = requests.post(
        ENDPOINT_AUTH_REFRESH,
        json={"refreshToken": refresh_token},
        timeout=30
    )

    if resp.status_code == 200:
        data = resp.json()
        token_data = data.get("tokens", {})
        new_access = token_data.get("accessToken") or data.get("accessToken") or data.get("access_token")
        if new_access:
            tokens["accessToken"] = new_access
            tokens["obtainedAt"]  = datetime.now(timezone.utc).isoformat()
            STATE_TOKEN_FILE.write_text(json.dumps(tokens, indent=2, ensure_ascii=False))
            log.info("[OK] Token renovado com sucesso")
            return new_access

    log.warning(f"Falha ao renovar token ({resp.status_code}). Reautenticando...")
    return authenticate()["accessToken"]


if __name__ == "__main__":
    tokens = authenticate()
    print("\n[OK] Autenticacao concluida com sucesso!")
    print(f"  accessToken[:30]: {tokens['accessToken'][:30]}...")
