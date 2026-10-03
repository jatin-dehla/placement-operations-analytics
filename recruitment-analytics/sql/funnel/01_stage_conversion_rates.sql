-- ==============================================================================
-- SQL Module: Funnel Conversion Analytics
-- Target File: sql/funnel/01_stage_conversion_rates.sql
-- Description: Analytical view computing stage-over-stage candidate pass rates
-- Approved Entities: candidates, companies, applications, recruitment_stages, interview_slots
-- ==============================================================================

/*
SELECT 
    c.company_name,
    c.priority_tier,
    rs.stage_name,
    rs.sequence_order,
    COUNT(DISTINCT a.application_id) AS applications_entered,
    COUNT(DISTINCT CASE WHEN s.slot_status = 'Completed' AND s.score >= 70 THEN a.application_id END) AS applications_passed,
    ROUND(
        COUNT(DISTINCT CASE WHEN s.slot_status = 'Completed' AND s.score >= 70 THEN a.application_id END)::NUMERIC / 
        NULLIF(COUNT(DISTINCT a.application_id), 0) * 100, 2
    ) AS stage_pass_rate_pct
FROM applications a
JOIN companies c ON a.company_id = c.company_id
JOIN recruitment_stages rs ON a.current_stage_id = rs.stage_id
LEFT JOIN interview_slots s ON a.application_id = s.application_id AND a.current_stage_id = s.stage_id
GROUP BY c.company_name, c.priority_tier, rs.stage_name, rs.sequence_order
ORDER BY rs.sequence_order ASC;
*/
