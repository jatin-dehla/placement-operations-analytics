-- ==============================================================================
-- Recruitment Funnel & Capacity Analytics Platform
-- Production PostgreSQL DDL Schema Definition
-- Target File: database/schema/01_create_tables.sql
-- Engine: PostgreSQL 15+
-- Approved Tables Only (7): candidates, companies, applications,
--                           recruitment_stage_records, rooms, panels, interview_slots
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- 1. Table: candidates
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS candidates (
    candidate_id VARCHAR(50) PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone_number VARCHAR(20),
    degree_program VARCHAR(100) NOT NULL,
    academic_major VARCHAR(100) NOT NULL,
    gpa NUMERIC(4, 2) NOT NULL,
    cgpa_band VARCHAR(50) NOT NULL,
    graduation_year INT NOT NULL,
    gender VARCHAR(20),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_candidates_gpa CHECK (gpa >= 0.00 AND gpa <= 10.00),
    CONSTRAINT chk_candidates_grad_year CHECK (graduation_year >= 2000 AND graduation_year <= 2100)
);

COMMENT ON TABLE candidates IS 'Master repository storing student/applicant profile records, academic performance metrics, and demographic attributes.';
COMMENT ON COLUMN candidates.candidate_id IS 'Unique candidate primary key identifier (e.g., CND-1001).';
COMMENT ON COLUMN candidates.full_name IS 'Full legal name of the student applicant.';
COMMENT ON COLUMN candidates.email IS 'Unique personal or university contact email address.';
COMMENT ON COLUMN candidates.phone_number IS 'Contact telephone number.';
COMMENT ON COLUMN candidates.degree_program IS 'Enrolled academic degree program (e.g., B.Tech, M.Tech).';
COMMENT ON COLUMN candidates.academic_major IS 'Branch of study or major specialization.';
COMMENT ON COLUMN candidates.gpa IS 'Cumulative Grade Point Average on a 0.00 to 10.00 scale.';
COMMENT ON COLUMN candidates.cgpa_band IS 'Categorical academic performance classification band.';
COMMENT ON COLUMN candidates.graduation_year IS 'Expected graduation year.';
COMMENT ON COLUMN candidates.gender IS 'Self-reported demographic gender identity.';
COMMENT ON COLUMN candidates.created_at IS 'Record creation timestamp.';

-- ------------------------------------------------------------------------------
-- 2. Table: companies
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS companies (
    company_id VARCHAR(50) PRIMARY KEY,
    company_name VARCHAR(255) NOT NULL,
    industry_sector VARCHAR(100) NOT NULL,
    priority_tier VARCHAR(50) NOT NULL,
    contact_email VARCHAR(255) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE companies IS 'Master list of corporate hiring partner organizations conducting recruitment drives.';
COMMENT ON COLUMN companies.company_id IS 'Unique corporate partner primary key identifier (e.g., CMP-101).';
COMMENT ON COLUMN companies.company_name IS 'Official registered corporate name.';
COMMENT ON COLUMN companies.industry_sector IS 'Industry sector classification.';
COMMENT ON COLUMN companies.priority_tier IS 'Strategic partnership tier (e.g., Tier 1 Dream Partner).';
COMMENT ON COLUMN companies.contact_email IS 'Primary corporate HR lead contact email address.';
COMMENT ON COLUMN companies.created_at IS 'Record creation timestamp.';

-- ------------------------------------------------------------------------------
-- 3. Table: applications
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS applications (
    application_id VARCHAR(50) PRIMARY KEY,
    candidate_id VARCHAR(50) NOT NULL REFERENCES candidates(candidate_id) ON DELETE CASCADE,
    company_id VARCHAR(50) NOT NULL REFERENCES companies(company_id) ON DELETE CASCADE,
    applied_role VARCHAR(100) NOT NULL,
    overall_status VARCHAR(50) NOT NULL DEFAULT 'Active',
    application_date DATE NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_applications_status CHECK (overall_status IN ('Active', 'Hired', 'Rejected', 'Withdrawn')),
    CONSTRAINT uq_applications_candidate_company_role UNIQUE (candidate_id, company_id, applied_role)
);

COMMENT ON TABLE applications IS 'Central application record connecting candidates to hiring companies.';
COMMENT ON COLUMN applications.application_id IS 'Unique application primary key identifier (e.g., APP-5001).';
COMMENT ON COLUMN applications.candidate_id IS 'Foreign key referencing the applying candidate.';
COMMENT ON COLUMN applications.company_id IS 'Foreign key referencing the target hiring company.';
COMMENT ON COLUMN applications.applied_role IS 'Job role type applied for.';
COMMENT ON COLUMN applications.overall_status IS 'Lifecycle state of application (Active, Hired, Rejected, Withdrawn).';
COMMENT ON COLUMN applications.application_date IS 'Date application was submitted.';
COMMENT ON COLUMN applications.updated_at IS 'Timestamp of last application status update.';

-- ------------------------------------------------------------------------------
-- 4. Table: recruitment_stage_records (Funnel & SLA Engine)
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS recruitment_stage_records (
    stage_record_id VARCHAR(50) PRIMARY KEY,
    application_id VARCHAR(50) NOT NULL REFERENCES applications(application_id) ON DELETE CASCADE,
    stage_name VARCHAR(100) NOT NULL,
    sequence_order INT NOT NULL,
    stage_entry_time TIMESTAMPTZ NOT NULL,
    stage_exit_time TIMESTAMPTZ,
    stage_status VARCHAR(50) NOT NULL DEFAULT 'Pending',
    evaluation_score NUMERIC(5, 2),
    target_sla_hours INT NOT NULL,
    sla_breached_flag BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_stage_sequence CHECK (sequence_order > 0),
    CONSTRAINT chk_stage_status CHECK (stage_status IN ('Passed', 'Failed', 'Pending', 'Withdrawn')),
    CONSTRAINT chk_stage_times CHECK (stage_exit_time IS NULL OR stage_exit_time >= stage_entry_time),
    CONSTRAINT chk_stage_score CHECK (evaluation_score IS NULL OR (evaluation_score >= 0.00 AND evaluation_score <= 100.00)),
    CONSTRAINT chk_stage_target_sla CHECK (target_sla_hours >= 0)
);

COMMENT ON TABLE recruitment_stage_records IS 'Single source of truth for funnel progression, stage turnaround times (TAT), pass rates, scores, and SLA breach flags.';
COMMENT ON COLUMN recruitment_stage_records.stage_record_id IS 'Unique stage event record primary key identifier (e.g., SR-10001).';
COMMENT ON COLUMN recruitment_stage_records.application_id IS 'Foreign key referencing the evaluated application.';
COMMENT ON COLUMN recruitment_stage_records.stage_name IS 'Standard pipeline stage name (e.g., Technical Interview 1).';
COMMENT ON COLUMN recruitment_stage_records.sequence_order IS 'Numerical sequence order in pipeline execution (must be > 0).';
COMMENT ON COLUMN recruitment_stage_records.stage_entry_time IS 'Timestamp when candidate entered this funnel stage.';
COMMENT ON COLUMN recruitment_stage_records.stage_exit_time IS 'Timestamp when evaluation outcome was rendered (must be >= entry time).';
COMMENT ON COLUMN recruitment_stage_records.stage_status IS 'Outcome of stage evaluation (Passed, Failed, Pending, Withdrawn).';
COMMENT ON COLUMN recruitment_stage_records.evaluation_score IS 'Numerical evaluation score awarded (0.00 to 100.00 scale).';
COMMENT ON COLUMN recruitment_stage_records.target_sla_hours IS 'Target turnaround SLA window in hours for this stage.';
COMMENT ON COLUMN recruitment_stage_records.sla_breached_flag IS 'Boolean flag indicating if evaluation turnaround exceeded target SLA hours.';
COMMENT ON COLUMN recruitment_stage_records.created_at IS 'Record creation timestamp.';

-- ------------------------------------------------------------------------------
-- 5. Table: rooms
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS rooms (
    room_id VARCHAR(50) PRIMARY KEY,
    room_name VARCHAR(255) NOT NULL,
    building_location VARCHAR(100),
    interview_mode VARCHAR(50) NOT NULL,
    seating_capacity INT NOT NULL,
    CONSTRAINT chk_rooms_capacity CHECK (seating_capacity > 0),
    CONSTRAINT chk_rooms_mode CHECK (interview_mode IN ('In-Person', 'Virtual', 'Hybrid'))
);

COMMENT ON TABLE rooms IS 'Physical desks or virtual conference link resources reserved for interview slots.';
COMMENT ON COLUMN rooms.room_id IS 'Unique room resource primary key identifier (e.g., RM-101).';
COMMENT ON COLUMN rooms.room_name IS 'Physical room designation or virtual portal desk name.';
COMMENT ON COLUMN rooms.building_location IS 'Physical building location or virtual URL domain.';
COMMENT ON COLUMN rooms.interview_mode IS 'Operational interview medium (In-Person, Virtual, Hybrid).';
COMMENT ON COLUMN rooms.seating_capacity IS 'Maximum person capacity of the room (must be > 0).';

-- ------------------------------------------------------------------------------
-- 6. Table: panels
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS panels (
    panel_id VARCHAR(50) PRIMARY KEY,
    panel_code VARCHAR(100) NOT NULL UNIQUE,
    department VARCHAR(100) NOT NULL,
    max_daily_slots INT NOT NULL DEFAULT 8,
    CONSTRAINT chk_panels_max_slots CHECK (max_daily_slots > 0)
);

COMMENT ON TABLE panels IS 'Evaluator panel units assigned to conduct technical and HR interview loops.';
COMMENT ON COLUMN panels.panel_id IS 'Unique panel primary key identifier (e.g., PNL-SWE-01).';
COMMENT ON COLUMN panels.panel_code IS 'Human-readable panel reference code.';
COMMENT ON COLUMN panels.department IS 'Department governing the panel evaluators.';
COMMENT ON COLUMN panels.max_daily_slots IS 'Maximum daily interview slots panel can conduct (must be > 0).';

-- ------------------------------------------------------------------------------
-- 7. Table: interview_slots (Capacity & Scheduling Engine)
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS interview_slots (
    slot_id VARCHAR(50) PRIMARY KEY,
    company_id VARCHAR(50) NOT NULL REFERENCES companies(company_id) ON DELETE CASCADE,
    room_id VARCHAR(50) NOT NULL REFERENCES rooms(room_id) ON DELETE RESTRICT,
    panel_id VARCHAR(50) NOT NULL REFERENCES panels(panel_id) ON DELETE RESTRICT,
    hiring_day VARCHAR(50) NOT NULL,
    slot_start_time TIMESTAMPTZ NOT NULL,
    slot_end_time TIMESTAMPTZ NOT NULL,
    slot_status VARCHAR(50) NOT NULL DEFAULT 'Available',
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_slots_time_order CHECK (slot_end_time > slot_start_time),
    CONSTRAINT chk_slots_status CHECK (slot_status IN ('Available', 'Booked', 'Completed', 'Cancelled'))
);

COMMENT ON TABLE interview_slots IS 'Decoupled capacity table modeling scheduling time blocks, room allocations, panel workload, and booking statuses.';
COMMENT ON COLUMN interview_slots.slot_id IS 'Unique interview slot primary key identifier (e.g., SLT-9001).';
COMMENT ON COLUMN interview_slots.company_id IS 'Foreign key referencing the hosting company.';
COMMENT ON COLUMN interview_slots.room_id IS 'Foreign key referencing the allocated room resource.';
COMMENT ON COLUMN interview_slots.panel_id IS 'Foreign key referencing the assigned evaluator panel.';
COMMENT ON COLUMN interview_slots.hiring_day IS 'Placement drive day designation (e.g., Day 1, Day 2).';
COMMENT ON COLUMN interview_slots.slot_start_time IS 'Scheduled start timestamp of the slot.';
COMMENT ON COLUMN interview_slots.slot_end_time IS 'Scheduled end timestamp of the slot (must be > start time).';
COMMENT ON COLUMN interview_slots.slot_status IS 'State of slot booking (Available, Booked, Completed, Cancelled).';
COMMENT ON COLUMN interview_slots.created_at IS 'Record creation timestamp.';

-- ==============================================================================
-- INDEX DEFINITIONS FOR HIGH-PERFORMANCE ANALYTICS
-- ==============================================================================

-- Candidates Indexes
CREATE INDEX IF NOT EXISTS idx_candidates_email ON candidates(email);
CREATE INDEX IF NOT EXISTS idx_candidates_major ON candidates(academic_major);

-- Applications Indexes
CREATE INDEX IF NOT EXISTS idx_applications_candidate ON applications(candidate_id);
CREATE INDEX IF NOT EXISTS idx_applications_company ON applications(company_id);
CREATE INDEX IF NOT EXISTS idx_applications_status ON applications(overall_status);

-- Recruitment Stage Records Indexes (Funnel Analysis & SLA Alerts)
CREATE INDEX IF NOT EXISTS idx_stage_records_app ON recruitment_stage_records(application_id);
CREATE INDEX IF NOT EXISTS idx_stage_records_app_seq ON recruitment_stage_records(application_id, sequence_order);
CREATE INDEX IF NOT EXISTS idx_stage_records_sla ON recruitment_stage_records(sla_breached_flag) WHERE sla_breached_flag = TRUE;

-- Interview Slots Indexes (Capacity & Schedule Overlap Checks)
CREATE INDEX IF NOT EXISTS idx_slots_company ON interview_slots(company_id);
CREATE INDEX IF NOT EXISTS idx_slots_room_time ON interview_slots(room_id, slot_start_time, slot_end_time);
CREATE INDEX IF NOT EXISTS idx_slots_panel_time ON interview_slots(panel_id, slot_start_time, slot_end_time);
CREATE INDEX IF NOT EXISTS idx_slots_status ON interview_slots(slot_status);
