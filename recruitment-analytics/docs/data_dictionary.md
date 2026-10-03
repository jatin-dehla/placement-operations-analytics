# Data Dictionary

## 1. Entity: `campuses`

| Column Name | Data Type | Nullable | Primary/Foreign Key | Description |
| :--- | :--- | :--- | :--- | :--- |
| `campus_id` | VARCHAR(50) | No | Primary Key | Unique campus identifier (e.g. `CMP-001`) |
| `campus_name` | VARCHAR(255) | No | None | Official name of the university/institution |
| `tier` | ENUM | No | None | University tier classification (`Tier 1`, `Tier 2`, `Tier 3`) |
| `region` | VARCHAR(100) | No | None | Geographic region (e.g. `North`, `West`, `South`) |
| `created_at` | TIMESTAMPTZ | No | None | Record creation timestamp |

---

## 2. Entity: `candidates`

| Column Name | Data Type | Nullable | Primary/Foreign Key | Description |
| :--- | :--- | :--- | :--- | :--- |
| `candidate_id` | VARCHAR(50) | No | Primary Key | Unique candidate identifier (e.g. `CND-1001`) |
| `full_name` | VARCHAR(255) | No | None | Full legal name of applicant |
| `email` | VARCHAR(255) | No | None | Contact email address |
| `gpa` | NUMERIC(3,2) | Yes | None | Graduation GPA / CGPA score |
| `degree` | VARCHAR(100) | Yes | None | Degree program (e.g. B.Tech, M.S.) |
| `major` | VARCHAR(100) | Yes | None | Academic major (e.g. Computer Science) |
| `created_at` | TIMESTAMPTZ | No | None | Record creation timestamp |

---

## 3. Entity: `applications`

| Column Name | Data Type | Nullable | Primary/Foreign Key | Description |
| :--- | :--- | :--- | :--- | :--- |
| `application_id`| VARCHAR(50) | No | Primary Key | Unique application record ID |
| `candidate_id` | VARCHAR(50) | No | Foreign Key (`candidates.candidate_id`) | Associated candidate ID |
| `campus_id` | VARCHAR(50) | No | Foreign Key (`campuses.campus_id`) | Campus drive location |
| `recruiter_id` | VARCHAR(50) | Yes | Foreign Key (`recruiters.recruiter_id`) | Lead recruiter assigned |
| `applied_role` | VARCHAR(100) | No | None | Job role applied for |
| `current_stage` | ENUM | No | None | Current funnel status |
| `application_date`| DATE | No | None | Date of initial application submission |

---

## 4. Entity: `stage_evaluations`

| Column Name | Data Type | Nullable | Primary/Foreign Key | Description |
| :--- | :--- | :--- | :--- | :--- |
| `evaluation_id` | VARCHAR(50) | No | Primary Key | Unique stage evaluation record ID |
| `application_id`| VARCHAR(50) | No | Foreign Key (`applications.application_id`)| Associated application ID |
| `stage_name` | ENUM | No | None | Pipeline stage evaluated |
| `evaluator_id` | VARCHAR(50) | Yes | Foreign Key (`interviewers.interviewer_id`)| Assigned evaluator / interviewer |
| `stage_entry_time`| TIMESTAMPTZ| No | None | Timestamp when candidate entered stage |
| `stage_exit_time` | TIMESTAMPTZ| Yes | None | Timestamp when evaluation was completed |
| `status` | VARCHAR(50) | No | None | Outcome: `Passed`, `Failed`, `Pending` |
| `score` | NUMERIC(5,2)| Yes | None | Evaluation numerical score |
