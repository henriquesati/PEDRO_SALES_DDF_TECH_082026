"""Aba 4: Vitrine & Gerador Visual de Apresentação de Produto (Item Bônus GenAI) (View)."""

import pandas as pd
import streamlit as st

from app.components.chat_preview import render_showcase_card
from app.services.copy_service import generate_showcase_presentation

def render_showcase_tab(df_products: pd.DataFrame | None) -> None:
    """Renderiza a visualização da aba de vitrines e apresentações GenAI."""
    st.subheader("🎨 Gerador de Apresentações de Produto com GenAI (Item Bônus)")
    st.markdown(
        "Gere apresentações comerciais de alto impacto visual e argumentativo para "
        "destacar os atributos de valor dos produtos e impulsionar as taxas de conversão de resgate."
    )
    
    if df_products is None or df_products.empty:
        st.warning("⚠️ Base de produtos enriquecidos não encontrada.")
        return

    # -------------------------------------------------------------------------
    # 🎛️ SELETOR DE PRODUTO
    # -------------------------------------------------------------------------
    col_sel1, col_sel2 = st.columns([3, 1])
    with col_sel1:
        product_list = df_products["nome_bruto"].tolist()
        selected_product = st.selectbox("Selecione o Produto para Apresentação:", options=product_list, index=0)
        prod_row = df_products[df_products["nome_bruto"] == selected_product].iloc[0]
        
    with col_sel2:
        target_audience = st.selectbox(
            "Público Alvo da Campanha:",
            options=["Consumidor Final (B2C)", "Corporativo / Premium (B2B)", "Tech Enthusiasts"],
            index=0
        )

    # -------------------------------------------------------------------------
    # 🧠 CHAMADA AO SERVIÇO DE SHOWCASE
    # -------------------------------------------------------------------------
    showcase_data = generate_showcase_presentation(
        product_title=str(prod_row["nome_bruto"]),
        category=str(prod_row.get("categoria_normalizada", "Geral")),
        price=float(prod_row.get("preco_atual", 0.0)),
        material=str(prod_row.get("material_construcao", "Material Premium")),
        technical_differential=str(prod_row.get("diferencial_tecnico", "Alta Tecnologia")),
        target_audience=target_audience,
    )

    st.divider()

    # -------------------------------------------------------------------------
    # 🖼️ APRESENTAÇÃO & PROMPTS DOCUMENTADOS
    # -------------------------------------------------------------------------
    col_card, col_prompts = st.columns([3, 2])
    
    with col_card:
        st.markdown("#### 📱 Card de Apresentação Comercial")
        render_showcase_card(showcase_data, prod_row)

    with col_prompts:
        st.markdown("#### 📝 Engenharia de Prompts (Item Bônus GenAI)")
        st.markdown("Prompts declarativos e documentados para geração de estúdio com DALL-E e síntese de texto:")
        
        with st.expander("🖼️ Prompt de Imagem para DALL-E / Estúdio Visual", expanded=True):
            st.code(showcase_data.visual_prompt_reference, language="text")
            st.caption("Prompt estruturado para renderizar fotografia de estúdio com iluminação no padrão visual Dadosfera.")

        with st.expander("📄 Prompt de Síntese de Texto (LLM)", expanded=True):
            llm_prompt = (
                f"Você é um copywriter sênior de e-commerce da Dadosfera.\n"
                f"Gere um card comercial para o produto '{prod_row['nome_bruto']}'\n"
                f"destacando o material '{prod_row.get('material_construcao')}' e diferencial '{prod_row.get('diferencial_tecnico')}'.\n"
                f"Foco: conversão imediata de carrinho abandonado com preservação de margem."
            )
            st.code(llm_prompt, language="text")
