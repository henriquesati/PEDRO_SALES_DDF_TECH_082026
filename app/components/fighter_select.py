"""Componentes visuais da Central do Avaliador: Agentes e Skills (Layout Refinado: Header Integrado, Cards 100% e Referências Expandidas sem Título)."""

import streamlit as st
from app.services.agents_service import get_file_content
def render_evaluator_header() -> str:
    """Renderiza o header unificado com título e botões Agentes / Skills DENTRO da mesma caixa delimitadora."""
    if "evaluator_sub_tab" not in st.session_state:
        st.session_state["evaluator_sub_tab"] = "Agentes"

    current_tab = st.session_state["evaluator_sub_tab"]

    with st.container(border=True):
        st.markdown('<span class="evaluator-header-marker" style="display:none;"></span>', unsafe_allow_html=True)
        col_title, col_btn_ag, col_btn_sk = st.columns([3.2, 0.85, 0.85], gap="small")

        with col_title:
            st.markdown(
                '<div style="padding-left: 0.2rem;">'
                '<div style="font-family: monospace; font-size: 1.08rem; font-weight: bold; color: #F0F6FC; line-height: 1.2;">Agentes & Engenharia</div>'
                '<div style="font-size: 0.70rem; color: #94A3B8; margin-top: 0.05rem;">Console Multi-Agente e Dossiês</div>'
                '</div>',
                unsafe_allow_html=True
            )

        with col_btn_ag:
            if st.button("Agentes", key="btn_eval_hdr_agents", type="primary" if current_tab == "Agentes" else "secondary", use_container_width=True):
                st.session_state["evaluator_sub_tab"] = "Agentes"
                st.rerun()

        with col_btn_sk:
            if st.button("Skills", key="btn_eval_hdr_skills", type="primary" if current_tab == "Skills" else "secondary", use_container_width=True):
                st.session_state["evaluator_sub_tab"] = "Skills"
                st.rerun()

    return current_tab


def render_agents_list(agents: tuple[AgentProfile, ...], selected_id: str) -> None:
    """Renderiza o menu lateral com slots de agentes expandidos a 100% da largura útil."""
    st.markdown(
        '<div style="font-family: monospace; font-size: 0.74rem; font-weight: 700; color: #38BDF8; margin-bottom: 0.35rem; text-transform: uppercase; letter-spacing: 0.5px; border-bottom: 1px solid #1E293B; padding-bottom: 0.25rem; text-align: left; width: 100%;">'
        'AGENTES DISPONÍVEIS'
        '</div>',
        unsafe_allow_html=True
    )

    for agent in agents:
        is_active = (agent.agent_id == selected_id)
        btn_label = f"{agent.arcade_title}\n{agent.display_name}"

        if st.button(
            label=btn_label,
            key=f"btn_agent_slot_{agent.agent_id}",
            use_container_width=True,
            type="primary" if is_active else "secondary"
        ):
            st.session_state["selected_agent_id"] = agent.agent_id
            st.rerun()


def render_skills_list(skills: tuple[SkillProfile, ...], selected_id: str) -> None:
    """Renderiza o menu lateral com slots de skills expandidos a 100% da largura útil."""
    st.markdown(
        '<div style="font-family: monospace; font-size: 0.74rem; font-weight: 700; color: #34D399; margin-bottom: 0.35rem; text-transform: uppercase; letter-spacing: 0.5px; border-bottom: 1px solid #1E293B; padding-bottom: 0.25rem; text-align: left; width: 100%;">'
        'SKILLS DISPONÍVEIS'
        '</div>',
        unsafe_allow_html=True
    )

    for skill in skills:
        is_active = (skill.skill_id == selected_id)
        btn_label = f"{skill.archetype.upper()}\n{skill.display_name}"

        if st.button(
            label=btn_label,
            key=f"btn_skill_slot_{skill.skill_id}",
            use_container_width=True,
            type="primary" if is_active else "secondary"
        ):
            st.session_state["selected_skill_id"] = skill.skill_id
            st.rerun()


def render_agent_view(agent: AgentProfile) -> None:
    """Renderiza a visão do agente: Header Compacto (-10%), Dossiê Principal Amplo e Referências Expandidas para Cima (sem título)."""
    file_text = get_file_content(agent.file_path)

    # 1. Header de Identidade (Padding reduzido em 10% e mais compacto)
    header_html = (
        '<div style="background-color: #090D16; border: 1px solid #1E293B; border-top: 3px solid #38BDF8; border-radius: 8px; padding: 0.70rem 1.0rem; margin-bottom: 0.45rem;">'
        '<div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.4rem;">'
        '<div>'
        f'<div style="font-family: monospace; font-size: 0.72rem; color: #38BDF8; font-weight: bold; letter-spacing: 0.5px;">{agent.arcade_title}</div>'
        f'<div style="font-size: 1.15rem; font-weight: 700; color: #F0F6FC; margin-top: 0.05rem;">{agent.display_name}</div>'
        f'<div style="font-family: monospace; font-size: 0.72rem; color: #94A3B8; margin-top: 0.15rem;"><code>{agent.file_path}</code></div>'
        '</div>'
        '<div style="text-align: right;">'
        f'<span style="font-family: monospace; font-size: 0.68rem; color: #A7F3D0; background-color: #064E3B; border: 1px solid #059669; padding: 0.18rem 0.45rem; border-radius: 4px;">Modo: {agent.mode}</span>'
        '</div>'
        '</div>'
        '</div>'
    )
    st.markdown(header_html, unsafe_allow_html=True)

    # 2. Visualizador Deslizável Principal
    with st.container(height=460):
        st.code(file_text, language="markdown")

    # 3. Seção de Referências Expandida para Cima (sem string de título, height=210)
    st.markdown("<div style='margin-top: 0.4rem;'></div>", unsafe_allow_html=True)
    with st.container(height=210):
        st.markdown("**📁 Diretórios & Skills Vinculadas:**")
        for s in agent.skills_equipped:
            st.markdown(f"- <code>.agents/skills/{s}/</code> — *Diretório e especificações de execução*", unsafe_allow_html=True)

        st.markdown("<div style='margin-top: 0.4rem;'></div>", unsafe_allow_html=True)
        st.markdown("**📄 Especificações & Artefatos Fonte:**")
        for art in agent.artifacts_managed:
            st.markdown(f"- <code>{art}</code>", unsafe_allow_html=True)


def render_skill_view(skill: SkillProfile) -> None:
    """Renderiza a visão da skill: Header Compacto (-10%), Dossiê Principal Amplo e Referências Expandidas para Cima (sem título)."""
    file_text = get_file_content(skill.file_path)

    # 1. Header de Identidade (Padding reduzido em 10% e mais compacto)
    header_html = (
        '<div style="background-color: #090D16; border: 1px solid #1E293B; border-top: 3px solid #10B981; border-radius: 8px; padding: 0.70rem 1.0rem; margin-bottom: 0.45rem;">'
        '<div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.4rem;">'
        '<div>'
        f'<div style="font-family: monospace; font-size: 0.72rem; color: #34D399; font-weight: bold; letter-spacing: 0.5px;">{skill.archetype.upper()}</div>'
        f'<div style="font-size: 1.15rem; font-weight: 700; color: #F0F6FC; margin-top: 0.05rem;">{skill.display_name}</div>'
        f'<div style="font-family: monospace; font-size: 0.72rem; color: #94A3B8; margin-top: 0.15rem;"><code>{skill.file_path}</code></div>'
        '</div>'
        '<div style="text-align: right;">'
        '<span style="font-family: monospace; font-size: 0.68rem; color: #6EE7B7; background-color: #064E3B; border: 1px solid #059669; padding: 0.18rem 0.45rem; border-radius: 4px;">Skill Ativa</span>'
        '</div>'
        '</div>'
        '</div>'
    )
    st.markdown(header_html, unsafe_allow_html=True)

    # 2. Visualizador Deslizável Principal
    with st.container(height=460):
        st.code(file_text, language="markdown")

    # 3. Seção de Referências Expandida para Cima (sem string de título, height=210)
    st.markdown("<div style='margin-top: 0.4rem;'></div>", unsafe_allow_html=True)
    with st.container(height=210):
        st.markdown("**🛠️ Ferramentas Habilitadas:**")
        tools_str = " &nbsp; ".join([f"`{t}`" for t in skill.tools_available])
        st.markdown(tools_str)

        st.markdown("<div style='margin-top: 0.4rem;'></div>", unsafe_allow_html=True)
        st.markdown("**📄 Especificações & Artefatos Fonte:**")
        for art in skill.artifacts_managed:
            st.markdown(f"- <code>{art}</code>", unsafe_allow_html=True)
