"""
Recruitment Funnel & Capacity Optimization Platform (OCS Logistics Engine)
Streamlit Main Application Entry Point
"""

import streamlit as st
from components.filters import inject_dashboard_css
from utils.db import check_warehouse_health, get_warehouse_path
from utils.queries import get_executive_kpis

# Page configuration
st.set_page_config(
    page_title="OCS Logistics Engine | Placement Analytics",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Apply unified dashboard CSS
inject_dashboard_css()

# Custom card styling for warehouse status box
st.markdown("""
<style>
    .status-card {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 0.85rem 1.1rem;
        margin-bottom: 0.5rem;
        font-size: 13.5px;
        line-height: 1.6;
    }
</style>
""", unsafe_allow_html=True)

# Title Hierarchy: Page Title 36-40px
st.markdown('<div class="page-title">🎓 Recruitment Funnel & Capacity Optimization Platform</div>', unsafe_allow_html=True)
st.markdown('<div class="page-subtitle">Office of Career Services (OCS) Logistics Engine — Production Analytics Cockpit</div>', unsafe_allow_html=True)

# Quick Platform Overview
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<div class="section-header">🎯 Platform Overview</div>', unsafe_allow_html=True)
    st.markdown("""
    During peak university campus recruitment drives, the **OCS Logistics Engine** provides centralized, real-time decision support for Career Services teams, operations managers, and corporate hiring partners.
    
    By connecting directly to the **DuckDB in-process analytics warehouse**, this dashboard transforms raw application milestones and physical interview bookings into actionable operational intelligence.
    
    #### 🧭 Operational Modules:
    - **Page 1: Executive Overview** — Macro-level applicant volume, placement yield, outcome distributions, and academic branch benchmarks.
    - **Page 2: Candidate Funnel Monitoring** — Micro-level funnel progression, attrition points, stage conversion pass rates, and evaluation scoring.
    - **Page 3: Company Analytics** — Corporate partner engagement, selectivity, offer acceptance rates (OAR), and review turnaround times.
    - **Page 4: Operations & Capacity Analytics** — Logistics control tower monitoring interview room occupancy, panel workload caps, and rule-based capacity reallocations.
    """)

with col2:
    st.markdown('<div class="section-header">⚡ Warehouse Health Status</div>', unsafe_allow_html=True)
    try:
        health = check_warehouse_health()
        db_path = get_warehouse_path()
        st.success(f"**DuckDB Connected:** `placement_analytics.duckdb`")
        
        st.markdown(f"""
        <div class="status-card">
            <b>Production Relational Scale:</b><br>
            • <b>Candidates:</b> {health.get('candidates', 0):,} records<br>
            • <b>Companies:</b> {health.get('companies', 0):,} partners<br>
            • <b>Applications:</b> {health.get('applications', 0):,} submissions<br>
            • <b>Stage Transitions:</b> {health.get('recruitment_stage_records', 0):,} events<br>
            • <b>Interview Slots:</b> {health.get('interview_slots', 0):,} time-blocks<br>
            • <b>Interview Panels:</b> {health.get('panels', 0):,} evaluators<br>
            • <b>Venue Rooms:</b> {health.get('rooms', 0):,} venues<br>
            <hr style="margin: 0.5rem 0;">
            <b>Total Warehouse Records:</b> <b>{health.get('total_warehouse_records', 0):,}</b> (100% Star/Snowflake schema)
        </div>
        """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Warehouse Connection Failed: {e}")

# Quick KPI Highlights (Unfiltered)
st.markdown('<div class="section-header">📊 Topline Operational Snapshot</div>', unsafe_allow_html=True)
kpis = get_executive_kpis()

kpi_c1, kpi_c2, kpi_c3, kpi_c4 = st.columns(4)
with kpi_c1:
    st.metric("Total Applications", f"{kpis['total_applications']:,}", help="Total candidate applications submitted across all hiring drives.")
with kpi_c2:
    st.metric("Unique Candidates", f"{kpis['total_candidates']:,}", help="Total registered students participating in recruitment.")
with kpi_c3:
    st.metric("Hiring Companies", f"{kpis['total_companies']:,}", help="Registered corporate partners conducting campus evaluations.")
with kpi_c4:
    st.metric("Total Interview Slots", f"{kpis['total_interview_slots']:,}", help="Dedicated physical and virtual interview schedule blocks.")

st.markdown("---")
st.info("👈 **Select a page from the sidebar to explore detailed interactive analytics.**")
