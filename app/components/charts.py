"""Componentes visuais de gráficos Plotly reutilizáveis e desacoplados."""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from app.constants.settings import (
    COLOR_DANGER_RED,
    COLOR_PRIMARY_NAVY,
    COLOR_SUCCESS_GREEN,
    COLOR_WARNING_AMBER,
)
from app.types.models import SimulationOutput

def render_waterfall_chart(sim_output: SimulationOutput) -> None:
    """Renderiza gráfico de cascata (Waterfall) com decomposição de receita e custos."""
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
        connector={"line": {"color": "#64748B"}},
        decreasing={"marker": {"color": COLOR_DANGER_RED}},
        increasing={"marker": {"color": COLOR_SUCCESS_GREEN}},
        totals={"marker": {"color": COLOR_PRIMARY_NAVY}}
    ))
    fig.update_layout(
        height=360,
        margin=dict(l=20, r=20, t=20, b=20),
        plot_bgcolor="#FFFFFF",
        yaxis_title="R$ (Reais)",
    )
    st.plotly_chart(fig, use_container_width=True)

def render_sensitivity_chart(df_sensitivity: pd.DataFrame, current_discount: float) -> None:
    """Renderiza a curva de sensibilidade de desconto vs ROI multiplicador."""
    fig = px.line(
        df_sensitivity,
        x="Desconto (%)",
        y="ROI Multiplicador",
        markers=True,
        title="Curva de Elasticidade e Ponto Ótimo de Margem",
        labels={"ROI Multiplicador": "Multiplicador de ROI (x)"}
    )
    fig.update_traces(
        line=dict(color=COLOR_SUCCESS_GREEN, width=3),
        marker=dict(size=8, color=COLOR_PRIMARY_NAVY)
    )
    fig.add_vline(x=current_discount, line_dash="dash", line_color=COLOR_WARNING_AMBER, annotation_text="Cenário Atual")
    fig.update_layout(
        height=360,
        margin=dict(l=20, r=20, t=40, b=20),
        plot_bgcolor="#FFFFFF",
    )
    st.plotly_chart(fig, use_container_width=True)

def render_semantic_scatter_chart(df_projected: pd.DataFrame, selected_id: str | int, proj_method: str) -> None:
    """Renderiza o mapa semântico 2D com clusterização de categorias."""
    fig = px.scatter(
        df_projected,
        x="dim_x",
        y="dim_y",
        color="categoria_normalizada",
        hover_name="nome_bruto",
        hover_data={
            "preco_atual": ":.2f",
            "sensibilidade_preco": True,
            "motivo_raiz": True,
            "dim_x": False,
            "dim_y": False,
        },
        title=f"Clusterização Semântica do Catálogo ({len(df_projected)} SKUs)",
        labels={"dim_x": f"Componente 1 ({proj_method})", "dim_y": f"Componente 2 ({proj_method})"},
    )
    fig.update_traces(marker=dict(opacity=0.85, line=dict(width=1, color="#334155")))
    fig.update_layout(
        height=420,
        margin=dict(l=10, r=10, t=40, b=10),
        plot_bgcolor="#F8FAFC",
        legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5)
    )
    st.plotly_chart(fig, use_container_width=True)
