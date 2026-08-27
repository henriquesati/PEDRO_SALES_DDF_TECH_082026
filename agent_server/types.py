"""Immutable domain types and API data contracts for the Agent Server with OpenAPI schemas."""

from dataclasses import dataclass
from typing import Final, Literal, Optional, Sequence
from pydantic import BaseModel, Field

from agent_server.config import DEFAULT_AGENT_NAME

# ---------------------------------------------------------------------------
# Domain Models (Frozen & Immutable)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class AgentMeta:
    """Metadata representing an available Agent discovered in the workspace."""
    name: str
    description: str
    system_instructions: str
    file_path: str


@dataclass(frozen=True)
class SkillMeta:
    """Metadata representing a Skill discovered in the workspace."""
    name: str
    description: str
    directory_path: str


# ---------------------------------------------------------------------------
# HTTP Schema Contracts (Pydantic Models with OpenAPI Metadata)
# ---------------------------------------------------------------------------

class ChatInput(BaseModel):
    """Payload for executing an autonomous agent turn."""
    message: str = Field(
        ...,
        description="Prompt, instrução ou tarefa analítica a ser executada autonomamente pelo agente.",
        examples=["Gere um diagnóstico do abandono de carrinhos na categoria Eletrônicos."],
    )
    agent_name: str = Field(
        default=DEFAULT_AGENT_NAME,
        description="Nome do agente especializado a ser invocado (.agents/agents/).",
        examples=["case-context-specialist", "data-strategy-analyst", "charts-maker"],
    )
    api_key: Optional[str] = Field(
        default=None,
        description="Chave de API Gemini/Google GenAI opcional para autenticação de runtime.",
        examples=[None, "AIzaSy..."],
    )

    class Config:
        frozen = True
        json_schema_extra = {
            "example": {
                "message": "Qual é o impacto financeiro de recuperar carrinhos abandonados acima de R$ 500?",
                "agent_name": "data-strategy-analyst",
                "api_key": None,
            }
        }



class ChatOutput(BaseModel):
    """Response payload returned by the autonomous agent server."""
    agent_name: str = Field(
        ...,
        description="Identificador do agente que processou a requisição.",
        examples=["case-context-specialist"],
    )
    response: str = Field(
        ...,
        description="Conteúdo textual gerado pelo agente com raciocínio e dados analíticos.",
        examples=["Com base no Lakehouse Dadosfera, carrinhos > R$ 500 representam 42% do GMV recuperável..."],
    )
    status: Literal["success", "error"] = Field(
        ...,
        description="Status da execução do turno.",
        examples=["success"],
    )
    error_message: Optional[str] = Field(
        default=None,
        description="Mensagem de erro em caso de falha durante a orquestração.",
        examples=[None],
    )

    class Config:
        frozen = True
        json_schema_extra = {
            "example": {
                "agent_name": "case-context-specialist",
                "response": "O case técnico da Dadosfera foca em 9 requisitos fundamentais integrando o Lakehouse.",
                "status": "success",
                "error_message": None,
            }
        }


class AgentInfo(BaseModel):
    """Representation of an autonomous agent for catalog discovery."""
    name: str = Field(
        ...,
        description="Nome único do agente no ecossistema Antigravity.",
        examples=["case-context-specialist"],
    )
    description: str = Field(
        ...,
        description="Missão, especialidade e papel funcional do agente.",
        examples=["Fonte central de contexto estratégico e requisitos do case técnico na Dadosfera."],
    )

    class Config:
        frozen = True


class SkillInfo(BaseModel):
    """Representation of a modular skill for discovery."""
    name: str = Field(
        ...,
        description="Nome da skill modular (.agents/skills/).",
        examples=["cart-recovery-insights"],
    )
    description: str = Field(
        ...,
        description="Capacidades funcionais e diretrizes operacionais providas pela skill.",
        examples=["Define e organiza insights de negócio de recuperação de carrinhos abandonados."],
    )

    class Config:
        frozen = True


class ServerStatus(BaseModel):
    """System health, runtime metadata and discovered cluster assets."""
    status: str = Field(
        ...,
        description="Estado operacional do servidor web (ex: healthy).",
        examples=["healthy"],
    )
    active_agent_default: str = Field(
        ...,
        description="Nome do agente padrão configurado para inferência.",
        examples=["case-context-specialist"],
    )
    agents_count: int = Field(
        ...,
        description="Quantidade de agentes descobertos no workspace.",
        examples=[9],
    )
    skills_count: int = Field(
        ...,
        description="Quantidade de skills descobertas no workspace.",
        examples=[7],
    )
    agents: Sequence[AgentInfo] = Field(
        ...,
        description="Lista completa dos agentes disponíveis para orquestração.",
    )
    skills: Sequence[SkillInfo] = Field(
        ...,
        description="Lista completa das skills disponíveis no catálogo.",
    )

    class Config:
        frozen = True


class ErrorResponse(BaseModel):
    """Padronização OpenAPI para mensagens de erro HTTP estruturadas."""
    detail: str = Field(
        ...,
        description="Explicação detalhada da falha ou recurso não encontrado.",
        examples=["Agent 'invalid-agent' not found. Available: ['case-context-specialist', ...]"],
    )
    error_type: Optional[str] = Field(
        default="AgentServerError",
        description="Identificador da classe de erro.",
        examples=["NotFoundError"],
    )

    class Config:
        frozen = True

