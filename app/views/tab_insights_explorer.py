"""Aba de Galeria de Insights & Artefatos: Navegação por Tipos, Gráficos 300 DPI e Specs Markdown."""

import streamlit as st

from app.components.insights_view import (
    render_insight_detail,
    render_insight_sub_navigation,
    render_insights_header,
)
from app.services.insights_service import get_insights_by_category


def render_insights_explorer_tab() -> None:
    """Renderiza a view consolidada da Galeria de Insights & Artefatos."""
    # 1. Header e seletor de Categoria (Descritivo, Risco, Prescritivo, Inteligência & IA)
    selected_cat = render_insights_header()

    # 2. Itens da categoria selecionada
    items = get_insights_by_category(selected_cat)

    if not items:
        st.info("Nenhum insight cadastrado para esta categoria.")
        return

    # 3. Navegação Horizontal em Abas/Pills para os Insights da Categoria
    selected_insight = render_insight_sub_navigation(items)

    # 4. Detalhe do Insight com Tabs (Gráfico 300 DPI vs Spec Markdown Deslizável)
    if selected_insight:
        render_insight_detail(selected_insight)
