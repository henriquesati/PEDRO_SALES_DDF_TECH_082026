"""Componentes visuais para a Galeria de Insights & Artefatos (Layout Side-by-Side: Gráfico 300 DPI + Spec Markdown Deslizável)."""

import os
import streamlit as st
from app.services.agents_service import get_file_content
from app.services.insights_service import (
    InsightItem,
    get_categories,
    get_insights_by_category,
)


def render_insights_header() -> str:
    """Renderiza o cabeçalho executivo e o seletor de categorias dos insights."""
    categories = get_categories()
    if "selected_insight_cat" not in st.session_state:
        st.session_state["selected_insight_cat"] = categories[0][0]

    current_cat = st.session_state["selected_insight_cat"]

    st.markdown(
        '<div style="background: #090D16; border: 1px solid #1E293B; border-top: 3px solid #38BDF8; border-radius: 8px; padding: 0.85rem 1.2rem; margin-bottom: 0.8rem;">'
        '<div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: gap; gap: 0.5rem;">'
        '<div>'
        '<div style="font-family: monospace; font-size: 1.35rem; font-weight: bold; color: #F0F6FC;">Galeria de Insights</div>'
        '<div style="font-size: 0.80rem; color: #94A3B8; margin-top: 0.15rem;">Explorador de Blueprints, Gráficos Executivos (300 DPI) e Especificações Analíticas do Diretório <code>insights/</code></div>'
        '</div>'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )

    # 4 Cards/Botões de Categoria no Topo
    cols = st.columns(len(categories))
    for i, (cat_key, cat_label, cat_col) in enumerate(categories):
        with cols[i]:
            is_active = (current_cat == cat_key)
            if st.button(
                label=cat_label,
                key=f"btn_cat_tab_{cat_key}",
                type="primary" if is_active else "secondary",
                use_container_width=True
            ):
                st.session_state["selected_insight_cat"] = cat_key
                # Reset selected item for this category
                items = get_insights_by_category(cat_key)
                if items:
                    st.session_state["selected_insight_id"] = items[0].insight_id
                st.rerun()

    return st.session_state["selected_insight_cat"]


def render_insight_sub_navigation(items: tuple[InsightItem, ...]) -> InsightItem:
    """Renderiza a barra de navegação estilo pills web para alternar entre os insights da categoria."""
    if not items:
        return None

    if "selected_insight_id" not in st.session_state:
        st.session_state["selected_insight_id"] = items[0].insight_id

    # Garante que o ID selecionado pertence à categoria atual
    valid_ids = [item.insight_id for item in items]
    if st.session_state["selected_insight_id"] not in valid_ids:
        st.session_state["selected_insight_id"] = items[0].insight_id

    st.markdown("<div style='margin-top: 0.6rem;'></div>", unsafe_allow_html=True)

    # Navegação horizontal em pills
    cols = st.columns(len(items))
    for idx, item in enumerate(items):
        with cols[idx]:
            is_sel = (item.insight_id == st.session_state["selected_insight_id"])
            if st.button(
                label=item.title.split("&")[0].strip(),
                key=f"sub_nav_btn_{item.insight_id}",
                type="primary" if is_sel else "secondary",
                use_container_width=True
            ):
                st.session_state["selected_insight_id"] = item.insight_id
                st.rerun()

    selected_item = next(
        (it for it in items if it.insight_id == st.session_state["selected_insight_id"]),
        items[0]
    )
    return selected_item


def render_insight_detail(insight: InsightItem) -> None:
    """Renderiza o detalhe completo do insight: Layout Side-by-Side (Gráfico 300 DPI + Spec Markdown Deslizável) e Contextos no modelo limpo do README."""
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

    # 1. Header de Identidade do Insight
    identity_html = (
        f'<div style="background-color: #090D16; border: 1px solid #1E293B; border-top: 3px solid {insight.category_badge_color}; border-radius: 8px; padding: 0.95rem 1.3rem; margin-top: 0.8rem; margin-bottom: 0.9rem;">'
        '<div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.5rem;">'
        '<div>'
        f'<div style="font-family: monospace; font-size: 0.75rem; color: {insight.category_badge_color}; font-weight: bold; letter-spacing: 0.5px;">{insight.category_label.upper()}</div>'
        f'<div style="font-size: 1.25rem; font-weight: 700; color: #F0F6FC; margin-top: 0.1rem;">{insight.title}</div>'
        f'<div style="font-family: monospace; font-size: 0.75rem; color: #94A3B8; margin-top: 0.25rem;">📁 Diretório: <code>{insight.directory_path}</code></div>'
        '</div>'
        '<div style="text-align: right;">'
        '<span style="font-family: monospace; font-size: 0.72rem; color: #A7F3D0; background-color: #064E3B; border: 1px solid #059669; padding: 0.25rem 0.55rem; border-radius: 4px;">100% Ground Truth</span>'
        '<div style="font-family: monospace; font-size: 0.70rem; color: #64748B; margin-top: 0.35rem;">300 DPI &bull; White Theme</div>'
        '</div>'
        '</div>'
        f'<div style="font-size: 0.82rem; color: #CBD5E1; margin-top: 0.6rem; border-top: 1px solid #1E293B; padding-top: 0.5rem; line-height: 1.4;">{insight.description}</div>'
        '</div>'
    )
    st.markdown(identity_html, unsafe_allow_html=True)

    # 2. KPIs Rápidos do Insight
    kpi_cols = st.columns(len(insight.key_kpis))
    for idx, (label, val) in enumerate(insight.key_kpis):
        with kpi_cols[idx]:
            st.metric(label=label, value=val)

    st.markdown("<div style='margin-top: 0.9rem;'></div>", unsafe_allow_html=True)

    # 3. LAYOUT SIDE-BY-SIDE (PAINEL ESQUERDO: GRÁFICO 300 DPI vs PAINEL DIREITO: SPEC MARKDOWN)
    col_chart, col_spec = st.columns([1.55, 1.05], gap="large")

    with col_chart:
        st.markdown(
            '<div style="font-family: monospace; font-size: 0.80rem; font-weight: 700; color: #38BDF8; margin-bottom: 0.45rem; text-transform: uppercase; letter-spacing: 0.5px;">📊 Visualização do Gráfico (300 DPI • Ground Truth)</div>',
            unsafe_allow_html=True
        )
        img_full_path = os.path.join(root_dir, insight.chart_image_path)
        if os.path.exists(img_full_path):
            st.image(img_full_path, use_container_width=True)
        else:
            st.info(f"Artefato gráfico localizado em: `{insight.chart_image_path}` (Execute `python {insight.directory_path}generate_chart.py` para compilar)")

    with col_spec:
        spec_text = get_file_content(insight.spec_file_path)
        st.markdown(
            f'<div style="font-family: monospace; font-size: 0.80rem; font-weight: 700; color: #34D399; margin-bottom: 0.45rem; text-transform: uppercase; letter-spacing: 0.5px;">📄 Especificação da Análise ({len(spec_text.splitlines())} linhas)</div>',
            unsafe_allow_html=True
        )
        with st.container(height=480):
            st.code(spec_text, language="markdown")

    # 4. Contextos e Referências dentro de Container com Scroll (height=180)
    st.markdown("<div style='margin-top: 0.8rem; font-family: monospace; font-size: 0.85rem; font-weight: 700; color: #38BDF8; text-transform: uppercase;'>📁 Contextos e Referências</div>", unsafe_allow_html=True)
    with st.container(height=180):
        st.markdown(f"- **Diretório Fonte:** <code>{insight.directory_path}</code>", unsafe_allow_html=True)
        st.markdown(f"- **Especificação:** <code>{insight.spec_file_path}</code>", unsafe_allow_html=True)
        st.markdown(f"- **Camada Lakehouse:** *{insight.architecture_notes}*")
        st.markdown("- **Garantia de Ground Truth:** 100% dos dados lidos de `data/mock/output_cleaned/parquet/` (300 DPI)")
