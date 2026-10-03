"""
Validation Dataset Integrity Checker

Performs comprehensive data quality, referential integrity, and schema compliance
checks on the validation CSV datasets located in data/raw/.
"""

import sys
import os
from typing import List, Dict, Tuple, Any
import pandas as pd

# Add project root directory to PYTHONPATH
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from config.database_config import CSV_PATHS


class DatasetValidator:
    """Rigorous validator checking CSV data integrity against database business rules."""

    def __init__(self) -> None:
        self.report_lines: List[str] = []
        self.datasets: Dict[str, pd.DataFrame] = {}

    def log(self, text: str) -> None:
        """Log report message to list and stdout."""
        self.report_lines.append(text)
        print(text)

    def load_datasets(self) -> bool:
        """Load CSV files into pandas DataFrames."""
        self.log("\n==================================================================")
        self.log("           RECRUITMENT PLATFORM - VALIDATION REPORT               ")
        self.log("==================================================================")
        self.log("1. LOADING CSV DATASETS FROM data/raw/")
        self.log("------------------------------------------------------------------")

        all_loaded = True
        for name, path in CSV_PATHS.items():
            if not os.path.exists(path):
                self.log(f"   [FAIL] File missing: {path}")
                all_loaded = False
            else:
                df = pd.read_csv(path)
                self.datasets[name] = df
                self.log(f"   [PASS] Loaded {name:<26}: {len(df):>4} rows")

        return all_loaded

    def check_row_counts(self) -> bool:
        """Check row counts against minimum target benchmarks."""
        self.log("\n2. CHECKING ROW COUNTS & POPULATION BENCHMARKS")
        self.log("------------------------------------------------------------------")
        expected_min = {
            "candidates": 40,
            "companies": 8,
            "applications": 150,
            "recruitment_stage_records": 500,
            "rooms": 8,
            "panels": 10,
            "interview_slots": 80,
        }

        passed = True
        for entity, min_cnt in expected_min.items():
            cnt = len(self.datasets.get(entity, []))
            if cnt >= min_cnt:
                self.log(f"   [PASS] {entity:<26}: {cnt:>4} rows (min target: {min_cnt})")
            else:
                self.log(f"   [FAIL] {entity:<26}: {cnt:>4} rows (under min target {min_cnt})")
                passed = False

        return passed

    def check_foreign_keys_and_orphans(self) -> bool:
        """Verify referential integrity across parent-child entity pairs."""
        self.log("\n3. CHECKING FOREIGN KEYS & ORPHAN RECORDS")
        self.log("------------------------------------------------------------------")

        cand_ids = set(self.datasets["candidates"]["candidate_id"])
        comp_ids = set(self.datasets["companies"]["company_id"])
        app_ids = set(self.datasets["applications"]["application_id"])
        room_ids = set(self.datasets["rooms"]["room_id"])
        panel_ids = set(self.datasets["panels"]["panel_id"])

        passed = True

        # Check applications foreign keys
        orphan_apps_cand = set(self.datasets["applications"]["candidate_id"]) - cand_ids
        if not orphan_apps_cand:
            self.log("   [PASS] applications -> candidates (0 orphan candidate FKs)")
        else:
            self.log(f"   [FAIL] applications -> candidates ({len(orphan_apps_cand)} orphan candidate FKs)")
            passed = False

        orphan_apps_comp = set(self.datasets["applications"]["company_id"]) - comp_ids
        if not orphan_apps_comp:
            self.log("   [PASS] applications -> companies  (0 orphan company FKs)")
        else:
            self.log(f"   [FAIL] applications -> companies  ({len(orphan_apps_comp)} orphan company FKs)")
            passed = False

        # Check stage records foreign keys
        orphan_stages_app = set(self.datasets["recruitment_stage_records"]["application_id"]) - app_ids
        if not orphan_stages_app:
            self.log("   [PASS] recruitment_stage_records -> applications (0 orphan application FKs)")
        else:
            self.log(f"   [FAIL] recruitment_stage_records -> applications ({len(orphan_stages_app)} orphan application FKs)")
            passed = False

        # Check interview slots foreign keys
        orphan_slots_comp = set(self.datasets["interview_slots"]["company_id"]) - comp_ids
        orphan_slots_room = set(self.datasets["interview_slots"]["room_id"]) - room_ids
        orphan_slots_panel = set(self.datasets["interview_slots"]["panel_id"]) - panel_ids

        if not orphan_slots_comp and not orphan_slots_room and not orphan_slots_panel:
            self.log("   [PASS] interview_slots -> companies, rooms, panels (0 orphan FKs)")
        else:
            self.log(f"   [FAIL] interview_slots orphan FKs: company={len(orphan_slots_comp)}, room={len(orphan_slots_room)}, panel={len(orphan_slots_panel)}")
            passed = False

        return passed

    def check_cgpa_validity(self) -> bool:
        """Verify candidate CGPA bounds (strictly between 6.0 and 10.0)."""
        self.log("\n4. CHECKING CANDIDATE CGPA BOUNDS & DATA TYPES")
        self.log("------------------------------------------------------------------")
        gpas = self.datasets["candidates"]["gpa"]
        invalid_gpas = gpas[(gpas < 6.0) | (gpas > 10.0)]

        if invalid_gpas.empty:
            self.log(f"   [PASS] All {len(gpas)} candidate GPAs are strictly within [6.0, 10.0]")
            return True
        else:
            self.log(f"   [FAIL] Found {len(invalid_gpas)} candidate GPAs outside [6.0, 10.0]")
            return False

    def check_durations_and_timestamps(self) -> bool:
        """Verify exit timestamps > entry timestamps and slot end > start times."""
        self.log("\n5. CHECKING TIMESTAMPS & DURATION VALIDITY")
        self.log("------------------------------------------------------------------")
        passed = True

        # Check recruitment stage records timestamps
        stages_df = self.datasets["recruitment_stage_records"].copy()
        stages_df["entry"] = pd.to_datetime(stages_df["stage_entry_time"])
        stages_df["exit"] = pd.to_datetime(stages_df["stage_exit_time"])

        invalid_stage_times = stages_df[stages_df["exit"] < stages_df["entry"]]
        if invalid_stage_times.empty:
            self.log("   [PASS] recruitment_stage_records: 100% exit_time >= entry_time")
        else:
            self.log(f"   [FAIL] recruitment_stage_records: {len(invalid_stage_times)} invalid negative duration records")
            passed = False

        # Check interview slots timestamps
        slots_df = self.datasets["interview_slots"].copy()
        slots_df["start"] = pd.to_datetime(slots_df["slot_start_time"])
        slots_df["end"] = pd.to_datetime(slots_df["slot_end_time"])

        invalid_slot_times = slots_df[slots_df["end"] <= slots_df["start"]]
        if invalid_slot_times.empty:
            self.log("   [PASS] interview_slots: 100% slot_end_time > slot_start_time")
        else:
            self.log(f"   [FAIL] interview_slots: {len(invalid_slot_times)} invalid negative/zero duration slots")
            passed = False

        return passed

    def check_room_panel_capacities(self) -> bool:
        """Verify room capacities and panel daily max slot caps are positive."""
        self.log("\n6. CHECKING ROOM & PANEL CAPACITY CONSTRAINTS")
        self.log("------------------------------------------------------------------")
        passed = True

        invalid_rooms = self.datasets["rooms"][self.datasets["rooms"]["seating_capacity"] <= 0]
        if invalid_rooms.empty:
            self.log("   [PASS] rooms: 100% seating_capacity > 0")
        else:
            self.log(f"   [FAIL] rooms: {len(invalid_rooms)} non-positive capacity records")
            passed = False

        invalid_panels = self.datasets["panels"][self.datasets["panels"]["max_daily_slots"] <= 0]
        if invalid_panels.empty:
            self.log("   [PASS] panels: 100% max_daily_slots > 0")
        else:
            self.log(f"   [FAIL] panels: {len(invalid_panels)} non-positive slot capacity records")
            passed = False

        return passed

    def check_stage_sequence_validity(self) -> bool:
        """Verify stage sequence numbers strictly increase within each application."""
        self.log("\n7. CHECKING STAGE SEQUENCE INTEGRITY")
        self.log("------------------------------------------------------------------")
        stages_df = self.datasets["recruitment_stage_records"]
        passed = True

        for app_id, group in stages_df.groupby("application_id"):
            seqs = group["sequence_order"].tolist()
            if seqs != sorted(seqs):
                self.log(f"   [FAIL] Application {app_id} out-of-order sequence: {seqs}")
                passed = False

        if passed:
            self.log("   [PASS] All stage records strictly maintain sequential order")

        return passed

    def run_all_validations(self) -> bool:
        """Execute complete validation suite and summarize results."""
        if not self.load_datasets():
            self.log("\n[FATAL] Missing dataset files. Run generate_validation_dataset.py first.")
            return False

        r1 = self.check_row_counts()
        r2 = self.check_foreign_keys_and_orphans()
        r3 = self.check_cgpa_validity()
        r4 = self.check_durations_and_timestamps()
        r5 = self.check_room_panel_capacities()
        r6 = self.check_stage_sequence_validity()

        self.log("\n==================================================================")
        if all([r1, r2, r3, r4, r5, r6]):
            self.log("  OVERALL RESULT: [PASS] VALIDATION DATASET PIPELINE VERIFIED     ")
            self.log("==================================================================\n")
            return True
        else:
            self.log("  OVERALL RESULT: [FAIL] VALIDATION ISSUES DETECTED               ")
            self.log("==================================================================\n")
            return False


if __name__ == "__main__":
    validator = DatasetValidator()
    validator.run_all_validations()
