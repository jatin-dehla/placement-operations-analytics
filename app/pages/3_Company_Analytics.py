"""
Page 3: Company Analytics
Mirrors Power BI Company Analytics page.
Evaluates corporate partner engagement, hiring volumes, offer releases,
offer acceptance rates (OAR), application popularity, and interview capacity.
"""

import streamlit as st
from components.filters import render_sidebar_filters
from components.charts import (
    render_bar_chart,
    render_donut_chart,
    COLOR_PRIMARY,
    COLOR_SECONDARY,
    COLOR_SUCCESS,
    COLOR_DANGER,
)
from utils.queries import (
    get_company_analytics_kpis,
    get_top_hiring_companies,
    get_top_companies_by_offers,
    get_top_companies_by_applications,
    get_interview_capacity_by_company,
    get_sector_analytics,
    get_slowest_companies,
)

st.set_page_config(
    page_title="Company Analytics | Placement Analytics",
    page_icon="🏢",
    layout="wide",
)

# Title Hierarchy: Page Title 36-40px
st.markdown('<div class="page-title">🏢 Company Analytics</div>', unsafe_allow_html=True)
st.markdown('<div class="page-subtitle">Corporate partner intelligence, employer selectivity, offer generation, acceptance yield, and interview slot bandwidth.</div>', unsafe_allow_html=True)

# Sidebar Filters
filters = render_sidebar_filters()

# Retrieve Company Analytics Data
co_kpis = get_company_analytics_kpis(filters)
top_hiring_df = get_top_hiring_companies(filters, limit=10)
top_offers_df = get_top_companies_by_offers(filters, limit=10)
most_applied_df = get_top_companies_by_applications(filters, limit=10)
capacity_co_df = get_interview_capacity_by_company(filters, limit=10)
sector_df = get_sector_analytics(filters)
slowest_co_df = get_slowest_companies(filters, limit=10)

# Section 1: Partner Engagement & Offer KPIs (Directly mirroring Power BI Cards)
st.markdown('<div class="section-header">📊 Corporate Engagement & Offer KPIs</div>', unsafe_allow_html=True)
k1, k2, k3, k4 = st.columns(4)
with k1:
    st.metric(
        label="Participating Companies",
        value=f"{co_kpis.get('participating_companies', 0):,}",
        help="Number of registered corporate partners evaluating student candidates.",
    )
with k2:
    st.metric(
        label="Offers Released",
        value=f"{co_kpis.get('offers_released', 0):,}",
        help="Total formal employment offers extended by corporate partners.",
    )
with k3:
    st.metric(
        label="Offer Acceptance Rate",
        value=f"{co_kpis.get('offer_acceptance_rate_pct', 0.0):.1f}%",
        help="Percentage of extended employment offers accepted by candidates (OAR).",
    )
with k4:
    st.metric(
        label="Students Hired",
        value=f"{co_kpis.get('students_hired', 0):,}",
        help="Total candidates successfully placed and confirmed.",
    )

# Section 2: Top Employers by Hires & Offers Extended
st.markdown('<div class="section-header">🤝 Top Employers: Hires & Offers</div>', unsafe_allow_html=True)
c1, c2 = st.columns(2)

with c1:
    if not top_hiring_df.empty:
        render_bar_chart(
            top_hiring_df,
            x_col="hires_count",
            y_col="company_name",
            title="Top Hiring Companies",
            orientation="h",
            color_discrete_sequence=[COLOR_SUCCESS],
            height=380,
        )
    else:
        st.info("No hiring data matches current filters.")

with c2:
    if not top_offers_df.empty:
        render_bar_chart(
            top_offers_df,
            x_col="total_offers",
            y_col="company_name",
            title="Top Companies by Offers",
            orientation="h",
            color_discrete_sequence=[COLOR_PRIMARY],
            height=380,
        )
    else:
        st.info("No offer records available.")

# Section 3: Applications Volume & Interview Capacity
st.markdown('<div class="section-header">📈 Candidate Demand & Interview Capacity</div>', unsafe_allow_html=True)
c3, c4 = st.columns(2)

with c3:
    if not most_applied_df.empty:
        render_bar_chart(
            most_applied_df,
            x_col="total_applications",
            y_col="company_name",
            title="Most Applied Companies",
            orientation="h",
            color_discrete_sequence=[COLOR_SECONDARY],
            height=380,
        )
    else:
        st.info("No application records available.")

with c4:
    if not capacity_co_df.empty:
        render_bar_chart(
            capacity_co_df,
            x_col="total_slots",
            y_col="company_name",
            title="Interview Capacity by Company",
            orientation="h",
            color_discrete_sequence=[COLOR_PRIMARY],
            height=380,
        )
    else:
        st.info("No interview capacity data found.")

# Section 4: Sector Dynamics & Evaluation Turnaround Time
with st.expander("🏭 Sector Dynamics & Partner SLA Latency", expanded=False):
    c5, c6 = st.columns(2)
    with c5:
        if not sector_df.empty:
            render_donut_chart(
                sector_df,
                names_col="industry_sector",
                values_col="applications_count",
                title="Student Interest Across Industry Sectors",
                height=350,
            )
        else:
            st.info("No industry sector data available.")
    with c6:
        if not slowest_co_df.empty:
            render_bar_chart(
                slowest_co_df,
                x_col="avg_turnaround_hours",
                y_col="company_name",
                title="Slowest Corporate Review Latency (Mean Hours)",
                orientation="h",
                color_discrete_sequence=[COLOR_DANGER],
                height=350,
            )
        else:
            st.info("No turnaround time records available.")
