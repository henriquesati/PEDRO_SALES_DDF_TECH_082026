"""Componente atômico para renderização de KPI Cards com deltas e formatação executiva."""

import streamlit as st

def render_kpi_card(
    label: str,
    value: str,
    delta: str | None = None,
    delta_type: str = "positive",  # "positive", "negative", "neutral", "purple"
    help_text: str | None = None,
) -> None:
    """Renderiza um card visual de métrica formatado com visual executivo."""
    delta_html = ""
    if delta:
        arrow = "▲" if delta_type == "positive" else ("▼" if delta_type == "negative" else "•")
        delta_html = f'<div class="kpi-delta {delta_type}">{arrow} {delta}</div>'
        
    tooltip_html = f' title="{help_text}"' if help_text else ""
    
    html = f"""
    <div class="kpi-card"{tooltip_html}>
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        {delta_html}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
