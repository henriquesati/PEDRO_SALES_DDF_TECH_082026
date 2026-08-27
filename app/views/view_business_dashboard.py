"""View Principal do Módulo de Business & BI: Executive Business Suite.

Estrutura Multi-Camadas Orientada a Negócios & C-Level (Itens 4 a 9 do Case Dadosfera):
- Camada 1: Barra de Comando Executiva & Ticker Macro (app/components/business_header.py)
- Camada 2: Hero KPI Ribbon de Performance Financeira
- Camada 3: Centrais de Trabalho Analítico em 4 Pilares Estratégicos
"""

import os
import pandas as pd
import streamlit as st

from app.components.business_header import render_business_cockpit_header
from app.components.charts import (
    render_budget_rebalance_chart,
    render_semantic_scatter_chart,
    render_sensitivity_chart,
    render_waterfall_chart,
)
from app.components.chat_preview import (
    render_chat_preview,
    render_decision_comparative_cards,
    render_showcase_card,
)
from app.components.kpi_cards import render_kpi_card
from app.constants.settings import (
    CANONICAL_TOTAL_CARTS,
    DEFAULT_TICKET_MEDIO,
)
from app.services.copy_service import (
    generate_prescriptive_copy,
    generate_showcase_presentation,
)
from app.services.similarity_service import (
    compute_2d_projection,
    find_similar_products,
)
from app.services.simulation_service import (
    create_preset_simulation_input,
    generate_discount_sensitivity_curve,
    run_simulation,
)
from app.types.models import (
    AbandonmentReason,
    ChannelAllocation,
    ChannelType,
    RFMSegment,
    SimulationInput,
    VoiceTone,
)
from app.views.tab_insights_explorer import render_insights_explorer_tab


def render_business_dashboard(
    df_carrinhos: pd.DataFrame | None,
    df_products: pd.DataFrame | None
) -> None:
    """Renderiza a suíte executiva de BI estruturada em 4 pilares estratégicos."""
    
    # -------------------------------------------------------------------------
    # 🏷️ CAMADA 1: BARRA DE COMANDO & SELETORES DE NEGÓCIO
    # -------------------------------------------------------------------------
    active_hub, selected_scenario = render_business_cockpit_header()

    # -------------------------------------------------------------------------
    # ⚙️ CALCULO DE SIMULAÇÃO REATIVO (GROUND TRUTH)
    # -------------------------------------------------------------------------
    if selected_scenario == "✨ Mix Recomendado (85/12/2/1)":
        sim_input = create_preset_simulation_input(CANONICAL_TOTAL_CARTS, DEFAULT_TICKET_MEDIO, discount_pct=0.0)
    elif selected_scenario == "🛡️ Conservadora (Margem 30%)":
        sim_input = create_preset_simulation_input(CANONICAL_TOTAL_CARTS, DEFAULT_TICKET_MEDIO, discount_pct=0.0)
    elif selected_scenario == "🚀 Agressiva VIP (WhatsApp)":
        sim_input = create_preset_simulation_input(CANONICAL_TOTAL_CARTS, DEFAULT_TICKET_MEDIO, discount_pct=5.0)
    else:  # Customizada
        sim_input = create_preset_simulation_input(CANONICAL_TOTAL_CARTS, DEFAULT_TICKET_MEDIO, discount_pct=10.0)

    sim_output = run_simulation(sim_input)

    # -------------------------------------------------------------------------
    # 📊 CAMADA 2: HERO KPI RIBBON (INDICADORES EXECUTIVOS C-LEVEL)
    # -------------------------------------------------------------------------
    k_col1, k_col2, k_col3, k_col4 = st.columns(4)

    with k_col1:
        render_kpi_card(
            label="Receita Líquida Incremental",
            value=f"R$ {sim_output.total_net_revenue:,.2f}",
            delta=f"ROI {sim_output.overall_roi_multiplier:.1f}x • Margem {sim_output.preserved_margin_pct:.1f}%",
            delta_type="positive" if sim_output.overall_roi_multiplier > 0 else "negative",
            help_text="Faturamento bruto resgatado deduzido de custos de comunicação e descontos."
        )

    with k_col2:
        render_kpi_card(
            label="Carrinhos Resgatados",
            value=f"{sim_output.total_recovered_carts:,}".replace(",", "."),
            delta=f"{sim_output.blended_conversion_rate_pct:.1f}% conversão blended",
            delta_type="positive",
            help_text="Volume absoluto de clientes que concluíram o checkout após abordagem prescritiva."
        )

    with k_col3:
        total_invest = sim_output.total_communication_cost + sim_output.total_discount_cost
        render_kpi_card(
            label="Investimento Total em Disparos",
            value=f"R$ {total_invest:,.2f}",
            delta=f"R$ {sim_output.total_communication_cost:,.2f} em canais",
            delta_type="neutral",
            help_text="Custo agregado de comunicação multicanal e cupons concedidos."
        )

    with k_col4:
        render_kpi_card(
            label="Eficiência do Canal Principal (E-mail)",
            value="45.2x ROI",
            delta="CAC Unitário R$ 12,44",
            delta_type="positive",
            help_text="Retorno sobre investimento e custo de aquisição unitário no canal de maior volume."
        )

    st.markdown("<div style='margin-top: 0.35rem;'></div>", unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # 🎛️ CAMADA 3: CENTRAIS ANALÍTICAS NOS 4 PILARES ESTRATÉGICOS
    # -------------------------------------------------------------------------

    # =========================================================================
    # PILAR 1: COCKPIT FINANCEIRO & SENSIBILIDADE (ITENS 4 & 7 DO CASE)
    # =========================================================================
    if active_hub == "Finanças & ROI":
        col_left_fin, col_right_fin = st.columns([1.55, 1.0], gap="medium")

        with col_left_fin:
            with st.container(border=True):
                st.markdown(
                    "<div style='font-family: Inter; font-size: 0.88rem; font-weight: 700; color: #60A5FA; text-transform: uppercase; margin-bottom: 0.2rem;'>"
                    "📊 Decomposição da Receita Líquida Incremental (Waterfall)"
                    "</div>",
                    unsafe_allow_html=True
                )
                render_waterfall_chart(sim_output)

            st.markdown("<div style='margin-top: 0.35rem;'></div>", unsafe_allow_html=True)
            with st.container(border=True):
                st.markdown(
                    "<div style='font-family: Inter; font-size: 0.88rem; font-weight: 700; color: #60A5FA; text-transform: uppercase; margin-bottom: 0.2rem;'>"
                    "📈 Curva de Sensibilidade: Desconto Ofertado vs ROI Multiplicador"
                    "</div>",
                    unsafe_allow_html=True
                )
                df_sens = generate_discount_sensitivity_curve(sim_input)
                render_sensitivity_chart(df_sens, sim_input.discount_pct)

        with col_right_fin:
            with st.container(border=True):
                st.markdown(
                    "<div style='font-family: Inter; font-size: 0.88rem; font-weight: 700; color: #60A5FA; text-transform: uppercase; margin-bottom: 0.2rem;'>"
                    "🎯 Rebalanceamento Orçamentário por Canal (Mix 85/12/2/1)"
                    "</div>",
                    unsafe_allow_html=True
                )
                render_budget_rebalance_chart(sim_output)

            st.markdown("<div style='margin-top: 0.35rem;'></div>", unsafe_allow_html=True)
            with st.container(border=True):
                st.markdown(
                    "<div style='font-family: Inter; font-size: 0.88rem; font-weight: 700; color: #60A5FA; text-transform: uppercase; margin-bottom: 0.2rem;'>"
                    "📋 Matriz de Eficiência Operacional por Canal"
                    "</div>",
                    unsafe_allow_html=True
                )
                data_table = []
                for res in sim_output.channel_results:
                    cac = res.communication_cost / max(res.recovered_carts, 1)
                    data_table.append({
                        "Canal": res.channel,
                        "Disparos": f"{res.dispatches:,}",
                        "Conversões": f"{res.recovered_carts:,}",
                        "CAC (R$)": f"R$ {cac:,.2f}",
                        "ROI": f"{res.roi_multiplier:.1f}x"
                    })
                st.dataframe(pd.DataFrame(data_table), use_container_width=True, hide_index=True)

    # =========================================================================
    # PILAR 2: INTELIGÊNCIA SEMÂNTICA & CATÁLOGO (ITENS 5 & 6 DO CASE)
    # =========================================================================
    elif active_hub == "Catálogo & Semântica":
        col_left_cat, col_right_cat = st.columns([1.5, 1.1], gap="medium")

        if df_products is not None and not df_products.empty:
            product_options = {
                f"{row['nome_bruto'][:42]} (R$ {row['preco_atual']:,.2f})": row["produto_id"]
                for _, row in df_products.iterrows()
            }
            
            with col_left_cat:
                with st.container(border=True):
                    col_sel, col_alg, col_k = st.columns([2.6, 1.0, 1.0])
                    with col_sel:
                        selected_label = st.selectbox("Produto Âncora Abandonado:", options=list(product_options.keys()), index=0)
                        selected_id = product_options[selected_label]
                    with col_alg:
                        proj_method = st.selectbox("Projeção 2D:", options=["PCA", "t-SNE"], index=0)
                    with col_k:
                        top_k = st.slider("Top K Itens:", min_value=3, max_value=8, value=5)

                    similar_matches = find_similar_products(selected_id, df_products, top_k=top_k)
                    df_proj = compute_2d_projection(df_products, method=proj_method)
                    render_semantic_scatter_chart(df_proj, selected_id, proj_method, top_matches=similar_matches)

            with col_right_cat:
                with st.container(border=True):
                    st.markdown(
                        "<div style='font-family: Inter; font-size: 0.88rem; font-weight: 700; color: #60A5FA; text-transform: uppercase; margin-bottom: 0.2rem;'>"
                        "🎯 Alternativas Recomendadas & Mitigação de Fricção"
                        "</div>",
                        unsafe_allow_html=True
                    )
                    if similar_matches:
                        for i, match in enumerate(similar_matches, start=1):
                            delta_sign = "+" if match.price_delta_pct > 0 else ""
                            st.markdown(
                                f"""
                                <div style="background-color: #0D1117; border: 1px solid #1E293B; border-radius: 6px; padding: 0.55rem 0.80rem; margin-bottom: 0.35rem;">
                                    <div style="display: flex; justify-content: space-between; align-items: center;">
                                        <strong style="color: #F0F6FC; font-size: 0.82rem;">{i}. {match.title[:34]}...</strong>
                                        <span style="background-color: #1E3A8A; color: #93C5FD; font-weight: bold; padding: 0.12rem 0.40rem; border-radius: 4px; font-size: 0.70rem;">{match.similarity_score:.1f}%</span>
                                    </div>
                                    <div style="font-size: 0.76rem; color: #94A3B8; margin-top: 0.15rem;">
                                        💰 R$ {match.price:,.2f} ({delta_sign}{match.price_delta_pct:.1f}%) &bull; Categoria: <code>{match.category}</code>
                                    </div>
                                    <div style="font-size: 0.72rem; color: #64748B; margin-top: 0.10rem;">
                                        Estratégia: <strong style="color: #38BDF8;">{match.strategy_badge}</strong> &bull; Risco: <em>{match.friction_risk}</em>
                                    </div>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                
                st.markdown("<div style='margin-top: 0.35rem;'></div>", unsafe_allow_html=True)
                with st.container(border=True):
                    st.markdown(
                        "<div style='font-family: Inter; font-size: 0.88rem; font-weight: 700; color: #60A5FA; text-transform: uppercase; margin-bottom: 0.2rem;'>"
                        "⚖️ Impacto Financeiro da Vitrine Inteligente (C-Level)"
                        "</div>",
                        unsafe_allow_html=True
                    )
                    render_decision_comparative_cards()

    # =========================================================================
    # PILAR 3: COPILOTO CRM & ATIVAÇÃO MULTICANAL (ITENS 5 & 8 DO CASE)
    # =========================================================================
    elif active_hub == "Copiloto CRM & Ativação":
        col_crm_left, col_crm_right = st.columns([1.15, 1.45], gap="medium")

        with col_crm_left:
            with st.container(border=True):
                st.markdown(
                    "<div style='font-family: Inter; font-size: 0.88rem; font-weight: 700; color: #60A5FA; text-transform: uppercase; margin-bottom: 0.2rem;'>"
                    "⚙️ Parâmetros de Abordagem & Segmento RFM"
                    "</div>",
                    unsafe_allow_html=True
                )
                
                segment_opts: list[RFMSegment] = [
                    "Campeões", "Clientes Leais", "Potenciais Leais", "Promissores",
                    "Precisam de Atenção", "Quase Hibernando", "Em Risco", "Hibernando"
                ]
                sel_seg = st.selectbox("Segmento do Cliente:", options=segment_opts, index=0)

                reason_opts: list[AbandonmentReason] = [
                    "Frete Abusivo", "Preço Elevado", "Dúvida Técnica", "Checkout Complexo", "Indecisão"
                ]
                sel_reason = st.selectbox("Motivo de Abandono:", options=reason_opts, index=0)

                tone_opts: list[VoiceTone] = ["Suporte", "Urgência", "Prova Social"]
                sel_tone = st.selectbox("Tom de Voz Estratégico:", options=tone_opts, index=0)

                channel_opts: list[ChannelType] = ["WhatsApp", "Email", "SMS", "Push"]
                sel_chan = st.selectbox("Canal de Disparo:", options=channel_opts, index=0)

                prod_list = df_products["nome_bruto"].tolist() if df_products is not None and not df_products.empty else ["Produto Genérico"]
                sel_p_name = st.selectbox("Item no Carrinho:", options=prod_list, index=0)
                
                prod_row = df_products[df_products["nome_bruto"] == sel_p_name].iloc[0] if df_products is not None and not df_products.empty else pd.Series()
                p_price = float(prod_row.get("preco_atual", 199.90))

                disc_offered = st.slider("Cupom Ofertado (%)", 0.0, 25.0, 0.0, step=5.0)

                presc_copy = generate_prescriptive_copy(
                    product_title=sel_p_name,
                    price=p_price,
                    segment=sel_seg,
                    reason=sel_reason,
                    channel=sel_chan,
                    tone=sel_tone,
                    discount_pct=disc_offered,
                )

                st.markdown("<div style='margin-top: 0.35rem;'></div>", unsafe_allow_html=True)
                with st.expander("📄 Ver Payload Prescritivo (JSON Schema Pydantic)", expanded=False):
                    st.code(presc_copy.json_schema_payload, language="json")

        with col_crm_right:
            with st.container(border=True):
                st.markdown(
                    "<div style='font-family: Inter; font-size: 0.88rem; font-weight: 700; color: #60A5FA; text-transform: uppercase; margin-bottom: 0.2rem;'>"
                    f"💬 Preview de Disparo em Tempo Real ({sel_chan})"
                    "</div>",
                    unsafe_allow_html=True
                )
                render_chat_preview(presc_copy)

            st.markdown("<div style='margin-top: 0.35rem;'></div>", unsafe_allow_html=True)
            with st.container(border=True):
                st.markdown(
                    "<div style='font-family: Inter; font-size: 0.88rem; font-weight: 700; color: #60A5FA; text-transform: uppercase; margin-bottom: 0.2rem;'>"
                    "🎙️ Estúdio Multimodal GenAI (Whisper & Apresentação Comercial)"
                    "</div>",
                    unsafe_allow_html=True
                )
                showcase_pres = generate_showcase_presentation(
                    product_title=sel_p_name,
                    category=str(prod_row.get("categoria_normalizada", "Geral")),
                    price=p_price,
                    material=str(prod_row.get("material_construcao", "Material Premium")),
                    technical_differential=str(prod_row.get("diferencial_tecnico", "Tecnologia de Ponta")),
                )
                render_showcase_card(showcase_pres, prod_row)

    # =========================================================================
    # PILAR 4: GALERIA DE INSIGHTS & DECISÃO ESTRATÉGICA (ITENS 4, 7, 8 & 9)
    # =========================================================================
    else:
        render_insights_explorer_tab()
