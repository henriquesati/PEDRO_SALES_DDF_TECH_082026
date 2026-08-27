import os
import sys
import streamlit as st

# Inserção prioritária da raiz no PYTHONPATH
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR in sys.path:
    sys.path.remove(ROOT_DIR)
sys.path.insert(0, ROOT_DIR)

import importlib
for mod_name in list(sys.modules.keys()):
    if mod_name.startswith("app.") and mod_name != "app.app":
        try:
            importlib.reload(sys.modules[mod_name])
        except Exception:
            pass

from app.components.business_header import render_business_cockpit_header
from app.components.fighter_select import render_evaluator_header
from app.private_chat.view import render_private_chat_page
from app.services.lakehouse_service import load_lakehouse_data
from app.views.tab_agents import render_agents_tab, render_skills_tab, render_specs_tab
from app.views.tab_copilot import render_copilot_tab
from app.views.tab_insights_explorer import render_insights_explorer_tab
from app.views.tab_roi import render_roi_tab
from app.views.tab_showcase import render_showcase_tab
from app.views.tab_similarity import render_similarity_tab
from app.views.view_hub_landing import render_hub_landing

# =============================================================================
# ⚙️ CONFIGURAÇÃO DA PÁGINA STREAMLIT
# =============================================================================
st.set_page_config(
    page_title="Dadosfera | Hub de Recuperação de Carrinhos & IA",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# 🧭 MODOS DE NAVEGAÇÃO & INICIALIZAÇÃO DE ESTADO
# =============================================================================
MODES = (
    "🏠 Hub Central de Entrada",
    "🥋 Central do Avaliador (Agentes, Skills & Insights)",
    "🏢 Módulo de Negócio (BI & Consumo Executivo)",
    "💬 Console de Inferência Autônoma (/chat)",
    "🌐 Visão Unificada (Todas as Abas)"
)

# Sincronização imediata via Query Params (suporte a links âncora nativos)
query_nav = st.query_params.get("nav")
if query_nav == "management":
    st.session_state["app_navigation_mode"] = MODES[1]
elif query_nav == "business":
    st.session_state["app_navigation_mode"] = MODES[2]
elif query_nav == "chat":
    st.session_state["app_navigation_mode"] = MODES[3]
elif query_nav == "hub":
    st.session_state["app_navigation_mode"] = MODES[0]

if "app_navigation_mode" not in st.session_state:
    st.session_state["app_navigation_mode"] = MODES[0]

current_mode = st.session_state["app_navigation_mode"]


# =============================================================================
# 🎨 INJEÇÃO DINÂMICA DE CSS (DESACOPLAMENTO VISUAL POR AMBIENTE)
# =============================================================================
def inject_theme(mode: str) -> None:
    """Injeta a folha de estilo modular correspondente ao modo ativo para isolamento estético total."""
    styles_dir = os.path.join(os.path.dirname(__file__), "styles")
    
    if mode == "🏠 Hub Central de Entrada":
        css_file = "hub_theme.css"
    elif mode == "🥋 Central do Avaliador (Agentes, Skills & Insights)":
        css_file = "command_center.css"
    elif mode == "🏢 Módulo de Negócio (BI & Consumo Executivo)":
        css_file = "custom.css"
    else:  # Visão Unificada
        css_file = "custom.css"
        
    css_path = os.path.join(styles_dir, css_file)
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

inject_theme(current_mode)

# =============================================================================
# 📁 CARREGAMENTO DOS DATASETS DO LAKEHOUSE (GROUND TRUTH)
# =============================================================================
df_products, df_carrinhos, df_resgate, df_clientes = load_lakehouse_data()

# =============================================================================
# 🧭 BARRA LATERAL (SIDEBAR) - APENAS EXIBIDA QUANDO FORA DA TELA INICIAL
# =============================================================================
if current_mode != "🏠 Hub Central de Entrada":
    with st.sidebar:
        st.markdown(
            """
            <div style="font-family: monospace; font-size: 1.15rem; font-weight: bold; color: #38BDF8; margin-bottom: 0.2rem;">
                🛒 DADOSFERA SAAS
            </div>
            <div style="font-family: monospace; font-size: 0.75rem; color: #94A3B8; margin-bottom: 0.8rem;">
                Tenant: <code>pedro-sales</code> &bull; Case: Carrinho Abandonado
            </div>
            """,
            unsafe_allow_html=True
        )
        st.divider()

        st.markdown("#### 🎯 Navegação de Ambientes")
        selected_sidebar_mode = st.radio(
            label="Selecione o Módulo:",
            options=MODES,
            index=MODES.index(current_mode) if current_mode in MODES else 0,
            key="sidebar_mode_select"
        )
        
        if selected_sidebar_mode != current_mode:
            st.session_state["app_navigation_mode"] = selected_sidebar_mode
            if selected_sidebar_mode == MODES[1]:
                st.query_params["nav"] = "management"
            elif selected_sidebar_mode == MODES[2]:
                st.query_params["nav"] = "business"
            elif selected_sidebar_mode == MODES[3]:
                st.query_params["nav"] = "chat"
            elif selected_sidebar_mode == MODES[0]:
                st.query_params["nav"] = "hub"
            st.rerun()

        st.markdown("<div style='margin-top: 6rem;'></div>", unsafe_allow_html=True)
        st.divider()
        st.markdown(
            """
            <div style="font-family: monospace; font-size: 0.75rem; color: #94A3B8;">
                Autor: <strong style="color: #F8FAFC;">Pedro Sales</strong><br>
                <em>Candidate &bull; DDF Tech Case</em>
            </div>
            """,
            unsafe_allow_html=True
        )

# =============================================================================
# 📑 RENDERIZAÇÃO DAS TELAS CONFORME O MODO SELECIONADO
# =============================================================================

# -----------------------------------------------------------------------------
# 1. 🏠 HUB CENTRAL DE ENTRADA (SPLIT-SCREEN HERO PURA E PLANA)
# -----------------------------------------------------------------------------
if current_mode == "🏠 Hub Central de Entrada":
    render_hub_landing()

# -----------------------------------------------------------------------------
# 2. 🥋 CENTRAL DO AVALIADOR & GESTÃO DE AGENTES (DARK COMMAND CENTER)
# -----------------------------------------------------------------------------
elif current_mode == "🥋 Central do Avaliador (Agentes, Skills & Insights)":
    active_eval_tab = render_evaluator_header()
    if active_eval_tab == "Agentes":
        render_agents_tab()
    elif active_eval_tab == "Skills":
        render_skills_tab()
    elif active_eval_tab == "Specs":
        render_specs_tab()

# -----------------------------------------------------------------------------
# 3. 🏢 MÓDULO EXECUTIVO DE NEGÓCIOS & BI (BUSINESS COCKPIT & DATA PANELS)
# -----------------------------------------------------------------------------
elif current_mode == "🏢 Módulo de Negócio (BI & Consumo Executivo)":
    render_business_cockpit_header()
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "1. Simulador de ROI",
        "2. Explorador Semântico",
        "3. Copiloto Prescritivo",
        "4. Vitrine Visual de Produtos",
        "5. Galeria de Insights",
    ])

    with tab1:
        render_roi_tab(df_carrinhos)

    with tab2:
        render_similarity_tab(df_products)

    with tab3:
        render_copilot_tab(df_products)

    with tab4:
        render_showcase_tab(df_products)

    with tab5:
        render_insights_explorer_tab()

# -----------------------------------------------------------------------------
# 4. 💬 CONSOLE DE INFERÊNCIA AUTÔNOMA (/chat - ISOLADO)
# -----------------------------------------------------------------------------
elif current_mode == "💬 Console de Inferência Autônoma (/chat)":
    render_private_chat_page()

# -----------------------------------------------------------------------------
# 5. 🌐 VISÃO UNIFICADA (TODAS AS ABAS)
# -----------------------------------------------------------------------------

else:
    tab0, tab_sk, tab_sp, tab_ins, tab1, tab2, tab3, tab4 = st.tabs([
        "Agentes",
        "Skills",
        "Specs da Codebase",
        "Galeria de Insights",
        "1. Simulador de ROI",
        "2. Explorador Semântico",
        "3. Copiloto Prescritivo",
        "4. Vitrine Visual de Produtos"
    ])

    with tab0:
        render_agents_tab()

    with tab_sk:
        render_skills_tab()

    with tab_sp:
        render_specs_tab()

    with tab_ins:
        render_insights_explorer_tab()

    with tab1:
        render_roi_tab(df_carrinhos)

    with tab2:
        render_similarity_tab(df_products)

    with tab3:
        render_copilot_tab(df_products)

    with tab4:
        render_showcase_tab(df_products)


# =============================================================================
# 🧹 RODAPÉ CORPORATIVO (APENAS QUANDO FORA DO HUB INICIAL)
# =============================================================================
if current_mode != "🏠 Hub Central de Entrada":
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #64748B; font-family: monospace; font-size: 0.78rem;'>
            Dadosfera Data App &bull; <strong style='color: #94A3B8;'>Pedro Sales</strong>
        </div>
        """,
        unsafe_allow_html=True
    )
