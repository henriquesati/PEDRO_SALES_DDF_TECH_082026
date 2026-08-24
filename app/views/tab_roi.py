"""Aba 1: Simulador Prescritivo de ROI & Sensibilidade de Resgate (View)."""

import pandas as pd
import streamlit as st

from app.components.charts import render_sensitivity_chart, render_waterfall_chart
from app.components.kpi_cards import render_kpi_card
from app.constants.settings import (
    CUSTO_POR_DISPARO,
    DEFAULT_TICKET_MEDIO,
    TAXA_CONVERSAO_POR_CANAL,
)
from app.services.simulation_service import (
    generate_discount_sensitivity_curve,
    run_simulation,
)
from app.types.models import ChannelAllocation, SimulationInput

def render_roi_tab(df_summary: pd.DataFrame | None = None) -> None:
    """Renderiza a visualização da aba de simulação de ROI."""
    st.subheader("📊 Simulador de Sensibilidade de ROI & Otimização de Resgate")
    st.markdown(
        "Calibre os parâmetros orçamentários da campanha de resgate para projetar a "
        "recuperação de receita líquida, volume de conversões e eficiência de canais."
    )
    
    # -------------------------------------------------------------------------
    # 🎛️ CONTROLES DA CAMPANHA
    # -------------------------------------------------------------------------
    with st.expander("⚙️ Parâmetros Operacionais da Campanha", expanded=True):
        col_p1, col_p2, col_p3 = st.columns(3)
        with col_p1:
            total_carrinhos = st.slider(
                "Volume de Carrinhos em Risco",
                min_value=1_000,
                max_value=50_000,
                value=7_500,
                step=500,
                help="Quantidade total de sessões de abandono elegíveis para comunicação."
            )
            ticket_medio = st.number_input(
                "Ticket Médio do Carrinho (R$)",
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
                value=10.0,
                step=1.0,
                help="Desconto percentual aplicado na finalização do pedido."
            )
            elasticidade = st.slider(
                "Elasticidade de Conversão / Desconto",
                min_value=0.5,
                max_value=3.0,
                value=1.5,
                step=0.1,
                help="Fator multiplicador do efeito do desconto sobre a taxa de conversão."
            )
            
        with col_p3:
            st.markdown("**Mix de Canais de Resgate (%)**")
            wpp_share = st.slider("WhatsApp (R$ 12,00)", 0, 100, 40)
            email_share = st.slider("E-mail (R$ 1,02)", 0, 100, 40)
            sms_share = st.slider("SMS (R$ 3,00)", 0, 100, 20)
            
            # Normalização
            total_share = wpp_share + email_share + sms_share
            if total_share == 0:
                wpp_norm, email_norm, sms_norm = 0.34, 0.33, 0.33
            else:
                wpp_norm = wpp_share / total_share
                email_norm = email_share / total_share
                sms_norm = sms_share / total_share

    # -------------------------------------------------------------------------
    # 🧠 CHAMADA AO SERVIÇO PURO
    # -------------------------------------------------------------------------
    allocations = (
        ChannelAllocation(
            channel="WhatsApp",
            share_pct=wpp_norm,
            dispatches_count=int(total_carrinhos * wpp_norm),
            cost_per_dispatch=CUSTO_POR_DISPARO["WhatsApp"],
            base_conversion_rate=TAXA_CONVERSAO_POR_CANAL["WhatsApp"],
        ),
        ChannelAllocation(
            channel="Email",
            share_pct=email_norm,
            dispatches_count=int(total_carrinhos * email_norm),
            cost_per_dispatch=CUSTO_POR_DISPARO["Email"],
            base_conversion_rate=TAXA_CONVERSAO_POR_CANAL["Email"],
        ),
        ChannelAllocation(
            channel="SMS",
            share_pct=sms_norm,
            dispatches_count=int(total_carrinhos * sms_norm),
            cost_per_dispatch=CUSTO_POR_DISPARO["SMS"],
            base_conversion_rate=TAXA_CONVERSAO_POR_CANAL["SMS"],
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
    # 📈 CARDS DE KPIS
    # -------------------------------------------------------------------------
    st.markdown("### 🏆 Indicadores de Performance Projetados")
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
    
    with kpi_col1:
        render_kpi_card(
            label="Carrinhos Resgatados",
            value=f"{sim_output.total_recovered_carts:,}".replace(",", "."),
            delta=f"{sim_output.blended_conversion_rate_pct:.1f}% conversão",
            is_positive=True,
            help_text="Volume absoluto de carrinhos convertidos em vendas."
        )
    with kpi_col2:
        render_kpi_card(
            label="Receita Bruta Gerada",
            value=f"R$ {sim_output.total_gross_revenue:,.2f}",
            delta="Faturamento Bruto",
            is_positive=True,
        )
    with kpi_col3:
        total_invest = sim_output.total_communication_cost + sim_output.total_discount_cost
        render_kpi_card(
            label="Investimento Total (CAC+Desc)",
            value=f"R$ {total_invest:,.2f}",
            delta=f"R$ {sim_output.total_communication_cost:,.2f} disparos",
            is_positive=False,
        )
    with kpi_col4:
        render_kpi_card(
            label="Receita Líquida Incremental",
            value=f"R$ {sim_output.total_net_revenue:,.2f}",
            delta=f"ROI {sim_output.overall_roi_multiplier:.1f}x",
            is_positive=(sim_output.overall_roi_multiplier > 0),
        )
        
    st.divider()
    
    # -------------------------------------------------------------------------
    # 📊 GRÁFICOS INTERATIVOS
    # -------------------------------------------------------------------------
    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        st.markdown("#### 🌊 Decomposição de Receita Líquida (Waterfall)")
        render_waterfall_chart(sim_output)
        
    with chart_col2:
        st.markdown("#### 🎯 Curva de Sensibilidade (ROI vs Desconto)")
        df_sensitivity = generate_discount_sensitivity_curve(sim_input)
        render_sensitivity_chart(df_sensitivity, desconto_pct)

    # -------------------------------------------------------------------------
    # 📋 TABELA DE EFICIÊNCIA
    # -------------------------------------------------------------------------
    st.markdown("#### 📱 Detalhamento de Eficiência por Canal")
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
