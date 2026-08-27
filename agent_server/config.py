"""Centralized and immutable settings for the Agent Server."""

from pathlib import Path
from types import MappingProxyType
from typing import Final, Mapping, Sequence

# ---------------------------------------------------------------------------
# Network & Server Constants
# ---------------------------------------------------------------------------
HOST: Final[str] = "127.0.0.1"
PORT: Final[int] = 8000
SERVER_TITLE: Final[str] = "Antigravity Agent Server"
SERVER_DESCRIPTION: Final[str] = (
    "Servidor web local e autônomo para orquestração de Agentes e Skills "
    "usando o Google Antigravity SDK sem intervenção humana."
)
SERVER_VERSION: Final[str] = "1.0.0"

# ---------------------------------------------------------------------------
# OpenAPI 3.1.0 Specification Metadata
# ---------------------------------------------------------------------------
OPENAPI_TAGS: Final[Sequence[Mapping[str, str]]] = (
    {
        "name": "Health",
        "description": "Diagnóstico de integridade do cluster, status de runtime e contagem de ativos descobertos.",
    },
    {
        "name": "Discovery",
        "description": "Catálogo de descoberta dinâmica de Agentes e Skills do workspace (.agents/).",
    },
    {
        "name": "Inference",
        "description": "Execução de turnos autônomos dos Agentes (chamadas síncronas e SSE streaming em tempo real).",
    },
)

CONTACT_INFO: Final[Mapping[str, str]] = MappingProxyType({
    "name": "Pedro Sales & Dadosfera AI Team",
    "url": "https://github.com/henriquesati/PEDRO_SALES_DDF_TECH_082026",
    "email": "candidate@dadosfera.ia",
})

LICENSE_INFO: Final[Mapping[str, str]] = MappingProxyType({
    "name": "Apache 2.0 / DDF Tech Standard",
    "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
})

# ---------------------------------------------------------------------------
# Filesystem Paths
# ---------------------------------------------------------------------------
WORKSPACE_ROOT: Final[Path] = Path(__file__).resolve().parent.parent
AGENTS_DIR: Final[Path] = WORKSPACE_ROOT / ".agents" / "agents"
SKILLS_DIR: Final[Path] = WORKSPACE_ROOT / ".agents" / "skills"
RULES_DIR: Final[Path] = WORKSPACE_ROOT / ".agents" / "rules"

# ---------------------------------------------------------------------------
# Agent Runtime Defaults
# ---------------------------------------------------------------------------
DEFAULT_AGENT_NAME: Final[str] = "case-context-specialist"
DEFAULT_MODEL: Final[str] = "gemini-3.7-flash"

# Operational Profile Mapping
RUNTIME_DEFAULTS: Final[Mapping[str, object]] = MappingProxyType({
    "max_subagent_depth": 3,
    "enable_subagents": True,
    "auto_approve_policies": True,
    "temperature": 0.2,
})

