"""
Page 4: Operations & Capacity Analytics
Mirrors Power BI Placement Operations & Resource Planning page.
Acts as the physical logistics control tower: panel workload quotas, venue occupancy,
process delay bottlenecks, severity hours, and rule-based capacity recommendations.
"""

import streamlit as st
from components.filters import render_sidebar_filters
from components.charts import (
    render_bar_chart,
    render_stacked_bar_chart,
    COLOR_PRIMARY,
    COLOR_SECONDARY,
    COLOR_SUCCESS,
    COLOR_DANGER,
    COLOR_WARNING,
    COLOR_SLATE,
)
from utils.queries import (
    get_operations_resource_kpis,
    get_interview_load_by_room,
    get_interview_load_by_panel,
    get_process_delays_by_stage,
    get_daily_slot_allocation,
    get_capacity_recommendations,
)

st.set_page_config(
    page_title="Operations & Capacity | Placement Analytics",
    page_icon="⚙️",
    layout="wide",
)

# Title Hierarchy: Page Title 36-40px
st.markdown('<div class="page-title">⚙️ Placement Operations & Resource Planning</div>', unsafe_allow_html=True)
st.markdown('<div class="page-subtitle">Physical and virtual scheduling logistics, panel workload quotas, venue room occupancy, process delays, and capacity rebalancing.</div>', unsafe_allow_html=True)

# Sidebar Filters (Optional context)
filters = render_sidebar_filters()

# Retrieve Capacity & Operations Data
ops_kpis = get_operations_resource_kpis()
room_load_df = get_interview_load_by_room(limit=12)
panel_load_df = get_interview_load_by_panel(limit=12)
delays_df = get_process_delays_by_stage(filters)
slots_day_df = get_daily_slot_allocation()
recs_df = get_capacity_recommendations()

# Section 1: Operations Capacity KPIs (Directly mirroring Power BI Cards)
st.markdown('<div class="section-header">📊 Logistics & Infrastructure Capacity</div>', unsafe_allow_html=True)
k1, k2, k3, k4 = st.columns(4)
with k1:
    st.metric(
        label="Total Scheduled Interviews",
        value=f"{ops_kpis.get('total_scheduled_interviews', 0):,}",
        help="Total dedicated physical and virtual interview schedule blocks.",
    )
with k2:
    st.metric(
        label="Total Panels",
        value=f"{ops_kpis.get('total_panels', 0):,}",
        help="Evaluator panels active across technical and domain departments.",
    )
with k3:
    st.metric(
        label="Total Interview Rooms",
        value=f"{ops_kpis.get('total_rooms', 0):,}",
        help="Physical interview venue rooms and virtual video desks.",
    )
with k4:
    st.metric(
        label="Average Slots per Panel",
        value=f"{ops_kpis.get('avg_slots_per_panel', 0.0):.1f}",
        help="Mean interview slot workload distributed per interviewer panel.",
    )

# Section 2: Resource Utilization (Room & Panel Workload)
st.markdown('<div class="section-header">🏢 Resource Allocation: Rooms & Interview Panels</div>', unsafe_allow_html=True)
c1, c2 = st.columns(2)

with c1:
    if not room_load_df.empty:
        render_bar_chart(
            room_load_df,
            x_col="slot_count",
            y_col="room_name",
            title="Interview Load by Room",
            orientation="h",
            color_discrete_sequence=[COLOR_PRIMARY],
            height=380,
        )
    else:
        st.info("No room workload records found.")

with c2:
    if not panel_load_df.empty:
        render_bar_chart(
            panel_load_df,
            x_col="slot_count",
            y_col="panel_code",
            title="Interview Load by Panel",
            orientation="h",
            color_discrete_sequence=[COLOR_SECONDARY],
            height=380,
        )
    else:
        st.info("No panel workload records found.")

# Section 3: Process Delays & Delay Severity
st.markdown('<div class="section-header">⏱️ Operational Bottlenecks: Delays & Severity Hours</div>', unsafe_allow_html=True)
c3, c4 = st.columns(2)

with c3:
    if not delays_df.empty:
        render_bar_chart(
            delays_df,
            x_col="stage_name",
            y_col="delayed_records",
            title="Delayed Processes by Stage",
            orientation="v",
            color_discrete_sequence=[COLOR_DANGER],
            height=380,
        )
    else:
        st.info("No delayed process records available.")

with c4:
    if not delays_df.empty:
        render_bar_chart(
            delays_df,
            x_col="stage_name",
            y_col="avg_delay_hours",
            title="Average Delay Severity by Stage (Hours)",
            orientation="v",
            color_discrete_sequence=[COLOR_WARNING],
            height=380,
        )
    else:
        st.info("No delay severity data found.")

# Section 4: Daily Slot Allocation & Automated Capacity Recommendations
st.markdown('<div class="section-header">📅 Schedule Distribution & Rule-Based Bottleneck Rebalancing</div>', unsafe_allow_html=True)
c5, c6 = st.columns([1, 1])

with c5:
    if not slots_day_df.empty:
        render_stacked_bar_chart(
            slots_day_df,
            x_col="hiring_day",
            y_cols=["available_slots", "booked_slots", "completed_slots", "cancelled_slots"],
            title="Interview Slots by Booking State per Hiring Day",
            color_discrete_sequence=[COLOR_SLATE, COLOR_PRIMARY, COLOR_SUCCESS, COLOR_DANGER],
            height=380,
        )
    else:
        st.info("No daily slot distribution data available.")

with c6:
    st.markdown('<div style="font-size: 17px; font-weight: 600; color: #1e293b; margin-top: 0.25rem; margin-bottom: 0.75rem;"><b>Automated Capacity Rebalancing Alerts</b></div>', unsafe_allow_html=True)
    if not recs_df.empty:
        st.dataframe(
            recs_df[["severity", "issue_type", "resource_name", "load_pct", "recommended_action"]],
            column_config={
                "severity": st.column_config.TextColumn("Severity"),
                "issue_type": st.column_config.TextColumn("Issue Type"),
                "resource_name": st.column_config.TextColumn("Resource"),
                "load_pct": st.column_config.NumberColumn("Load %", format="%.1f%%"),
                "recommended_action": st.column_config.TextColumn("Prescribed Remediation"),
            },
            hide_index=True,
            use_container_width=True,
            height=340,
        )
    else:
        st.success("All resources operating within safe operational capacity thresholds.")
