"""Aba 1: Simulador Prescritivo de ROI & Sensibilidade de Resgate (View)."""

import pandas as pd
import streamlit as st

from app.components.charts import (
    render_budget_rebalance_chart,
    render_sensitivity_chart,
    render_waterfall_chart,
)
from app.components.kpi_cards import render_kpi_card
from app.constants.settings import (
    CANONICAL_TOTAL_CARTS,
    CUSTO_POR_DISPARO,
    DEFAULT_TICKET_MEDIO,
    PRESCRIBED_MIX,
    TAXA_CONVERSAO_POR_CANAL,
)
from app.services.simulation_service import (
    create_preset_simulation_input,
    generate_discount_sensitivity_curve,
    run_simulation,
)
from app.types.models import ChannelAllocation, SimulationInput

def render_roi_tab(df_summary: pd.DataFrame | None = None) -> None:
    """Renderiza a visualização da aba de simulação de ROI."""
    st.subheader("📊 Simulador de Sensibilidade de ROI & Otimização de Resgate")
    st.markdown(
        "Calibre os parâmetros operacionais da campanha de resgate para projetar a "
        "recuperação de receita líquida, preservação de margem e eficiência por canal de comunicação."
    )
    
    # -------------------------------------------------------------------------
    # 🎛️ CONTROLES DA CAMPANHA & PRESET INTELIGENTE
    # -------------------------------------------------------------------------
    with st.expander("⚙️ Parâmetros Operacionais & Mix de Canais", expanded=True):
        col_mode1, col_mode2 = st.columns([2, 2])
        with col_mode1:
            preset_choice = st.radio(
                "Estratégia de Alocação de Orçamento:",
                options=["✨ Mix Recomendado Dadosfera (85% E-mail / 12% Wpp VIP / 2% SMS / 1% Push)", "🛠️ Alocação Customizada Manual"],
                index=0,
                horizontal=True
            )
        with col_mode2:
            st.caption("💡 **Recomendação Canônica:** Concentrar 85% no E-mail (CAC R$ 12,44) e 12% no WhatsApp VIP para clientes de alto ticket maximiza o ROI em até 45x.")

        st.divider()
        col_p1, col_p2, col_p3 = st.columns(3)
        with col_p1:
            total_carrinhos = st.slider(
                "Volume de Carrinhos em Risco",
                min_value=1_000,
                max_value=30_000,
                value=CANONICAL_TOTAL_CARTS,
                step=500,
                help="Volume total de sessões de abandono semestrais registradas no Lakehouse."
            )
            ticket_medio = st.number_input(
                "Ticket Médio do Catálogo (R$)",
                min_value=50.0,
                max_value=2_000.0,
                value=DEFAULT_TICKET_MEDIO,
                step=10.0,
                format="%.2f"
            )
            
        with col_p2:
            desconto_pct = st.slider(
                "Cupom de Desconto Ofertado (%)",
                min_value=0.0,
                max_value=30.0,
                value=0.0 if "Recomendado" in preset_choice else 10.0,
                step=1.0,
                help="Desconto médio aplicado. Nota: Na estratégia recomendada, a margem é preservada sem cupom agressivo."
            )
            elasticidade = st.slider(
                "Elasticidade Conversão / Desconto",
                min_value=0.5,
                max_value=3.0,
                value=1.2,
                step=0.1,
                help="Sensibilidade dos clientes ao desconto ofertado."
            )
            
        with col_p3:
            st.markdown("**Mix de Canais de Disparo (%)**")
            if "Recomendado" in preset_choice:
                st.info("📨 **E-mail:** 85% | 💬 **WhatsApp VIP:** 12% | 📱 **SMS:** 2% | 🔔 **Push:** 1%")
                wpp_norm = PRESCRIBED_MIX["WhatsApp"]
                email_norm = PRESCRIBED_MIX["Email"]
                sms_norm = PRESCRIBED_MIX["SMS"]
                push_norm = PRESCRIBED_MIX["Push"]
            else:
                wpp_share = st.slider("WhatsApp VIP (R$ 12,00)", 0, 100, 30)
                email_share = st.slider("E-mail (R$ 1,02)", 0, 100, 40)
                sms_share = st.slider("SMS (R$ 3,00)", 0, 100, 20)
                push_share = st.slider("Push (R$ 1,67)", 0, 100, 10)
                total_s = wpp_share + email_share + sms_share + push_share
                if total_s == 0:
                    wpp_norm, email_norm, sms_norm, push_norm = 0.25, 0.25, 0.25, 0.25
                else:
                    wpp_norm, email_norm, sms_norm, push_norm = wpp_share/total_s, email_share/total_s, sms_share/total_s, push_share/total_s

    # -------------------------------------------------------------------------
    # 🧠 EXECUÇÃO DO SERVIÇO PURO
    # -------------------------------------------------------------------------
    allocations = (
        ChannelAllocation(
            channel="Email",
            share_pct=email_norm,
            dispatches_count=int(total_carrinhos * email_norm),
            cost_per_dispatch=CUSTO_POR_DISPARO["Email"],
            base_conversion_rate=TAXA_CONVERSAO_POR_CANAL["Email"],
        ),
        ChannelAllocation(
            channel="WhatsApp",
            share_pct=wpp_norm,
            dispatches_count=int(total_carrinhos * wpp_norm),
            cost_per_dispatch=CUSTO_POR_DISPARO["WhatsApp"],
            base_conversion_rate=TAXA_CONVERSAO_POR_CANAL["WhatsApp"],
        ),
        ChannelAllocation(
            channel="SMS",
            share_pct=sms_norm,
            dispatches_count=int(total_carrinhos * sms_norm),
            cost_per_dispatch=CUSTO_POR_DISPARO["SMS"],
            base_conversion_rate=TAXA_CONVERSAO_POR_CANAL["SMS"],
        ),
        ChannelAllocation(
            channel="Push",
            share_pct=push_norm,
            dispatches_count=int(total_carrinhos * push_norm),
            cost_per_dispatch=CUSTO_POR_DISPARO["Push"],
            base_conversion_rate=TAXA_CONVERSAO_POR_CANAL["Push"],
        ),
    )
    
    sim_input = SimulationInput(
        total_abandoned_carts=total_carrinhos,
        average_ticket=ticket_medio,
        discount_pct=desconto_pct,
        conversion_elasticity=elasticidade,
        channel_allocations=allocations,
    )
    
    sim_output = run_simulation(sim_input)
    
    # -------------------------------------------------------------------------
    # 📈 CARDS DE KPIS EXECUTIVOS
    # -------------------------------------------------------------------------
    st.markdown("### 🏆 Indicadores de Performance Projetados (C-Level)")
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
    
    with kpi_col1:
        render_kpi_card(
            label="Carrinhos Resgatados",
            value=f"{sim_output.total_recovered_carts:,}".replace(",", "."),
            delta=f"{sim_output.blended_conversion_rate_pct:.1f}% conversão blended",
            delta_type="positive",
            help_text="Volume absoluto de sessões convertidas em pedidos finalizados."
        )
    with kpi_col2:
        render_kpi_card(
            label="Receita Bruta Gerada",
            value=f"R$ {sim_output.total_gross_revenue:,.2f}",
            delta="Faturamento Bruto Resgatado",
            delta_type="positive",
        )
    with kpi_col3:
        total_invest = sim_output.total_communication_cost + sim_output.total_discount_cost
        render_kpi_card(
            label="Investimento Total (CAC+Cupom)",
            value=f"R$ {total_invest:,.2f}",
            delta=f"R$ {sim_output.total_communication_cost:,.2f} em disparos",
            delta_type="neutral",
        )
    with kpi_col4:
        render_kpi_card(
            label="Receita Líquida Incremental",
            value=f"R$ {sim_output.total_net_revenue:,.2f}",
            delta=f"ROI {sim_output.overall_roi_multiplier:.1f}x • Margem {sim_output.preserved_margin_pct:.1f}%",
            delta_type="positive" if sim_output.overall_roi_multiplier > 0 else "negative",
        )
        
    st.divider()
    
    # -------------------------------------------------------------------------
    # 📊 GRÁFICOS INTERATIVOS
    # -------------------------------------------------------------------------
    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        render_waterfall_chart(sim_output)
        
    with chart_col2:
        df_sensitivity = generate_discount_sensitivity_curve(sim_input)
        render_sensitivity_chart(df_sensitivity, desconto_pct)

    # -------------------------------------------------------------------------
    # 📋 REBALANCEAMENTO ORÇAMENTÁRIO & TABELA DE EFICIÊNCIA
    # -------------------------------------------------------------------------
    st.divider()
    st.markdown("#### 📱 Detalhamento de Eficiência & Rebalanceamento de Canais")
    
    tab_col1, tab_col2 = st.columns([3, 2])
    with tab_col1:
        channel_rows = [
            {
                "Canal": c.channel,
                "Disparos": f"{c.dispatches:,}".replace(",", "."),
                "Taxa Conv. (%)": f"{c.conversion_rate_pct:.1f}%",
                "Carrinhos Resgatados": f"{c.recovered_carts:,}".replace(",", "."),
                "Receita Bruta (R$)": f"R$ {c.gross_recovered_revenue:,.2f}",
                "Custo Comunicação (R$)": f"R$ {c.communication_cost:,.2f}",
                "Receita Líquida (R$)": f"R$ {c.net_recovered_revenue:,.2f}",
                "ROI Multiplicador": f"{c.roi_multiplier:.1f}x",
            }
            for c in sim_output.channel_breakdown
        ]
        st.dataframe(pd.DataFrame(channel_rows), use_container_width=True, hide_index=True)

    with tab_col2:
        render_budget_rebalance_chart()
