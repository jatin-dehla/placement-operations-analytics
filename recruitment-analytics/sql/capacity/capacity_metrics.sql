-- ==============================================================================
-- Capacity & Scheduling Analytics Module
-- Target File: sql/capacity/capacity_metrics.sql
-- Dialect: PostgreSQL 15+
-- Description: Analytical queries for room utilization, panel daily slot workload,
--              slot occupancy rates, peak scheduling windows, and underutilized resources.
-- Tables Queried: rooms, panels, interview_slots, companies
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- QUERY 1: Room Utilization
-- Business Purpose: Measures physical and virtual venue capacity utilization.
-- CTE Breakdown:
--   - room_slot_stats: Calculates total hours booked and slot counts per room.
-- ------------------------------------------------------------------------------
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
    room_id,
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


-- ------------------------------------------------------------------------------
-- QUERY 2: Panel Utilization
-- Business Purpose: Measures evaluator interviewing workload against daily slot caps.
-- CTE Breakdown:
--   - panel_workload: Aggregates booked slots per panel across hiring days.
-- ------------------------------------------------------------------------------
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
    panel_id,
    panel_code,
    department,
    max_daily_slots,
    active_days_count,
    total_slots_assigned,
    booked_slots_count,
    ROUND(
        (booked_slots_count::NUMERIC / NULLIF(max_daily_slots * NULLIF(active_days_count, 0), 0)) * 100, 2
    ) AS panel_capacity_utilization_pct
FROM panel_workload
ORDER BY panel_capacity_utilization_pct DESC;


-- ------------------------------------------------------------------------------
-- QUERY 3: Slot Occupancy Rate by Hiring Day
-- Business Purpose: Evaluates schedule slot fill rates across placement drive days.
-- CTE Breakdown:
--   - day_occupancy: Summarizes available vs booked slots per hiring day.
-- ------------------------------------------------------------------------------
WITH day_occupancy AS (
    SELECT 
        hiring_day,
        COUNT(slot_id) AS total_slots,
        COUNT(CASE WHEN slot_status = 'Available' THEN 1 END) AS available_slots,
        COUNT(CASE WHEN slot_status = 'Booked' THEN 1 END) AS booked_slots,
        COUNT(CASE WHEN slot_status = 'Completed' THEN 1 END) AS completed_slots
    FROM interview_slots
    GROUP BY hiring_day
)
SELECT 
    hiring_day,
    total_slots,
    available_slots,
    booked_slots,
    completed_slots,
    ROUND(
        ((booked_slots + completed_slots)::NUMERIC / NULLIF(total_slots, 0)) * 100, 2
    ) AS day_slot_occupancy_rate_pct
FROM day_occupancy
ORDER BY hiring_day ASC;


-- ------------------------------------------------------------------------------
-- QUERY 4: Peak Scheduling Windows
-- Business Purpose: Identifies high-demand interview hours across hiring days.
-- CTE Breakdown:
--   - hourly_slots: Extracts hour of day from slot start time.
-- ------------------------------------------------------------------------------
WITH hourly_slots AS (
    SELECT 
        hiring_day,
        TO_CHAR(slot_start_time, 'HH24:00') AS slot_hour_window,
        COUNT(slot_id) AS total_scheduled_slots,
        COUNT(CASE WHEN slot_status IN ('Booked', 'Completed') THEN 1 END) AS active_booked_slots
    FROM interview_slots
    GROUP BY hiring_day, TO_CHAR(slot_start_time, 'HH24:00')
)
SELECT 
    hiring_day,
    slot_hour_window,
    total_scheduled_slots,
    active_booked_slots,
    ROUND(
        (active_booked_slots::NUMERIC / NULLIF(total_scheduled_slots, 0)) * 100, 2
    ) AS hourly_utilization_pct
FROM hourly_slots
ORDER BY active_booked_slots DESC, hiring_day ASC;


-- ------------------------------------------------------------------------------
-- QUERY 5: Underutilized Resources
-- Business Purpose: Highlights rooms and panels operating below 50% capacity threshold.
-- CTE Breakdown:
--   - underutilized_rooms: Rooms with <50% occupancy.
--   - underutilized_panels: Panels with <50% workload.
-- ------------------------------------------------------------------------------
WITH room_calc AS (
    SELECT 
        r.room_id,
        r.room_name,
        'Room Resource' AS resource_type,
        COUNT(s.slot_id) AS total_slots,
        COUNT(CASE WHEN s.slot_status IN ('Booked', 'Completed') THEN 1 END) AS active_slots
    FROM rooms r
    LEFT JOIN interview_slots s ON r.room_id = s.room_id
    GROUP BY r.room_id, r.room_name
),
panel_calc AS (
    SELECT 
        p.panel_id,
        p.panel_code AS resource_name,
        'Panel Resource' AS resource_type,
        (p.max_daily_slots * 3) AS total_slots,
        COUNT(CASE WHEN s.slot_status IN ('Booked', 'Completed') THEN 1 END) AS active_slots
    FROM panels p
    LEFT JOIN interview_slots s ON p.panel_id = s.panel_id
    GROUP BY p.panel_id, p.panel_code, p.max_daily_slots
)
SELECT 
    resource_type,
    room_name AS resource_name,
    total_slots,
    active_slots,
    ROUND((active_slots::NUMERIC / NULLIF(total_slots, 0)) * 100, 2) AS utilization_pct,
    'UNDERUTILIZED (< 50%)' AS alert_status
FROM room_calc
WHERE (active_slots::NUMERIC / NULLIF(total_slots, 0)) < 0.50

UNION ALL

SELECT 
    resource_type,
    resource_name,
    total_slots,
    active_slots,
    ROUND((active_slots::NUMERIC / NULLIF(total_slots, 0)) * 100, 2) AS utilization_pct,
    'UNDERUTILIZED (< 50%)' AS alert_status
FROM panel_calc
WHERE (active_slots::NUMERIC / NULLIF(total_slots, 0)) < 0.50;
