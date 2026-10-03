"""
Sidebar Filter Component Module

Provides unified, interactive sidebar filter controls (Company, Sector, Stage, Date Range)
that reactively update warehouse SQL queries across all dashboard pages.
"""

from typing import Dict, Any
from datetime import datetime, date
import streamlit as st
from utils.queries import get_filter_options




def inject_dashboard_css():
    """Inject unified executive dashboard CSS for compact layout and title hierarchy."""
    st.markdown("""
    <style>
        /* Compact executive layout & screen utilization */
        .block-container {
            padding-top: 1.25rem !important;
            padding-bottom: 2rem !important;
            padding-left: 2.25rem !important;
            padding-right: 2.25rem !important;
            max-width: 100% !important;
        }

        /* Title Hierarchy: Page Title 36-40px */
        .page-title {
            font-size: 38px !important;
            font-weight: 700 !important;
            color: #0f172a !important;
            letter-spacing: -0.025em !important;
            line-height: 1.2 !important;
            margin: 0 !important;
        }
        .page-subtitle {
            font-size: 15px !important;
            color: #64748b !important;
            margin-top: 0.25rem !important;
            margin-bottom: 1.25rem !important;
            line-height: 1.4 !important;
        }

        /* Title Hierarchy: Section Headers 22-26px */
        .section-header {
            font-size: 24px !important;
            font-weight: 600 !important;
            color: #1e293b !important;
            letter-spacing: -0.015em !important;
            margin-top: 1.25rem !important;
            margin-bottom: 0.75rem !important;
            padding-bottom: 0.35rem !important;
            border-bottom: 1.5px solid #e2e8f0 !important;
            display: flex !important;
            align-items: center !important;
            gap: 0.5rem !important;
        }

        /* Professional Metric Cards */
        div[data-testid="stMetric"] {
            background-color: #f8fafc !important;
            border: 1px solid #e2e8f0 !important;
            border-radius: 8px !important;
            padding: 0.75rem 1rem !important;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.02) !important;
        }
        div[data-testid="stMetricLabel"] p {
            font-size: 13px !important;
            font-weight: 500 !important;
            color: #64748b !important;
            margin: 0 0 0.15rem 0 !important;
        }
        div[data-testid="stMetricValue"] div {
            font-size: 26px !important;
            font-weight: 700 !important;
            color: #0f172a !important;
            letter-spacing: -0.02em !important;
        }

        /* Tighten default Streamlit margins */
        .stPlotlyChart {
            margin-bottom: 0.25rem !important;
        }
        hr {
            margin: 1rem 0 !important;
            border-color: #e2e8f0 !important;
        }
        .element-container {
            margin-bottom: 0.25rem !important;
        }
    </style>
    """, unsafe_allow_html=True)


def render_sidebar_filters() -> Dict[str, Any]:
    """
    Render standard filter widgets inside st.sidebar and return active filter state.
    """
    inject_dashboard_css()
    st.sidebar.markdown("### 🔍 Filters")

    options = get_filter_options()
    companies_df = options["companies"]
    sectors_list = options["sectors"]
    stages_list = options["stages"]
    min_date = options["min_date"]
    max_date = options["max_date"]

    # 1. Industry Sector Filter
    selected_sectors = st.sidebar.multiselect(
        "Industry Sector",
        options=sectors_list,
        default=[],
        placeholder="All Sectors",
        help="Filter candidates and applications by corporate industry sector."
    )

    # 2. Company Filter (Filtered by sector if sector is selected)
    if selected_sectors and not companies_df.empty:
        filtered_companies = companies_df[companies_df["industry_sector"].isin(selected_sectors)]
    else:
        filtered_companies = companies_df

    company_mapping = dict(zip(filtered_companies["company_name"], filtered_companies["company_id"])) if not filtered_companies.empty else {}
    selected_company_names = st.sidebar.multiselect(
        "Hiring Company",
        options=list(company_mapping.keys()),
        default=[],
        placeholder="All Companies",
        help="Select specific corporate partners to evaluate."
    )
    selected_company_ids = [company_mapping[name] for name in selected_company_names]

    # 3. Funnel Stage Filter
    selected_stages = st.sidebar.multiselect(
        "Recruitment Stage",
        options=stages_list,
        default=[],
        placeholder="All Stages",
        help="Focus on specific evaluation stages in the hiring pipeline."
    )

    # 4. Date Range Filter
    selected_date_range = None
    if min_date and max_date:
        try:
            if isinstance(min_date, str):
                min_d = datetime.strptime(min_date, "%Y-%m-%d").date()
            else:
                min_d = min_date
            if isinstance(max_date, str):
                max_d = datetime.strptime(max_date, "%Y-%m-%d").date()
            else:
                max_d = max_date

            date_input = st.sidebar.date_input(
                "Application Date Range",
                value=(min_d, max_d),
                min_value=min_d,
                max_value=max_d,
                help="Filter applications submitted within this date window."
            )
            if isinstance(date_input, (tuple, list)) and len(date_input) == 2:
                selected_date_range = (date_input[0].strftime("%Y-%m-%d"), date_input[1].strftime("%Y-%m-%d"))
        except Exception:
            pass

    st.sidebar.markdown("---")
    active_filters_count = sum([
        bool(selected_sectors),
        bool(selected_company_ids),
        bool(selected_stages),
        bool(selected_date_range and selected_date_range != (str(min_date), str(max_date))),
    ])

    if active_filters_count > 0:
        st.sidebar.caption(f"⚡ {active_filters_count} active filter(s) applied")

    if st.sidebar.button("🔄 Refresh Data / Clear Cache", use_container_width=True, help="Force reload data directly from DuckDB analytics warehouse."):
        from utils.db import clear_warehouse_cache
        clear_warehouse_cache()
        st.rerun()

    return {
        "company_ids": selected_company_ids if selected_company_ids else None,
        "sectors": selected_sectors if selected_sectors else None,
        "stages": selected_stages if selected_stages else None,
        "date_range": selected_date_range,
    }
