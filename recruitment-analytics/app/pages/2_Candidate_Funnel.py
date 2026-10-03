"""
Page 2: Candidate Funnel Monitoring
Mirrors Power BI Candidate Funnel Monitoring page.
Analyzes stage conversion rates, drop-off leakage, SLA compliance, and score distributions.
"""

import streamlit as st
from components.filters import render_sidebar_filters
from components.charts import (
    render_funnel_chart,
    render_bar_chart,
    render_donut_chart,
    COLOR_PRIMARY,
    COLOR_DANGER,
    COLOR_SUCCESS,
)
from utils.queries import (
    get_candidate_progression_pipeline,
    get_stage_dropoffs,
    get_sla_breach_analysis,
    get_stage_scores_and_tat,
    get_candidates_by_degree,
)

st.set_page_config(
    page_title="Candidate Funnel | Placement Analytics",
    page_icon="🔍",
    layout="wide",
)

# Title Hierarchy: Page Title 36-40px
st.markdown('<div class="page-title">🔍 Candidate Funnel Monitoring</div>', unsafe_allow_html=True)
st.markdown('<div class="page-subtitle">Deep-dive into stage transition velocity, candidate drop-offs, evaluation scores, and SLA turnaround compliance.</div>', unsafe_allow_html=True)

# Sidebar Filters
filters = render_sidebar_filters()

# Retrieve Funnel Datasets
funnel_df = get_candidate_progression_pipeline(filters)
dropoffs_df = get_stage_dropoffs(filters)
sla_df = get_sla_breach_analysis(filters)
scores_tat_df = get_stage_scores_and_tat(filters)
degree_df = get_candidates_by_degree(filters)

# Section 1: Funnel Performance Highlights (KPI Cards replacing large matrix table)
st.markdown('<div class="section-header">⚡ Funnel Performance Summary</div>', unsafe_allow_html=True)

# Compute KPI metrics
if not dropoffs_df.empty and "stage_dropoff_rate_pct" in dropoffs_df.columns:
    max_drop_idx = dropoffs_df["stage_dropoff_rate_pct"].idxmax()
    max_drop_row = dropoffs_df.loc[max_drop_idx]
    highest_drop_stage = max_drop_row["stage_name"]
    highest_drop_val = f"{max_drop_row['stage_dropoff_rate_pct']:.1f}%"
else:
    highest_drop_stage = "N/A"
    highest_drop_val = "0.0%"

if not funnel_df.empty and "stage_pass_rate_pct" in funnel_df.columns:
    max_pass_idx = funnel_df["stage_pass_rate_pct"].idxmax()
    max_pass_row = funnel_df.loc[max_pass_idx]
    highest_pass_stage = max_pass_row["stage_name"]
    highest_pass_val = f"{max_pass_row['stage_pass_rate_pct']:.1f}%"
else:
    highest_pass_stage = "N/A"
    highest_pass_val = "0.0%"

if not scores_tat_df.empty and "evaluations_completed" in scores_tat_df.columns and scores_tat_df["evaluations_completed"].sum() > 0:
    mean_score = (scores_tat_df["avg_score"] * scores_tat_df["evaluations_completed"]).sum() / scores_tat_df["evaluations_completed"].sum()
    avg_score_val = f"{mean_score:.1f} / 100"
else:
    avg_score_val = "N/A"

k1, k2, k3 = st.columns(3)
with k1:
    st.metric(
        label="Highest Drop-off Stage",
        value=highest_drop_stage,
        delta=f"{highest_drop_val} Attrition",
        delta_color="inverse",
        help="Recruitment milestone with the highest candidate elimination rate.",
    )
with k2:
    st.metric(
        label="Highest Pass Rate Stage",
        value=highest_pass_stage,
        delta=f"{highest_pass_val} Pass Rate",
        delta_color="normal",
        help="Evaluation milestone with the greatest conversion to next round.",
    )
with k3:
    st.metric(
        label="Average Evaluation Score",
        value=avg_score_val,
        help="Weighted average candidate assessment rating across all completed evaluations.",
    )

# Section 2: Pipeline Progression & Stage Drop-off
st.markdown('<div class="section-header">🔄 Pipeline Progression & Drop-off Leakage</div>', unsafe_allow_html=True)
c1, c2 = st.columns(2)

with c1:
    if not funnel_df.empty:
        render_funnel_chart(
            funnel_df,
            stage_col="stage_name",
            val_col="total_candidates_entered",
            title="Stage Progression Volume",
            height=380,
        )
    else:
        st.info("No funnel data matches current filters.")

with c2:
    if not dropoffs_df.empty:
        render_bar_chart(
            dropoffs_df,
            x_col="stage_dropoff_rate_pct",
            y_col="stage_name",
            title="Stage Candidate Drop-off Rate (%)",
            orientation="h",
            color_discrete_sequence=[COLOR_DANGER],
            height=380,
        )
    else:
        st.info("No drop-off records available.")

# Section 3: Evaluation Standards & Turnaround Compliance
st.markdown('<div class="section-header">⏱️ Process Efficiency & SLA Compliance</div>', unsafe_allow_html=True)
c3, c4 = st.columns(2)

with c3:
    if not sla_df.empty:
        render_bar_chart(
            sla_df,
            x_col="stage_name",
            y_col="sla_breach_rate_pct",
            title="SLA Breach Frequency (%) by Evaluation Stage",
            orientation="v",
            color_discrete_sequence=[COLOR_DANGER],
            height=380,
        )
    else:
        st.info("No SLA breach records found.")

with c4:
    if not scores_tat_df.empty:
        render_bar_chart(
            scores_tat_df,
            x_col="stage_name",
            y_col="avg_score",
            title="Mean Candidate Evaluation Score (0-100 Scale)",
            orientation="v",
            color_discrete_sequence=[COLOR_PRIMARY],
            height=380,
        )
    else:
        st.info("No evaluation score data available.")

# Section 4: Academic Cohort Demographics (Moved from Executive Overview)
st.markdown('<div class="section-header">🎓 Candidate Cohort Demographics</div>', unsafe_allow_html=True)
c5, c6 = st.columns([1, 1])

with c5:
    if not degree_df.empty:
        render_donut_chart(
            degree_df,
            names_col="degree_program",
            values_col="candidate_count",
            title="Candidate Share by Academic Degree Program",
            height=380,
        )
    else:
        st.info("No degree program distribution data available.")

with c6:
    if not degree_df.empty:
        render_bar_chart(
            degree_df,
            x_col="avg_gpa",
            y_col="degree_program",
            title="Average GPA by Degree Program",
            orientation="h",
            color_discrete_sequence=[COLOR_PRIMARY],
            height=380,
        )
    else:
        st.info("No GPA benchmark data available.")

