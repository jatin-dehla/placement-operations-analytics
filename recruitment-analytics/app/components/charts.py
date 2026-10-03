"""
Plotly Data Visualization Components Module

Provides interactive, portfolio-grade Plotly charts tailored to the
blue/slate theme of the Recruitment Funnel & Capacity Optimization Platform.
"""

from typing import Optional, List, Dict, Any
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Curated Executive Palette
COLOR_PRIMARY = "#1e40af"       # Deep Corporate Blue (Performance Metrics)
COLOR_SECONDARY = "#2563eb"     # Royal Blue (Secondary Volume / Active)
COLOR_TEAL = "#0ea5e9"          # Sky / Cyan
COLOR_SUCCESS = "#10b981"       # Emerald Green (Positive Outcomes / Hires / Passes)
COLOR_DANGER = "#ef4444"        # Crimson Red (Drop-offs / SLA Breaches / Failures)
COLOR_WARNING = "#f59e0b"       # Amber Orange (Pending / High Load)
COLOR_SLATE = "#64748b"         # Neutral Slate Gray

OUTCOME_COLORS = {
    "Hired": "#10b981",
    "Rejected": "#ef4444",
    "Active": "#2563eb",
    "Withdrawn": "#64748b",
}

STAGE_COLORS = [
    "#1e3a8a", "#1e40af", "#2563eb", "#3b82f6", "#60a5fa", "#93c5fd", "#10b981"
]


def _apply_layout_styling(fig: go.Figure, title: str, height: int = 380) -> go.Figure:
    """Apply unified font, background, margin, and legend styling to Plotly figures."""
    fig.update_layout(
        title=dict(
            text=f"<b>{title}</b>",
            font=dict(size=17, family="'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif", color="#1e293b"),
            x=0.01,
            y=0.97,
        ),
        margin=dict(l=24, r=24, t=44, b=24),
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif", size=12, color="#475569"),
        hoverlabel=dict(bgcolor="#0f172a", font_size=12, font_family="sans-serif"),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.12,
            xanchor="center",
            x=0.5,
            font=dict(size=11),
        ),
    )
    fig.update_xaxes(showgrid=True, gridcolor="#f1f5f9", zeroline=False)
    fig.update_yaxes(showgrid=True, gridcolor="#f1f5f9", zeroline=False)
    return fig


def render_funnel_chart(
    df: pd.DataFrame,
    stage_col: str,
    val_col: str,
    title: str = "Recruitment Funnel",
    height: int = 380,
):
    """Render a simplified, clean Funnel chart displaying only stage names and counts."""
    if df.empty:
        st.info("No data available for funnel visualization.")
        return

    # Simplified labels: stage name and formatted candidate count
    fig = go.Figure(
        go.Funnel(
            y=df[stage_col],
            x=df[val_col],
            textinfo="text",
            text=[f"{val:,}" for val in df[val_col]],
            marker=dict(
                color=STAGE_COLORS[:len(df)],
                line=dict(width=1, color="#ffffff"),
            ),
            connector=dict(line=dict(color="#cbd5e1", width=1.5, dash="solid")),
        )
    )
    _apply_layout_styling(fig, title, height=height)
    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})


def render_donut_chart(
    df: pd.DataFrame,
    names_col: str,
    values_col: str,
    title: str,
    color_map: Optional[Dict[str, str]] = None,
    height: int = 380,
    hole: float = 0.52,
):
    """Render a modern Donut chart with legend positioned below the chart."""
    if df.empty:
        st.info(f"No data available for {title}.")
        return

    fig = px.pie(
        df,
        names=names_col,
        values=values_col,
        hole=hole,
        color=names_col if color_map else None,
        color_discrete_map=color_map,
        color_discrete_sequence=[COLOR_PRIMARY, COLOR_SUCCESS, COLOR_SECONDARY, COLOR_SLATE, COLOR_DANGER],
    )
    fig.update_traces(
        textposition="inside",
        textinfo="percent+label",
        marker=dict(line=dict(color="#ffffff", width=2)),
    )
    _apply_layout_styling(fig, title, height=height)
    # Ensure legend is placed neatly below chart
    fig.update_layout(
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.08,
            xanchor="center",
            x=0.5,
            font=dict(size=11),
        )
    )
    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})


def render_bar_chart(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    title: str,
    orientation: str = "v",
    color: Optional[str] = None,
    color_discrete_sequence: Optional[List[str]] = None,
    height: int = 380,
):
    """Render a standard vertical or horizontal bar chart without toolbar."""
    if df.empty:
        st.info(f"No data available for {title}.")
        return

    fig = px.bar(
        df,
        x=x_col,
        y=y_col,
        orientation=orientation,
        color=color,
        color_discrete_sequence=color_discrete_sequence or [COLOR_PRIMARY],
        text_auto=True,
    )
    fig.update_traces(textposition="outside", marker=dict(cornerradius=4))
    _apply_layout_styling(fig, title, height=height)
    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})


def render_grouped_bar_chart(
    df: pd.DataFrame,
    x_col: str,
    y_cols: List[str],
    title: str,
    color_discrete_sequence: Optional[List[str]] = None,
    height: int = 380,
):
    """Render a multi-metric grouped bar chart with legend positioned below."""
    if df.empty:
        st.info(f"No data available for {title}.")
        return

    fig = px.bar(
        df,
        x=x_col,
        y=y_cols,
        barmode="group",
        color_discrete_sequence=color_discrete_sequence or [COLOR_PRIMARY, COLOR_SUCCESS, COLOR_DANGER],
        text_auto=True,
    )
    fig.update_traces(textposition="outside", marker=dict(cornerradius=4))
    _apply_layout_styling(fig, title, height=height)
    fig.update_layout(
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.12,
            xanchor="center",
            x=0.5,
            title="",
            font=dict(size=11),
        )
    )
    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})


def render_stacked_bar_chart(
    df: pd.DataFrame,
    x_col: str,
    y_cols: List[str],
    title: str,
    color_discrete_sequence: Optional[List[str]] = None,
    height: int = 380,
):
    """Render stacked bar charts with legend positioned below."""
    if df.empty:
        st.info(f"No data available for {title}.")
        return

    fig = px.bar(
        df,
        x=x_col,
        y=y_cols,
        barmode="stack",
        color_discrete_sequence=color_discrete_sequence or [COLOR_SLATE, COLOR_PRIMARY, COLOR_SUCCESS, COLOR_DANGER],
        text_auto=True,
    )
    fig.update_traces(marker=dict(cornerradius=3))
    _apply_layout_styling(fig, title, height=height)
    fig.update_layout(
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.12,
            xanchor="center",
            x=0.5,
            title="",
            font=dict(size=11),
        )
    )
    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})


def render_heatmap(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    z_col: str,
    title: str,
    height: int = 380,
):
    """Render a 2D heatmap matrix with hidden modebar."""
    if df.empty:
        st.info(f"No data available for {title}.")
        return

    pivot_df = df.pivot(index=y_col, columns=x_col, values=z_col).fillna(0)
    fig = px.imshow(
        pivot_df,
        labels=dict(x=x_col, y=y_col, color=z_col),
        x=pivot_df.columns,
        y=pivot_df.index,
        color_continuous_scale="Blues",
        text_auto=True,
        aspect="auto",
    )
    _apply_layout_styling(fig, title, height=height)
    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})

