"""Aba de Agentes & Skills: Central de Engenharia Multi-Agente & Dossiês Fidedignos."""

import streamlit as st

from app.components.fighter_select import (
    render_agent_view,
    render_agents_list,
    render_skill_view,
    render_skills_list,
)
from app.services.agents_service import (
    get_agent_by_id,
    get_all_agents,
    get_all_skills,
    get_skill_by_id,
)


def render_agents_tab() -> None:
    """Renderiza a visão dedicada de Agentes (sem header banner intermediário, direto no topo)."""
    all_agents = get_all_agents()

    if "selected_agent_id" not in st.session_state:
        st.session_state["selected_agent_id"] = all_agents[0].agent_id

    # Layout em 3 Colunas: Menu Esquerdo (0.85), Conteúdo Fidedigno (2.65), Gutter Direito (0.50)
    col_menu, col_content, _gutter_right = st.columns([0.85, 2.65, 0.50], gap="large")

    with col_menu:
        render_agents_list(all_agents, st.session_state["selected_agent_id"])

    with col_content:
        selected_agent = get_agent_by_id(st.session_state["selected_agent_id"]) or all_agents[0]
        render_agent_view(selected_agent)


def render_skills_tab() -> None:
    """Renderiza a visão dedicada de Skills (sem header banner intermediário, direto no topo)."""
    all_skills = get_all_skills()

    if "selected_skill_id" not in st.session_state:
        st.session_state["selected_skill_id"] = all_skills[0].skill_id

    # Layout em 3 Colunas: Menu Esquerdo (0.85), Conteúdo Fidedigno (2.65), Gutter Direito (0.50)
    col_menu, col_content, _gutter_right = st.columns([0.85, 2.65, 0.50], gap="large")

    with col_menu:
        render_skills_list(all_skills, st.session_state["selected_skill_id"])

    with col_content:
        selected_skill = get_skill_by_id(st.session_state["selected_skill_id"]) or all_skills[0]
        render_skill_view(selected_skill)
