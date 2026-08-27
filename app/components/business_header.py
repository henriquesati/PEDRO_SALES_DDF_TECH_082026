"""Componente do Cockpit Executivo de Negócios & BI (Header Integrado, Ticker de KPIs e Navegação em Painéis Modulares)."""

import streamlit as st

BI_PANELS = (
    ("roi", "📊 Simulador de ROI", "Simulador de ROI"),
    ("similarity", "🔍 Catálogo & Similares", "Explorador Semântico"),
    ("copilot", "🤖 Copiloto CRM", "Copiloto Prescritivo"),
    ("showcase", "🎙️ Vitrine GenAI", "Vitrine Visual"),
    ("insights", "💡 Galeria de Insights", "Galeria de Insights")
)


def render_business_cockpit_header() -> str:
    """Renderiza a barra de comando executiva com Título, Ticker de Métricas Macro e Seletores de Painéis."""
    if "business_active_panel" not in st.session_state:
        st.session_state["business_active_panel"] = "Simulador de ROI"

    current_panel = st.session_state["business_active_panel"]

    # 1. Box de Comando Executivo com Header & Navegação Integrada
    with st.container(border=True):
        st.markdown('<span class="business-cockpit-marker" style="display:none;"></span>', unsafe_allow_html=True)
        
        col_info, col_p1, col_p2, col_p3, col_p4, col_p5 = st.columns(
            [2.6, 1.0, 1.1, 1.0, 1.0, 1.1],
            gap="small",
            vertical_alignment="center"
        )

        with col_info:
            st.markdown(
                """
                <div style="display: flex; flex-direction: column; justify-content: center; padding-left: 0.2rem;">
                    <div style="display: flex; align-items: center; gap: 0.5rem;">
                        <span style="font-family: 'Inter', sans-serif; font-size: 1.12rem; font-weight: 800; color: #F8FAFC; letter-spacing: -0.3px;">
                            🏢 Cockpit Executivo de Negócios & BI
                        </span>
                        <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.64rem; background: #1E3A8A; color: #93C5FD; border: 1px solid #3B82F6; padding: 0.12rem 0.40rem; border-radius: 4px; font-weight: bold;">
                            DADOSFERA LAKEHOUSE
                        </span>
                    </div>
                    <div style="font-size: 0.72rem; color: #94A3B8; margin-top: 0.10rem;">
                        Painel Analítico de Preservação de Margem, Otimização de ROI e Recuperação de Carrinhos
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        # Botões de Navegação dos 5 Painéis Executivos
        panel_cols = [col_p1, col_p2, col_p3, col_p4, col_p5]
        for idx, (panel_id, panel_label, target_value) in enumerate(BI_PANELS):
            with panel_cols[idx]:
                is_active = (current_panel == target_value)
                if st.button(
                    label=panel_label,
                    key=f"btn_biz_nav_{panel_id}",
                    type="primary" if is_active else "secondary",
                    use_container_width=True
                ):
                    st.session_state["business_active_panel"] = target_value
                    st.rerun()

    # 2. Ticker de Métricas Macro & Contexto de Negócio (Camada de Visão Geral Executiva)
    st.markdown(
        """
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.5rem; background: #090D16; border: 1px solid #1E293B; border-radius: 6px; padding: 0.35rem 0.85rem; margin-top: 0.35rem; margin-bottom: 0.65rem;">
            <div style="display: flex; align-items: center; gap: 0.4rem;">
                <span style="font-size: 0.68rem; font-weight: 700; color: #64748B; text-transform: uppercase; font-family: monospace;">INDICADORES MACRO:</span>
            </div>
            <div style="display: flex; gap: 1.2rem; flex-wrap: wrap; font-family: 'JetBrains Mono', monospace; font-size: 0.72rem;">
                <div>💰 <span style="color: #94A3B8;">Receita Recuperável:</span> <strong style="color: #34D399;">R$ 314.5k</strong></div>
                <div>📈 <span style="color: #94A3B8;">ROI Prescrito:</span> <strong style="color: #38BDF8;">45.2x (E-mail)</strong></div>
                <div>🛡️ <span style="color: #94A3B8;">Margem Preservada:</span> <strong style="color: #F59E0B;">28.5%</strong></div>
                <div>🎯 <span style="color: #94A3B8;">Acurácia Semântica:</span> <strong style="color: #A78BFA;">89.4%</strong></div>
                <div>🛒 <span style="color: #94A3B8;">Volume em Risco:</span> <strong style="color: #F8FAFC;">12.870 carrinhos</strong></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    return st.session_state["business_active_panel"]
