-- ==============================================================================
-- Recruitment Funnel Analytics Module
-- Target File: sql/funnel/funnel_metrics.sql
-- Dialect: PostgreSQL 15+
-- Description: Analytical queries for application distribution, stage conversion rates,
--              candidate drop-offs, offer acceptance rates, and department yield.
-- Tables Queried: candidates, companies, applications, recruitment_stage_records
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- QUERY 1: Applications by Company
-- Business Purpose: Evaluates applicant interest and hiring yield per company.
-- CTE Breakdown:
--   - company_app_counts: Aggregates total, active, hired, and rejected applications per company.
-- ------------------------------------------------------------------------------
WITH company_app_counts AS (
    SELECT 
        c.company_id,
        c.company_name,
        c.industry_sector,
        c.priority_tier,
        COUNT(a.application_id) AS total_applications,
        COUNT(DISTINCT a.candidate_id) AS unique_applicants,
        COUNT(CASE WHEN a.overall_status = 'Active' THEN 1 END) AS active_applications,
        COUNT(CASE WHEN a.overall_status = 'Hired' THEN 1 END) AS hired_applications,
        COUNT(CASE WHEN a.overall_status = 'Rejected' THEN 1 END) AS rejected_applications
    FROM companies c
    LEFT JOIN applications a ON c.company_id = a.company_id
    GROUP BY c.company_id, c.company_name, c.industry_sector, c.priority_tier
)
SELECT 
    company_id,
    company_name,
    industry_sector,
    priority_tier,
    total_applications,
    unique_applicants,
    active_applications,
    hired_applications,
    rejected_applications,
    ROUND(
        (hired_applications::NUMERIC / NULLIF(total_applications, 0)) * 100, 2
    ) AS company_hiring_rate_pct
FROM company_app_counts
ORDER BY total_applications DESC;


-- ------------------------------------------------------------------------------
-- QUERY 2: Stage Conversion Rates
-- Business Purpose: Calculates stage-over-stage pass rates across the pipeline.
-- CTE Breakdown:
--   - stage_aggregates: Counts candidate entries and passes for each funnel stage.
-- ------------------------------------------------------------------------------
WITH stage_aggregates AS (
    SELECT 
        sequence_order,
        stage_name,
        COUNT(stage_record_id) AS total_candidates_entered,
        COUNT(CASE WHEN stage_status = 'Passed' THEN 1 END) AS candidates_passed,
        COUNT(CASE WHEN stage_status = 'Failed' THEN 1 END) AS candidates_failed,
        COUNT(CASE WHEN stage_status = 'Pending' THEN 1 END) AS candidates_pending
    FROM recruitment_stage_records
    GROUP BY sequence_order, stage_name
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
    ) AS stage_pass_rate_pct
FROM stage_aggregates
ORDER BY sequence_order ASC;


-- ------------------------------------------------------------------------------
-- QUERY 3: Drop-Off Rates
-- Business Purpose: Identifies pipeline leakage points where candidates fail/exit.
-- CTE Breakdown:
--   - dropoff_calc: Measures percentage of stage entrants who fail at that stage.
-- ------------------------------------------------------------------------------
WITH dropoff_calc AS (
    SELECT 
        sequence_order,
        stage_name,
        COUNT(stage_record_id) AS stage_entrants,
        COUNT(CASE WHEN stage_status = 'Failed' THEN 1 END) AS stage_failures
    FROM recruitment_stage_records
    GROUP BY sequence_order, stage_name
)
SELECT 
    sequence_order,
    stage_name,
    stage_entrants,
    stage_failures,
    ROUND(
        (stage_failures::NUMERIC / NULLIF(stage_entrants, 0)) * 100, 2
    ) AS stage_dropoff_rate_pct
FROM dropoff_calc
ORDER BY sequence_order ASC;


-- ------------------------------------------------------------------------------
-- QUERY 4: Offer Conversion Rates (Offer Acceptance Rate - OAR)
-- Business Purpose: Measures how effectively extended offers convert to hires per company.
-- CTE Breakdown:
--   - offer_stats: Compares offers extended vs. offers accepted.
-- ------------------------------------------------------------------------------
WITH offer_stats AS (
    SELECT 
        c.company_name,
        c.priority_tier,
        COUNT(CASE WHEN sr.stage_name = 'Offer' THEN 1 END) AS total_offers_extended,
        COUNT(CASE WHEN sr.stage_name = 'Offer' AND sr.stage_status = 'Passed' THEN 1 END) AS offers_accepted
    FROM companies c
    JOIN applications a ON c.company_id = a.company_id
    JOIN recruitment_stage_records sr ON a.application_id = sr.application_id
    WHERE sr.stage_name = 'Offer'
    GROUP BY c.company_name, c.priority_tier
)
SELECT 
    company_name,
    priority_tier,
    total_offers_extended,
    offers_accepted,
    ROUND(
        (offers_accepted::NUMERIC / NULLIF(total_offers_extended, 0)) * 100, 2
    ) AS offer_acceptance_rate_pct
FROM offer_stats
ORDER BY total_offers_extended DESC;


-- ------------------------------------------------------------------------------
-- QUERY 5: Department-Wise Funnel Performance
-- Business Purpose: Compares candidate progression and hiring rates across academic majors.
-- CTE Breakdown:
--   - major_performance: Joins candidate majors with application hiring outcomes.
-- ------------------------------------------------------------------------------
WITH major_performance AS (
    SELECT 
        cand.academic_major,
        cand.degree_program,
        COUNT(DISTINCT cand.candidate_id) AS total_students,
        COUNT(DISTINCT a.application_id) AS total_applications_submitted,
        COUNT(DISTINCT CASE WHEN a.overall_status = 'Hired' THEN a.application_id END) AS total_hires
    FROM candidates cand
    LEFT JOIN applications a ON cand.candidate_id = a.candidate_id
    GROUP BY cand.academic_major, cand.degree_program
)
SELECT 
    academic_major,
    degree_program,
    total_students,
    total_applications_submitted,
    total_hires,
    ROUND(
        (total_hires::NUMERIC / NULLIF(total_applications_submitted, 0)) * 100, 2
    ) AS major_hiring_yield_pct
FROM major_performance
ORDER BY total_hires DESC;
