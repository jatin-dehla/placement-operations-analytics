"""
Page 3: Company Analytics
Mirrors Power BI Company Analytics page.
Evaluates corporate partner engagement, hiring volumes, offer acceptance rates (OAR), and review speed.
"""

import streamlit as st
from components.filters import render_sidebar_filters
from components.charts import (
    render_bar_chart,
    render_grouped_bar_chart,
    render_donut_chart,
    COLOR_PRIMARY,
    COLOR_SUCCESS,
    COLOR_DANGER,
)
from utils.queries import (
    get_company_kpis,
    get_top_hiring_companies,
    get_offers_by_company,
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
st.markdown('<div class="page-subtitle">Corporate partner intelligence, employer selectivity, offer conversion benchmarks, and evaluation turnaround speeds.</div>', unsafe_allow_html=True)

# Sidebar Filters
filters = render_sidebar_filters()

# Retrieve Company Analytics Data
co_kpis = get_company_kpis(filters)
top_hiring_df = get_top_hiring_companies(filters, limit=10)
offers_df = get_offers_by_company(filters, limit=10)
sector_df = get_sector_analytics(filters)
slowest_co_df = get_slowest_companies(filters, limit=10)

# Section 1: Partner Engagement KPIs
st.markdown('<div class="section-header">📊 Corporate Engagement Summary</div>', unsafe_allow_html=True)
k1, k2, k3, k4 = st.columns(4)
with k1:
    st.metric(
        label="Active Corporate Partners",
        value=f"{co_kpis.get('active_partners', 0):,}",
        help="Number of hiring companies with candidate applications.",
    )
with k2:
    st.metric(
        label="Total Confirmed Hires",
        value=f"{co_kpis.get('total_hires', 0):,}",
        help="Total candidates successfully placed with corporate partners.",
    )
with k3:
    st.metric(
        label="Avg Applications per Partner",
        value=f"{co_kpis.get('avg_apps_per_company', 0):.1f}",
        help="Mean candidate applications received per visiting corporate company.",
    )
with k4:
    st.metric(
        label="Overall Hiring Conversion Yield",
        value=f"{co_kpis.get('hiring_yield_pct', 0.0):.2f}%",
        help="Percentage of submitted applications resulting in confirmed hires.",
    )

# Section 2: Partner Hiring Volumes & Offer Conversions
st.markdown('<div class="section-header">🤝 Placement Yield & Offer Conversions</div>', unsafe_allow_html=True)
c1, c2 = st.columns(2)

with c1:
    if not top_hiring_df.empty:
        render_bar_chart(
            top_hiring_df,
            x_col="hires_count",
            y_col="company_name",
            title="Top Employers by Confirmed Placement Hires",
            orientation="h",
            color_discrete_sequence=[COLOR_SUCCESS],
            height=380,
        )
    else:
        st.info("No hiring data matches current filters.")

with c2:
    if not offers_df.empty:
        render_grouped_bar_chart(
            offers_df,
            x_col="company_name",
            y_cols=["total_offers_extended", "offers_accepted"],
            title="Offers Extended vs. Accepted by Partner",
            color_discrete_sequence=[COLOR_PRIMARY, COLOR_SUCCESS],
            height=380,
        )
    else:
        st.info("No offer records available.")

# Section 3: Industry Sectors & Evaluation Turnaround Time
st.markdown('<div class="section-header">🏭 Sector Dynamics & Partner SLA Latency</div>', unsafe_allow_html=True)
c3, c4 = st.columns(2)

with c3:
    if not sector_df.empty:
        render_donut_chart(
            sector_df,
            names_col="industry_sector",
            values_col="applications_count",
            title="Student Interest Across Industry Sectors",
            height=380,
        )
    else:
        st.info("No industry sector data available.")

with c4:
    if not slowest_co_df.empty:
        render_bar_chart(
            slowest_co_df,
            x_col="avg_turnaround_hours",
            y_col="company_name",
            title="Slowest Corporate Review Latency (Mean Hours)",
            orientation="h",
            color_discrete_sequence=[COLOR_DANGER],
            height=380,
        )
    else:
        st.info("No turnaround time records available.")

