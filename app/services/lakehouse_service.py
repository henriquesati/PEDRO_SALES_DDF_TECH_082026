"""Serviço de acesso e carregamento de dados do Data Lakehouse com cache inteligente."""

import os
import pandas as pd
import streamlit as st

from app.constants.settings import DATA_PATHS

@st.cache_data(show_spinner="Carregando catálogo e dados analíticos...")
def load_lakehouse_data() -> tuple[pd.DataFrame | None, pd.DataFrame | None]:
    """Carrega os datasets da Camada Silver e Gold com resolução resiliente de caminhos."""
    # 1. Catálogo Enriquecido (Silver Qualify GenAI)
    prod_path = DATA_PATHS["produtos_enriquecidos"]
    df_products = None
    if os.path.exists(prod_path):
        df_products = pd.read_parquet(prod_path)
    else:
        # Fallback para raw caso qualify não esteja no caminho padrão
        alt_prod = DATA_PATHS.get("produtos_raw")
        if alt_prod and os.path.exists(alt_prod):
            df_products = pd.read_parquet(alt_prod)
            
    # 2. Resumo de Abandono (Gold View)
    view_path = DATA_PATHS["v_abandonment_summary"]
    df_summary = None
    if os.path.exists(view_path):
        df_summary = pd.read_parquet(view_path)
    elif os.path.exists(DATA_PATHS["carrinhos_raw"]):
        df_summary = pd.read_parquet(DATA_PATHS["carrinhos_raw"])
        
    return df_products, df_summary
