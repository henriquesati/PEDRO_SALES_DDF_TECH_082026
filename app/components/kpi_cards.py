"""Componente atômico para renderização de KPI Cards com deltas e formatação."""

import streamlit as st

def render_kpi_card(
    label: str,
    value: str,
    delta: str | None = None,
    is_positive: bool = True,
    help_text: str | None = None,
) -> None:
    """Renderiza um card visual de métrica formatado."""
    delta_html = ""
    if delta:
        delta_class = "positive" if is_positive else "negative"
        arrow = "▲" if is_positive else "▼"
        delta_html = f'<div class="kpi-delta {delta_class}">{arrow} {delta}</div>'
        
    tooltip_html = f' title="{help_text}"' if help_text else ""
    
    html = f"""
    <div class="kpi-card"{tooltip_html}>
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        {delta_html}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
