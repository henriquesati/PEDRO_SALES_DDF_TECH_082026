"""Componentes visuais de gráficos Plotly reutilizáveis e desacoplados (White Theme Standard)."""

from typing import List
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from app.constants.settings import (
    COLOR_BORDER,
    COLOR_DANGER_RED,
    COLOR_PRIMARY_BLUE,
    COLOR_PRIMARY_NAVY,
    COLOR_SUCCESS_EMERALD,
    COLOR_SUCCESS_GREEN,
    COLOR_WARNING_AMBER,
)
from app.constants.theme import apply_executive_layout
from app.types.models import ProductSimilarityMatch, SimulationOutput

def render_waterfall_chart(sim_output: SimulationOutput) -> None:
    """Renderiza gráfico de cascata (Waterfall) com decomposição de receita e custos no padrão White Theme."""
    fig = go.Figure(go.Waterfall(
        name="Economia da Ação",
        orientation="v",
        measure=["relative", "relative", "relative", "total"],
        x=["Receita Bruta", "Custo Comunicação", "Custo Desconto", "Receita Líquida"],
        textposition="outside",
        text=[
            f"+R$ {sim_output.total_gross_revenue:,.0f}",
            f"-R$ {sim_output.total_communication_cost:,.0f}",
            f"-R$ {sim_output.total_discount_cost:,.0f}",
            f"R$ {sim_output.total_net_revenue:,.0f}"
        ],
        y=[
            sim_output.total_gross_revenue,
            -sim_output.total_communication_cost,
            -sim_output.total_discount_cost,
            sim_output.total_net_revenue
        ],
        connector={"line": {"color": "#94A3B8", "width": 1.5, "dash": "dot"}},
        decreasing={"marker": {"color": COLOR_DANGER_RED}},
        increasing={"marker": {"color": COLOR_SUCCESS_GREEN}},
        totals={"marker": {"color": COLOR_PRIMARY_BLUE}}
    ))
    
    apply_executive_layout(fig, title="Decomposição da Receita Líquida Incremental", height=380, show_legend=False)
    fig.update_yaxes(title="Valor em Reais (R$)")
    st.plotly_chart(fig, use_container_width=True)

def render_sensitivity_chart(df_sensitivity: pd.DataFrame, current_discount: float) -> None:
    """Renderiza a curva de sensibilidade de desconto vs ROI multiplicador e margem preservada."""
    fig = go.Figure()

    # Linha de ROI Multiplicador
    fig.add_trace(go.Scatter(
        x=df_sensitivity["Desconto (%)"],
        y=df_sensitivity["ROI Multiplicador"],
        name="ROI Multiplicador (x)",
        mode="lines+markers",
        line=dict(color=COLOR_SUCCESS_GREEN, width=3.2),
        marker=dict(size=8, color=COLOR_PRIMARY_NAVY, symbol="circle"),
        yaxis="y1"
    ))

    # Linha de Margem Preservada se disponível
    if "Margem Preservada (%)" in df_sensitivity.columns:
        fig.add_trace(go.Scatter(
            x=df_sensitivity["Desconto (%)"],
            y=df_sensitivity["Margem Preservada (%)"],
            name="Margem Preservada (%)",
            mode="lines+markers",
            line=dict(color=COLOR_PRIMARY_BLUE, width=2.5, dash="dash"),
            marker=dict(size=6, color=COLOR_PRIMARY_BLUE),
            yaxis="y2"
        ))

    # Marcador do Cenário Atual
    fig.add_vline(
        x=current_discount,
        line_dash="dash",
        line_color=COLOR_WARNING_AMBER,
        annotation_text=f"Cenário Selecionado ({current_discount:.0f}%)",
        annotation_position="top right"
    )

    apply_executive_layout(fig, title="Curva de Sensibilidade & Ponto Ótimo de Margem", height=380, show_legend=True)
    fig.update_layout(
        xaxis=dict(title="Cupom de Desconto Ofertado (%)"),
        yaxis=dict(title="Multiplicador de ROI (x)", side="left"),
        yaxis2=dict(title="Margem Preservada (%)", overlaying="y", side="right", showgrid=False) if "Margem Preservada (%)" in df_sensitivity.columns else None
    )
    st.plotly_chart(fig, use_container_width=True)

def render_semantic_scatter_chart(
    df_projected: pd.DataFrame,
    selected_id: str | int,
    proj_method: str,
    top_matches: List[ProductSimilarityMatch] | None = None
) -> None:
    """Renderiza o mapa semântico 2D com clusterização por categoria e trajetórias vetoriais de resgate."""
    if df_projected.empty:
        st.info("Sem dados para projeção 2D.")
        return

    fig = px.scatter(
        df_projected,
        x="dim_x",
        y="dim_y",
        color="categoria_normalizada" if "categoria_normalizada" in df_projected.columns else None,
        hover_name="nome_bruto" if "nome_bruto" in df_projected.columns else None,
        hover_data={
            "preco_atual": ":.2f" if "preco_atual" in df_projected.columns else False,
            "sensibilidade_preco": True if "sensibilidade_preco" in df_projected.columns else False,
            "dim_x": False,
            "dim_y": False,
        },
        color_discrete_sequence=px.colors.qualitative.Safe,
    )
    fig.update_traces(marker=dict(size=8, opacity=0.75, line=dict(width=0.8, color="#FFFFFF")))

    # Destaque do Produto Âncora
    anchor_row = df_projected[df_projected["produto_id"].astype(str) == str(selected_id)]
    if not anchor_row.empty:
        anc_x = float(anchor_row.iloc[0]["dim_x"])
        anc_y = float(anchor_row.iloc[0]["dim_y"])
        anc_name = str(anchor_row.iloc[0].get("nome_bruto", "SKU Âncora"))

        # Ponto do produto âncora
        fig.add_trace(go.Scatter(
            x=[anc_x],
            y=[anc_y],
            mode="markers+text",
            marker=dict(size=16, color=COLOR_DANGER_RED, symbol="diamond", line=dict(width=2, color="#FFFFFF")),
            name="Produto Abandonado",
            text=[f" 🛒 {anc_name[:20]}..."],
            textposition="top center",
            textfont=dict(size=11, color=COLOR_DANGER_RED, family="Segoe UI")
        ))

        # Trajetórias para os top matches
        if top_matches:
            for match in top_matches[:3]:
                match_row = df_projected[df_projected["produto_id"].astype(str) == str(match.product_id)]
                if not match_row.empty:
                    m_x = float(match_row.iloc[0]["dim_x"])
                    m_y = float(match_row.iloc[0]["dim_y"])
                    
                    # Linha tracejada conectando o âncora ao similar
                    fig.add_trace(go.Scatter(
                        x=[anc_x, m_x],
                        y=[anc_y, m_y],
                        mode="lines+markers",
                        line=dict(color=COLOR_PRIMARY_BLUE, width=1.8, dash="dash"),
                        marker=dict(size=[0, 11], color=COLOR_SUCCESS_EMERALD, symbol="circle"),
                        name=f"→ {match.strategy_badge}: {match.title[:15]}",
                        showlegend=False,
                        hoverinfo="skip"
                    ))

    apply_executive_layout(
        fig,
        title=f"Espaço Vetorial 2D de Produtos & Trajetórias ({proj_method.upper()})",
        height=450,
        show_legend=True
    )
    fig.update_xaxes(title=f"Componente 1 ({proj_method.upper()})")
    fig.update_yaxes(title=f"Componente 2 ({proj_method.upper()})")
    st.plotly_chart(fig, use_container_width=True)

def render_budget_rebalance_chart() -> None:
    """Renderiza a comparação executiva entre a Alocação Convencional vs Otimizada Dadosfera."""
    canais = ["Push", "SMS", "WhatsApp VIP", "E-mail"]
    convencional = [10.0, 20.0, 30.0, 40.0]
    otimizado = [1.0, 2.0, 12.0, 85.0]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=canais,
        x=convencional,
        name="Mix Convencional (Dispersão)",
        orientation="h",
        marker=dict(color="#94A3B8"),
        text=[f"{v:.0f}%" for v in convencional],
        textposition="auto"
    ))
    fig.add_trace(go.Bar(
        y=canais,
        x=otimizado,
        name="Mix Prescritivo Dadosfera (85% ROI Máx)",
        orientation="h",
        marker=dict(color=COLOR_SUCCESS_GREEN),
        text=[f"{v:.0f}%" for v in otimizado],
        textposition="auto"
    ))

    apply_executive_layout(fig, title="Rebalanceamento Orçamentário de Resgate (Budget Allocation)", height=320, show_legend=True)
    fig.update_xaxes(title="Participação no Orçamento (%)", range=[0, 100])
    st.plotly_chart(fig, use_container_width=True)
