"""Aba 3: Copiloto Prescritivo de Resgate & Playground de Copies LLM (View)."""

import pandas as pd
import streamlit as st

from app.components.chat_preview import render_chat_preview
from app.services.copy_service import generate_prescriptive_copy
from app.types.models import AbandonmentReason, ChannelType, RFMSegment

def render_copilot_tab(df_products: pd.DataFrame | None) -> None:
    """Renderiza a visualização da aba do copiloto de comunicação."""
    st.subheader("🤖 Copiloto Prescritivo de Comunicação & CRM (LLM Playground)")
    st.markdown(
        "Gere abordagens de resgate altamente personalizadas combinando "
        "o perfil RFM do cliente, o motivo raiz do abandono de checkout e o canal de disparo."
    )
    
    if df_products is None or df_products.empty:
        st.warning("⚠️ Base de produtos enriquecidos não encontrada.")
        return

    # -------------------------------------------------------------------------
    # 🎛️ SELEÇÃO DE PARÂMETROS
    # -------------------------------------------------------------------------
    col_c1, col_c2, col_c3 = st.columns(3)
    
    with col_c1:
        segment_options: list[RFMSegment] = [
            "Campeões", "Clientes Leais", "Potenciais Leais", "Promissores",
            "Precisam de Atenção", "Quase Hibernando", "Em Risco", "Hibernando"
        ]
        selected_segment = st.selectbox("Segmento RFM do Cliente:", options=segment_options, index=0)
        
    with col_c2:
        reason_options: list[AbandonmentReason] = [
            "Frete Abusivo", "Preço Elevado", "Dúvida Técnica", "Checkout Complexo", "Indecisão"
        ]
        selected_reason = st.selectbox("Motivo Primário de Abandono:", options=reason_options, index=0)
        
    with col_c3:
        channel_options: list[ChannelType] = ["WhatsApp", "Email", "SMS", "Push"]
        selected_channel = st.selectbox("Canal de Comunicação:", options=channel_options, index=0)

    col_prod, col_disc = st.columns([3, 1])
    with col_prod:
        product_list = df_products["nome_bruto"].tolist()
        selected_product = st.selectbox("Produto no Carrinho:", options=product_list, index=0)
        prod_row = df_products[df_products["nome_bruto"] == selected_product].iloc[0]
        prod_price = float(prod_row["preco_atual"])
        
    with col_disc:
        discount_offered = st.slider("Cupom Aplicado (%)", 0.0, 30.0, 10.0, step=5.0)

    st.divider()

    # -------------------------------------------------------------------------
    # 🧠 CHAMADA AO SERVIÇO DE COPY
    # -------------------------------------------------------------------------
    copy_result = generate_prescriptive_copy(
        product_title=selected_product,
        price=prod_price,
        segment=selected_segment,
        reason=selected_reason,
        channel=selected_channel,
        discount_pct=discount_offered,
    )

    col_preview, col_meta = st.columns([3, 2])
    
    with col_preview:
        st.markdown(f"#### 💬 Preview da Mensagem ({selected_channel})")
        render_chat_preview(copy_result)

    with col_meta:
        st.markdown("#### 🎯 Heurística de Conversão & Gatilho")
        st.info(f"**Gatilho Mental Ativado:** {copy_result.persuasion_trigger}")
        st.markdown(
            f"- **Alinhamento RFM:** O segmento `{selected_segment}` recebe tom condizente com seu LTV.\n"
            f"- **Resolução de Objeção:** O texto ataca frontalmente o atrito de `{selected_reason}`.\n"
            f"- **Ticket Envolvido:** `R$ {prod_price:,.2f}`.\n"
            f"- **Canal Selecionado:** `{selected_channel}`."
        )
        st.text_area("Código / Texto Puro para Copiar:", value=f"{copy_result.body_text}\n\n{copy_result.call_to_action}", height=120)
