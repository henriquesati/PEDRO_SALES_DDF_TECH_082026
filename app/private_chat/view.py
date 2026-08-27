"""View principal da página isolada Private Chat."""

import datetime
from typing import Any, Dict, List, Optional
import streamlit as st

from app.private_chat.client import (
    DEFAULT_SERVER_URL,
    check_server_health,
    fetch_agents_catalog,
    fetch_openapi_spec,
    send_chat_turn,
    stream_chat_turn,
)
from app.private_chat.components import (
    render_agent_selection_panel,
    render_chat_header,
    render_chat_message,
    render_connection_failure_alert,
    render_openapi_inspector_drawer,
    render_quick_prompt_chips,
)
from app.private_chat.styles import inject_private_chat_theme


def init_chat_session_state() -> None:
    """Inicializa as variáveis de estado de sessão do chat de forma pura e idempotente."""
    if "private_chat_messages" not in st.session_state:
        st.session_state["private_chat_messages"] = [
            {
                "role": "assistant",
                "content": (
                    "Olá! Sou a interface de orquestração autônoma multi-agente do ecossistema Dadosfera.\n\n"
                    "Todos os 10 agentes e 10 skills do workspace estão conectados via **FastAPI** e padronizados "
                    "sob a especificação **OpenAPI 3.1.0**.\n\n"
                    "Selecione um agente especialista e envie sua dúvida ou utilize os botões rápidos abaixo!"
                ),
                "agent_name": "case-context-specialist",
                "meta": "Inicialização do Sistema",
            }
        ]

    if "private_chat_selected_agent" not in st.session_state:
        st.session_state["private_chat_selected_agent"] = "case-context-specialist"

    if "private_chat_server_url" not in st.session_state:
        st.session_state["private_chat_server_url"] = DEFAULT_SERVER_URL

    if "private_chat_stream_mode" not in st.session_state:
        st.session_state["private_chat_stream_mode"] = True


def render_private_chat_page() -> None:
    """Renderiza a página completa do Private Chat isolada do restante do aplicativo."""
    init_chat_session_state()
    inject_private_chat_theme()

    base_url = st.session_state["private_chat_server_url"]

    # Obter diagnósticos do backend
    health_info = check_server_health(base_url)
    agents_catalog = fetch_agents_catalog(base_url)
    openapi_spec = fetch_openapi_spec(base_url)

    # Fallback caso servidor esteja offline para manter a UX amigável
    if not agents_catalog:
        agents_catalog = [
            {"name": "case-context-specialist", "description": "Contexto estratégico e requisitos do case."},
            {"name": "data-strategy-analyst", "description": "Consultor sênior de dados e camadas analíticas."},
            {"name": "cart-recovery-insights", "description": "Insights e oportunidades de negócio de resgate."},
            {"name": "charts-maker", "description": "Geração executiva de gráficos analíticos com Ground Truth."},
            {"name": "platform-registry-consultant", "description": "Mapeamento oficial de ativos da plataforma."},
        ]

    # 1. Header do Chat
    render_chat_header(health_info, base_url)

    # Alerta de Falha de Conexão com o Backend (se offline)
    if health_info is None:
        render_connection_failure_alert(
            base_url=base_url,
            error_detail="Servidor FastAPI offline ou inacessível em http://127.0.0.1:8000.",
        )

    # 2. Configurações de Conexão e Agente
    col_agent, col_settings = st.columns([2.5, 1.5], gap="medium")

    with col_agent:
        selected_agent = render_agent_selection_panel(
            agents=agents_catalog,
            current_agent=st.session_state["private_chat_selected_agent"],
        )
        st.session_state["private_chat_selected_agent"] = selected_agent

    with col_settings:
        with st.container(border=True):
            st.markdown(
                "<div style='font-family: monospace; font-size: 0.8rem; font-weight: bold; color: #94A3B8;'>⚙️ CONFIGURAÇÕES DE RUNTIME</div>",
                unsafe_allow_html=True,
            )
            stream_mode = st.toggle(
                "Streaming em Tempo Real (SSE)",
                value=st.session_state["private_chat_stream_mode"],
                key="toggle_stream_mode",
            )
            st.session_state["private_chat_stream_mode"] = stream_mode

            col_btn_clear, col_btn_reload = st.columns(2)
            with col_btn_clear:
                if st.button("🗑️ Limpar Chat", key="btn_clear_chat", use_container_width=True):
                    st.session_state["private_chat_messages"] = []
                    st.rerun()
            with col_btn_reload:
                if st.button("🔄 Reconectar", key="btn_reconnect_server", use_container_width=True):
                    st.rerun()

    # 3. Inspetor OpenAPI 3.1.0
    render_openapi_inspector_drawer(openapi_spec, base_url)

    # 4. Chips de Prompts Rápidos
    clicked_chip_prompt = render_quick_prompt_chips()

    st.divider()

    # 5. Feed de Mensagens
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state["private_chat_messages"]:
            render_chat_message(
                role=msg["role"],
                content=msg["content"],
                agent_name=msg.get("agent_name"),
                meta=msg.get("meta"),
            )

    # 6. Processamento de Entrada (Input do Chat ou Chip Clicado)
    user_input = st.chat_input("Digite sua mensagem para o agente autônomo...")
    prompt_to_send = clicked_chip_prompt or user_input

    if prompt_to_send:
        now_str = datetime.datetime.now().strftime("%H:%M:%S")

        # Adicionar mensagem do usuário ao histórico
        st.session_state["private_chat_messages"].append(
            {
                "role": "user",
                "content": prompt_to_send,
                "meta": now_str,
            }
        )

        # Se for modo streaming e o servidor estiver online
        if st.session_state["private_chat_stream_mode"] and health_info is not None:
            # Renderiza a mensagem do usuário imediatamente
            render_chat_message(role="user", content=prompt_to_send, meta=now_str)

            # Placeholder para streaming de resposta
            with st.chat_message("assistant"):
                st.markdown(f"**🤖 {selected_agent}** *(Gerando resposta...)*")
                token_stream = stream_chat_turn(
                    message=prompt_to_send,
                    agent_name=selected_agent,
                    base_url=base_url,
                )
                full_response = st.write_stream(token_stream)

            st.session_state["private_chat_messages"].append(
                {
                    "role": "assistant",
                    "content": full_response or "(Resposta vazia)",
                    "agent_name": selected_agent,
                    "meta": datetime.datetime.now().strftime("%H:%M:%S"),
                }
            )
            st.rerun()
        else:
            # Modo síncrono (/chat) com spinner
            with st.spinner(f"Agente '{selected_agent}' está processando..."):
                resp = send_chat_turn(
                    message=prompt_to_send,
                    agent_name=selected_agent,
                    base_url=base_url,
                )

            resp_text = resp.get("response") or resp.get("error_message") or "Sem resposta."
            status = resp.get("status", "error")
            elapsed = resp.get("_elapsed_sec", 0.0)

            if status != "success":
                st.toast("🚨 Falha ao comunicar com o Backend FastAPI!", icon="⚠️")

            meta_info = f"{now_str} &bull; {elapsed}s" if status == "success" else f"{now_str} &bull; ⚠️ Erro de Comunicação"

            st.session_state["private_chat_messages"].append(
                {
                    "role": "assistant",
                    "content": resp_text,
                    "agent_name": selected_agent,
                    "meta": meta_info,
                }
            )
            st.rerun()

