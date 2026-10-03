"""
Analytical SQL Queries Module

Exposes parameterized, cached query functions for the 4 dashboard pages.
Faithfully executes the analytical business logic established in:
- sql/funnel/funnel_metrics.sql
- sql/process_efficiency/process_metrics.sql
- sql/capacity/capacity_metrics.sql
- sql/recommendations/01_capacity_allocation_recommendations.sql
"""

from typing import Dict, Any, List, Optional
import pandas as pd
from utils.db import run_query




def _build_where_clause(
    company_ids: Optional[List[int]] = None,
    sectors: Optional[List[str]] = None,
    stages: Optional[List[str]] = None,
    date_range: Optional[tuple] = None,
    table_alias: str = "a",
) -> str:
    """Helper to dynamically generate SQL WHERE conditions based on sidebar filters."""
    conditions = []

    if company_ids:
        ids_str = ", ".join(f"'{cid}'" if isinstance(cid, str) else str(cid) for cid in company_ids)
        conditions.append(f"{table_alias}.company_id IN ({ids_str})")

    if sectors:
        sec_str = ", ".join(f"'{s.replace("'", "''")}'" for s in sectors)
        conditions.append(f"c.industry_sector IN ({sec_str})")

    if stages:
        stg_str = ", ".join(f"'{s.replace("'", "''")}'" for s in stages)
        conditions.append(f"sr.stage_name IN ({stg_str})")

    if date_range and len(date_range) == 2 and date_range[0] and date_range[1]:
        conditions.append(f"{table_alias}.application_date BETWEEN '{date_range[0]}' AND '{date_range[1]}'")

    if not conditions:
        return ""
    return "WHERE " + " AND ".join(conditions)


# ==============================================================================
# Filter Options
# ==============================================================================

def get_filter_options() -> Dict[str, Any]:
    """Retrieve distinct filter options from warehouse dimensions."""
    companies_df = run_query("SELECT company_id, company_name, industry_sector, priority_tier FROM companies ORDER BY company_name")
    stages_df = run_query("SELECT DISTINCT sequence_order, stage_name FROM recruitment_stage_records ORDER BY sequence_order")
    dates_df = run_query("SELECT MIN(application_date) AS min_date, MAX(application_date) AS max_date FROM applications")

    return {
        "companies": companies_df,
        "sectors": sorted(companies_df["industry_sector"].dropna().unique().tolist()) if not companies_df.empty else [],
        "stages": stages_df["stage_name"].tolist() if not stages_df.empty else [],
        "min_date": dates_df["min_date"].iloc[0] if not dates_df.empty else None,
        "max_date": dates_df["max_date"].iloc[0] if not dates_df.empty else None,
    }


# ==============================================================================
# Page 1: Executive Overview Queries
# ==============================================================================

def get_executive_kpis(filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Retrieve top-level operational KPIs for the Executive Overview."""
    filters = filters or {}
    company_ids = filters.get("company_ids")
    sectors = filters.get("sectors")
    date_range = filters.get("date_range")

    where_clause = _build_where_clause(company_ids=company_ids, sectors=sectors, date_range=date_range, table_alias="a")

    sql = f"""
    SELECT 
        COUNT(DISTINCT a.application_id) AS total_applications,
        COUNT(DISTINCT a.candidate_id) AS total_candidates,
        COUNT(DISTINCT a.company_id) AS total_companies,
        COUNT(DISTINCT CASE WHEN a.overall_status = 'Hired' THEN a.application_id END) AS total_hires,
        COUNT(DISTINCT CASE WHEN a.overall_status = 'Active' THEN a.application_id END) AS total_active,
        ROUND(
            (COUNT(DISTINCT CASE WHEN a.overall_status = 'Hired' THEN a.application_id END)::NUMERIC / 
            NULLIF(COUNT(DISTINCT a.application_id), 0)) * 100, 2
        ) AS placement_yield_pct
    FROM applications a
    JOIN companies c ON a.company_id = c.company_id
    {where_clause};
    """
    df = run_query(sql)

    # Slots count from interview_slots
    slots_sql = "SELECT COUNT(*) AS total_slots FROM interview_slots;"
    slots_df = run_query(slots_sql)
    total_slots = slots_df["total_slots"].iloc[0] if not slots_df.empty else 0

    if not df.empty:
        row = df.iloc[0].to_dict()
        row["total_interview_slots"] = total_slots
        return row
    return {
        "total_applications": 0, "total_candidates": 0, "total_companies": 0,
        "total_hires": 0, "total_active": 0, "placement_yield_pct": 0.0,
        "total_interview_slots": total_slots
    }


def get_outcome_distribution(filters: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    """Distribution of application outcomes (Hired, Rejected, Active, Withdrawn)."""
    filters = filters or {}
    where_clause = _build_where_clause(
        company_ids=filters.get("company_ids"),
        sectors=filters.get("sectors"),
        date_range=filters.get("date_range"),
        table_alias="a"
    )

    sql = f"""
    SELECT 
        a.overall_status AS outcome_status,
        COUNT(a.application_id) AS application_count,
        ROUND(
            COUNT(a.application_id)::NUMERIC / NULLIF(SUM(COUNT(a.application_id)) OVER(), 0) * 100, 2
        ) AS share_pct
    FROM applications a
    JOIN companies c ON a.company_id = c.company_id
    {where_clause}
    GROUP BY a.overall_status
    ORDER BY application_count DESC;
    """
    return run_query(sql)


def get_candidates_by_degree(filters: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    """Distribution of candidates by academic degree program and major."""
    sql = """
    SELECT 
        degree_program,
        COUNT(candidate_id) AS candidate_count,
        ROUND(AVG(gpa)::NUMERIC, 2) AS avg_gpa
    FROM candidates
    GROUP BY degree_program
    ORDER BY candidate_count DESC;
    """
    return run_query(sql)


def get_top_companies_by_applications(filters: Optional[Dict[str, Any]] = None, limit: int = 10) -> pd.DataFrame:
    """Top companies ranked by total applicant volume (Reuses funnel_metrics.sql Query 1)."""
    filters = filters or {}
    where_clause = _build_where_clause(
        company_ids=filters.get("company_ids"),
        sectors=filters.get("sectors"),
        date_range=filters.get("date_range"),
        table_alias="a"
    )

    sql = f"""
    WITH company_app_counts AS (
        SELECT 
            c.company_id,
            c.company_name,
            c.industry_sector,
            c.priority_tier,
            COUNT(a.application_id) AS total_applications,
            COUNT(CASE WHEN a.overall_status = 'Active' THEN 1 END) AS active_applications,
            COUNT(CASE WHEN a.overall_status = 'Hired' THEN 1 END) AS hired_applications,
            COUNT(CASE WHEN a.overall_status = 'Rejected' THEN 1 END) AS rejected_applications
        FROM companies c
        JOIN applications a ON c.company_id = a.company_id
        {where_clause}
        GROUP BY c.company_id, c.company_name, c.industry_sector, c.priority_tier
    )
    SELECT 
        company_name,
        industry_sector,
        priority_tier,
        total_applications,
        active_applications,
        hired_applications,
        rejected_applications,
        ROUND(
            (hired_applications::NUMERIC / NULLIF(total_applications, 0)) * 100, 2
        ) AS hiring_yield_pct
    FROM company_app_counts
    ORDER BY total_applications DESC
    LIMIT {limit};
    """
    return run_query(sql)


# ==============================================================================
# Page 2: Candidate Funnel Monitoring Queries
# ==============================================================================

def get_candidate_progression_pipeline(filters: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    """Funnel progression across standardized recruitment stages (funnel_metrics.sql Query 2)."""
    filters = filters or {}
    where_clause = _build_where_clause(
        company_ids=filters.get("company_ids"),
        sectors=filters.get("sectors"),
        stages=filters.get("stages"),
        date_range=filters.get("date_range"),
        table_alias="a"
    )

    sql = f"""
    WITH stage_aggregates AS (
        SELECT 
            sr.sequence_order,
            sr.stage_name,
            COUNT(sr.stage_record_id) AS total_candidates_entered,
            COUNT(CASE WHEN sr.stage_status = 'Passed' THEN 1 END) AS candidates_passed,
            COUNT(CASE WHEN sr.stage_status = 'Failed' THEN 1 END) AS candidates_failed,
            COUNT(CASE WHEN sr.stage_status = 'Pending' THEN 1 END) AS candidates_pending,
            ROUND(AVG(sr.evaluation_score)::NUMERIC, 2) AS avg_stage_score
        FROM recruitment_stage_records sr
        JOIN applications a ON sr.application_id = a.application_id
        JOIN companies c ON a.company_id = c.company_id
        {where_clause}
        GROUP BY sr.sequence_order, sr.stage_name
    )
    SELECT 
        sequence_order,
        stage_name,
        total_candidates_entered,
        candidates_passed,
        candidates_failed,
        candidates_pending,
        ROUND(
            (candidates_passed::NUMERIC / NULLIF(total_candidates_entered, 0)) * 100, 2
        ) AS stage_pass_rate_pct,
        avg_stage_score
    FROM stage_aggregates
    ORDER BY sequence_order ASC;
    """
    return run_query(sql)


def get_stage_dropoffs(filters: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    """Stage drop-off rates and candidate attrition (funnel_metrics.sql Query 3)."""
    filters = filters or {}
    where_clause = _build_where_clause(
        company_ids=filters.get("company_ids"),
        sectors=filters.get("sectors"),
        stages=filters.get("stages"),
        date_range=filters.get("date_range"),
        table_alias="a"
    )

    sql = f"""
    WITH dropoff_calc AS (
        SELECT 
            sr.sequence_order,
            sr.stage_name,
            COUNT(sr.stage_record_id) AS stage_entrants,
            COUNT(CASE WHEN sr.stage_status = 'Failed' THEN 1 END) AS stage_failures
        FROM recruitment_stage_records sr
        JOIN applications a ON sr.application_id = a.application_id
        JOIN companies c ON a.company_id = c.company_id
        {where_clause}
        GROUP BY sr.sequence_order, sr.stage_name
    )
    SELECT 
        sequence_order,
        stage_name,
        stage_entrants,
        stage_failures,
        ROUND(
            (stage_failures::NUMERIC / NULLIF(stage_entrants, 0)) * 100, 2
        ) AS stage_dropoff_rate_pct,
        ROUND(
            stage_failures::NUMERIC / NULLIF(SUM(stage_failures) OVER(), 0) * 100, 2
        ) AS share_of_total_losses_pct
    FROM dropoff_calc
    ORDER BY sequence_order ASC;
    """
    return run_query(sql)


def get_sla_breach_analysis(filters: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    """SLA breach frequency and average delay hours (process_metrics.sql Query 5)."""
    filters = filters or {}
    where_clause = _build_where_clause(
        company_ids=filters.get("company_ids"),
        sectors=filters.get("sectors"),
        stages=filters.get("stages"),
        date_range=filters.get("date_range"),
        table_alias="a"
    )
    extra_exit = "AND sr.stage_exit_time IS NOT NULL" if where_clause else "WHERE sr.stage_exit_time IS NOT NULL"

    sql = f"""
    WITH sla_breach_stats AS (
        SELECT 
            sr.sequence_order,
            sr.stage_name,
            sr.target_sla_hours,
            COUNT(sr.stage_record_id) AS total_evaluations,
            COUNT(CASE WHEN sr.sla_breached_flag = TRUE THEN 1 END) AS breach_count,
            AVG(
                CASE WHEN sr.sla_breached_flag = TRUE 
                    THEN (EXTRACT(EPOCH FROM (sr.stage_exit_time - sr.stage_entry_time)) / 3600.0) - sr.target_sla_hours 
                END
            ) AS avg_delay_hours
        FROM recruitment_stage_records sr
        JOIN applications a ON sr.application_id = a.application_id
        JOIN companies c ON a.company_id = c.company_id
        {where_clause} {extra_exit}
        GROUP BY sr.sequence_order, sr.stage_name, sr.target_sla_hours
    )
    SELECT 
        sequence_order,
        stage_name,
        target_sla_hours,
        total_evaluations,
        breach_count,
        ROUND(
            (breach_count::NUMERIC / NULLIF(total_evaluations, 0)) * 100, 2
        ) AS sla_breach_rate_pct,
        ROUND(COALESCE(avg_delay_hours, 0)::NUMERIC, 2) AS avg_overdue_delay_hours
    FROM sla_breach_stats
    ORDER BY sequence_order ASC;
    """
    return run_query(sql)


def get_stage_scores_and_tat(filters: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    """Stage evaluation scores and turnaround time latency (process_metrics.sql Query 1)."""
    filters = filters or {}
    where_clause = _build_where_clause(
        company_ids=filters.get("company_ids"),
        sectors=filters.get("sectors"),
        stages=filters.get("stages"),
        date_range=filters.get("date_range"),
        table_alias="a"
    )
    extra_exit = "AND sr.stage_exit_time IS NOT NULL" if where_clause else "WHERE sr.stage_exit_time IS NOT NULL"

    sql = f"""
    SELECT 
        sr.sequence_order,
        sr.stage_name,
        sr.target_sla_hours,
        COUNT(sr.stage_record_id) AS evaluation_count,
        ROUND(AVG(sr.evaluation_score)::NUMERIC, 2) AS avg_score,
        ROUND(MIN(sr.evaluation_score)::NUMERIC, 2) AS min_score,
        ROUND(MAX(sr.evaluation_score)::NUMERIC, 2) AS max_score,
        ROUND(AVG(EXTRACT(EPOCH FROM (sr.stage_exit_time - sr.stage_entry_time)) / 3600.0)::NUMERIC, 2) AS avg_tat_hours
    FROM recruitment_stage_records sr
    JOIN applications a ON sr.application_id = a.application_id
    JOIN companies c ON a.company_id = c.company_id
    {where_clause} {extra_exit}
    GROUP BY sr.sequence_order, sr.stage_name, sr.target_sla_hours
    ORDER BY sr.sequence_order ASC;
    """
    return run_query(sql)


# ==============================================================================
# Page 3: Company Analytics Queries
# ==============================================================================

def get_company_kpis(filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Summary metrics for the corporate partner landscape."""
    filters = filters or {}
    where_clause = _build_where_clause(
        company_ids=filters.get("company_ids"),
        sectors=filters.get("sectors"),
        date_range=filters.get("date_range"),
        table_alias="a"
    )

    sql = f"""
    SELECT 
        COUNT(DISTINCT c.company_id) AS active_partners,
        COUNT(DISTINCT a.application_id) AS total_apps,
        COUNT(DISTINCT CASE WHEN a.overall_status = 'Hired' THEN a.application_id END) AS total_hires,
        ROUND(
            COUNT(DISTINCT a.application_id)::NUMERIC / NULLIF(COUNT(DISTINCT c.company_id), 0), 1
        ) AS avg_apps_per_company,
        ROUND(
            (COUNT(DISTINCT CASE WHEN a.overall_status = 'Hired' THEN a.application_id END)::NUMERIC / 
            NULLIF(COUNT(DISTINCT a.application_id), 0)) * 100, 2
        ) AS hiring_yield_pct
    FROM companies c
    JOIN applications a ON c.company_id = a.company_id
    {where_clause};
    """
    df = run_query(sql)
    if not df.empty:
        return df.iloc[0].to_dict()
    return {"active_partners": 0, "total_apps": 0, "total_hires": 0, "avg_apps_per_company": 0.0, "hiring_yield_pct": 0.0}


def get_top_hiring_companies(filters: Optional[Dict[str, Any]] = None, limit: int = 15) -> pd.DataFrame:
    """Top companies by confirmed hires (funnel_metrics.sql Query 1)."""
    filters = filters or {}
    where_clause = _build_where_clause(
        company_ids=filters.get("company_ids"),
        sectors=filters.get("sectors"),
        date_range=filters.get("date_range"),
        table_alias="a"
    )

    sql = f"""
    SELECT 
        c.company_name,
        c.industry_sector,
        c.priority_tier,
        COUNT(CASE WHEN a.overall_status = 'Hired' THEN 1 END) AS hires_count,
        COUNT(a.application_id) AS applications_count,
        ROUND(
            (COUNT(CASE WHEN a.overall_status = 'Hired' THEN 1 END)::NUMERIC / NULLIF(COUNT(a.application_id), 0)) * 100, 2
        ) AS hire_rate_pct
    FROM companies c
    JOIN applications a ON c.company_id = a.company_id
    {where_clause}
    GROUP BY c.company_name, c.industry_sector, c.priority_tier
    HAVING COUNT(CASE WHEN a.overall_status = 'Hired' THEN 1 END) > 0
    ORDER BY hires_count DESC
    LIMIT {limit};
    """
    return run_query(sql)


def get_offers_by_company(filters: Optional[Dict[str, Any]] = None, limit: int = 15) -> pd.DataFrame:
    """Offer conversion & acceptance rate per company (funnel_metrics.sql Query 4)."""
    filters = filters or {}
    where_clause = _build_where_clause(
        company_ids=filters.get("company_ids"),
        sectors=filters.get("sectors"),
        date_range=filters.get("date_range"),
        table_alias="a"
    )
    extra_offer = "AND sr.stage_name = 'Offer Extended'" if where_clause else "WHERE sr.stage_name = 'Offer Extended'"

    sql = f"""
    WITH offer_stats AS (
        SELECT 
            c.company_name,
            c.priority_tier,
            c.industry_sector,
            COUNT(CASE WHEN sr.stage_name = 'Offer Extended' THEN 1 END) AS total_offers_extended,
            COUNT(CASE WHEN sr.stage_name = 'Offer Extended' AND sr.stage_status = 'Passed' THEN 1 END) AS offers_accepted
        FROM companies c
        JOIN applications a ON c.company_id = a.company_id
        JOIN recruitment_stage_records sr ON a.application_id = sr.application_id
        {where_clause} {extra_offer}
        GROUP BY c.company_name, c.priority_tier, c.industry_sector
    )
    SELECT 
        company_name,
        priority_tier,
        industry_sector,
        total_offers_extended,
        offers_accepted,
        ROUND(
            (offers_accepted::NUMERIC / NULLIF(total_offers_extended, 0)) * 100, 2
        ) AS offer_acceptance_rate_pct
    FROM offer_stats
    ORDER BY total_offers_extended DESC
    LIMIT {limit};
    """
    return run_query(sql)


def get_sector_analytics(filters: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    """Industry sector breakdown of applications, hires, and company presence."""
    filters = filters or {}
    where_clause = _build_where_clause(
        company_ids=filters.get("company_ids"),
        sectors=filters.get("sectors"),
        date_range=filters.get("date_range"),
        table_alias="a"
    )

    sql = f"""
    SELECT 
        c.industry_sector,
        COUNT(DISTINCT c.company_id) AS companies_count,
        COUNT(a.application_id) AS applications_count,
        COUNT(CASE WHEN a.overall_status = 'Hired' THEN 1 END) AS hires_count,
        ROUND(
            (COUNT(CASE WHEN a.overall_status = 'Hired' THEN 1 END)::NUMERIC / NULLIF(COUNT(a.application_id), 0)) * 100, 2
        ) AS sector_hire_rate_pct
    FROM companies c
    LEFT JOIN applications a ON c.company_id = a.company_id
    {where_clause}
    GROUP BY c.industry_sector
    ORDER BY applications_count DESC;
    """
    return run_query(sql)


def get_slowest_companies(filters: Optional[Dict[str, Any]] = None, limit: int = 15) -> pd.DataFrame:
    """Companies ranked by average stage turnaround latency (process_metrics.sql Query 3)."""
    filters = filters or {}
    where_clause = _build_where_clause(
        company_ids=filters.get("company_ids"),
        sectors=filters.get("sectors"),
        date_range=filters.get("date_range"),
        table_alias="a"
    )
    extra_exit = "AND sr.stage_exit_time IS NOT NULL" if where_clause else "WHERE sr.stage_exit_time IS NOT NULL"

    sql = f"""
    SELECT 
        c.company_name,
        c.industry_sector,
        c.priority_tier,
        COUNT(sr.stage_record_id) AS total_evaluations,
        ROUND(AVG(EXTRACT(EPOCH FROM (sr.stage_exit_time - sr.stage_entry_time)) / 3600.0)::NUMERIC, 2) AS avg_turnaround_hours
    FROM companies c
    JOIN applications a ON c.company_id = a.company_id
    JOIN recruitment_stage_records sr ON a.application_id = sr.application_id
    {where_clause} {extra_exit}
    GROUP BY c.company_name, c.industry_sector, c.priority_tier
    ORDER BY avg_turnaround_hours DESC
    LIMIT {limit};
    """
    return run_query(sql)


# ==============================================================================
# Page 4: Operations & Capacity Queries
# ==============================================================================

def get_operations_kpis() -> Dict[str, Any]:
    """High-level venue and panel capacity utilization indicators."""
    sql = """
    SELECT 
        (SELECT COUNT(*) FROM rooms) AS total_rooms,
        (SELECT COUNT(*) FROM panels) AS total_panels,
        (SELECT COUNT(*) FROM interview_slots) AS total_slots,
        (SELECT COUNT(*) FROM interview_slots WHERE slot_status IN ('Booked', 'Completed')) AS booked_slots,
        ROUND(
            (SELECT COUNT(*) FROM interview_slots WHERE slot_status IN ('Booked', 'Completed'))::NUMERIC / 
            NULLIF((SELECT COUNT(*) FROM interview_slots), 0) * 100, 2
        ) AS overall_slot_occupancy_pct,
        (SELECT COUNT(*) FROM recruitment_stage_records WHERE sla_breached_flag = TRUE) AS total_sla_breaches;
    """
    df = run_query(sql)
    if not df.empty:
        return df.iloc[0].to_dict()
    return {"total_rooms": 0, "total_panels": 0, "total_slots": 0, "booked_slots": 0, "overall_slot_occupancy_pct": 0.0, "total_sla_breaches": 0}


def get_panel_utilization() -> pd.DataFrame:
    """Interviewer workload against daily slot caps (capacity_metrics.sql Query 2)."""
    sql = """
    WITH panel_workload AS (
        SELECT 
            p.panel_id,
            p.panel_code,
            p.department,
            p.max_daily_slots,
            COUNT(DISTINCT s.hiring_day) AS active_days_count,
            COUNT(s.slot_id) AS total_slots_assigned,
            COUNT(CASE WHEN s.slot_status IN ('Booked', 'Completed') THEN 1 END) AS booked_slots_count
        FROM panels p
        LEFT JOIN interview_slots s ON p.panel_id = s.panel_id
        GROUP BY p.panel_id, p.panel_code, p.department, p.max_daily_slots
    )
    SELECT 
        panel_code,
        department,
        max_daily_slots,
        active_days_count,
        total_slots_assigned,
        booked_slots_count,
        ROUND(
            (booked_slots_count::NUMERIC / NULLIF(max_daily_slots * NULLIF(active_days_count, 0), 0)) * 100, 2
        ) AS panel_utilization_pct
    FROM panel_workload
    ORDER BY panel_utilization_pct DESC;
    """
    return run_query(sql)


def get_room_utilization() -> pd.DataFrame:
    """Room occupancy rates and hours booked (capacity_metrics.sql Query 1)."""
    sql = """
    WITH room_slot_stats AS (
        SELECT 
            r.room_id,
            r.room_name,
            r.interview_mode,
            r.seating_capacity,
            COUNT(s.slot_id) AS total_slots_created,
            COUNT(CASE WHEN s.slot_status IN ('Booked', 'Completed') THEN 1 END) AS booked_slots,
            COALESCE(
                SUM(CASE WHEN s.slot_status IN ('Booked', 'Completed') 
                    THEN EXTRACT(EPOCH FROM (s.slot_end_time - s.slot_start_time)) / 3600.0 END), 0
            ) AS booked_hours
        FROM rooms r
        LEFT JOIN interview_slots s ON r.room_id = s.room_id
        GROUP BY r.room_id, r.room_name, r.interview_mode, r.seating_capacity
    )
    SELECT 
        room_name,
        interview_mode,
        seating_capacity,
        total_slots_created,
        booked_slots,
        ROUND(booked_hours::NUMERIC, 2) AS total_booked_hours,
        ROUND(
            (booked_slots::NUMERIC / NULLIF(total_slots_created, 0)) * 100, 2
        ) AS room_occupancy_rate_pct
    FROM room_slot_stats
    ORDER BY room_occupancy_rate_pct DESC;
    """
    return run_query(sql)


def get_daily_slot_allocation() -> pd.DataFrame:
    """Schedule distribution across hiring days (capacity_metrics.sql Query 3)."""
    sql = """
    SELECT 
        hiring_day,
        COUNT(slot_id) AS total_slots,
        COUNT(CASE WHEN slot_status = 'Available' THEN 1 END) AS available_slots,
        COUNT(CASE WHEN slot_status = 'Booked' THEN 1 END) AS booked_slots,
        COUNT(CASE WHEN slot_status = 'Completed' THEN 1 END) AS completed_slots,
        COUNT(CASE WHEN slot_status = 'Cancelled' THEN 1 END) AS cancelled_slots,
        ROUND(
            ((COUNT(CASE WHEN slot_status = 'Booked' THEN 1 END) + COUNT(CASE WHEN slot_status = 'Completed' THEN 1 END))::NUMERIC / 
            NULLIF(COUNT(slot_id), 0)) * 100, 2
        ) AS day_occupancy_rate_pct
    FROM interview_slots
    GROUP BY hiring_day
    ORDER BY hiring_day ASC;
    """
    return run_query(sql)


def get_peak_scheduling_windows() -> pd.DataFrame:
    """Peak interview congestion hours across hiring days (capacity_metrics.sql Query 4)."""
    sql = """
    SELECT 
        hiring_day,
        to_char(slot_start_time, 'HH24:00') AS slot_hour_window,
        COUNT(slot_id) AS total_slots,
        COUNT(CASE WHEN slot_status IN ('Booked', 'Completed') THEN 1 END) AS active_booked_slots
    FROM interview_slots
    GROUP BY hiring_day, to_char(slot_start_time, 'HH24:00')
    ORDER BY hiring_day ASC, slot_hour_window ASC;
    """
    return run_query(sql)


def get_capacity_recommendations() -> pd.DataFrame:
    """
    Actionable capacity allocation warnings and bottleneck indicators
    based on actual warehouse thresholds (01_capacity_allocation_recommendations.sql & underutilized resources).
    """
    sql = """
    WITH panel_status AS (
        SELECT 
            'Panel Overload Alert' AS issue_type,
            'CRITICAL' AS severity,
            p.panel_code || ' (' || p.department || ')' AS resource_name,
            COUNT(CASE WHEN s.slot_status IN ('Booked', 'Completed') THEN 1 END) AS current_load,
            (p.max_daily_slots * 3) AS max_capacity,
            ROUND((COUNT(CASE WHEN s.slot_status IN ('Booked', 'Completed') THEN 1 END)::NUMERIC / 
                   NULLIF(p.max_daily_slots * 3, 0)) * 100, 1) AS load_pct,
            'Panel exceeds capacity threshold (>85%). Rebalance upcoming interview slots to underutilized evaluators.' AS recommended_action
        FROM panels p
        LEFT JOIN interview_slots s ON p.panel_id = s.panel_id
        GROUP BY p.panel_id, p.panel_code, p.department, p.max_daily_slots
        HAVING (COUNT(CASE WHEN s.slot_status IN ('Booked', 'Completed') THEN 1 END)::NUMERIC / NULLIF(p.max_daily_slots * 3, 0)) >= 0.85
    ),
    room_status AS (
        SELECT 
            'Room Underutilization' AS issue_type,
            'INFO' AS severity,
            r.room_name || ' (' || r.interview_mode || ')' AS resource_name,
            COUNT(CASE WHEN s.slot_status IN ('Booked', 'Completed') THEN 1 END) AS current_load,
            COUNT(s.slot_id) AS max_capacity,
            ROUND((COUNT(CASE WHEN s.slot_status IN ('Booked', 'Completed') THEN 1 END)::NUMERIC / 
                   NULLIF(COUNT(s.slot_id), 0)) * 100, 1) AS load_pct,
            'Venue space operating below 40% capacity. Consolidate hybrid interview sessions into this venue.' AS recommended_action
        FROM rooms r
        LEFT JOIN interview_slots s ON r.room_id = s.room_id
        GROUP BY r.room_id, r.room_name, r.interview_mode
        HAVING (COUNT(CASE WHEN s.slot_status IN ('Booked', 'Completed') THEN 1 END)::NUMERIC / NULLIF(COUNT(s.slot_id), 0)) < 0.40
    )
    SELECT * FROM panel_status
    UNION ALL
    SELECT * FROM room_status
    ORDER BY severity ASC, load_pct DESC;
    """
    return run_query(sql)
