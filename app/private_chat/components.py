"""Componentes visuais modulares para a interface isolada de Private Chat com Alerta Modal de Falha."""

import json
from typing import Any, Callable, Dict, List, Optional
import streamlit as st


def render_chat_header(health_info: Optional[Dict[str, Any]], base_url: str) -> None:
    """Renderiza a barra superior com status em tempo real do backend, modelo Gemini e atalhos OpenAPI."""
    is_online = health_info is not None and health_info.get("status") == "healthy"
    latency = health_info.get("_latency_ms", 0.0) if health_info else 0.0
    agents_count = health_info.get("agents_count", 0) if health_info else 0
    skills_count = health_info.get("skills_count", 0) if health_info else 0

    col_title, col_status = st.columns([2.6, 1.4], gap="medium")

    with col_title:
        st.markdown(
            """
            <div style="font-family: monospace; font-size: 1.28rem; font-weight: 800; color: #F8FAFC; letter-spacing: -0.02em;">
                💬 AGENT ORCHESTRATION CONSOLE <span style="font-size: 0.8rem; color: #38BDF8; font-weight: normal;">/chat</span>
            </div>
            <div style="font-size: 0.82rem; color: #94A3B8; margin-top: 0.2rem; display: flex; align-items: center; gap: 0.5rem; flex-wrap: wrap;">
                <span>Interface direta de inferência autônoma</span>
                <span style="background: rgba(56, 189, 248, 0.12); color: #38BDF8; border: 1px solid rgba(56, 189, 248, 0.3); border-radius: 4px; padding: 0.1rem 0.4rem; font-family: monospace; font-size: 0.72rem; font-weight: 600;">
                    🤖 Gemini 3.7 Flash
                </span>
                <span style="background: rgba(99, 102, 241, 0.12); color: #A5B4FC; border: 1px solid rgba(99, 102, 241, 0.3); border-radius: 4px; padding: 0.1rem 0.4rem; font-family: monospace; font-size: 0.72rem;">
                    📄 OpenAPI 3.1.0
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_status:
        if is_online:
            st.markdown(
                f"""
                <div style="text-align: right;">
                    <span class="private-chat-badge-online">
                        🟢 CLUSTER ONLINE ({latency}ms)
                    </span>
                    <div style="font-family: monospace; font-size: 0.72rem; color: #64748B; margin-top: 0.3rem;">
                        {agents_count} Agentes &bull; {skills_count} Skills
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                """
                <div style="text-align: right;">
                    <span class="private-chat-badge-offline">
                        🔴 SERVER OFFLINE (8000)
                    </span>
                    <div style="font-family: monospace; font-size: 0.70rem; color: #EF4444; margin-top: 0.3rem;">
                        Execute: <code>python make.py agent-server</code>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_connection_failure_alert(base_url: str, error_detail: Optional[str] = None) -> None:
    """Renderiza um alerta visual de alta visibilidade e popup explicativo quando a comunicação com o backend falha."""
    st.markdown(
        f"""
        <div style="background: linear-gradient(135deg, rgba(239, 68, 68, 0.15) 0%, rgba(153, 27, 27, 0.25) 100%);
                    border: 1px solid #EF4444; border-left: 5px solid #DC2626; border-radius: 8px;
                    padding: 1.1rem 1.3rem; margin-bottom: 1.2rem; color: #FEE2E2;">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div>
                    <div style="font-weight: 700; font-size: 1.02rem; color: #FCA5A5; display: flex; align-items: center; gap: 0.5rem;">
                        ⚠️ FALHA DE COMUNICAÇÃO COM O BACKEND AUTÔNOMO
                    </div>
                    <div style="font-size: 0.85rem; color: #FECACA; margin-top: 0.35rem; line-height: 1.5;">
                        O console <code>/chat</code> não conseguiu se conectar ao <strong>Antigravity Agent Server</strong> em <code>{base_url}</code>.
                        {f"<br><span style='color: #F87171; font-family: monospace; font-size: 0.78rem;'>Detalhes: {error_detail}</span>" if error_detail else ""}
                    </div>
                </div>
            </div>
            <div style="margin-top: 0.9rem; padding: 0.7rem 0.9rem; background: #0B0F19; border-radius: 6px; border: 1px solid #374151;">
                <div style="font-family: monospace; font-size: 0.78rem; color: #94A3B8; margin-bottom: 0.3rem;">
                    💡 Para inicializar o backend autônomo FastAPI (Gemini 3.7 Flash + OpenAPI 3.1.0):
                </div>
                <code style="color: #38BDF8; font-size: 0.88rem; font-weight: bold;">python make.py agent-server</code>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_agent_selection_panel(
    agents: List[Dict[str, str]],
    current_agent: str,
    on_change: Optional[Callable[[str], None]] = None,
) -> str:
    """Renderiza o painel de seleção e inspeção de capacidades do agente ativo."""
    if not agents:
        st.warning("⚠️ Nenhum agente retornado pelo cluster. Verifique a conexão com o backend.")
        return current_agent

    agent_names = [a.get("name", "") for a in agents]
    current_index = agent_names.index(current_agent) if current_agent in agent_names else 0

    selected = st.selectbox(
        label="🎯 Selecione o Agente Especialista:",
        options=agent_names,
        index=current_index,
        key="private_chat_agent_selector",
        help="Agentes cadastrados e orquestrados de forma 100% autônoma pelo servidor via Gemini 3.7 Flash.",
    )

    # Localizar metadados do agente selecionado
    selected_meta = next((a for a in agents if a.get("name") == selected), None)
    if selected_meta:
        st.markdown(
            f"""
            <div class="agent-active-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span class="agent-active-name">🤖 {selected_meta.get('name')}</span>
                    <span style="font-family: monospace; font-size: 0.72rem; color: #38BDF8; background: rgba(56, 189, 248, 0.1); padding: 0.15rem 0.5rem; border-radius: 4px;">
                        Google Gemini 3.7 Flash
                    </span>
                </div>
                <div class="agent-active-desc">{selected_meta.get('description', 'Sem descrição.')}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    return selected


def render_quick_prompt_chips() -> Optional[str]:
    """Renderiza botões de ação rápida para perguntas frequentes e retorna o prompt se clicado."""
    st.markdown(
        """
        <div style="font-family: monospace; font-size: 0.78rem; font-weight: 600; color: #64748B; margin-bottom: 0.5rem;">
            ⚡ PROMPTS DE ACELERAÇÃO ANALÍTICA:
        </div>
        """,
        unsafe_allow_html=True,
    )

    prompts = [
        ("📊 Diagnóstico de Abandono", "Gere um diagnóstico conciso dos principais motivos de abandono de carrinhos e o impacto no GMV."),
        ("💰 Simulação de ROI", "Explique como funciona o simulador prescritivo de ROI e as faixas ótimas de desconto para recuperação."),
        ("🧠 Requisitos do Case", "Quais são os 9 requisitos do case técnico na Dadosfera e quais artefatos foram entregues?"),
        ("🛠️ Skills & Ferramentas", "Quais skills e ferramentas estão integradas no cluster para execução autônoma?"),
    ]

    cols = st.columns(len(prompts), gap="small")
    clicked_prompt: Optional[str] = None

    for i, (label, prompt_text) in enumerate(prompts):
        with cols[i]:
            if st.button(label, key=f"chip_prompt_{i}", use_container_width=True):
                clicked_prompt = prompt_text

    return clicked_prompt


def render_chat_message(role: str, content: str, agent_name: Optional[str] = None, meta: Optional[str] = None) -> None:
    """Renderiza uma única mensagem do histórico de conversação com estilização rica."""
    if role == "user":
        st.markdown(
            f"""
            <div class="chat-message-user">
                <div class="chat-message-meta">
                    <span>👤 VOCÊ</span>
                    <span>{meta or ''}</span>
                </div>
                <div style="font-size: 0.94rem; line-height: 1.5; white-space: pre-wrap;">{content}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
            <div class="chat-message-agent">
                <div class="chat-message-meta">
                    <span style="color: #818CF8; font-weight: 700;">🤖 {agent_name or 'AGENTE AUTÔNOMO'}</span>
                    <span>{meta or ''}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(content)


def render_openapi_inspector_drawer(openapi_spec: Optional[Dict[str, Any]], base_url: str) -> None:
    """Renderiza um inspetor interativo dos contratos e documentação OpenAPI 3.1.0."""
    with st.expander("📖 Inspetor OpenAPI 3.1.0 & Contratos da API", expanded=False):
        if not openapi_spec:
            st.info("ℹ️ Servidor offline. Inicie o backend (`python make.py agent-server`) para carregar a documentação interativa ao vivo.")
            return

        info = openapi_spec.get("info", {})
        st.markdown(
            f"""
            <div style="font-family: monospace; font-size: 0.95rem; font-weight: bold; color: #38BDF8;">
                📄 {info.get('title', 'API')} <span style="color: #94A3B8;">v{info.get('version', '1.0.0')}</span>
            </div>
            <div style="font-size: 0.82rem; color: #CBD5E1; margin: 0.3rem 0 0.8rem 0;">
                {info.get('description', '')}
            </div>
            """,
            unsafe_allow_html=True,
        )

        col_docs1, col_docs2, col_docs3 = st.columns(3)
        with col_docs1:
            st.link_button("🌐 Abrir Swagger UI (/docs)", f"{base_url.rstrip('/')}/docs", use_container_width=True)
        with col_docs2:
            st.link_button("📑 Abrir ReDoc (/redoc)", f"{base_url.rstrip('/')}/redoc", use_container_width=True)
        with col_docs3:
            st.link_button("⚙️ Raw OpenAPI JSON", f"{base_url.rstrip('/')}/openapi.json", use_container_width=True)

        st.divider()
        st.markdown("#### 🛣️ Endpoints Mapeados na Especificação")

        paths = openapi_spec.get("paths", {})
        for path_key, path_obj in paths.items():
            for method, op_details in path_obj.items():
                pill_class = "pill-get" if method.upper() == "GET" else "pill-post"
                summary = op_details.get("summary", "")
                tags = ", ".join(op_details.get("tags", []))

                st.markdown(
                    f"""
                    <div style="background: #0B0F19; border: 1px solid #1E293B; border-radius: 6px; padding: 0.6rem 0.9rem; margin-bottom: 0.5rem; font-family: monospace;">
                        <span class="openapi-endpoint-pill {pill_class}">{method.upper()}</span>
                        <strong style="color: #F8FAFC;">{path_key}</strong>
                        <span style="color: #64748B; font-size: 0.78rem; margin-left: 0.8rem;">[{tags}] {summary}</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        st.markdown("#### 💻 Exemplo cURL de Consumo Direto")
        curl_code = f"""curl -X POST "{base_url.rstrip('/')}/chat" \\
  -H "Content-Type: application/json" \\
  -d '{{\"agent_name\": \"case-context-specialist\", \"message\": \"Explique o case da Dadosfera.\"}}'"""
        st.code(curl_code, language="bash")
