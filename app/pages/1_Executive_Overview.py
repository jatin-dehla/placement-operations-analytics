"""
Page 1: Executive Overview
Mirrors Power BI Executive Summary page.
Provides macro-level recruitment KPIs, pipeline funnel, outcome distributions,
academic degree benchmarks, and corporate partner capacity.
"""

import streamlit as st
from components.filters import render_sidebar_filters
from components.charts import (
    render_donut_chart,
    render_bar_chart,
    render_funnel_chart,
    OUTCOME_COLORS,
    COLOR_PRIMARY,
    COLOR_SECONDARY,
)
from utils.queries import (
    get_executive_kpis,
    get_outcome_distribution,
    get_candidates_by_degree,
    get_top_companies_by_applications,
    get_candidate_progression_pipeline,
    get_interview_capacity_by_company,
)

st.set_page_config(
    page_title="Executive Overview | Placement Analytics",
    page_icon="📈",
    layout="wide",
)

# Title Hierarchy: Page Title 36-40px
st.markdown('<div class="page-title">📈 Executive Overview</div>', unsafe_allow_html=True)
st.markdown('<div class="page-subtitle">Macro-level campus recruitment performance, placement yields, cohort outcome distributions, and partner capacity.</div>', unsafe_allow_html=True)

# Sidebar Filters
filters = render_sidebar_filters()

# Retrieve KPI metrics
kpi_data = get_executive_kpis(filters)

# Section 1: KPI Summary (Directly mirroring Power BI Cards)
st.markdown('<div class="section-header">📊 Executive KPI Summary</div>', unsafe_allow_html=True)
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
        help="Total distinct student applicants registered in the recruitment drive.",
    )
with k3:
    st.metric(
        label="Hiring Companies",
        value=f"{kpi_data.get('total_companies', 0):,}",
        help="Total participating corporate partners offering campus positions.",
    )
with k4:
    st.metric(
        label="Total Interview Slots",
        value=f"{kpi_data.get('total_interview_slots', 0):,}",
        help="Total dedicated physical and virtual interview blocks allocated.",
    )

# Section 2: Recruitment Pipeline & Outcomes
st.markdown('<div class="section-header">🔄 Recruitment Pipeline & Cohort Outcomes</div>', unsafe_allow_html=True)
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
            title="Recruitment Outcomes",
            color_map=OUTCOME_COLORS,
            height=380,
        )
    else:
        st.info("No outcome data matches current filters.")

# Section 3: Candidate Academic Distribution & Cohort Demographics
st.markdown('<div class="section-header">🎓 Candidate Cohort Distribution</div>', unsafe_allow_html=True)
c3, c4 = st.columns([1, 1])

with c3:
    degree_df = get_candidates_by_degree(filters)
    if not degree_df.empty:
        render_donut_chart(
            degree_df,
            names_col="degree_program",
            values_col="candidate_count",
            title="Candidate Distribution by Degree",
            height=380,
        )
    else:
        st.info("No degree program distribution data available.")

with c4:
    tot_apps = kpi_data.get('total_applications', 0)
    tot_cands = kpi_data.get('total_candidates', 1) or 1
    avg_apps_cand = tot_apps / tot_cands
    tot_hires = kpi_data.get('total_hires', 0)
    yield_pct = kpi_data.get('placement_yield_pct', 0.0)

    st.markdown('<div style="font-size: 17px; font-weight: 600; color: #1e293b; margin-top: 0.25rem; margin-bottom: 0.75rem;"><b>Cohort Placement Yield Highlights</b></div>', unsafe_allow_html=True)
    m1, m2 = st.columns(2)
    with m1:
        st.metric("Confirmed Hires", f"{tot_hires:,}", help="Total candidate applications successfully converted to hires.")
        st.metric("Placement Yield", f"{yield_pct:.1f}%", help="Percentage of applications that resulted in confirmed hires.")
    with m2:
        st.metric("Avg Applications / Student", f"{avg_apps_cand:.1f}", help="Average employer applications per registered student.")
        active_in_proc = kpi_data.get('total_active', 0)
        st.metric("Active in Evaluation", f"{active_in_proc:,}", help="Candidates still undergoing stage assessments.")

# Section 4: Corporate Engagement & Capacity
st.markdown('<div class="section-header">🏢 Corporate Partner Demand & Interview Capacity</div>', unsafe_allow_html=True)
c5, c6 = st.columns(2)

with c5:
    top_co_df = get_top_companies_by_applications(filters, limit=10)
    if not top_co_df.empty:
        render_bar_chart(
            top_co_df,
            x_col="total_applications",
            y_col="company_name",
            title="Top Companies by Applications",
            orientation="h",
            color_discrete_sequence=[COLOR_PRIMARY],
            height=380,
        )
    else:
        st.info("No corporate application records found for current filters.")

with c6:
    capacity_co_df = get_interview_capacity_by_company(filters, limit=10)
    if not capacity_co_df.empty:
        render_bar_chart(
            capacity_co_df,
            x_col="total_slots",
            y_col="company_name",
            title="Interview Capacity by Company",
            orientation="h",
            color_discrete_sequence=[COLOR_SECONDARY],
            height=380,
        )
    else:
        st.info("No company interview capacity records found.")
