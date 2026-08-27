"""Injeção dinâmica de folhas de estilo encapsuladas para a camada Private Chat."""

import os
import streamlit as st


def inject_private_chat_theme() -> None:
    """Injeta a folha de estilos CSS isolada para o Private Chat."""
    css_path = os.path.join(os.path.dirname(__file__), "chat_theme.css")
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
