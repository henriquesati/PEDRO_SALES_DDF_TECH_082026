"""Componentes visuais de preview de mensagens multicanais, transcrições e cards de decisão executiva."""

import streamlit as st
import pandas as pd
from app.types.models import GeneratedCopy, ShowcasePresentation

def render_chat_preview(copy_result: GeneratedCopy) -> None:
    """Renderiza a mensagem contextualizada no formato visual do canal de disparo."""
    if copy_result.channel == "WhatsApp":
        st.markdown(
            f"""
            <div class="chat-preview-wpp">
                <div style="font-size: 0.85rem; color: #475569; margin-bottom: 0.6rem; font-weight: 600;">
                    🟢 <strong>WhatsApp Business API</strong> • Canal Oficial Dadosfera
                </div>
                <div class="chat-bubble-wpp">
                    <strong style="color: #059669;">Dadosfera Concierge:</strong><br><br>
                    {copy_result.body_text}<br><br>
                    <em style="color: #2563EB;">{copy_result.call_to_action}</em>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    elif copy_result.channel == "Email":
        st.markdown(
            f"""
            <div class="email-preview-card">
                <div style="font-size: 0.88rem; color: #64748B; border-bottom: 1px solid #E2E8F0; padding-bottom: 0.5rem; margin-bottom: 1rem;">
                    <strong>Assunto:</strong> <span style="color: #0F172A; font-weight: 600;">{copy_result.subject_or_headline}</span>
                </div>
                <div style="font-size: 0.95rem; color: #334155; white-space: pre-line; line-height: 1.6;">
                    {copy_result.body_text}
                </div>
                <div style="margin-top: 1.5rem; text-align: center;">
                    <a style="background-color: #2563EB; color: white; padding: 0.7rem 1.6rem; border-radius: 6px; text-decoration: none; font-weight: 600; display: inline-block;">
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
            <div style="background-color: #0F172A; color: #F8FAFC; padding: 1.2rem; border-radius: 10px; font-family: monospace; border: 1px solid #334155;">
                📱 <strong>{copy_result.channel.upper()} NOTIFICATION</strong> • ddf.ai<br><br>
                {copy_result.body_text}<br><br>
                <span style="color: #38BDF8;">{copy_result.call_to_action}</span>
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
                <span class="pill-badge badge-substitute">
                    {prod_row.get('categoria_normalizada', 'Catálogo')}
                </span>
                <span style="font-size: 1.4rem; font-weight: 800; color: #059669;">
                    R$ {float(prod_row.get('preco_atual', 0.0)):,.2f}
                </span>
            </div>
            <h3 style="color: #0F172A; margin-top: 0; font-size: 1.25rem;">{showcase.title}</h3>
            <p style="font-size: 0.98rem; color: #334155; font-style: italic; background: #F8FAFC; padding: 0.8rem; border-left: 4px solid #2563EB; border-radius: 4px;">
                "{showcase.value_proposition}"
            </p>
            <div style="margin-top: 1.2rem; color: #1E293B; font-size: 0.92rem;">
                {showcase.key_pillars.replace(chr(10), '<br>')}
            </div>
            <div style="margin-top: 1.4rem; padding: 0.8rem 1.0rem; background: #FEF3C7; border-radius: 6px; border: 1px solid #FDE68A; color: #92400E; font-size: 0.88rem;">
                <strong>🎯 Gancho de Conversão:</strong> {showcase.sales_pitch_hook}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_decision_comparative_cards() -> None:
    """Renderiza os cards comparativos de decisão executiva C-Level (Estratégia Convencional vs Dadosfera)."""
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        st.markdown(
            """
            <div class="decision-card-danger">
                <div style="font-weight: 700; color: #9F1239; font-size: 0.95rem; margin-bottom: 0.5rem;">
                    ❌ ESTRATÉGIA CONVENCIONAL (QUEIMA DE MARGEM)
                </div>
                <div style="font-size: 0.88rem; color: #4C0519; line-height: 1.5;">
                    • Disparo agressivo de cupom de 20% para qualquer abandono.<br>
                    • <strong>Erosão de Margem:</strong> Queima até R$ 779,80 em pedidos de alto ticket.<br>
                    • <strong>Conversão Média:</strong> Apenas 8.2% devido à falta de contexto técnico.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col_d2:
        st.markdown(
            """
            <div class="decision-card-success">
                <div style="font-weight: 700; color: #065F46; font-size: 0.95rem; margin-bottom: 0.5rem;">
                    ✅ VITRINE INTELIGENTE DADOSFERA (MARGEM PRESERVADA)
                </div>
                <div style="font-size: 0.88rem; color: #064E3B; line-height: 1.5;">
                    • Recomendação de alternativas correlatas (Substituto, Cross-sell, Acessório).<br>
                    • <strong>Preservação Financeira:</strong> Margem de <strong>28.5%</strong> preservada sem cupom.<br>
                    • <strong>Conversão Elevada:</strong> <strong>+14.2%</strong> atacando a dúvida do cliente.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
