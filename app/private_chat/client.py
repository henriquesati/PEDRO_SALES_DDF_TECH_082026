"""Cliente HTTP e SSE resiliente e desacoplado para comunicação com o Antigravity Agent Server."""

import json
import time
from typing import Any, Dict, Generator, List, Optional
import urllib.error
import urllib.parse
import urllib.request

DEFAULT_SERVER_URL: str = "http://127.0.0.1:8000"


def check_server_health(base_url: str = DEFAULT_SERVER_URL, timeout_sec: float = 2.0) -> Optional[Dict[str, Any]]:
    """Verifica a integridade do cluster e retorna os metadados do servidor se saudável."""
    url = f"{base_url.rstrip('/')}/health"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "DadosferaPrivateChat/1.0"})
        start_t = time.perf_counter()
        with urllib.request.urlopen(req, timeout=timeout_sec) as response:
            latency_ms = (time.perf_counter() - start_t) * 1000.0
            if response.status == 200:
                data = json.loads(response.read().decode("utf-8"))
                data["_latency_ms"] = round(latency_ms, 1)
                return data
    except Exception:
        pass
    return None


def fetch_agents_catalog(base_url: str = DEFAULT_SERVER_URL, timeout_sec: float = 2.5) -> List[Dict[str, str]]:
    """Obtém o catálogo atualizado de todos os agentes autônomos registrados no backend."""
    url = f"{base_url.rstrip('/')}/agents"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "DadosferaPrivateChat/1.0"})
        with urllib.request.urlopen(req, timeout=timeout_sec) as response:
            if response.status == 200:
                return json.loads(response.read().decode("utf-8"))
    except Exception:
        pass
    return []


def fetch_openapi_spec(base_url: str = DEFAULT_SERVER_URL, timeout_sec: float = 3.0) -> Optional[Dict[str, Any]]:
    """Recupera a especificação bruta OpenAPI 3.1.0 gerada pelo FastAPI."""
    url = f"{base_url.rstrip('/')}/openapi.json"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "DadosferaPrivateChat/1.0"})
        with urllib.request.urlopen(req, timeout=timeout_sec) as response:
            if response.status == 200:
                return json.loads(response.read().decode("utf-8"))
    except Exception:
        pass
    return None


def send_chat_turn(
    message: str,
    agent_name: str,
    base_url: str = DEFAULT_SERVER_URL,
    api_key: Optional[str] = None,
    timeout_sec: float = 60.0,
) -> Dict[str, Any]:
    """Envia uma mensagem para o agente no modo síncrono (/chat) e retorna o resultado estruturado."""
    url = f"{base_url.rstrip('/')}/chat"
    payload_dict = {"message": message, "agent_name": agent_name}
    if api_key and api_key.strip():
        payload_dict["api_key"] = api_key.strip()

    payload = json.dumps(payload_dict).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json", "User-Agent": "DadosferaPrivateChat/1.0"},
        method="POST",
    )

    start_t = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=timeout_sec) as response:
            elapsed_sec = time.perf_counter() - start_t
            if response.status == 200:
                res_data = json.loads(response.read().decode("utf-8"))
                res_data["_elapsed_sec"] = round(elapsed_sec, 2)
                return res_data
    except urllib.error.HTTPError as http_err:
        err_body = http_err.read().decode("utf-8")
        try:
            parsed_err = json.loads(err_body)
            detail = parsed_err.get("detail", str(http_err))
        except Exception:
            detail = err_body or str(http_err)
        return {
            "agent_name": agent_name,
            "response": "",
            "status": "error",
            "error_message": f"Erro HTTP {http_err.code}: {detail}",
            "_elapsed_sec": round(time.perf_counter() - start_t, 2),
        }
    except Exception as exc:
        return {
            "agent_name": agent_name,
            "response": "",
            "status": "error",
            "error_message": f"Falha de conexão com o servidor: {exc}",
            "_elapsed_sec": round(time.perf_counter() - start_t, 2),
        }


def stream_chat_turn(
    message: str,
    agent_name: str,
    base_url: str = DEFAULT_SERVER_URL,
    api_key: Optional[str] = None,
    timeout_sec: float = 60.0,
) -> Generator[str, None, None]:
    """Consome a rota SSE (/stream) emitindo tokens em tempo real."""
    url = f"{base_url.rstrip('/')}/stream"
    payload_dict = {"message": message, "agent_name": agent_name}
    if api_key and api_key.strip():
        payload_dict["api_key"] = api_key.strip()

    payload = json.dumps(payload_dict).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json", "Accept": "text/event-stream"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=timeout_sec) as response:
            for line in response:
                line_str = line.decode("utf-8").strip()
                if not line_str or line_str.startswith(":"):
                    continue
                if line_str.startswith("data:"):
                    data_str = line_str[5:].strip()
                    if data_str == "[DONE]":
                        break
                    try:
                        parsed = json.loads(data_str)
                        if "token" in parsed:
                            yield parsed["token"]
                        elif "error" in parsed:
                            yield f"\n\n❌ [Erro do Agente]: {parsed['error']}"
                    except json.JSONDecodeError:
                        yield data_str
    except Exception as exc:
        yield f"\n\n❌ [Erro de Conexão Streaming]: {exc}"

