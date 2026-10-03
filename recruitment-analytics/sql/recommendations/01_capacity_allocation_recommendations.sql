-- ==============================================================================
-- SQL Module: Decision Support & Recommendations
-- Target File: sql/recommendations/01_capacity_allocation_recommendations.sql
-- Description: Rebalancing alerts for panel slot load and SLA breaches
-- Approved Entities: panels, interview_slots, companies, recruitment_stages
-- ==============================================================================

/*
SELECT 
    p.panel_id,
    p.panel_code,
    p.department,
    COUNT(s.slot_id) AS booked_slots,
    p.max_daily_slots,
    CASE 
        WHEN COUNT(s.slot_id) > p.max_daily_slots THEN 'CRITICAL: Panel Overloaded - Reallocate Slots'
        WHEN COUNT(s.slot_id) >= (p.max_daily_slots * 0.85) THEN 'WARNING: High Capacity Load'
        ELSE 'OPTIMAL'
    END AS recommendation_status
FROM panels p
LEFT JOIN interview_slots s ON p.panel_id = s.panel_id 
    AND s.slot_status = 'Booked'
GROUP BY p.panel_id, p.panel_code, p.department, p.max_daily_slots;
*/
