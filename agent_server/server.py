"""FastAPI web server exposing autonomous Antigravity Agents and Skills with OpenAPI 3.1.0 standardization."""

import json
from typing import Sequence
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from agent_server.config import (
    CONTACT_INFO,
    DEFAULT_AGENT_NAME,
    LICENSE_INFO,
    OPENAPI_TAGS,
    SERVER_DESCRIPTION,
    SERVER_TITLE,
    SERVER_VERSION,
)
from agent_server.discovery import (
    find_agent_by_name,
    get_skills_paths,
    scan_all_agents,
    scan_all_skills,
)
from agent_server.runtime import execute_agent_turn, stream_agent_turn
from agent_server.types import (
    AgentInfo,
    ChatInput,
    ChatOutput,
    ErrorResponse,
    ServerStatus,
    SkillInfo,
)


# ---------------------------------------------------------------------------
# FastAPI Application Factory & OpenAPI Configuration
# ---------------------------------------------------------------------------

def create_app() -> FastAPI:
    """Pure factory function to construct and configure the FastAPI application with OpenAPI 3.1.0."""
    app = FastAPI(
        title=SERVER_TITLE,
        description=SERVER_DESCRIPTION,
        version=SERVER_VERSION,
        openapi_tags=list(OPENAPI_TAGS),
        contact=dict(CONTACT_INFO),
        license_info=dict(LICENSE_INFO),
        openapi_url="/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # Enable CORS for local web UIs, Streamlit apps and external tools
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # -----------------------------------------------------------------------
    # Informational / Health Endpoints
    # -----------------------------------------------------------------------

    @app.get(
        "/health",
        response_model=ServerStatus,
        tags=["Health"],
        summary="Diagnóstico de Saúde e Cluster",
        description="Retorna o status operacional do servidor, agente default e inventário completo de agentes e skills descobertos.",
        response_description="Status de integridade do cluster e ativos registrados.",
        responses={
            200: {"description": "Servidor saudável e catálogo sincronizado.", "model": ServerStatus},
        },
    )
    async def get_health_status() -> ServerStatus:
        """Returns health status along with all discovered agents and skills."""
        agents = scan_all_agents()
        skills = scan_all_skills()

        return ServerStatus(
            status="healthy",
            active_agent_default=DEFAULT_AGENT_NAME,
            agents_count=len(agents),
            skills_count=len(skills),
            agents=[
                AgentInfo(name=a.name, description=a.description)
                for a in agents
            ],
            skills=[
                SkillInfo(name=s.name, description=s.description)
                for s in skills
            ],
        )

    @app.get(
        "/agents",
        response_model=Sequence[AgentInfo],
        tags=["Discovery"],
        summary="Catálogo de Agentes Disponíveis",
        description="Lista todos os agentes autônomos cadastrados no diretório `.agents/agents/` com suas respectivas especialidades.",
        response_description="Coleção de metadados dos agentes descobertos.",
        responses={
            200: {"description": "Lista de agentes disponíveis para inferência.", "model": Sequence[AgentInfo]},
        },
    )
    async def list_agents() -> Sequence[AgentInfo]:
        """Lists all agents discovered in .agents/agents/."""
        agents = scan_all_agents()
        return [AgentInfo(name=a.name, description=a.description) for a in agents]

    @app.get(
        "/skills",
        response_model=Sequence[SkillInfo],
        tags=["Discovery"],
        summary="Catálogo de Skills Modulares",
        description="Lista todas as diretrizes funcionais e habilidades técnicas cadastradas em `.agents/skills/`.",
        response_description="Coleção de metadados das skills descobertas.",
        responses={
            200: {"description": "Lista de skills carregadas no workspace.", "model": Sequence[SkillInfo]},
        },
    )
    async def list_skills() -> Sequence[SkillInfo]:
        """Lists all skills discovered in .agents/skills/."""
        skills = scan_all_skills()
        return [SkillInfo(name=s.name, description=s.description) for s in skills]

    # -----------------------------------------------------------------------
    # Agent Invocation Endpoints (100% Autonomous)
    # -----------------------------------------------------------------------

    @app.post(
        "/chat",
        response_model=ChatOutput,
        tags=["Inference"],
        summary="Execução Autônoma de Turno do Agente (Síncrono)",
        description=(
            "Executa um turno de raciocínio 100% autônomo com o agente especificado.\n"
            "O agente tem acesso automático a todas as skills do workspace e políticas de auto-aprovação ativas."
        ),
        response_description="Resultado textual do turno e status de execução.",
        responses={
            200: {"description": "Turno executado com sucesso.", "model": ChatOutput},
            404: {"description": "Agente especificado não encontrado.", "model": ErrorResponse},
            500: {"description": "Erro interno durante orquestração do turno.", "model": ErrorResponse},
        },
    )
    async def chat_with_agent(payload: ChatInput) -> ChatOutput:
        """Executes a 100% autonomous turn with the designated agent."""
        agents = scan_all_agents()
        agent_meta = find_agent_by_name(agents, payload.agent_name)

        if agent_meta is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Agent '{payload.agent_name}' not found. Available: {[a.name for a in agents]}",
            )

        skills_paths = get_skills_paths()

        try:
            response_text = await execute_agent_turn(
                agent_meta=agent_meta,
                skills_paths=skills_paths,
                prompt=payload.message,
            )
            return ChatOutput(
                agent_name=payload.agent_name,
                response=response_text,
                status="success",
            )
        except Exception as exc:
            return ChatOutput(
                agent_name=payload.agent_name,
                response="",
                status="error",
                error_message=str(exc),
            )

    @app.post(
        "/stream",
        tags=["Inference"],
        summary="Streaming de Inferência Token a Token (SSE)",
        description=(
            "Inicia uma sessão de streaming em tempo real via Server-Sent Events (SSE).\n"
            "Emite eventos `data: {\"token\": \"...\", \"agent\": \"...\"}` finalizando com `data: [DONE]`."
        ),
        response_description="Stream SSE contínuo de tokens de texto gerados pelo modelo.",
        responses={
            200: {
                "description": "Stream de tokens em tempo real.",
                "content": {"text/event-stream": {}},
            },
            404: {"description": "Agente especificado não encontrado.", "model": ErrorResponse},
        },
    )
    async def stream_agent(payload: ChatInput):
        """Streams agent response tokens in real-time via Server-Sent Events (SSE)."""
        agents = scan_all_agents()
        agent_meta = find_agent_by_name(agents, payload.agent_name)

        if agent_meta is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Agent '{payload.agent_name}' not found.",
            )

        skills_paths = get_skills_paths()

        async def sse_event_generator():
            try:
                async for token in stream_agent_turn(
                    agent_meta=agent_meta,
                    skills_paths=skills_paths,
                    prompt=payload.message,
                ):
                    data_payload = json.dumps({"token": token, "agent": payload.agent_name})
                    yield f"data: {data_payload}\n\n"
                yield "data: [DONE]\n\n"
            except Exception as exc:
                err_payload = json.dumps({"error": str(exc)})
                yield f"data: {err_payload}\n\n"

        return StreamingResponse(
            sse_event_generator(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
            },
        )

    return app


# Application Singleton for ASGI servers (uvicorn)
app: FastAPI = create_app()

