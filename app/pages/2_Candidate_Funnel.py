"""
Page 2: Candidate Funnel Monitoring
Mirrors Power BI Candidate Funnel Monitoring page.
Analyzes stage conversion rates, transition drop-offs, share of total candidate loss,
evaluation scoring, and process delays by stage.
"""

import streamlit as st
from components.filters import render_sidebar_filters
from components.charts import (
    render_funnel_chart,
    render_bar_chart,
    render_donut_chart,
    COLOR_PRIMARY,
    COLOR_DANGER,
    COLOR_WARNING,
    COLOR_SUCCESS,
)
from utils.queries import (
    get_candidate_progression_pipeline,
    get_transition_dropoffs,
    get_stage_conversion_table,
    get_process_delays_by_stage,
)

st.set_page_config(
    page_title="Candidate Funnel | Placement Analytics",
    page_icon="🔍",
    layout="wide",
)

# Title Hierarchy: Page Title 36-40px
st.markdown('<div class="page-title">🔍 Candidate Funnel Monitoring</div>', unsafe_allow_html=True)
st.markdown('<div class="page-subtitle">Deep-dive into recruitment stage conversion velocity, candidate attrition drop-offs, evaluation scoring, and process delays.</div>', unsafe_allow_html=True)

# Sidebar Filters
filters = render_sidebar_filters()

# Retrieve Funnel Datasets
funnel_df = get_candidate_progression_pipeline(filters)
dropoffs_df = get_transition_dropoffs(filters)
conv_table_df = get_stage_conversion_table(filters)
delays_df = get_process_delays_by_stage(filters)

# Section 1: Funnel Performance Summary KPIs
st.markdown('<div class="section-header">⚡ Funnel Performance Summary</div>', unsafe_allow_html=True)

if not dropoffs_df.empty:
    max_drop_row = dropoffs_df.loc[dropoffs_df["dropoff_count"].idxmax()]
    highest_drop_trans = max_drop_row["transition"]
    highest_drop_count = f"{max_drop_row['dropoff_count']:,} ({max_drop_row['share_of_total_loss_pct']:.1f}% of total loss)"
else:
    highest_drop_trans = "N/A"
    highest_drop_count = "0"

if not funnel_df.empty:
    max_pass_row = funnel_df.loc[funnel_df["stage_pass_rate_pct"].idxmax()]
    highest_pass_stage = f"{max_pass_row['stage_name']} ({max_pass_row['stage_pass_rate_pct']:.1f}%)"
else:
    highest_pass_stage = "N/A"

if not delays_df.empty and "avg_score" in delays_df.columns:
    overall_avg_score = delays_df["avg_score"].mean()
    avg_score_val = f"{overall_avg_score:.1f} / 100"
else:
    avg_score_val = "N/A"

k1, k2, k3 = st.columns(3)
with k1:
    st.metric(
        label="Highest Drop-off Point",
        value=highest_drop_trans,
        delta=highest_drop_count,
        delta_color="inverse",
        help="Recruitment transition step where the largest candidate volume exits.",
    )
with k2:
    st.metric(
        label="Highest Pass Rate Stage",
        value=highest_pass_stage,
        delta="Max Stage Conversion",
        delta_color="normal",
        help="Evaluation milestone with the highest candidate conversion rate.",
    )
with k3:
    st.metric(
        label="Average Evaluation Score",
        value=avg_score_val,
        help="Mean candidate evaluation score across all assessed stages.",
    )

# Section 2: Recruitment Funnel & Stage Drop-offs
st.markdown('<div class="section-header">🔄 Recruitment Funnel & Stage Drop-offs</div>', unsafe_allow_html=True)
c1, c2 = st.columns(2)

with c1:
    if not funnel_df.empty:
        render_funnel_chart(
            funnel_df,
            stage_col="stage_name",
            val_col="total_candidates_entered",
            title="Recruitment Funnel",
            height=380,
        )
    else:
        st.info("No funnel data matches current filters.")

with c2:
    if not dropoffs_df.empty:
        render_bar_chart(
            dropoffs_df,
            x_col="dropoff_count",
            y_col="transition",
            title="Stage Drop-offs",
            orientation="h",
            color_discrete_sequence=[COLOR_DANGER],
            height=380,
        )
    else:
        st.info("No drop-off records available.")

# Section 3: Share of Candidate Loss & Stage Conversion Matrix
st.markdown('<div class="section-header">📊 Loss Distribution & Stage Conversion Table</div>', unsafe_allow_html=True)
c3, c4 = st.columns([1, 1])

with c3:
    if not dropoffs_df.empty:
        render_donut_chart(
            dropoffs_df,
            names_col="transition",
            values_col="dropoff_count",
            title="Share of Total Candidate Loss",
            height=380,
        )
    else:
        st.info("No candidate loss distribution data available.")

with c4:
    st.markdown('<div style="font-size: 17px; font-weight: 600; color: #1e293b; margin-top: 0.25rem; margin-bottom: 0.75rem;"><b>Stage Conversion & Pipeline Retention</b></div>', unsafe_allow_html=True)
    if not conv_table_df.empty:
        st.dataframe(
            conv_table_df,
            hide_index=True,
            use_container_width=True,
            height=340,
        )
    else:
        st.info("No conversion table data available.")

# Section 4: Evaluation Standards & Process Delays
st.markdown('<div class="section-header">⏱️ Stage Evaluation Scores & Process Delays</div>', unsafe_allow_html=True)
c5, c6 = st.columns(2)

with c5:
    if not delays_df.empty:
        render_bar_chart(
            delays_df,
            x_col="stage_name",
            y_col="avg_score",
            title="Stage Evaluation Scores (AVG)",
            orientation="v",
            color_discrete_sequence=[COLOR_PRIMARY],
            height=380,
        )
    else:
        st.info("No evaluation score data available.")

with c6:
    if not delays_df.empty:
        render_bar_chart(
            delays_df,
            x_col="stage_name",
            y_col="delayed_records",
            title="Process Delays by Stage",
            orientation="v",
            color_discrete_sequence=[COLOR_WARNING],
            height=380,
        )
    else:
        st.info("No process delay records found.")
