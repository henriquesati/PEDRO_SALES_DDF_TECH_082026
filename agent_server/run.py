"""Direct CLI runner for the Agent Web Server."""

import sys
from pathlib import Path

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

import uvicorn
from agent_server.config import HOST, PORT


def main() -> None:
    """Entrypoint to run Uvicorn server."""
    print("=" * 60)
    print("[INIT] Antigravity Agent Server (100% Autonomo)")
    print(f"[ADDR] Endereco: http://{HOST}:{PORT}")
    print(f"[DOCS] Documentacao Swagger: http://{HOST}:{PORT}/docs")
    print(f"[HLTH] Healthcheck: http://{HOST}:{PORT}/health")
    print("=" * 60)

    uvicorn.run(
        "agent_server.server:app",
        host=HOST,
        port=PORT,
        reload=False,
        log_level="info",
    )


if __name__ == "__main__":
    main()
