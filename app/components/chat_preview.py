"""Componentes visuais de preview de mensagens e vitrines de produto."""

import streamlit as st
import pandas as pd

from app.types.models import GeneratedCopy, ShowcasePresentation

def render_chat_preview(copy_result: GeneratedCopy) -> None:
    """Renderiza a mensagem contextualizada no formato visual do canal de disparo."""
    if copy_result.channel == "WhatsApp":
        st.markdown(
            f"""
            <div class="chat-preview">
                <div class="chat-bubble">
                    <strong>Dadosfera Concierge:</strong><br><br>
                    {copy_result.body_text}<br><br>
                    <em>{copy_result.call_to_action}</em>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    elif copy_result.channel == "Email":
        st.markdown(
            f"""
            <div class="showcase-card">
                <div style="font-size: 0.9rem; color: #64748B; border-bottom: 1px solid #E2E8F0; padding-bottom: 0.5rem; margin-bottom: 1rem;">
                    <strong>Assunto:</strong> {copy_result.subject_or_headline}
                </div>
                <div style="font-size: 1.0rem; color: #1E293B; white-space: pre-line; line-height: 1.6;">
                    {copy_result.body_text}
                </div>
                <div style="margin-top: 1.5rem; text-align: center;">
                    <a style="background-color: #1E3A8A; color: white; padding: 0.7rem 1.4rem; border-radius: 6px; text-decoration: none; font-weight: 600;">
                        {copy_result.call_to_action}
                    </a>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:  # SMS / Push
        st.markdown(
            f"""
            <div style="background-color: #1F2937; color: #F9FAFB; padding: 1.2rem; border-radius: 12px; font-family: monospace;">
                📱 <strong>SMS NOTIFICATION</strong><br><br>
                {copy_result.body_text}<br><br>
                {copy_result.call_to_action}
            </div>
            """,
            unsafe_allow_html=True
        )

def render_showcase_card(showcase: ShowcasePresentation, prod_row: pd.Series) -> None:
    """Renderiza o card comercial de apresentação do produto (Item Bônus)."""
    st.markdown(
        f"""
        <div class="showcase-card">
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #F1F5F9; padding-bottom: 0.8rem; margin-bottom: 1rem;">
                <span style="background: #1E3A8A; color: white; padding: 0.3rem 0.8rem; border-radius: 20px; font-size: 0.8rem; font-weight: bold;">
                    {prod_row.get('categoria_normalizada', 'Catálogo')}
                </span>
                <span style="font-size: 1.4rem; font-weight: 700; color: #059669;">
                    R$ {float(prod_row.get('preco_atual', 0.0)):,.2f}
                </span>
            </div>
            <h3 style="color: #0F172A; margin-top: 0;">{showcase.title}</h3>
            <p style="font-size: 1.05rem; color: #334155; font-style: italic; background: #F8FAFC; padding: 0.8rem; border-left: 4px solid #3B82F6; border-radius: 4px;">
                "{showcase.value_proposition}"
            </p>
            <div style="margin-top: 1.2rem; color: #1E293B;">
                {showcase.key_pillars.replace(chr(10), '<br>')}
            </div>
            <div style="margin-top: 1.5rem; padding: 0.8rem; background: #FEF3C7; border-radius: 6px; border: 1px solid #FDE68A;">
                <strong>🎯 Gancho de Vendas:</strong> {showcase.sales_pitch_hook}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
