"""
Page 4: Operations & Capacity Analytics
Mirrors Power BI Placement Operations & Resource Planning page.
Acts as the physical logistics control tower: panel utilization, room occupancy,
peak scheduling congestion windows, and rule-based capacity recommendations.
"""

import streamlit as st
from components.filters import render_sidebar_filters
from components.charts import (
    render_bar_chart,
    render_stacked_bar_chart,
    render_heatmap,
    COLOR_PRIMARY,
    COLOR_SECONDARY,
    COLOR_SUCCESS,
    COLOR_DANGER,
    COLOR_SLATE,
)
from utils.queries import (
    get_operations_kpis,
    get_panel_utilization,
    get_room_utilization,
    get_daily_slot_allocation,
    get_peak_scheduling_windows,
    get_capacity_recommendations,
)

st.set_page_config(
    page_title="Operations & Capacity | Placement Analytics",
    page_icon="⚙️",
    layout="wide",
)

# Title Hierarchy: Page Title 36-40px
st.markdown('<div class="page-title">⚙️ Placement Operations & Capacity Analytics</div>', unsafe_allow_html=True)
st.markdown('<div class="page-subtitle">Physical and virtual scheduling logistics, panel workload quotas, venue occupancy, and bottleneck rebalancing.</div>', unsafe_allow_html=True)

# Sidebar Filters (Optional context)
filters = render_sidebar_filters()

# Retrieve Capacity Data
ops_kpis = get_operations_kpis()
panel_df = get_panel_utilization()
room_df = get_room_utilization()
slots_day_df = get_daily_slot_allocation()
peak_df = get_peak_scheduling_windows()
recs_df = get_capacity_recommendations()

# Section 1: Operations Capacity KPIs
st.markdown('<div class="section-header">📊 Logistics & Infrastructure Capacity</div>', unsafe_allow_html=True)
k1, k2, k3, k4 = st.columns(4)
with k1:
    st.metric(
        label="Total Venue Rooms",
        value=f"{ops_kpis.get('total_rooms', 0):,}",
        help="Physical and virtual conference interview rooms.",
    )
with k2:
    st.metric(
        label="Total Interviewer Panels",
        value=f"{ops_kpis.get('total_panels', 0):,}",
        help="Evaluator panels active across technical departments.",
    )
with k3:
    st.metric(
        label="Overall Slot Occupancy Rate",
        value=f"{ops_kpis.get('overall_slot_occupancy_pct', 0.0):.1f}%",
        help="Percentage of total scheduled slots booked or completed.",
    )
with k4:
    st.metric(
        label="SLA Breached Evaluations",
        value=f"{ops_kpis.get('total_sla_breaches', 0):,}",
        help="Stage evaluation reviews exceeding agreed turnaround limits.",
    )

# Section 2: Resource Utilization (Panel & Room Occupancy)
st.markdown('<div class="section-header">🏢 Resource Allocation & Workload Saturation</div>', unsafe_allow_html=True)
c1, c2 = st.columns(2)

with c1:
    if not panel_df.empty:
        render_bar_chart(
            panel_df.head(12),
            x_col="panel_utilization_pct",
            y_col="panel_code",
            title="Panel Workload vs Max Daily Capacity Cap (Top 12)",
            orientation="h",
            color_discrete_sequence=[COLOR_PRIMARY],
            height=380,
        )
    else:
        st.info("No panel workload data available.")

with c2:
    if not room_df.empty:
        render_bar_chart(
            room_df.head(12),
            x_col="room_occupancy_rate_pct",
            y_col="room_name",
            title="Venue Room Hours Occupied vs Scheduled Capacity",
            orientation="h",
            color_discrete_sequence=[COLOR_SECONDARY],
            height=380,
        )
    else:
        st.info("No room occupancy records found.")

# Section 3: Daily Slot Allocation & Peak Scheduling Congestion
st.markdown('<div class="section-header">📅 Schedule Distribution & Congestion Heatmap</div>', unsafe_allow_html=True)
c3, c4 = st.columns(2)

with c3:
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

with c4:
    if not peak_df.empty:
        render_heatmap(
            peak_df,
            x_col="slot_hour_window",
            y_col="hiring_day",
            z_col="active_booked_slots",
            title="Active Interview Demand Heatmap Across Windows",
            height=380,
        )
    else:
        st.info("No hourly peak scheduling records available.")

# Section 4: Capacity Rebalancing Alerts
st.markdown('<div class="section-header">🚨 Capacity Allocation Recommendations & Bottlenecks</div>', unsafe_allow_html=True)

if not recs_df.empty:
    display_recs = recs_df.copy()
    display_recs = display_recs.rename(columns={
        "issue_type": "Alert Category",
        "severity": "Severity",
        "resource_name": "Resource / Entity",
        "current_load": "Booked Slots",
        "max_capacity": "Max Capacity",
        "load_pct": "Load (%)",
        "recommended_action": "Operational Intervention",
    })

    st.dataframe(
        display_recs,
        width="stretch",
        hide_index=True,
    )
else:
    st.success("All panels and venue rooms are operating within optimal capacity bands.")

