# Power BI Dashboard Module

This directory contains Power BI report assets, desktop templates (`.pbit`), data model documentation, and DAX measure definitions for the **Recruitment Funnel & Capacity Analytics Platform**.

---

## 📊 Dashboard Structure

1. **Executive Hiring Summary:**
   - **Visuals:** High-level KPI cards (Total Applicants, Offers Extended, Offers Accepted, Overall Conversion Rate), Campus Tier Yield Breakdown.
   - **Slicers:** Date Range, Campus Tier, Applied Role, Region.

2. **Operations & Funnel Velocity:**
   - **Visuals:** Stage-by-Stage Funnel Chart (Sourcing $\rightarrow$ Joined), SLA Turnaround Time Heatmap, Evaluation Breach Matrix.
   - **Slicers:** Funnel Stage, Recruiter Name, University.

3. **Capacity & Workload Center:**
   - **Visuals:** Interviewer Capacity Utilization Gauge, Recruiter Load Distribution Bar Chart, Pending Evaluation Queue by Department.
   - **Slicers:** Department, Evaluator Name, Capacity Alert Status.

---

## 🔌 Data Source Connection Instructions

1. Open Power BI Desktop.
2. Select **Get Data** $\rightarrow$ **PostgreSQL database**.
3. Server: `localhost:5432` (or configured PostgreSQL host).
4. Database: `recruitment_analytics`.
5. Data Connectivity mode: **DirectQuery** (for real-time SLA tracking) or **Import** (for high-performance historical analysis).
6. Execute initial SQL view imports from `sql/` directory.

---

## 📐 Core DAX Measures (Template)

```dax
// Total Applicants
Total Applicants = COUNTROWS(applications)

// Offer Acceptance Rate %
Offer Acceptance Rate % = 
DIVIDE(
    CALCULATE(COUNTROWS(applications), applications[current_stage] = "Joined"),
    CALCULATE(COUNTROWS(applications), applications[current_stage] IN {"Offer Extended", "Joined"}),
    0
) * 100

// Average Stage Turnaround (Hours)
Avg Stage Turnaround Hours = AVERAGE(stage_evaluations[stage_turnaround_hours])
```
