"""Componente de Cabeçalho e Navegação Executiva do Módulo de Business & BI.

Estruturado em 4 Pilares Estratégicos correlacionados aos requisitos do Case Dadosfera:
1. Cockpit Financeiro & Sensibilidade (Itens 4 & 7)
2. Inteligência Semântica & Catálogo (Itens 5 & 6)
3. Copiloto Prescritivo CRM & Ativação Multicanal (Itens 5 & 8)
4. Galeria de Insights & Decisão Estratégica (Itens 4, 7, 8 & 9)
"""

import streamlit as st

BI_HUBS = (
    ("finance", "📊 1. Cockpit Financeiro & ROI", "Finanças & ROI"),
    ("catalog", "🔍 2. Catálogo & Semântica", "Catálogo & Semântica"),
    ("crm", "🤖 3. Copiloto CRM & Ativação", "Copiloto CRM & Ativação"),
    ("insights", "💡 4. Galeria de Insights", "Galeria de Insights")
)


def render_business_cockpit_header() -> tuple[str, str]:
    """Renderiza a barra de comando executiva com branding corporativo, seletor de cenários e navegação em 4 pilares.
    
    Retorna:
        tuple[str, str]: (hub_ativo, cenario_selecionado)
    """
    if "biz_active_hub" not in st.session_state:
        st.session_state["biz_active_hub"] = "Finanças & ROI"

    if "biz_scenario_preset" not in st.session_state:
        st.session_state["biz_scenario_preset"] = "✨ Mix Recomendado (85/12/2/1)"

    current_hub = st.session_state["biz_active_hub"]

    # 1. Barra de Comando Executiva Integrada
    with st.container(border=True):
        st.markdown('<span class="business-cockpit-marker" style="display:none;"></span>', unsafe_allow_html=True)
        
        col_brand, col_scenario, col_h1, col_h2, col_h3, col_h4 = st.columns(
            [2.4, 1.8, 1.2, 1.2, 1.3, 1.2],
            gap="small",
            vertical_alignment="center"
        )

        with col_brand:
            st.markdown(
                """
                <div style="padding-left: 0.1rem;">
                    <div style="display: flex; align-items: center; gap: 0.45rem;">
                        <span style="font-family: 'Inter', sans-serif; font-size: 1.10rem; font-weight: 800; color: #F8FAFC; letter-spacing: -0.3px;">
                            🏢 Executive BI Suite
                        </span>
                        <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.62rem; background: #1E3A8A; color: #93C5FD; border: 1px solid #3B82F6; padding: 0.10rem 0.35rem; border-radius: 4px; font-weight: bold;">
                            DADOSFERA LAKEHOUSE
                        </span>
                    </div>
                    <div style="font-size: 0.68rem; color: #94A3B8; margin-top: 0.05rem;">
                        Painel Analítico de Preservação de Margem, Otimização de ROI e Recuperação de Carrinhos
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col_scenario:
            selected_scenario = st.selectbox(
                "Estratégia Prescritiva:",
                options=[
                    "✨ Mix Recomendado (85/12/2/1)",
                    "🛡️ Conservadora (Margem 30%)",
                    "🚀 Agressiva VIP (WhatsApp)",
                    "🛠️ Customização Manual"
                ],
                index=0,
                key="biz_scenario_select",
                label_visibility="collapsed"
            )
            st.session_state["biz_scenario_preset"] = selected_scenario

        hub_cols = [col_h1, col_h2, col_h3, col_h4]
        for idx, (hub_id, hub_label, target_value) in enumerate(BI_HUBS):
            with hub_cols[idx]:
                is_active = (current_hub == target_value)
                if st.button(
                    label=hub_label,
                    key=f"btn_biz_pillar_{hub_id}",
                    type="primary" if is_active else "secondary",
                    use_container_width=True
                ):
                    st.session_state["biz_active_hub"] = target_value
                    st.rerun()

    # 2. Ticker de Métricas Macro (Visão Geral de Negócios)
    st.markdown(
        """
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.5rem; background: #0A101D; border: 1px solid #1E293B; border-radius: 6px; padding: 0.32rem 0.80rem; margin-top: 0.25rem; margin-bottom: 0.55rem;">
            <div style="display: flex; align-items: center; gap: 0.4rem;">
                <span style="font-size: 0.66rem; font-weight: 700; color: #64748B; text-transform: uppercase; font-family: monospace;">INDICADORES MACRO:</span>
            </div>
            <div style="display: flex; gap: 1.1rem; flex-wrap: wrap; font-family: 'JetBrains Mono', monospace; font-size: 0.70rem;">
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

    return st.session_state["biz_active_hub"], st.session_state["biz_scenario_preset"]
