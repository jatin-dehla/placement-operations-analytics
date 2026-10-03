-- ==============================================================================
-- SQL Module: Capacity & Scheduling Analytics
-- Target File: sql/capacity/01_recruiter_interviewer_capacity.sql
-- Description: Analytical queries measuring panel workload and room capacity utilization
-- Approved Entities: interview_slots, panels, rooms, companies
-- ==============================================================================

/*
-- 1. Panel Capacity Utilization Query
SELECT 
    p.panel_id,
    p.panel_code,
    p.department,
    p.max_daily_slots,
    COUNT(s.slot_id) AS scheduled_slots,
    ROUND(
        COUNT(s.slot_id)::NUMERIC / NULLIF(p.max_daily_slots, 0) * 100, 2
    ) AS panel_utilization_pct
FROM panels p
LEFT JOIN interview_slots s ON p.panel_id = s.panel_id 
    AND s.slot_status IN ('Booked', 'Completed')
GROUP BY p.panel_id, p.panel_code, p.department, p.max_daily_slots;

-- 2. Room Utilization Query
SELECT 
    r.room_id,
    r.room_name,
    r.interview_mode,
    COUNT(s.slot_id) AS allocated_slots,
    SUM(EXTRACT(EPOCH FROM (s.slot_end_time - s.slot_start_time)) / 3600)::NUMERIC(10,2) AS total_hours_booked
FROM rooms r
LEFT JOIN interview_slots s ON r.room_id = s.room_id
GROUP BY r.room_id, r.room_name, r.interview_mode;
*/
