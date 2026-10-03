-- ==============================================================================
-- Process Efficiency & SLA Analytics Module
-- Target File: sql/process_efficiency/process_metrics.sql
-- Dialect: PostgreSQL 15+
-- Description: Analytical queries for stage turnaround times (TAT), time-to-offer (TTO),
--              slowest companies, slowest stages, and SLA breach frequency analysis.
-- Tables Queried: recruitment_stage_records, applications, companies
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- QUERY 1: Average Stage Duration (Turnaround Time - TAT)
-- Business Purpose: Quantifies evaluation duration per funnel stage.
-- CTE Breakdown:
--   - stage_durations: Calculates elapsed hours between entry and exit timestamps.
-- ------------------------------------------------------------------------------
WITH stage_durations AS (
    SELECT 
        sequence_order,
        stage_name,
        target_sla_hours,
        EXTRACT(EPOCH FROM (stage_exit_time - stage_entry_time)) / 3600.0 AS duration_hours
    FROM recruitment_stage_records
    WHERE stage_exit_time IS NOT NULL
)
SELECT 
    sequence_order,
    stage_name,
    target_sla_hours,
    COUNT(*) AS completed_evaluations_count,
    ROUND(AVG(duration_hours)::NUMERIC, 2) AS avg_tat_hours,
    ROUND(MIN(duration_hours)::NUMERIC, 2) AS min_tat_hours,
    ROUND(MAX(duration_hours)::NUMERIC, 2) AS max_tat_hours
FROM stage_durations
GROUP BY sequence_order, stage_name, target_sla_hours
ORDER BY sequence_order ASC;


-- ------------------------------------------------------------------------------
-- QUERY 2: Average Time-to-Offer (TTO)
-- Business Purpose: Measures overall elapsed time from application submission to offer issuance.
-- CTE Breakdown:
--   - offer_timelines: Joins application date with Offer stage entry timestamp.
-- ------------------------------------------------------------------------------
WITH offer_timelines AS (
    SELECT 
        a.application_id,
        a.candidate_id,
        a.company_id,
        a.application_date,
        sr.stage_entry_time AS offer_issued_time,
        EXTRACT(EPOCH FROM (sr.stage_entry_time - a.application_date::timestamp)) / 86400.0 AS tto_days
    FROM applications a
    JOIN recruitment_stage_records sr ON a.application_id = sr.application_id
    WHERE sr.stage_name = 'Offer'
)
SELECT 
    COUNT(application_id) AS offers_evaluated,
    ROUND(AVG(tto_days)::NUMERIC, 2) AS avg_time_to_offer_days,
    ROUND(MIN(tto_days)::NUMERIC, 2) AS min_time_to_offer_days,
    ROUND(MAX(tto_days)::NUMERIC, 2) AS max_time_to_offer_days
FROM offer_timelines;


-- ------------------------------------------------------------------------------
-- QUERY 3: Slowest Companies
-- Business Purpose: Ranks hiring companies by average stage turnaround time.
-- CTE Breakdown:
--   - company_tat: Computes mean stage turnaround time per company.
-- ------------------------------------------------------------------------------
WITH company_tat AS (
    SELECT 
        c.company_id,
        c.company_name,
        c.priority_tier,
        COUNT(sr.stage_record_id) AS total_evaluations,
        AVG(EXTRACT(EPOCH FROM (sr.stage_exit_time - sr.stage_entry_time)) / 3600.0) AS avg_company_tat_hours
    FROM companies c
    JOIN applications a ON c.company_id = a.company_id
    JOIN recruitment_stage_records sr ON a.application_id = sr.application_id
    WHERE sr.stage_exit_time IS NOT NULL
    GROUP BY c.company_id, c.company_name, c.priority_tier
)
SELECT 
    company_id,
    company_name,
    priority_tier,
    total_evaluations,
    ROUND(avg_company_tat_hours::NUMERIC, 2) AS avg_company_tat_hours
FROM company_tat
ORDER BY avg_company_tat_hours DESC;


-- ------------------------------------------------------------------------------
-- QUERY 4: Slowest Recruitment Stages
-- Business Purpose: Identifies which pipeline stages consume the most evaluation time.
-- CTE Breakdown:
--   - stage_tat_ranking: Compares average duration to target SLA limits.
-- ------------------------------------------------------------------------------
WITH stage_tat_ranking AS (
    SELECT 
        sequence_order,
        stage_name,
        target_sla_hours,
        COUNT(stage_record_id) AS evaluation_count,
        AVG(EXTRACT(EPOCH FROM (stage_exit_time - stage_entry_time)) / 3600.0) AS avg_duration_hours
    FROM recruitment_stage_records
    WHERE stage_exit_time IS NOT NULL
    GROUP BY sequence_order, stage_name, target_sla_hours
)
SELECT 
    sequence_order,
    stage_name,
    target_sla_hours,
    evaluation_count,
    ROUND(avg_duration_hours::NUMERIC, 2) AS avg_duration_hours,
    ROUND((avg_duration_hours - target_sla_hours)::NUMERIC, 2) AS variance_from_sla_hours
FROM stage_tat_ranking
ORDER BY avg_duration_hours DESC;


-- ------------------------------------------------------------------------------
-- QUERY 5: SLA Breach Analysis
-- Business Purpose: Measures frequency and severity of evaluation SLA violations.
-- CTE Breakdown:
--   - sla_breach_stats: Counts breaches and computes average delay beyond SLA target.
-- ------------------------------------------------------------------------------
WITH sla_breach_stats AS (
    SELECT 
        sequence_order,
        stage_name,
        target_sla_hours,
        COUNT(stage_record_id) AS total_evaluations,
        COUNT(CASE WHEN sla_breached_flag = TRUE THEN 1 END) AS breach_count,
        AVG(
            CASE WHEN sla_breached_flag = TRUE 
                THEN (EXTRACT(EPOCH FROM (stage_exit_time - stage_entry_time)) / 3600.0) - target_sla_hours 
            END
        ) AS avg_delay_hours
    FROM recruitment_stage_records
    WHERE stage_exit_time IS NOT NULL
    GROUP BY sequence_order, stage_name, target_sla_hours
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
ORDER BY sla_breach_rate_pct DESC;
