"""
Recommendation & Decision Support Engine

Evaluates funnel metrics, capacity utilization, and process efficiency telemetry
against rule-based heuristics to generate structured operational interventions.

Output DataFrame Schema:
- category: Funnel Issues | Capacity Issues | Process Issues
- problem: Description of the operational bottleneck or risk
- evidence: Quantitative metrics supporting the finding
- severity: INFO | WARNING | CRITICAL
- recommendation: Actionable operational intervention steps
- expected_impact: Predicted performance improvement or risk mitigation
"""

import sys
import os
from typing import Dict, List, Any, Optional
import pandas as pd

# Add project root directory to PYTHONPATH
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from config.database_config import CSV_PATHS


class RecommendationEngine:
    """Rule-based decision support engine generating operational recommendations."""

    def __init__(self) -> None:
        self.recommendations: List[Dict[str, str]] = []

    def evaluate_funnel_rules(
        self, stage_records_df: pd.DataFrame, applications_df: pd.DataFrame
    ) -> List[Dict[str, str]]:
        """Evaluate candidate funnel progression for high drop-offs and low offer acceptance."""
        results = []

        # Rule A1: High Stage Drop-Off Rates (> 60%)
        stage_counts = stage_records_df.groupby(["sequence_order", "stage_name"]).agg(
            total_entered=("stage_record_id", "count"),
            failed_count=("stage_status", lambda s: (s == "Failed").sum()),
        ).reset_index()

        for _, row in stage_counts.iterrows():
            if row["total_entered"] > 0:
                dropoff_pct = (row["failed_count"] / row["total_entered"]) * 100.0
                if dropoff_pct >= 55.0:
                    severity = "CRITICAL" if dropoff_pct >= 70.0 else "WARNING"
                    results.append({
                        "category": "Funnel Issues",
                        "problem": f"High Candidate Drop-Off at {row['stage_name']} Stage",
                        "evidence": f"Drop-off rate is {dropoff_pct:.1f}% ({row['failed_count']} failures out of {row['total_entered']} entrants)",
                        "severity": severity,
                        "recommendation": f"Calibrate assessment difficulty or review evaluator scoring rubrics for {row['stage_name']}.",
                        "expected_impact": "Reduce pipeline leakage by 20-30% and preserve qualified candidate pool.",
                    })

        # Rule A2: Low Offer Conversion Rate (< 60%)
        offer_records = stage_records_df[stage_records_df["stage_name"] == "Offer"]
        if not offer_records.empty:
            total_offers = len(offer_records)
            offers_accepted = (offer_records["stage_status"] == "Passed").sum()
            acceptance_rate = (offers_accepted / total_offers) * 100.0 if total_offers > 0 else 100.0

            if acceptance_rate < 70.0:
                severity = "CRITICAL" if acceptance_rate < 50.0 else "WARNING"
                results.append({
                    "category": "Funnel Issues",
                    "problem": "Low Overall Offer Acceptance Rate",
                    "evidence": f"Offer acceptance rate is {acceptance_rate:.1f}% ({offers_accepted} accepted out of {total_offers} extended)",
                    "severity": severity,
                    "recommendation": "Review compensation competitiveness and activate personalized candidate engagement protocols.",
                    "expected_impact": "Increase offer conversion by 15-25% to achieve company target hiring quotas.",
                })

        return results

    def evaluate_capacity_rules(
        self, slots_df: pd.DataFrame, rooms_df: pd.DataFrame, panels_df: pd.DataFrame
    ) -> List[Dict[str, str]]:
        """Evaluate room and panel workload metrics for over/under-utilization."""
        results = []

        # Rule B1: Room Overutilization (> 80%) & Underutilization (< 30%)
        room_usage = slots_df.groupby("room_id").agg(
            total_slots=("slot_id", "count"),
            booked_slots=("slot_status", lambda s: s.isin(["Booked", "Completed"]).sum()),
        ).reset_index()

        room_merged = pd.merge(rooms_df, room_usage, on="room_id", how="left").fillna(0)

        for _, row in room_merged.iterrows():
            if row["total_slots"] > 0:
                occ_rate = (row["booked_slots"] / row["total_slots"]) * 100.0
                if occ_rate >= 80.0:
                    severity = "CRITICAL" if occ_rate >= 90.0 else "WARNING"
                    results.append({
                        "category": "Capacity Issues",
                        "problem": f"Room Overutilization at {row['room_name']}",
                        "evidence": f"Occupancy rate is {occ_rate:.1f}% ({int(row['booked_slots'])} booked out of {int(row['total_slots'])} slots)",
                        "severity": severity,
                        "recommendation": "Allocate virtual Zoom desks or extend evening interview operating windows.",
                        "expected_impact": "Eliminate venue bottlenecks and prevent room double-booking risks.",
                    })
                elif occ_rate < 30.0:
                    results.append({
                        "category": "Capacity Issues",
                        "problem": f"Underutilized Room Resource ({row['room_name']})",
                        "evidence": f"Occupancy rate is only {occ_rate:.1f}% ({int(row['booked_slots'])} booked slots)",
                        "severity": "INFO",
                        "recommendation": "Consolidate interviews into underutilized rooms to optimize venue space.",
                        "expected_impact": "Improve facility resource efficiency by 15-20%.",
                    })

        # Rule B2: Panel Workload Overutilization (> 80%)
        panel_usage = slots_df.groupby("panel_id").agg(
            booked_slots=("slot_status", lambda s: s.isin(["Booked", "Completed"]).sum()),
        ).reset_index()

        panel_merged = pd.merge(panels_df, panel_usage, on="panel_id", how="left").fillna(0)

        for _, row in panel_merged.iterrows():
            max_cap = row["max_daily_slots"] * 3  # Across 3 hiring days
            util_rate = (row["booked_slots"] / max_cap) * 100.0 if max_cap > 0 else 0.0

            if util_rate >= 75.0:
                severity = "CRITICAL" if util_rate >= 90.0 else "WARNING"
                results.append({
                    "category": "Capacity Issues",
                    "problem": f"Evaluator Panel Overload ({row['panel_code']} - {row['department']})",
                    "evidence": f"Workload utilization is {util_rate:.1f}% ({int(row['booked_slots'])} slots booked out of {max_cap} max capacity)",
                    "severity": severity,
                    "recommendation": f"Reassign 2-3 interviewers from underutilized panels in {row['department']}.",
                    "expected_impact": "Prevent evaluator burnout and reduce evaluation feedback delays.",
                })

        return results

    def evaluate_process_rules(
        self, stage_records_df: pd.DataFrame
    ) -> List[Dict[str, str]]:
        """Evaluate stage turnaround times (TAT) and SLA breach rates."""
        results = []

        completed_stages = stage_records_df[stage_records_df["stage_exit_time"].notnull()].copy()
        if completed_stages.empty:
            return results

        completed_stages["entry"] = pd.to_datetime(completed_stages["stage_entry_time"])
        completed_stages["exit"] = pd.to_datetime(completed_stages["stage_exit_time"])
        completed_stages["tat_hours"] = (completed_stages["exit"] - completed_stages["entry"]).dt.total_seconds() / 3600.0

        stage_metrics = completed_stages.groupby(["sequence_order", "stage_name", "target_sla_hours"]).agg(
            total_evals=("stage_record_id", "count"),
            avg_tat=("tat_hours", "mean"),
            breach_count=("sla_breached_flag", lambda s: (s == True).sum()),
        ).reset_index()

        for _, row in stage_metrics.iterrows():
            avg_tat = row["avg_tat"]
            sla_target = row["target_sla_hours"]
            breach_rate = (row["breach_count"] / row["total_evals"]) * 100.0 if row["total_evals"] > 0 else 0.0

            # Rule C1: Slow Stage Duration (TAT > Target SLA)
            if avg_tat > sla_target:
                severity = "CRITICAL" if avg_tat > (1.3 * sla_target) else "WARNING"
                results.append({
                    "category": "Process Issues",
                    "problem": f"Slow Evaluation Turnaround at {row['stage_name']} Stage",
                    "evidence": f"Avg TAT is {avg_tat:.1f} hours vs Target SLA limit of {sla_target} hours (Variance: +{avg_tat - sla_target:.1f} hrs)",
                    "severity": severity,
                    "recommendation": f"Send automated SLA reminder notifications to {row['stage_name']} evaluators.",
                    "expected_impact": "Bring average turnaround time within target SLA window.",
                })

            # Rule C2: High SLA Breach Rate (> 15%)
            if breach_rate >= 15.0:
                severity = "CRITICAL" if breach_rate >= 25.0 else "WARNING"
                results.append({
                    "category": "Process Issues",
                    "problem": f"High SLA Breach Frequency at {row['stage_name']} Stage",
                    "evidence": f"SLA breach rate is {breach_rate:.1f}% ({row['breach_count']} overdue evaluations out of {row['total_evals']} total)",
                    "severity": severity,
                    "recommendation": "Enforce mandatory 24-hour evaluation submission caps and rebalance candidate queues.",
                    "expected_impact": "Lower overall stage SLA breach rate below 5%.",
                })

        return results

    def generate_recommendations(
        self,
        candidates_df: pd.DataFrame,
        companies_df: pd.DataFrame,
        applications_df: pd.DataFrame,
        stage_records_df: pd.DataFrame,
        rooms_df: pd.DataFrame,
        panels_df: pd.DataFrame,
        slots_df: pd.DataFrame,
    ) -> pd.DataFrame:
        """Run all recommendation rules and return structured recommendations DataFrame."""
        all_recs = []
        all_recs.extend(self.evaluate_funnel_rules(stage_records_df, applications_df))
        all_recs.extend(self.evaluate_capacity_rules(slots_df, rooms_df, panels_df))
        all_recs.extend(self.evaluate_process_rules(stage_records_df))

        df_recs = pd.DataFrame(all_recs, columns=[
            "category", "problem", "evidence", "severity", "recommendation", "expected_impact"
        ])
        return df_recs


def run_recommendation_pipeline() -> pd.DataFrame:
    """Load raw CSV datasets and generate operational recommendations."""
    print("==================================================================")
    print("      RECRUITMENT PLATFORM - RECOMMENDATION ENGINE PIPELINE       ")
    print("==================================================================")

    # Load datasets from raw CSV files
    candidates_df = pd.read_csv(CSV_PATHS["candidates"])
    companies_df = pd.read_csv(CSV_PATHS["companies"])
    applications_df = pd.read_csv(CSV_PATHS["applications"])
    stage_records_df = pd.read_csv(CSV_PATHS["recruitment_stage_records"])
    rooms_df = pd.read_csv(CSV_PATHS["rooms"])
    panels_df = pd.read_csv(CSV_PATHS["panels"])
    slots_df = pd.read_csv(CSV_PATHS["interview_slots"])

    engine = RecommendationEngine()
    recs_df = engine.generate_recommendations(
        candidates_df, companies_df, applications_df,
        stage_records_df, rooms_df, panels_df, slots_df
    )

    print(f"\n-> Generated {len(recs_df)} Actionable Operational Recommendations:\n")
    for idx, row in recs_df.iterrows():
        print(f"[{idx + 1}] [{row['severity']}] [{row['category']}]")
        print(f"    Problem:         {row['problem']}")
        print(f"    Evidence:        {row['evidence']}")
        print(f"    Recommendation:  {row['recommendation']}")
        print(f"    Expected Impact: {row['expected_impact']}\n")

    return recs_df


if __name__ == "__main__":
    run_recommendation_pipeline()
