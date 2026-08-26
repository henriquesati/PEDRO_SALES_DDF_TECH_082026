"""Serviço de acesso e carregamento de dados do Data Lakehouse com cache inteligente (Ground Truth)."""

import os
from typing import Tuple, Dict, Any
import pandas as pd
import streamlit as st

from app.constants.settings import DATA_PATHS

@st.cache_data(show_spinner="Carregando catálogo e dados analíticos do Lakehouse...")
def load_lakehouse_data() -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Carrega os datasets persistidos da Camada Silver/Gold com resolução resiliente.
    
    Retorna:
        Tuple: (df_products, df_carrinhos, df_resgate, df_clientes)
    """
    # 1. Produtos Enriquecidos (Silver Qualify / GenAI Features)
    prod_qualify = DATA_PATHS.get("produtos_enriquecidos_qualify", "")
    prod_cleaned = DATA_PATHS.get("produtos_cleaned", "")
    
    if os.path.exists(prod_qualify):
        df_products = pd.read_parquet(prod_qualify)
    elif os.path.exists(prod_cleaned):
        df_products = pd.read_parquet(prod_cleaned)
        # Normalização de nomes de colunas se vier de cleaned
        if "nome" in df_products.columns and "nome_bruto" not in df_products.columns:
            df_products["nome_bruto"] = df_products["nome"]
        if "categoria" in df_products.columns and "categoria_normalizada" not in df_products.columns:
            df_products["categoria_normalizada"] = df_products["categoria"]
    else:
        df_products = pd.DataFrame()

    # 2. Carrinhos (Ground Truth)
    cart_path = DATA_PATHS.get("carrinhos_cleaned", "")
    df_carrinhos = pd.read_parquet(cart_path) if os.path.exists(cart_path) else pd.DataFrame()

    # 3. Eventos de Resgate (Telemetria Multicanal)
    res_path = DATA_PATHS.get("eventos_resgate_cleaned", "")
    df_resgate = pd.read_parquet(res_path) if os.path.exists(res_path) else pd.DataFrame()

    # 4. Clientes & Segmentação RFM
    cli_path = DATA_PATHS.get("clientes_cleaned", "")
    df_clientes = pd.read_parquet(cli_path) if os.path.exists(cli_path) else pd.DataFrame()

    return df_products, df_carrinhos, df_resgate, df_clientes
