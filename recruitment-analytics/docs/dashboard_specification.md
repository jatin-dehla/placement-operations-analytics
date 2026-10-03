# Power BI Dashboard Blueprint Specification

# Recruitment Funnel & Capacity Analytics Platform

**Document Version:** 1.0.0  
**Author:** Senior BI Architect  
**Target Repository:** `recruitment-analytics/docs/dashboard_specification.md`  
**Target Platform:** Power BI Desktop / Power BI Service  

---

## 1. Executive Summary & Design System

This document specifies the complete Power BI dashboard architecture for the **Recruitment Funnel & Capacity Analytics Platform**. It details the visual layouts, underlying DAX measures, data source table mappings, user drill-down paths, and decision support capabilities across 4 interactive pages.

```text
[ Page 1: Executive Overview ] ──► [ Page 2: Funnel Analytics ] ──► [ Page 3: Capacity & Scheduling ] ──► [ Page 4: Recommendations & Actions ]
```

### 🎨 Visual Theme & Color Palette Guidelines
The dashboard follows an enterprise dark-mode glassmorphism theme engineered for executive cockpits:

| Element | Color Name | Hex Code | HSL Value | Usage |
| :--- | :--- | :--- | :--- | :--- |
| **Canvas Background** | Deep Slate Dark | `#0F172A` | `hsl(222, 47%, 11%)` | Primary page background |
| **Card / Visual Container** | Slate Glass Layer | `#1E293B` | `hsl(215, 28%, 17%)` | Chart & KPI card containers |
| **Primary Accent** | Electric Indigo | `#6366F1` | `hsl(239, 84%, 67%)` | Header bars, active tab indicators |
| **Success / Passed** | Emerald Green | `#10B981` | `hsl(160, 84%, 39%)` | Hired status, SLA compliant, Passed |
| **Warning Alert** | Amber Gold | `#F59E0B` | `hsl(38, 92%, 50%)` | Moderate SLA breach, Panel load 75-85% |
| **Critical Alert** | Coral Red | `#EF4444` | `hsl(0, 84%, 60%)` | Critical SLA breach, Panel overload >85% |
| **Informational** | Cyan Blue | `#3B82F6` | `hsl(217, 91%, 60%)` | Info logs, general metrics |

---

## 2. Core DAX Measure Dictionary

The following DAX measures power the visual tiles across all 4 dashboard pages:

```dax
// 1. Total Applications
Total Applications = COUNTROWS(applications)

// 2. Unique Candidates
Total Applicants = DISTINCTCOUNT(applications[candidate_id])

// 3. Total Hired Applications
Total Hired = CALCULATE(COUNTROWS(applications), applications[overall_status] = "Hired")

// 4. Overall Funnel Yield %
Overall Funnel Yield % = 
DIVIDE([Total Hired], [Total Applications], 0) * 100

// 5. Offer Acceptance Rate (OAR %)
Offers Extended = CALCULATE(COUNTROWS(recruitment_stage_records), recruitment_stage_records[stage_name] = "Offer Extended")
Offers Accepted = CALCULATE(COUNTROWS(recruitment_stage_records), recruitment_stage_records[stage_name] = "Offer Extended" && recruitment_stage_records[stage_status] = "Passed")
Offer Acceptance Rate % = DIVIDE([Offers Accepted], [Offers Extended], 0) * 100

// 6. Average Stage Turnaround Time (Hours)
Avg Stage TAT Hours = 
AVERAGEX(
    FILTER(recruitment_stage_records, NOT(ISBLANK(recruitment_stage_records[stage_exit_time]))),
    DATEDIFF(recruitment_stage_records[stage_entry_time], recruitment_stage_records[stage_exit_time], HOUR)
)

// 7. SLA Breach Rate %
Total Completed Evaluations = CALCULATE(COUNTROWS(recruitment_stage_records), NOT(ISBLANK(recruitment_stage_records[stage_exit_time])))
SLA Breaches = CALCULATE(COUNTROWS(recruitment_stage_records), recruitment_stage_records[sla_breached_flag] = TRUE)
SLA Breach Rate % = DIVIDE([SLA Breaches], [Total Completed Evaluations], 0) * 100

// 8. Panel Capacity Utilization %
Booked Slots = CALCULATE(COUNTROWS(interview_slots), interview_slots[slot_status] IN {"Booked", "Completed"})
Total Daily Panel Capacity = SUM(panels[max_daily_slots]) * DISTINCTCOUNT(interview_slots[hiring_day])
Panel Utilization % = DIVIDE([Booked Slots], [Total Daily Panel Capacity], 0) * 100

// 9. Room Occupancy Rate %
Room Booked Slots = CALCULATE(COUNTROWS(interview_slots), interview_slots[slot_status] IN {"Booked", "Completed"})
Total Room Available Slots = COUNTROWS(interview_slots)
Room Occupancy Rate % = DIVIDE([Room Booked Slots], [Total Room Available Slots], 0) * 100
```

---

## 3. Page Specifications

---

### PAGE 1: EXECUTIVE OVERVIEW

#### 1. Business Objective
Provide C-level leadership and placement heads with immediate macro visibility into corporate drive fulfillment, overall funnel conversion yields, active SLA alerts, and hiring target performance.

#### 2. Layout Wireframe
```text
+---------------------------------------------------------------------------------------------------+
|  [SLICER: Company Sector]  [SLICER: Priority Tier]  [SLICER: Hiring Day]  [SLICER: Academic Major] |
+---------------------------------------------------------------------------------------------------+
|  [KPI CARD: Total Apps]  [KPI CARD: Hired Rate %]  [KPI CARD: OAR %]  [KPI CARD: SLA Breach Rate %] |
+--------------------------------------------------+------------------------------------------------+
|  VISUAL 1.1: Company Hiring Quota vs Hired       |  VISUAL 1.2: Overall Funnel Pass Ratios        |
|  (Grouped Bar Chart)                             |  (Funnel Chart)                                |
+--------------------------------------------------+------------------------------------------------+
|  VISUAL 1.3: Academic Major Hiring Yield         |  VISUAL 1.4: Corporate Priority Tier Yield     |
|  (Stacked Column Chart)                          |  (Donut Chart)                                 |
+---------------------------------------------------------------------------------------------------+
```

#### 3. Visual Element Specifications

##### Visual 1.1: Company Hiring Target vs. Actual Hired
* **Visual Type:** Grouped Horizontal Bar Chart
* **Purpose:** Compares target hiring quotas against actual hired candidate counts per company.
* **Data Sources:** `companies`, `applications`
* **SQL / DAX Metric:** `[Total Applications]`, `[Total Hired]`, `company_name`
* **Why It Exists:** Enables leadership to identify under-delivering company drives early.

##### Visual 1.2: Overall Pipeline Stage Progression
* **Visual Type:** Funnel Visual
* **Purpose:** Visualizes candidate volume decay across all 8 pipeline stages.
* **Data Sources:** `recruitment_stage_records`
* **SQL / DAX Metric:** `COUNT(stage_record_id)` grouped by `sequence_order` & `stage_name`
* **Why It Exists:** Pinpoints major top-of-funnel vs. bottom-of-funnel drop-offs.

##### Visual 1.3: Academic Major Hiring Yield
* **Visual Type:** Stacked Column Chart
* **Purpose:** Displays application volume and hired counts segmented by student academic major.
* **Data Sources:** `candidates`, `applications`
* **SQL / DAX Metric:** `[Total Applications]`, `[Total Hired]` by `academic_major`
* **Why It Exists:** Evaluates candidate quality and placement demand across engineering disciplines.

##### Visual 1.4: Corporate Priority Tier Yield
* **Visual Type:** Donut Chart
* **Purpose:** Shows candidate hiring distribution across Tier 1 Dream, Tier 2 Super Dream, and Tier 3 partners.
* **Data Sources:** `companies`, `applications`
* **SQL / DAX Metric:** `[Total Hired]` grouped by `priority_tier`
* **Why It Exists:** Validates institutional placement strategy and premium partner satisfaction.

#### 4. User Interactions & Decisions Supported
* **Interaction:** Clicking a company bar filters all visuals to that specific company's candidate cohort.
* **Decisions Supported:** Re-negotiating drive dates, allocating placement office support, extending drive schedules.

---

### PAGE 2: FUNNEL ANALYTICS

#### 1. Business Objective
Provide operational coordinators with deep diagnostic capabilities into stage-over-stage pass rates, evaluation scores, and pipeline leakage.

#### 2. Layout Wireframe
```text
+---------------------------------------------------------------------------------------------------+
|  [SLICER: Stage Name]      [SLICER: Company]        [SLICER: Degree Program]  [SLICER: CGPA Band]   |
+---------------------------------------------------------------------------------------------------+
|  [KPI CARD: Stage Entrants] [KPI CARD: Stage Pass %] [KPI CARD: Drop-off %] [KPI CARD: Avg Score] |
+--------------------------------------------------+------------------------------------------------+
|  VISUAL 2.1: Stage-over-Stage Pass Rate Matrix   |  VISUAL 2.2: Candidate Score Distribution      |
|  (Matrix Grid with Data Bars)                    |  (Histogram / Column Chart)                    |
+--------------------------------------------------+------------------------------------------------+
|  VISUAL 2.3: Stage Drop-off Failure Categorization                                               |
|  (Clustered Bar Chart by Company & Stage)                                                         |
+---------------------------------------------------------------------------------------------------+
```

#### 3. Visual Element Specifications

##### Visual 2.1: Stage Conversion Matrix
* **Visual Type:** Matrix Visual with conditional formatting data bars
* **Purpose:** Granular breakdown of stage entry count, pass count, fail count, and pass rate % by company and stage.
* **Data Sources:** `recruitment_stage_records`, `applications`, `companies`
* **SQL / DAX Metric:** `[Stage Entrants]`, `[Stage Pass %]`, `[Stage Fail %]`
* **Why It Exists:** Highlights anomalous pass rates (e.g. an unusually hard coding assessment).

##### Visual 2.2: Candidate Evaluation Score Distribution
* **Visual Type:** Column Chart (Histogram Bins)
* **Purpose:** Displays score frequency distributions (50-60, 60-70, 70-80, 80-90, 90-100).
* **Data Sources:** `recruitment_stage_records`
* **SQL / DAX Metric:** `COUNT(stage_record_id)` grouped by score bins
* **Why It Exists:** Helps calibrate passing threshold cutoffs dynamically.

##### Visual 2.3: Stage Drop-off Heatmap by Stage
* **Visual Type:** Clustered Bar Chart
* **Purpose:** Ranks stages by absolute candidate drop-off numbers.
* **Data Sources:** `recruitment_stage_records`
* **SQL / DAX Metric:** `COUNT(stage_record_id WHERE stage_status = 'Failed')`
* **Why It Exists:** Focuses intervention effort on the most leaky stage in the drive.

#### 4. User Interactions & Decisions Supported
* **Interaction:** Selecting an assessment stage filters the score distribution visual to show score spreads for that specific test.
* **Decisions Supported:** Lowering or raising assessment cutoff scores, recalibrating screening criteria.

---

### PAGE 3: CAPACITY & SCHEDULING

#### 1. Business Objective
Monitor venue room occupancy, evaluator panel workload utilization, and interview slot availability to eliminate operational scheduling bottlenecks.

#### 2. Layout Wireframe
```text
+---------------------------------------------------------------------------------------------------+
|  [SLICER: Hiring Day]     [SLICER: Department]      [SLICER: Interview Mode] [SLICER: Panel Code] |
+---------------------------------------------------------------------------------------------------+
|  [KPI CARD: Total Slots]   [KPI CARD: Booked Slots] [KPI CARD: Panel Util %] [KPI CARD: Room Occ %] |
+--------------------------------------------------+------------------------------------------------+
|  VISUAL 3.1: Panel Workload Utilization Gauges   |  VISUAL 3.2: Room Occupancy Heatmap            |
|  (Card Gauges / Bar Matrix)                      |  (Matrix by Room & Hiring Day)                 |
+--------------------------------------------------+------------------------------------------------+
|  VISUAL 3.3: Peak Hourly Interview Demand        |  VISUAL 3.4: Underutilized Resource List       |
|  (Line & Area Combo Chart by Time Window)        |  (Table Visual with Status Badges)             |
+---------------------------------------------------------------------------------------------------+
```

#### 3. Visual Element Specifications

##### Visual 3.1: Panel Workload Utilization
* **Visual Type:** Clustered Horizontal Bar Chart with 85% reference threshold line
* **Purpose:** Displays booked slot count vs. maximum daily slot capacity per evaluator panel.
* **Data Sources:** `panels`, `interview_slots`
* **SQL / DAX Metric:** `[Panel Utilization %]`, `max_daily_slots`
* **Why It Exists:** Flags overworked panels ($\ge 85\%$) needing immediate interviewer reassignment.

##### Visual 3.2: Room Occupancy Matrix
* **Visual Type:** Matrix Visual with Green-Yellow-Red conditional background formatting
* **Purpose:** Shows room slot occupancy percentages across Hiring Days (Day 1 through Day 5).
* **Data Sources:** `rooms`, `interview_slots`
* **SQL / DAX Metric:** `[Room Occupancy Rate %]` by `room_name` & `hiring_day`
* **Why It Exists:** Prevents room double-booking and highlights venue resource deficits.

##### Visual 3.3: Peak Hourly Interview Demand
* **Visual Type:** Area Chart
* **Purpose:** Tracks active booked slots by hour of day (09:00 to 17:00).
* **Data Sources:** `interview_slots`
* **SQL / DAX Metric:** `COUNT(slot_id)` by `slot_start_time` hour window
* **Why It Exists:** Identifies peak scheduling congestion windows during drive operations.

##### Visual 3.4: Underutilized Resource List
* **Visual Type:** Table Visual with red/amber alert icons
* **Purpose:** Lists rooms and panels operating below 30% utilization threshold.
* **Data Sources:** `rooms`, `panels`, `interview_slots`
* **SQL / DAX Metric:** `[Room Occupancy Rate %]`, `[Panel Utilization %]`
* **Why It Exists:** Supports resource consolidation to free up physical space and interviewer time.

#### 4. User Interactions & Decisions Supported
* **Interaction:** Selecting an overloaded panel filters the room matrix to show available rooms during that panel's active windows.
* **Decisions Supported:** Re-allocating interviewers across panels, opening secondary virtual Zoom desks.

---

### PAGE 4: RECOMMENDATIONS & ACTIONS

#### 1. Business Objective
Display real-time, rule-based operational intervention cards generated by the recommendation engine, classifying issues by severity and specifying expected impact.

#### 2. Layout Wireframe
```text
+---------------------------------------------------------------------------------------------------+
|  [SLICER: Severity Filter]       [SLICER: Category Filter]       [SLICER: Target Stage]           |
+---------------------------------------------------------------------------------------------------+
|  [KPI CARD: Critical Alerts]     [KPI CARD: Warning Alerts]      [KPI CARD: Info Alerts]          |
+---------------------------------------------------------------------------------------------------+
|  VISUAL 4.1: Operational Action Cards Feed                                                        |
|  (Custom Table / Table Cards with Rich Text, Severity Icons & Impact Callouts)                    |
+--------------------------------------------------+------------------------------------------------+
|  VISUAL 4.2: SLA Breach Turnaround Heatmap       |  VISUAL 4.3: Company Evaluation Delay Ranking |
|  (Matrix by Stage & Target SLA Hours)            |  (Bar Chart of Avg Overdue Hours)              |
+---------------------------------------------------------------------------------------------------+
```

#### 3. Visual Element Specifications

##### Visual 4.1: Operational Action Cards Feed
* **Visual Type:** Table / Card List Visual with severity formatting (Red/Yellow/Blue badges)
* **Purpose:** Displays structured outputs from [recommendation_engine.py](file:///c:/Users/Lenovo/Desktop/Project%20Product/recruitment-analytics/python/recommendations/recommendation_engine.py).
* **Columns Displayed:** `Severity`, `Category`, `Problem Statement`, `Quantitative Evidence`, `Recommended Action`, `Expected Impact`
* **Data Sources:** Recommendation Engine output DataFrame / Python execution feed
* **Why It Exists:** Serves as the primary operational decision cockpit for placement coordinators.

##### Visual 4.2: SLA Breach Turnaround Heatmap
* **Visual Type:** Matrix Visual
* **Purpose:** Highlights stages experiencing severe evaluation delays beyond target SLA limits.
* **Data Sources:** `recruitment_stage_records`
* **SQL / DAX Metric:** `[SLA Breach Rate %]`, `[Avg Stage TAT Hours]` vs `target_sla_hours`
* **Why It Exists:** Triggers escalation to department panel heads for delayed evaluation queues.

##### Visual 4.3: Company Evaluation Delay Ranking
* **Visual Type:** Horizontal Bar Chart
* **Purpose:** Ranks hiring companies by average evaluation turnaround time.
* **Data Sources:** `companies`, `applications`, `recruitment_stage_records`
* **SQL / DAX Metric:** `AVG(DATEDIFF(stage_entry_time, stage_exit_time, HOUR))`
* **Why It Exists:** Identifies external corporate HR teams slowing down placement turnaround.

#### 4. User Interactions & Decisions Supported
* **Interaction:** Clicking a `CRITICAL` alert card automatically filters the entire dashboard to the affected stage, company, and panel.
* **Decisions Supported:** Dispatching SLA reminder notifications, enforcing 24-hour evaluation submission caps.

---

## 4. Drill-Down Paths & Cross-Filtering Behavior

```mermaid
graph TD
    A[Page 1: Executive Overview] -- Click Company Bar --> B[Page 2: Funnel Analytics (Filtered to Company)]
    B -- Click Leaky Stage --> C[Page 3: Capacity (Filtered to Stage & Panel)]
    C -- Click Overloaded Panel --> D[Page 4: Recommendations (Action Cards for Panel)]
```

1. **Drill-Through Path 1 (Company Performance):**  
   Right-click Company in Page 1 $\rightarrow$ *Drill-through to Page 2 (Funnel Analytics)* $\rightarrow$ View exact candidate score distributions and stage pass rates for that company.
2. **Drill-Through Path 2 (Stage Bottleneck):**  
   Right-click Stage in Page 2 $\rightarrow$ *Drill-through to Page 3 (Capacity & Scheduling)* $\rightarrow$ View panel workload and room bookings associated with that stage.

---

## 5. Slicer Design & Filter Hierarchy

All dashboard pages feature a standardized top filter panel with standard slicer controls:

| Slicer Name | Selection Mode | Scope | Field Mapping |
| :--- | :--- | :--- | :--- |
| **Company Priority Tier** | Multi-Select Dropdown | Global | `companies.priority_tier` |
| **Industry Sector** | Multi-Select Dropdown | Global | `companies.industry_sector` |
| **Hiring Day** | Single-Select Pills | Global | `interview_slots.hiring_day` |
| **Academic Major** | Multi-Select Dropdown | Page 1 & 2 | `candidates.academic_major` |
| **Pipeline Stage** | Dropdown | Page 2 & 4 | `recruitment_stage_records.stage_name` |
| **Alert Severity** | Buttons (Critical / Warning / Info) | Page 4 | `recommendations.severity` |

---

## 6. Implementation Checklist for Power BI Developers

- [ ] Import 7 approved PostgreSQL tables via DirectQuery or Import Mode.
- [ ] Establish 1:N single-direction relationships (`candidates` $\rightarrow$ `applications`, `companies` $\rightarrow$ `applications`, `applications` $\rightarrow$ `recruitment_stage_records`, `companies` $\rightarrow$ `interview_slots`, `rooms` $\rightarrow$ `interview_slots`, `panels` $\rightarrow$ `interview_slots`).
- [ ] Create `DAX_Measures` table and add all 9 core DAX measure formulas.
- [ ] Set up JSON theme file with exact Hex palette (`#0F172A`, `#1E293B`, `#6366F1`, `#10B981`, `#F59E0B`, `#EF4444`).
- [ ] Configure conditional formatting rules on Matrix visuals (SLA breach rate $> 15\% \rightarrow$ Red).
- [ ] Implement drill-through page parameters for Company and Stage fields.
