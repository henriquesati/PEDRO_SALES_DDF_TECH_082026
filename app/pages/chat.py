"""Página nativa /chat do Streamlit isolada do restante do aplicativo."""

import os
import sys
import streamlit as st

# Inserção prioritária da raiz no PYTHONPATH
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from app.private_chat.view import render_private_chat_page

# Configuração de página se executado como entrypoint standalone
try:
    st.set_page_config(
        page_title="Dadosfera | Console Multi-Agente (/chat)",
        page_icon="💬",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
except Exception:
    pass

# Renderização do chat privado 100% isolado
render_private_chat_page()
