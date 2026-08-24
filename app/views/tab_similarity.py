"""Aba 2: Explorador Semântico & Similaridade de Produtos (View)."""

import pandas as pd
import streamlit as st

from app.components.charts import render_semantic_scatter_chart
from app.services.similarity_service import (
    compute_2d_projection,
    find_similar_products,
)

def render_similarity_tab(df_products: pd.DataFrame | None) -> None:
    """Renderiza a visualização da aba de exploração semântica."""
    st.subheader("🔍 Explorador Semântico & Similaridade de Catálogo (GenAI)")
    st.markdown(
        "Explore o espaço vetorial de produtos gerado a partir de features semânticas "
        "(materiais, diferenciais técnicos, categorias e sensibilidade a preço) "
        "para identificar alternativas de resgate e produtos correlacionados."
    )
    
    if df_products is None or df_products.empty:
        st.warning("⚠️ Base de produtos enriquecidos não encontrada. Verifique os Parquets da camada Qualify.")
        return

    # -------------------------------------------------------------------------
    # 🎛️ CONTROLES & FILTROS
    # -------------------------------------------------------------------------
    col_ctrl1, col_ctrl2, col_ctrl3 = st.columns([2, 1, 1])
    
    with col_ctrl1:
        product_options = {
            f"{row['produto_id']} - {row['nome_bruto'][:45]}... (R$ {row['preco_atual']:,.2f})": row["produto_id"]
            for _, row in df_products.iterrows()
        }
        selected_label = st.selectbox(
            "Selecione um Produto Âncora para Buscar Similares:",
            options=list(product_options.keys()),
            index=0
        )
        selected_id = product_options[selected_label]
        
    with col_ctrl2:
        top_k = st.slider("Top K Similares", min_value=3, max_value=10, value=5)
        
    with col_ctrl3:
        proj_method = st.selectbox("Algoritmo de Projeção 2D", options=["PCA", "t-SNE"], index=0)
        
    st.divider()
    
    # -------------------------------------------------------------------------
    # 🌐 MAPA 2D & LISTA DE SIMILARES
    # -------------------------------------------------------------------------
    col_map, col_details = st.columns([3, 2])
    
    with col_map:
        st.markdown(f"#### 🌌 Mapa Semântico 2D de Produtos ({proj_method})")
        df_proj = compute_2d_projection(df_products, method=proj_method.lower())
        render_semantic_scatter_chart(df_proj, selected_id, proj_method)

    with col_details:
        st.markdown("#### 🎯 Top Produtos Mais Próximos (Cosseno)")
        similar_matches = find_similar_products(selected_id, df_products, top_k=top_k)
        
        if similar_matches:
            for i, match in enumerate(similar_matches, start=1):
                with st.container():
                    st.markdown(
                        f"**{i}. {match.title}**  \n"
                        f"💰 **R$ {match.price:,.2f}** | Categoria: `{match.category}`  \n"
                        f"🎯 **Similaridade:** `{match.similarity_score:.1f}%` | "
                        f"Urgência: `{match.urgency_level}` | Sensibilidade: `{match.price_sensitivity}`"
                    )
                    st.caption(f"⚡ Risco de Abandono Detectado: {match.friction_risk}")
                    st.divider()
        else:
            st.info("Nenhum produto similar encontrado para este ID.")
            
    # -------------------------------------------------------------------------
    # 📋 TABELA COMPLETA
    # -------------------------------------------------------------------------
    with st.expander("📄 Ver Tabela Completa de Features Enriquecidas com LLMs", expanded=False):
        display_cols = [
            "produto_id", "nome_bruto", "preco_atual", "categoria_normalizada",
            "material_construcao", "diferencial_tecnico", "sensibilidade_preco", "motivo_raiz"
        ]
        available_cols = [c for c in display_cols if c in df_products.columns]
        st.dataframe(df_products[available_cols], use_container_width=True, hide_index=True)
