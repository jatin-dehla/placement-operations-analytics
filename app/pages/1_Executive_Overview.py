"""
Page 1: Executive Overview
Mirrors Power BI Executive Summary page.
Provides macro-level recruitment KPIs, outcome distributions, and top partner volumes.
"""

import streamlit as st
from components.filters import render_sidebar_filters
from components.charts import (
    render_donut_chart,
    render_bar_chart,
    render_funnel_chart,
    OUTCOME_COLORS,
    COLOR_PRIMARY,
)
from utils.queries import (
    get_executive_kpis,
    get_outcome_distribution,
    get_top_companies_by_applications,
    get_candidate_progression_pipeline,
)

st.set_page_config(
    page_title="Executive Overview | Placement Analytics",
    page_icon="📈",
    layout="wide",
)

# Title Hierarchy: Page Title 36-40px
st.markdown('<div class="page-title">📈 Executive Overview</div>', unsafe_allow_html=True)
st.markdown('<div class="page-subtitle">Macro-level campus recruitment performance, placement yields, and cohort outcome distributions.</div>', unsafe_allow_html=True)

# Sidebar Filters
filters = render_sidebar_filters()

# Retrieve KPI metrics
kpi_data = get_executive_kpis(filters)

# Section 1: KPI Summary
st.markdown('<div class="section-header">📊 KPI Summary</div>', unsafe_allow_html=True)
k1, k2, k3, k4 = st.columns(4)
with k1:
    st.metric(
        label="Total Applications",
        value=f"{kpi_data.get('total_applications', 0):,}",
        help="Total submitted applications across all candidate-company pairings.",
    )
with k2:
    st.metric(
        label="Unique Candidates",
        value=f"{kpi_data.get('total_candidates', 0):,}",
        help="Total distinct student applicants active in the recruitment drive.",
    )
with k3:
    st.metric(
        label="Hiring Companies",
        value=f"{kpi_data.get('total_companies', 0):,}",
        help="Total visiting corporate partners offering campus positions.",
    )
with k4:
    st.metric(
        label="Placement Yield Rate",
        value=f"{kpi_data.get('placement_yield_pct', 0.0):.1f}%",
        help="Percentage of submitted applications converted into confirmed student hires.",
    )

# Section 2: Recruitment Funnel
st.markdown('<div class="section-header">🔄 Recruitment Funnel</div>', unsafe_allow_html=True)
c1, c2 = st.columns(2)

with c1:
    funnel_df = get_candidate_progression_pipeline(filters)
    if not funnel_df.empty:
        render_funnel_chart(
            funnel_df,
            stage_col="stage_name",
            val_col="total_candidates_entered",
            title="Candidate Progression Pipeline",
            height=380,
        )
    else:
        st.info("No funnel progression data matches current filters.")

with c2:
    outcomes_df = get_outcome_distribution(filters)
    if not outcomes_df.empty:
        render_donut_chart(
            outcomes_df,
            names_col="outcome_status",
            values_col="application_count",
            title="Recruitment Outcomes Distribution",
            color_map=OUTCOME_COLORS,
            height=380,
        )
    else:
        st.info("No outcome data matches current filters.")

# Section 3: Candidate Insights
st.markdown('<div class="section-header">👥 Candidate Insights</div>', unsafe_allow_html=True)
c3, c4 = st.columns([3, 2])

with c3:
    top_co_df = get_top_companies_by_applications(filters, limit=10)
    if not top_co_df.empty:
        render_bar_chart(
            top_co_df,
            x_col="total_applications",
            y_col="company_name",
            title="Top 10 Employers by Candidate Application Volume",
            orientation="h",
            color_discrete_sequence=[COLOR_PRIMARY],
            height=380,
        )
    else:
        st.info("No corporate application records found for current filters.")

with c4:
    tot_apps = kpi_data.get('total_applications', 0)
    tot_cands = kpi_data.get('total_candidates', 1) or 1
    avg_apps_cand = tot_apps / tot_cands
    tot_hires = kpi_data.get('total_hires', 0)
    tot_active = kpi_data.get('total_active', 0)
    tot_slots = kpi_data.get('total_interview_slots', 0)

    st.markdown('<div style="font-size: 17px; font-weight: 600; color: #1e293b; margin-top: 0.25rem; margin-bottom: 0.75rem;"><b>Cohort Engagement Breakdown</b></div>', unsafe_allow_html=True)

    m1, m2 = st.columns(2)
    with m1:
        st.metric("Confirmed Hires", f"{tot_hires:,}", help="Total accepted employment offers.")
        st.metric("Active In-Process", f"{tot_active:,}", help="Candidates currently progressing through evaluation.")
    with m2:
        st.metric("Avg Apps / Candidate", f"{avg_apps_cand:.1f}", help="Average employer applications submitted per registered candidate.")
        st.metric("Interview Slots Allocated", f"{tot_slots:,}", help="Total campus interview time-blocks available.")

