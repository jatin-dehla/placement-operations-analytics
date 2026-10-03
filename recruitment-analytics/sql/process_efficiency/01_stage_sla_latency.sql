-- ==============================================================================
-- SQL Module: Process Efficiency & SLA Tracking
-- Target File: sql/process_efficiency/01_stage_sla_latency.sql
-- Description: Measures stage turnaround times (TAT) and SLA breach rates
-- Approved Entities: interview_slots, recruitment_stages, applications
-- ==============================================================================

/*
SELECT 
    rs.stage_name,
    rs.target_sla_hours,
    COUNT(s.slot_id) AS total_evaluations,
    COUNT(CASE WHEN s.sla_breached_flag = TRUE THEN 1 END) AS sla_breaches,
    ROUND(
        COUNT(CASE WHEN s.sla_breached_flag = TRUE THEN 1 END)::NUMERIC / 
        NULLIF(COUNT(s.slot_id), 0) * 100, 2
    ) AS sla_breach_rate_pct,
    AVG(EXTRACT(EPOCH FROM (s.stage_exit_time - s.stage_entry_time)) / 3600)::NUMERIC(10,2) AS avg_tat_hours
FROM interview_slots s
JOIN recruitment_stages rs ON s.stage_id = rs.stage_id
WHERE s.stage_exit_time IS NOT NULL
GROUP BY rs.stage_name, rs.target_sla_hours;
*/
