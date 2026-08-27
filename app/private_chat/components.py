"""Componentes visuais minimalistas e isolados no padrão ChatGPT para o Private Chat."""

from typing import Any, Callable, Dict, List, Optional
import streamlit as st


def render_sidebar_menu(
    agents: List[Dict[str, str]],
    current_agent: str,
    health_info: Optional[Dict[str, Any]],
    base_url: str,
) -> Dict[str, Any]:
    """Renderiza os controles no menu esquerdo com descrição do projeto, seletor de agentes e configurações."""
    is_online = health_info is not None and health_info.get("status") == "healthy"
    latency = health_info.get("_latency_ms", 0.0) if health_info else 0.0

    st.markdown(
        """
        <div class="sidebar-chat-desc-box">
            <div class="sidebar-chat-desc-title">💬 Assistente do Projeto</div>
            <div class="sidebar-chat-desc-text">
                Pergunte sobre as decisões de arquitetura e o racional de desenvolvimento do <strong>Pedro Sales</strong>: desde a modelagem Medallion no Lakehouse, pipelines declarativos e engenharia de features com GenAI, até a lógica do simulador de ROI e regras de negócio.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("➕ Novo Chat", key="btn_new_chat", use_container_width=True):
        st.session_state["private_chat_messages"] = []
        st.rerun()

    st.markdown("<div style='margin-top: 0.8rem;'></div>", unsafe_allow_html=True)

    # Seletor de Agente
    agent_names = [a.get("name", "") for a in agents] if agents else ["case-context-specialist"]
    current_idx = agent_names.index(current_agent) if current_agent in agent_names else 0

    selected_agent = st.selectbox(
        label="Especialista:",
        options=agent_names,
        index=current_idx,
        key="clean_chat_agent_selector",
        help="Agente autônomo responsável por responder.",
    )

    # Configurações minimalistas
    with st.expander("⚙️ Configurações", expanded=False):
        api_key_val = st.text_input(
            label="Chave Gemini (Opcional):",
            value=st.session_state.get("private_chat_api_key", ""),
            type="password",
            placeholder="AIzaSy...",
            key="clean_chat_api_key",
            help="Configurável também via arquivo .env (GEMINI_API_KEY).",
        )
        st.session_state["private_chat_api_key"] = api_key_val

        stream_mode = st.toggle(
            "Streaming em Tempo Real",
            value=st.session_state.get("private_chat_stream_mode", True),
            key="clean_chat_toggle_stream",
        )
        st.session_state["private_chat_stream_mode"] = stream_mode

    # Status de conexão no rodapé da sidebar
    if is_online:
        st.caption(f"🟢 Servidor Online ({latency}ms)")
    else:
        st.caption("🔴 Servidor Offline (Porta 8000)")

    return {
        "selected_agent": selected_agent,
    }


def render_welcome_hero() -> None:
    """Renderiza a saudação minimalista centralizada estilo ChatGPT quando não há histórico."""
    st.markdown(
        """
        <div class="chatgpt-welcome-hero">
            <div class="chatgpt-welcome-title">Dadosfera AI &bull; Concierge Técnico</div>
            <div class="chatgpt-welcome-subtitle">
                Converse com os agentes especializados sobre como <strong>Pedro Sales</strong> arquitetou as soluções deste case: modelagem Medallion, governança, embeddings vetoriais e otimização financeira de ROI.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_clean_message(role: str, content: str, agent_name: Optional[str] = None) -> None:
    """Renderiza mensagens no estilo limpo do ChatGPT."""
    if role == "user":
        st.markdown(
            f"""
            <div class="chat-turn-container">
                <div class="chat-bubble-user">
                    {content}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
            <div class="chat-turn-container">
                <div class="chat-bubble-assistant">
                    <div class="chat-assistant-header">
                        <span>🤖 {agent_name or 'Dadosfera AI'}</span>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        # Renderiza Markdown limpo do Streamlit
        st.markdown(content)


def render_clean_connection_alert(base_url: str, error_detail: Optional[str] = None) -> None:
    """Alerta clean quando o servidor de agentes estiver offline."""
    st.markdown(
        f"""
        <div class="chat-alert-clean">
            <div>
                <strong>⚠️ Servidor Offline:</strong> Backend não acessível em <code>{base_url}</code>.
            </div>
            <div>
                <code>python make.py agent-server</code>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
