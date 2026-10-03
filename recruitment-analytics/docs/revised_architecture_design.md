# Architecture Review & Revised Table Design Specification

# Recruitment Funnel & Capacity Analytics Platform

**Document Version:** 3.0.0 (Decoupled Funnel & Capacity Model)  
**Author:** Senior Data Architect  
**Target Repository:** `recruitment-analytics/docs/revised_architecture_design.md`  

---

## 1. Architectural Realignment Principles

To separate concerns cleanly between **Funnel Progression Tracking** and **Capacity Scheduling**, the platform architecture is re-aligned around four fundamental architectural principles:

1. **`recruitment_stage_records` represents funnel progression:** Every stage transition an application undergoes (from Sourcing to Joining) is recorded as a discrete event log.
2. **`interview_slots` represents capacity & scheduling only:** Time blocks, room bookings, panel allocations, and slot statuses are managed independently of evaluation outcomes.
3. **Funnel & Process Analytics are derived from `recruitment_stage_records`:** Conversion pass rates, stage turnaround times (TAT), and SLA breaches are computed exclusively from stage transition logs.
4. **Capacity Analytics are derived from `interview_slots`:** Panel daily utilization, room occupancy rates, and slot deficit forecasts are computed exclusively from scheduling slots.

---

## 2. Table Specifications

### 2.1 Table 1: `candidates`
* **Purpose:** Stores student/applicant master records and academic achievements.
* **Primary Key:** `candidate_id`
* **Foreign Keys:** *None*
* **Columns:** `candidate_id`, `full_name`, `email`, `phone_number`, `degree_program`, `academic_major`, `gpa`, `cgpa_band`, `graduation_year`, `gender`, `created_at`.

---

### 2.2 Table 2: `companies`
* **Purpose:** Master repository of hiring partner organizations.
* **Primary Key:** `company_id`
* **Foreign Keys:** *None*
* **Columns:** `company_id`, `company_name`, `industry_sector`, `priority_tier`, `contact_email`, `created_at`.

---

### 2.3 Table 3: `recruitment_stages`
* **Purpose:** Master reference dictionary defining standardized pipeline stages and target SLA limits.
* **Primary Key:** `stage_id`
* **Foreign Keys:** *None*
* **Columns:** `stage_id`, `stage_name`, `sequence_order`, `target_sla_hours`, `is_interview_stage`.

---

### 2.4 Table 4: `rooms`
* **Purpose:** Venue resource master table for physical desks and virtual conference links.
* **Primary Key:** `room_id`
* **Foreign Keys:** *None*
* **Columns:** `room_id`, `room_name`, `building_location`, `interview_mode`, `seating_capacity`.

---

### 2.5 Table 5: `panels`
* **Purpose:** Evaluator panel master table for department interviewing teams.
* **Primary Key:** `panel_id`
* **Foreign Keys:** *None*
* **Columns:** `panel_id`, `panel_code`, `department`, `max_daily_slots`.

---

### 2.6 Table 6: `applications`
* **Purpose:** Core application record linking a candidate to a target company and active stage.
* **Primary Key:** `application_id`
* **Foreign Keys:**
  - `candidate_id` $\rightarrow$ `candidates(candidate_id)`
  - `company_id` $\rightarrow$ `companies(company_id)`
  - `current_stage_id` $\rightarrow$ `recruitment_stages(stage_id)`
* **Columns:** `application_id`, `candidate_id`, `company_id`, `current_stage_id`, `applied_role`, `overall_status`, `application_date`, `updated_at`.

---

### 2.7 Table 7: `recruitment_stage_records` (Funnel Engine)
* **Purpose:** Stores actual stage progression events, entry/exit timestamps, scores, and SLA breach flags.
* **Primary Key:** `stage_record_id`
* **Foreign Keys:**
  - `application_id` $\rightarrow$ `applications(application_id)`
  - `stage_id` $\rightarrow$ `recruitment_stages(stage_id)`
* **Columns:** `stage_record_id`, `application_id`, `stage_id`, `stage_entry_time`, `stage_exit_time`, `stage_status` (*Passed*, *Failed*, *Pending*, *Withdrawn*), `evaluation_score`, `sla_breached_flag`, `created_at`.

---

### 2.8 Table 8: `interview_slots` (Capacity & Scheduling Engine)
* **Purpose:** Stores discrete interview time blocks, room allocations, panel assignments, and scheduling statuses.
* **Primary Key:** `slot_id`
* **Foreign Keys:**
  - `company_id` $\rightarrow$ `companies(company_id)`
  - `stage_id` $\rightarrow$ `recruitment_stages(stage_id)`
  - `room_id` $\rightarrow$ `rooms(room_id)`
  - `panel_id` $\rightarrow$ `panels(panel_id)`
  - `stage_record_id` $\rightarrow$ `recruitment_stage_records(stage_record_id)` *(Optional FK when slot is booked for an evaluation)*
* **Columns:** `slot_id`, `company_id`, `stage_id`, `room_id`, `panel_id`, `stage_record_id`, `hiring_day`, `slot_start_time`, `slot_end_time`, `slot_status` (*Available*, *Booked*, *Completed*, *Cancelled*), `created_at`.

---

## 3. Entity Responsibility Mapping

```text
+-----------------------------------------------------------------------------------+
|                                 APPLICATIONS                                      |
+-----------------------------------------------------------------------------------+
                                         │
        ┌────────────────────────────────┴────────────────────────────────┐
        ▼                                                                 ▼
+---------------------------------------+               +---------------------------------------+
|      RECRUITMENT_STAGE_RECORDS        |               |            INTERVIEW_SLOTS            |
|   (Funnel & Process Efficiency)       |               |        (Capacity & Scheduling)        |
+---------------------------------------+               +---------------------------------------+
| - Stage progression history           |               | - Time block start / end              |
| - Stage entry & exit timestamps       |               | - Room allocation                     |
| - Evaluation score & outcome          |  ◄─────────── | - Panel allocation                    |
| - SLA breach calculation              |  (Optional FK)| - Slot booking status                 |
+---------------------------------------+               +---------------------------------------+
```

---

## 4. KPI Derivation Framework

### 4.1 Funnel KPIs (Derived from `recruitment_stage_records` & `applications`)

1. **Stage Conversion Rate (SCR %):**
   - **Source Tables:** `recruitment_stage_records`
   - **Derivation Logic:** For stage $S_i$, count records where `stage_status = 'Passed'` divided by total records entering stage $S_i$.
   - **Formula:** $$\text{SCR}_{S_i} = \frac{\text{COUNT}(\text{stage\_record\_id WHERE stage\_status = 'Passed' AND stage\_id} = S_i)}{\text{COUNT}(\text{stage\_record\_id WHERE stage\_id} = S_i)} \times 100$$

2. **Overall Funnel Yield (OFY %):**
   - **Source Tables:** `applications` & `recruitment_stage_records`
   - **Derivation Logic:** Count applications with `overall_status = 'Hired'` divided by total initial `applications`.
   - **Formula:** $$\text{OFY} = \frac{\text{COUNT}(\text{application\_id WHERE overall\_status = 'Hired'})}{\text{COUNT}(\text{application\_id})} \times 100$$

3. **Offer Acceptance Rate (OAR %):**
   - **Source Tables:** `recruitment_stage_records`
   - **Derivation Logic:** Count stage records where `stage_id = 'STG-08' (Joined)` divided by stage records where `stage_id = 'STG-07' (Offer Extended)`.
   - **Formula:** $$\text{OAR} = \frac{\text{COUNT}(\text{stage\_record\_id WHERE stage\_id = 'STG-08'})}{\text{COUNT}(\text{stage\_record\_id WHERE stage\_id = 'STG-07'})} \times 100$$

---

### 4.2 Capacity KPIs (Derived from `interview_slots`, `panels`, & `rooms`)

4. **Panel Capacity Utilization (%):**
   - **Source Tables:** `interview_slots` & `panels`
   - **Derivation Logic:** Count booked/completed slots for a panel on a given day divided by `panels.max_daily_slots`.
   - **Formula:** $$\text{Panel Utilization} = \frac{\text{COUNT}(\text{slot\_id WHERE slot\_status IN ('Booked','Completed') AND panel\_id} = P_k)}{\text{panels.max\_daily\_slots}} \times 100$$

5. **Room Occupancy Ratio (%):**
   - **Source Tables:** `interview_slots` & `rooms`
   - **Derivation Logic:** Total hours of booked slots for room $R_m$ divided by total operating hours available in the drive schedule.
   - **Formula:** $$\text{Room Occupancy} = \frac{\sum (\text{slot\_end\_time} - \text{slot\_start\_time})_{\text{Booked}}}{\text{Total Available Operating Hours}} \times 100$$

---

### 4.3 Process Efficiency KPIs (Derived from `recruitment_stage_records` & `recruitment_stages`)

6. **Stage Turnaround Time (TAT in Hours):**
   - **Source Tables:** `recruitment_stage_records`
   - **Derivation Logic:** Difference between `stage_exit_time` and `stage_entry_time` averaged per stage.
   - **Formula:** $$\text{TAT}_{S_i} = \text{AVG}\left( \text{stage\_exit\_time} - \text{stage\_entry\_time} \right) \quad \text{for stage } S_i$$

7. **SLA Breach Rate (%):**
   - **Source Tables:** `recruitment_stage_records`
   - **Derivation Logic:** Count stage records where `sla_breached_flag = TRUE` divided by total completed stage records.
   - **Formula:** $$\text{SLA Breach Rate}_{S_i} = \frac{\text{COUNT}(\text{stage\_record\_id WHERE sla\_breached\_flag = TRUE AND stage\_id} = S_i)}{\text{COUNT}(\text{stage\_record\_id WHERE stage\_exit\_time IS NOT NULL AND stage\_id} = S_i)} \times 100$$

---

### 4.4 Company KPIs (Derived from `companies` & `applications`)

8. **Company Target Fulfillment Rate (%):**
   - **Source Tables:** `applications` & `companies`
   - **Derivation Logic:** Count applications with `overall_status = 'Hired'` for company $C_j$ divided by company hiring quota target.
