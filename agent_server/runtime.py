"""Pure functional orchestration runtime using Google Antigravity SDK."""

import os
from pathlib import Path
from typing import AsyncIterator, Final, Optional, Sequence
from dotenv import load_dotenv

from google.antigravity import Agent, LocalAgentConfig, types
from google.antigravity.hooks import policy

from agent_server.config import DEFAULT_MODEL, WORKSPACE_ROOT
from agent_server.types import AgentMeta

# Ensure .env is loaded if present
load_dotenv(WORKSPACE_ROOT / ".env")
load_dotenv(Path.home() / ".gemini" / ".env")


# ---------------------------------------------------------------------------
# Pure Config Builders
# ---------------------------------------------------------------------------

def resolve_api_key(explicit_key: Optional[str] = None) -> Optional[str]:
    """Resolve pure Gemini / Google GenAI API key from parameters or environment."""
    if explicit_key and explicit_key.strip():
        return explicit_key.strip()
    return (
        os.environ.get("GEMINI_API_KEY")
        or os.environ.get("GOOGLE_API_KEY")
        or os.environ.get("GOOGLE_GENAI_API_KEY")
        or os.environ.get("ANTIGRAVITY_API_KEY")
    )


def build_autonomous_config(
    agent_meta: AgentMeta,
    skills_paths: Sequence[str],
    model: str = DEFAULT_MODEL,
    api_key: Optional[str] = None,
) -> LocalAgentConfig:
    """Pure factory function to build a 100% autonomous LocalAgentConfig.

    Applies:
    - policy.allow_all(): Auto-approves all tool and command executions.
    - AgentBehavior.AUTONOMOUS: Prevents interactive pauses.
    - Automatic loading of discovered skill directories.
    """
    key = resolve_api_key(api_key)
    if not key:
        raise ValueError(
            "Chave de API Gemini não configurada. Defina a variável de ambiente "
            "GEMINI_API_KEY no arquivo .env ou informe sua chave no painel de configurações do /chat."
        )

    return LocalAgentConfig(
        model=model,
        api_key=key,
        system_instructions=agent_meta.system_instructions,
        skills_paths=list(skills_paths),
        policies=[policy.allow_all()],  # 100% autonomous - zero human confirmation prompts
        capabilities=types.CapabilitiesConfig(
            agent_behavior=types.AgentBehavior.AUTONOMOUS,
            enable_subagents=True,
        ),
    )



# ---------------------------------------------------------------------------
# Execution Functions
# ---------------------------------------------------------------------------

async def execute_agent_turn(
    agent_meta: AgentMeta,
    skills_paths: Sequence[str],
    prompt: str,
    model: str = DEFAULT_MODEL,
    api_key: Optional[str] = None,
) -> str:
    """Executes a single autonomous turn on the agent and returns the complete text."""
    config = build_autonomous_config(
        agent_meta=agent_meta,
        skills_paths=skills_paths,
        model=model,
        api_key=api_key,
    )

    async with Agent(config=config) as agent:
        response = await agent.chat(prompt)
        text_output = await response.text()
        return text_output


async def stream_agent_turn(
    agent_meta: AgentMeta,
    skills_paths: Sequence[str],
    prompt: str,
    model: str = DEFAULT_MODEL,
    api_key: Optional[str] = None,
) -> AsyncIterator[str]:
    """Asynchronously streams response tokens from the agent turn."""
    config = build_autonomous_config(
        agent_meta=agent_meta,
        skills_paths=skills_paths,
        model=model,
        api_key=api_key,
    )

    async with Agent(config=config) as agent:
        response = await agent.chat(prompt)
        async for token in response:
            yield str(token)
