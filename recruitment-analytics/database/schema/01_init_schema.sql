-- ==============================================================================
-- Recruitment Funnel & Capacity Analytics Platform
-- Schema Definition: 01_init_schema.sql
-- Approved Entities (7): candidates, companies, applications, recruitment_stages,
--                       interview_slots, rooms, panels
-- Engine: PostgreSQL 13+
-- ==============================================================================

-- 1. Candidates Entity
CREATE TABLE IF NOT EXISTS candidates (
    candidate_id VARCHAR(50) PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone_number VARCHAR(20),
    degree_program VARCHAR(100) NOT NULL,
    academic_major VARCHAR(100) NOT NULL,
    gpa NUMERIC(4, 2) NOT NULL,
    cgpa_band VARCHAR(50) NOT NULL,
    graduation_year INT NOT NULL,
    gender VARCHAR(20),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. Companies Entity
CREATE TABLE IF NOT EXISTS companies (
    company_id VARCHAR(50) PRIMARY KEY,
    company_name VARCHAR(255) NOT NULL,
    industry_sector VARCHAR(100) NOT NULL,
    priority_tier VARCHAR(50) NOT NULL,
    contact_email VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3. Recruitment Stages Entity
CREATE TABLE IF NOT EXISTS recruitment_stages (
    stage_id VARCHAR(50) PRIMARY KEY,
    stage_name VARCHAR(100) NOT NULL,
    sequence_order INT NOT NULL UNIQUE,
    target_sla_hours INT NOT NULL,
    is_interview_stage BOOLEAN DEFAULT TRUE
);

-- 4. Rooms Entity
CREATE TABLE IF NOT EXISTS rooms (
    room_id VARCHAR(50) PRIMARY KEY,
    room_name VARCHAR(255) NOT NULL,
    building_location VARCHAR(100),
    interview_mode VARCHAR(50) NOT NULL,
    seating_capacity INT NOT NULL
);

-- 5. Panels Entity
CREATE TABLE IF NOT EXISTS panels (
    panel_id VARCHAR(50) PRIMARY KEY,
    panel_code VARCHAR(100) NOT NULL UNIQUE,
    department VARCHAR(100) NOT NULL,
    max_daily_slots INT NOT NULL DEFAULT 8
);

-- 6. Applications Entity
CREATE TABLE IF NOT EXISTS applications (
    application_id VARCHAR(50) PRIMARY KEY,
    candidate_id VARCHAR(50) NOT NULL REFERENCES candidates(candidate_id) ON DELETE CASCADE,
    company_id VARCHAR(50) NOT NULL REFERENCES companies(company_id) ON DELETE CASCADE,
    current_stage_id VARCHAR(50) NOT NULL REFERENCES recruitment_stages(stage_id),
    applied_role VARCHAR(100) NOT NULL,
    overall_status VARCHAR(50) NOT NULL DEFAULT 'Active',
    application_date DATE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 7. Interview Slots Entity
CREATE TABLE IF NOT EXISTS interview_slots (
    slot_id VARCHAR(50) PRIMARY KEY,
    application_id VARCHAR(50) REFERENCES applications(application_id) ON DELETE SET NULL,
    company_id VARCHAR(50) NOT NULL REFERENCES companies(company_id) ON DELETE CASCADE,
    stage_id VARCHAR(50) NOT NULL REFERENCES recruitment_stages(stage_id),
    room_id VARCHAR(50) NOT NULL REFERENCES rooms(room_id),
    panel_id VARCHAR(50) NOT NULL REFERENCES panels(panel_id),
    hiring_day VARCHAR(50) NOT NULL,
    slot_start_time TIMESTAMP WITH TIME ZONE NOT NULL,
    slot_end_time TIMESTAMP WITH TIME ZONE NOT NULL,
    slot_status VARCHAR(50) NOT NULL DEFAULT 'Available',
    stage_entry_time TIMESTAMP WITH TIME ZONE,
    stage_exit_time TIMESTAMP WITH TIME ZONE,
    score NUMERIC(5, 2),
    sla_breached_flag BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_slot_time CHECK (slot_end_time > slot_start_time)
);

-- Analytics Performance Indexes
CREATE INDEX IF NOT EXISTS idx_applications_candidate ON applications(candidate_id);
CREATE INDEX IF NOT EXISTS idx_applications_company ON applications(company_id);
CREATE INDEX IF NOT EXISTS idx_applications_stage ON applications(current_stage_id);
CREATE INDEX IF NOT EXISTS idx_slots_room_time ON interview_slots(room_id, slot_start_time, slot_end_time);
CREATE INDEX IF NOT EXISTS idx_slots_panel_time ON interview_slots(panel_id, slot_start_time, slot_end_time);
CREATE INDEX IF NOT EXISTS idx_slots_company_stage ON interview_slots(company_id, stage_id);
