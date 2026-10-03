# Data Dictionary & Business Rules Specification

# Recruitment Funnel & Capacity Analytics Platform

**Document Version:** 2.0.0 (Updated Baseline)  
**Author:** Senior Data Architect  
**Target Repository:** `recruitment-analytics/docs/data_dictionary_and_business_rules.md`  

---

## 1. Approved Scope & Entities

Per the approved architecture correction, the platform uses **EXCLUSIVELY** the following 7 entities:

1. **`candidates`**
2. **`companies`**
3. **`applications`**
4. **`recruitment_stages`**
5. **`interview_slots`**
6. **`rooms`**
7. **`panels`**

---

## 2. Scale Assumptions

- **Candidates:** 1,000 – 1,500
- **Companies:** 150 – 300
- **Applications:** 4,000 – 8,000
- **Recruitment Stage Records (Slots):** 20,000 – 60,000

---

## 3. Data Dictionary

### 3.1 `candidates`
* **Purpose:** Stores student/applicant master records.
* **Primary Key:** `candidate_id`

| Column Name | Data Type | Nullable (Y/N) | Description | Example Value |
| :--- | :--- | :---: | :--- | :--- |
| `candidate_id` | VARCHAR(50) | N | Unique candidate identifier | `CND-1001` |
| `full_name` | VARCHAR(255) | N | Candidate's legal name | `Ananya Sharma` |
| `email` | VARCHAR(255) | N | Unique email address | `ananya.s@university.edu` |
| `phone_number` | VARCHAR(20) | Y | Phone number | `+91-9876543210` |
| `degree_program` | VARCHAR(100) | N | Degree (e.g. B.Tech) | `B.Tech` |
| `academic_major` | VARCHAR(100) | N | Major/branch | `Computer Science` |
| `gpa` | NUMERIC(4,2) | N | CGPA score (0.00-10.00) | `8.75` |
| `cgpa_band` | VARCHAR(50) | N | Performance band | `High Distinction` |
| `graduation_year` | INTEGER | N | Graduation year | `2026` |
| `gender` | VARCHAR(20) | Y | Gender identity | `Female` |
| `created_at` | TIMESTAMPTZ | N | Record creation timestamp | `2026-01-10 09:30:00+05:30` |

---

### 3.2 `companies`
* **Purpose:** Master list of hiring partner organizations.
* **Primary Key:** `company_id`

| Column Name | Data Type | Nullable (Y/N) | Description | Example Value |
| :--- | :--- | :---: | :--- | :--- |
| `company_id` | VARCHAR(50) | N | Unique company ID | `CMP-101` |
| `company_name` | VARCHAR(255) | N | Corporate name | `Acme Cloud Systems` |
| `industry_sector` | VARCHAR(100) | N | Sector classification | `Enterprise Software` |
| `priority_tier` | VARCHAR(50) | N | Corporate priority tier | `Tier 1 (Dream Partner)` |
| `contact_email` | VARCHAR(255) | N | HR email address | `campus@acmecloud.com` |
| `created_at` | TIMESTAMPTZ | N | Creation timestamp | `2025-11-01 10:00:00+05:30` |

---

### 3.3 `recruitment_stages`
* **Purpose:** Pipeline stage dictionary defining sequence order and SLA hours.
* **Primary Key:** `stage_id`

| Column Name | Data Type | Nullable (Y/N) | Description | Example Value |
| :--- | :--- | :---: | :--- | :--- |
| `stage_id` | VARCHAR(50) | N | Unique stage ID | `STG-04` |
| `stage_name` | VARCHAR(100) | N | Stage name | `Technical Interview 1` |
| `sequence_order` | INTEGER | N | Pipeline order (1-8) | `4` |
| `target_sla_hours` | INTEGER | N | Target completion SLA hours | `48` |
| `is_interview_stage` | BOOLEAN | N | Requires room/panel slot flag | `TRUE` |

---

### 3.4 `rooms`
* **Purpose:** Physical interview desks or virtual conference resources.
* **Primary Key:** `room_id`

| Column Name | Data Type | Nullable (Y/N) | Description | Example Value |
| :--- | :--- | :---: | :--- | :--- |
| `room_id` | VARCHAR(50) | N | Unique room resource ID | `RM-101` |
| `room_name` | VARCHAR(255) | N | Room name/number | `Complex Room A` |
| `building_location` | VARCHAR(100) | Y | Building or URL | `Student Activity Center` |
| `interview_mode` | VARCHAR(50) | N | Mode (*In-Person*, *Virtual*) | `In-Person` |
| `seating_capacity` | INTEGER | N | Max capacity | `4` |

---

### 3.5 `panels`
* **Purpose:** Evaluator panels assigned to conduct interview slots.
* **Primary Key:** `panel_id`

| Column Name | Data Type | Nullable (Y/N) | Description | Example Value |
| :--- | :--- | :---: | :--- | :--- |
| `panel_id` | VARCHAR(50) | N | Unique panel ID | `PNL-SWE-01` |
| `panel_code` | VARCHAR(100) | N | Panel code | `SWE-TechPanel-A` |
| `department` | VARCHAR(100) | N | Department | `Software Engineering` |
| `max_daily_slots` | INTEGER | N | Max daily slot cap | `8` |

---

### 3.6 `applications`
* **Purpose:** Represents candidate job application to a company.
* **Primary Key:** `application_id`

| Column Name | Data Type | Nullable (Y/N) | Description | Example Value |
| :--- | :--- | :---: | :--- | :--- |
| `application_id` | VARCHAR(50) | N | Unique application ID | `APP-5001` |
| `candidate_id` | VARCHAR(50) | N | FK to `candidates` | `CND-1001` |
| `company_id` | VARCHAR(50) | N | FK to `companies` | `CMP-101` |
| `current_stage_id` | VARCHAR(50) | N | FK to `recruitment_stages` | `STG-04` |
| `applied_role` | VARCHAR(100) | N | Applied job role | `SDE-1` |
| `overall_status` | VARCHAR(50) | N | Status (*Active*, *Hired*, *Rejected*) | `Active` |
| `application_date` | DATE | N | Date submitted | `2026-02-01` |

---

### 3.7 `interview_slots`
* **Purpose:** Scheduled evaluation time blocks storing evaluation outcomes and SLA metrics.
* **Primary Key:** `slot_id`

| Column Name | Data Type | Nullable (Y/N) | Description | Example Value |
| :--- | :--- | :---: | :--- | :--- |
| `slot_id` | VARCHAR(50) | N | Unique slot ID | `SLT-9001` |
| `application_id` | VARCHAR(50) | Y | FK to `applications` | `APP-5001` |
| `company_id` | VARCHAR(50) | N | FK to `companies` | `CMP-101` |
| `stage_id` | VARCHAR(50) | N | FK to `recruitment_stages` | `STG-04` |
| `room_id` | VARCHAR(50) | N | FK to `rooms` | `RM-101` |
| `panel_id` | VARCHAR(50) | N | FK to `panels` | `PNL-SWE-01` |
| `hiring_day` | VARCHAR(50) | N | Hiring day | `Day 1` |
| `slot_start_time` | TIMESTAMPTZ | N | Start time | `2026-02-02 10:00:00+05:30` |
| `slot_end_time` | TIMESTAMPTZ | N | End time | `2026-02-02 10:45:00+05:30` |
| `slot_status` | VARCHAR(50) | N | Status (*Available*, *Booked*, *Completed*)| `Booked` |
| `stage_entry_time` | TIMESTAMPTZ | Y | Stage entry time | `2026-02-01 14:00:00+05:30` |
| `stage_exit_time` | TIMESTAMPTZ | Y | Stage completion time | `2026-02-02 11:00:00+05:30` |
| `score` | NUMERIC(5,2) | Y | Evaluation score (0-100) | `85.00` |
| `sla_breached_flag` | BOOLEAN | N | SLA breach flag | `FALSE` |

---

## 4. Business Rules & Constraints

1. **Chronological Validity:** For every `interview_slots` record, `slot_end_time` MUST be strictly greater than `slot_start_time`.
2. **Room Overlap Constraint:** A single `room_id` CANNOT host multiple interview slots with overlapping time ranges.
3. **Panel Overlap Constraint:** A single `panel_id` CANNOT conduct multiple interview slots with overlapping time ranges.
4. **Daily Panel Workload Cap:** Daily booked slots per panel MUST NOT exceed `panels.max_daily_slots`.
5. **Stage SLA Violation:** If $(\text{stage\_exit\_time} - \text{stage\_entry\_time}) > \text{target\_sla\_hours}$, `sla_breached_flag` MUST be evaluated to `TRUE`.
