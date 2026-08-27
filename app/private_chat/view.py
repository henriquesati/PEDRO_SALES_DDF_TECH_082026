"""View principal do Private Chat com interface limpa e minimalista no padrão ChatGPT."""

from typing import Any, Dict, List, Optional
import streamlit as st

from app.private_chat.client import (
    DEFAULT_SERVER_URL,
    check_server_health,
    fetch_agents_catalog,
    send_chat_turn,
    stream_chat_turn,
)
from app.private_chat.components import (
    render_clean_connection_alert,
    render_clean_message,
    render_sidebar_menu,
    render_welcome_hero,
)
from app.private_chat.styles import inject_private_chat_theme


def init_chat_session_state() -> None:
    """Inicializa as variáveis de estado de sessão do chat de forma pura e idempotente."""
    if "private_chat_messages" not in st.session_state:
        st.session_state["private_chat_messages"] = []

    if "private_chat_selected_agent" not in st.session_state:
        st.session_state["private_chat_selected_agent"] = "case-context-specialist"

    if "private_chat_server_url" not in st.session_state:
        st.session_state["private_chat_server_url"] = DEFAULT_SERVER_URL

    if "private_chat_api_key" not in st.session_state:
        st.session_state["private_chat_api_key"] = ""

    if "private_chat_stream_mode" not in st.session_state:
        st.session_state["private_chat_stream_mode"] = True


def render_private_chat_page() -> None:
    """Renderiza a interface clean estilo ChatGPT 100% isolada em app/private_chat/."""
    init_chat_session_state()
    inject_private_chat_theme()

    base_url = st.session_state["private_chat_server_url"]

    # Obter diagnósticos do backend
    health_info = check_server_health(base_url)
    agents_catalog = fetch_agents_catalog(base_url)

    # Fallback caso servidor esteja offline para manter a UX amigável
    if not agents_catalog:
        agents_catalog = [
            {"name": "case-context-specialist", "description": "Contexto estratégico e requisitos do case."},
            {"name": "data-strategy-analyst", "description": "Consultor sênior de dados e camadas analíticas."},
            {"name": "cart-recovery-insights", "description": "Insights e oportunidades de negócio de resgate."},
            {"name": "charts-maker", "description": "Geração executiva de gráficos analíticos com Ground Truth."},
            {"name": "platform-registry-consultant", "description": "Mapeamento oficial de ativos da plataforma."},
        ]

    # 1. Menu Lateral Minimalista (Descrição, Novo Chat, Seletor de Agente, API Key)
    with st.sidebar:
        sidebar_data = render_sidebar_menu(
            agents=agents_catalog,
            current_agent=st.session_state["private_chat_selected_agent"],
            health_info=health_info,
            base_url=base_url,
        )
        selected_agent = sidebar_data["selected_agent"]
        st.session_state["private_chat_selected_agent"] = selected_agent

    # 2. Área Central de Conversação
    st.markdown('<div class="chatgpt-layout-container">', unsafe_allow_html=True)

    # Alerta de Falha de Conexão se o backend estiver offline
    if health_info is None:
        render_clean_connection_alert(base_url)

    # Se não houver mensagens, renderiza o Hero centralizado
    messages = st.session_state["private_chat_messages"]
    if not messages:
        render_welcome_hero()
    else:
        for msg in messages:
            render_clean_message(
                role=msg["role"],
                content=msg["content"],
                agent_name=msg.get("agent_name"),
            )

    st.markdown('</div>', unsafe_allow_html=True)

    # 3. Input do Usuário na Base da Página
    user_input = st.chat_input("Pergunte sobre o projeto e seu desenvolvimento...")

    if user_input:
        active_api_key = st.session_state.get("private_chat_api_key") or None

        # Adicionar mensagem do usuário ao histórico
        st.session_state["private_chat_messages"].append(
            {
                "role": "user",
                "content": user_input,
            }
        )

        # Se for modo streaming e o servidor estiver online
        if st.session_state["private_chat_stream_mode"] and health_info is not None:
            render_clean_message(role="user", content=user_input)

            with st.chat_message("assistant"):
                token_stream = stream_chat_turn(
                    message=user_input,
                    agent_name=selected_agent,
                    base_url=base_url,
                    api_key=active_api_key,
                )
                full_response = st.write_stream(token_stream)

            st.session_state["private_chat_messages"].append(
                {
                    "role": "assistant",
                    "content": full_response or "(Resposta vazia)",
                    "agent_name": selected_agent,
                }
            )
            st.rerun()
        else:
            # Modo síncrono (/chat) com spinner
            with st.spinner("Processando resposta..."):
                resp = send_chat_turn(
                    message=user_input,
                    agent_name=selected_agent,
                    base_url=base_url,
                    api_key=active_api_key,
                )

            resp_text = resp.get("response") or resp.get("error_message") or "Sem resposta do servidor."
            status = resp.get("status", "error")

            if status != "success":
                st.toast("🚨 Falha ao comunicar com o servidor!", icon="⚠️")

            st.session_state["private_chat_messages"].append(
                {
                    "role": "assistant",
                    "content": resp_text,
                    "agent_name": selected_agent,
                }
            )
            st.rerun()
