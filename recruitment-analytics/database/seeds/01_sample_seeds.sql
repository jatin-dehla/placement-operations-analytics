-- ==============================================================================
-- Recruitment Funnel & Capacity Analytics Platform
-- Seed Data Placeholder: 01_sample_seeds.sql
-- Uses strictly approved 7 entities
-- ==============================================================================

-- 1. Recruitment Stages Master Seeds
INSERT INTO recruitment_stages (stage_id, stage_name, sequence_order, target_sla_hours, is_interview_stage) VALUES
('STG-01', 'Sourcing', 1, 24, FALSE),
('STG-02', 'Resume Screening', 2, 48, FALSE),
('STG-03', 'Online Assessment', 3, 72, FALSE),
('STG-04', 'Technical Interview 1', 4, 48, TRUE),
('STG-05', 'Technical Interview 2', 5, 48, TRUE),
('STG-06', 'HR Interview', 6, 24, TRUE),
('STG-07', 'Offer Extended', 7, 72, FALSE),
('STG-08', 'Joined', 8, 0, FALSE)
ON CONFLICT (stage_id) DO NOTHING;

-- 2. Sample Companies
INSERT INTO companies (company_id, company_name, industry_sector, priority_tier, contact_email) VALUES
('CMP-101', 'Acme Cloud Systems', 'Enterprise Software', 'Tier 1 (Dream Partner)', 'campus@acmecloud.com'),
('CMP-102', 'FinTech Analytics Corp', 'Financial Technology', 'Tier 1 (Dream Partner)', 'recruiting@fintech.com'),
('CMP-103', 'NexGen Cyber Security', 'Cybersecurity', 'Tier 2 (Super Dream Partner)', 'careers@nexgen.io')
ON CONFLICT (company_id) DO NOTHING;

-- 3. Sample Rooms
INSERT INTO rooms (room_id, room_name, building_location, interview_mode, seating_capacity) VALUES
('RM-101', 'Complex Room A', 'Student Activity Center', 'In-Person', 4),
('RM-102', 'Complex Room B', 'Student Activity Center', 'In-Person', 4),
('RM-V01', 'Virtual Desk 1 (Zoom)', 'Online Portal', 'Virtual', 2)
ON CONFLICT (room_id) DO NOTHING;

-- 4. Sample Panels
INSERT INTO panels (panel_id, panel_code, department, max_daily_slots) VALUES
('PNL-SWE-01', 'SWE-TechPanel-A', 'Software Engineering', 8),
('PNL-SWE-02', 'SWE-TechPanel-B', 'Software Engineering', 8),
('PNL-DS-01', 'DS-Panel-Alpha', 'Data Science & Analytics', 6)
ON CONFLICT (panel_id) DO NOTHING;

-- 5. Sample Candidates
INSERT INTO candidates (candidate_id, full_name, email, phone_number, degree_program, academic_major, gpa, cgpa_band, graduation_year, gender) VALUES
('CND-1001', 'Ananya Sharma', 'ananya.s@university.edu', '+91-9876543210', 'B.Tech', 'Computer Science & Eng', 8.75, 'High Distinction (8.50 - 10.00)', 2026, 'Female'),
('CND-1002', 'Rohan Verma', 'rohan.v@university.edu', '+91-9876543211', 'B.Tech', 'Data Science', 7.80, 'First Class (7.00 - 8.49)', 2026, 'Male')
ON CONFLICT (candidate_id) DO NOTHING;

-- 6. Sample Applications
INSERT INTO applications (application_id, candidate_id, company_id, current_stage_id, applied_role, overall_status, application_date) VALUES
('APP-5001', 'CND-1001', 'CMP-101', 'STG-04', 'Software Development Engineer (SDE-1)', 'Active', '2026-02-01'),
('APP-5002', 'CND-1002', 'CMP-102', 'STG-03', 'Data Scientist Intern', 'Active', '2026-02-01')
ON CONFLICT (application_id) DO NOTHING;

-- 7. Sample Interview Slots
INSERT INTO interview_slots (slot_id, application_id, company_id, stage_id, room_id, panel_id, hiring_day, slot_start_time, slot_end_time, slot_status, score) VALUES
('SLT-9001', 'APP-5001', 'CMP-101', 'STG-04', 'RM-101', 'PNL-SWE-01', 'Day 1', '2026-02-02 10:00:00+05:30', '2026-02-02 10:45:00+05:30', 'Booked', 85.00)
ON CONFLICT (slot_id) DO NOTHING;
