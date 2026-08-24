"""Data App Streamlit: Recuperação de Carrinho Abandonado (Item 9 & Bônus GenAI).

Arquitetura em 5 camadas inspirada em React + TypeScript:
- types/: Contratos tipados imutáveis
- constants/: Tokens de design, paleta e constantes de negócio
- services/: Regras de negócio, cálculos puros e acesso a dados
- components/: Componentes visuais atômicos e gráficos Plotly
- views/: Telas/Abas modulares
"""

import os
import sys
import streamlit as st

# Inserção prioritária da raiz no PYTHONPATH
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR in sys.path:
    sys.path.remove(ROOT_DIR)
sys.path.insert(0, ROOT_DIR)


from app.services.lakehouse_service import load_lakehouse_data
from app.views.tab_copilot import render_copilot_tab
from app.views.tab_roi import render_roi_tab
from app.views.tab_showcase import render_showcase_tab
from app.views.tab_similarity import render_similarity_tab

# =============================================================================
# ⚙️ CONFIGURAÇÃO DA PÁGINA STREAMLIT
# =============================================================================
st.set_page_config(
    page_title="Dadosfera | Data App de Recuperação de Carrinho",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# 🎨 CARREGAMENTO DE ESTILOS CSS
# =============================================================================
def load_css() -> None:
    css_path = os.path.join(os.path.dirname(__file__), "styles", "custom.css")
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# =============================================================================
# 📁 CARREGAMENTO DOS DATASETS
# =============================================================================
df_products, df_summary = load_lakehouse_data()

# =============================================================================
# 🏢 BANNER EXECUTIVO DADOSFERA
# =============================================================================
st.markdown(
    """
    <div class="main-header">
        <h1>🛒 Plataforma de Recuperação de Carrinhos | Dadosfera</h1>
        <p>Data App Interativo de Análise Prescritiva, Simulação de ROI e Inteligência de Catálogo (Item 9 & Bônus)</p>
    </div>
    """,
    unsafe_allow_html=True
)

# =============================================================================
# 🧭 BARRA LATERAL (SIDEBAR)
# =============================================================================
with st.sidebar:
    st.markdown("### 🌐 Dadosfera SaaS")
    st.markdown("**Tenant:** `pedro-sales`  \n**Case:** Recuperação de Carrinho")
    st.divider()
    
    st.markdown("#### 📌 Governança & Data Lakehouse")
    st.markdown(
        "- **Camada Silver:** `PRODUTOS_ENRIQUECIDOS` (Qualify)\n"
        "- **Camada Gold:** `STAR_SCHEMA_KIMBALL` (DEC-008)\n"
        "- **Ativos Catalogados:** 7 Entidades Oficiais\n"
        "- **Qualidade:** 18 Regras Great Expectations"
    )
    
    st.divider()
    st.markdown("#### 🚀 Reprodutibilidade")
    st.caption("Execute localmente via terminal:")
    st.code("streamlit run app/app.py", language="bash")
    st.caption("Ou via Makefile: `python make.py data-app`")
    
    st.divider()
    st.markdown("**Autor:** Pedro Sales  \n*Lead Analytics Engineer Candidate*")

# =============================================================================
# 📑 ABAS DA APLICAÇÃO (VIEWS)
# =============================================================================
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 1. Simulador de ROI & Sensibilidade",
    "🔍 2. Explorador Semântico de Catálogo (GenAI)",
    "🤖 3. Copiloto Prescritivo de Resgate",
    "🎨 4. Vitrine Visual de Produtos (Bônus)"
])

with tab1:
    render_roi_tab(df_summary)

with tab2:
    render_similarity_tab(df_products)

with tab3:
    render_copilot_tab(df_products)

with tab4:
    render_showcase_tab(df_products)

# =============================================================================
# 🦶 RODAPÉ
# =============================================================================
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #64748B; font-size: 0.85rem;'>"
    "Dadosfera Data App • Arquitetura Modular em Camadas (React/TS Pattern) • "
    "Case Técnico de Estágio (Item 9 & Bônus GenAI)"
    "</div>",
    unsafe_allow_html=True
)
