"""
Executive KPI Component

Renders clean, styled executive metric cards with subtle borders,
typography hierarchy, and contextual status badges.
"""

from typing import Optional
import streamlit as st


def render_kpi_card(
    title: str,
    value: str,
    delta: Optional[str] = None,
    delta_color: str = "normal",  # "normal", "inverse", "off"
    help_text: Optional[str] = None,
):
    """Render a standard Streamlit metric with custom CSS styling."""
    st.metric(
        label=title,
        value=value,
        delta=delta,
        delta_color=delta_color,
        help=help_text,
    )


def render_kpi_row(kpis: list):
    """
    Render a responsive row of KPI cards.
    Each item in kpis is a dict: {label, value, delta, help_text, delta_color}
    """
    cols = st.columns(len(kpis))
    for col, kpi in zip(cols, kpis):
        with col:
            st.metric(
                label=kpi.get("label", ""),
                value=kpi.get("value", ""),
                delta=kpi.get("delta"),
                delta_color=kpi.get("delta_color", "normal"),
                help=kpi.get("help_text"),
            )
