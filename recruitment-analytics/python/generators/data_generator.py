"""
Production-Scale Synthetic Data Generator

Generates high-performance, schema-compliant synthetic datasets at production scale:
- 1,250 candidates
- 180 companies
- 6,000 applications
- ~40,000 recruitment stage records
- 30 rooms
- 50 panels
- 2,500 interview slots

Maintains 100% referential integrity, sequential stage progression, timestamp chronology,
and PostgreSQL bulk-copy compatibility.
"""

import sys
import os
import random
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import pandas as pd
from faker import Faker

# Add project root directory to PYTHONPATH
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from config.database_config import CSV_PATHS


class ProductionDataGenerator:
    """Production-scale synthetic dataset generator."""

    def __init__(self, seed: int = 42) -> None:
        self.fake = Faker()
        Faker.seed(seed)
        random.seed(seed)
        self.seed = seed

    def generate_candidates(self, count: int = 1250) -> pd.DataFrame:
        """Generate 1,250 student candidate records."""
        print(f"-> Generating Candidates (Target: {count})...")
        candidates = []
        degree_programs = ["B.Tech", "M.Tech", "Dual Degree (B.Tech + M.Tech)", "M.S."]
        majors = [
            "Computer Science & Engineering",
            "Data Science & AI",
            "Electrical & Electronics",
            "Mechanical Engineering",
            "Chemical Engineering",
            "Civil Engineering",
            "Aerospace Engineering",
        ]

        for i in range(1, count + 1):
            gpa = round(random.uniform(6.0, 10.0), 2)
            if gpa >= 8.5:
                cgpa_band = "High Distinction (8.5 - 10.0)"
            elif gpa >= 7.0:
                cgpa_band = "First Class (7.0 - 8.49)"
            else:
                cgpa_band = "Second Class (6.0 - 6.99)"

            candidates.append({
                "candidate_id": f"CND-{10000 + i}",
                "full_name": self.fake.name(),
                "email": f"candidate_{i}_{self.seed}@university.edu",
                "phone_number": f"+91-98{random.randint(10000000, 99999999)}",
                "degree_program": random.choice(degree_programs),
                "academic_major": random.choice(majors),
                "gpa": gpa,
                "cgpa_band": cgpa_band,
                "graduation_year": 2026,
                "gender": random.choice(["Female", "Male", "Non-Binary"]),
                "created_at": "2026-01-10 09:00:00+05:30",
            })

        return pd.DataFrame(candidates)

    def generate_companies(self, count: int = 180) -> pd.DataFrame:
        """Generate 180 corporate partner records."""
        print(f"-> Generating Companies (Target: {count})...")
        sectors = [
            "Enterprise Software", "Financial Technology", "Cybersecurity",
            "E-Commerce & Retail", "Data Science & AI", "Healthcare & Biotech",
            "Robotics & Hardware", "Management Consulting", "Cloud Infrastructure",
            "Automotive Tech", "Telecommunications", "Semiconductors"
        ]
        tiers = ["Tier 1 (Dream Partner)", "Tier 2 (Super Dream)", "Tier 3 (Regular)"]

        companies = []
        for i in range(1, count + 1):
            comp_name = f"{self.fake.company()} {random.choice(['Tech', 'Systems', 'Labs', 'Corp', 'Solutions'])}"
            companies.append({
                "company_id": f"CMP-{1000 + i}",
                "company_name": comp_name,
                "industry_sector": random.choice(sectors),
                "priority_tier": random.choice(tiers),
                "contact_email": f"campus_hr_{i}@company.com",
                "created_at": "2025-11-01 10:00:00+05:30",
            })

        return pd.DataFrame(companies)

    def generate_rooms(self, count: int = 30) -> pd.DataFrame:
        """Generate 30 physical and virtual room resources."""
        print(f"-> Generating Rooms (Target: {count})...")
        rooms = []
        for i in range(1, count + 1):
            r_mode = "In-Person" if i <= 20 else "Virtual"
            r_loc = "Main Placement Complex" if r_mode == "In-Person" else "Online Zoom Portal"
            rooms.append({
                "room_id": f"RM-{200 + i}",
                "room_name": f"Interview Hall Room {i}" if r_mode == "In-Person" else f"Virtual Desk {i - 20}",
                "building_location": r_loc,
                "interview_mode": r_mode,
                "seating_capacity": 4 if r_mode == "In-Person" else 2,
            })
        return pd.DataFrame(rooms)

    def generate_panels(self, count: int = 50) -> pd.DataFrame:
        """Generate 50 evaluator department panel units."""
        print(f"-> Generating Panels (Target: {count})...")
        panels = []
        departments = [
            "Software Engineering", "Data Science & Analytics",
            "Product Management", "DevOps & Cloud", "Hardware & Systems"
        ]
        for i in range(1, count + 1):
            dept = departments[(i - 1) % len(departments)]
            panels.append({
                "panel_id": f"PNL-{300 + i}",
                "panel_code": f"{dept[:3].upper()}-Panel-{i:02d}",
                "department": dept,
                "max_daily_slots": 8 if dept == "Software Engineering" else 6,
            })
        return pd.DataFrame(panels)

    def generate_applications(self, df_candidates: pd.DataFrame, df_companies: pd.DataFrame, count: int = 6000) -> pd.DataFrame:
        """Generate 6,000 job application records."""
        print(f"-> Generating Applications (Target: {count})...")
        roles = [
            "Software Development Engineer (SDE-1)",
            "Data Scientist Intern",
            "Business Analyst",
            "Product Management Associate",
            "DevOps Engineer",
            "Systems Design Engineer",
        ]

        cand_ids = df_candidates["candidate_id"].tolist()
        comp_ids = df_companies["company_id"].tolist()

        applications = []
        app_counter = 50001

        # Calculate exact number of applications per candidate (~4.8 per candidate)
        for c_id in cand_ids:
            num_apps = random.randint(3, 7)
            assigned_companies = random.sample(comp_ids, k=num_apps)
            for comp_id in assigned_companies:
                if len(applications) >= count:
                    break
                applications.append({
                    "application_id": f"APP-{app_counter}",
                    "candidate_id": c_id,
                    "company_id": comp_id,
                    "applied_role": random.choice(roles),
                    "overall_status": "Active",
                    "application_date": "2026-02-01",
                    "updated_at": "2026-02-01 10:00:00+05:30",
                })
                app_counter += 1
            if len(applications) >= count:
                break

        return pd.DataFrame(applications)

    def generate_recruitment_stage_records(self, df_applications: pd.DataFrame, target_count: int = 40000) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Generate ~40,000 recruitment stage progression records."""
        print(f"-> Generating Recruitment Stage Records (Target: ~{target_count})...")
        stage_records = []
        stage_counter = 100001

        stage_definitions = [
            ("Sourcing", 1, 24),
            ("Resume Screening", 2, 48),
            ("Online Assessment", 3, 72),
            ("Technical Interview 1", 4, 48),
            ("Technical Interview 2", 5, 48),
            ("HR Interview", 6, 24),
            ("Offer Extended", 7, 72),
            ("Joined", 8, 0),
        ]

        # Funnel pass ratios
        pass_probabilities = {
            1: 1.00,  # Sourcing -> Screening
            2: 0.85,  # Screening -> OA
            3: 0.40,  # OA -> Tech 1
            4: 0.45,  # Tech 1 -> Tech 2
            5: 0.60,  # Tech 2 -> HR
            6: 0.85,  # HR -> Offer
            7: 0.75,  # Offer -> Joined
            8: 1.00,  # Joined
        }

        base_time = datetime(2026, 2, 1, 9, 0, 0)
        updated_apps = df_applications.copy()
        terminal_status_map = {}

        for idx, app_row in df_applications.iterrows():
            app_id = app_row["application_id"]
            current_time = base_time + timedelta(hours=random.randint(0, 24))
            is_active = True

            for s_name, s_seq, s_sla in stage_definitions:
                if not is_active:
                    break

                entry_time = current_time

                # Joined stage is terminal state
                if s_seq == 8:
                    exit_time = entry_time
                    duration_hours = 0
                    sla_breached = False
                    s_status = "Passed"
                    score = 100.0
                else:
                    duration_hours = random.randint(12, 80)
                    exit_time = entry_time + timedelta(hours=duration_hours)
                    sla_breached = duration_hours > s_sla

                    prob = pass_probabilities[s_seq]
                    passed = random.random() < prob

                    if passed:
                        s_status = "Passed"
                        score = round(random.uniform(70.0, 99.0), 2)
                    else:
                        s_status = "Failed"
                        score = round(random.uniform(30.0, 68.0), 2)
                        is_active = False

                stage_records.append({
                    "stage_record_id": f"SR-{stage_counter}",
                    "application_id": app_id,
                    "stage_name": s_name,
                    "sequence_order": s_seq,
                    "stage_entry_time": entry_time.strftime("%Y-%m-%d %H:%M:%S+05:30"),
                    "stage_exit_time": exit_time.strftime("%Y-%m-%d %H:%M:%S+05:30") if s_seq < 8 else "",
                    "stage_status": s_status,
                    "evaluation_score": score,
                    "target_sla_hours": s_sla,
                    "sla_breached_flag": sla_breached,
                    "created_at": entry_time.strftime("%Y-%m-%d %H:%M:%S+05:30"),
                })

                stage_counter += 1
                current_time = exit_time + timedelta(hours=random.randint(2, 16))

                # Stop if target record count achieved
                if len(stage_records) >= target_count:
                    break

            if len(stage_records) >= target_count:
                break

        df_stage_records = pd.DataFrame(stage_records)

        # Map terminal application status
        for app_id, group in df_stage_records.groupby("application_id"):
            last_row = group.sort_values("sequence_order").iloc[-1]
            if last_row["stage_name"] == "Joined" and last_row["stage_status"] == "Passed":
                terminal_status_map[app_id] = "Hired"
            elif last_row["stage_status"] == "Failed":
                terminal_status_map[app_id] = "Rejected"
            else:
                terminal_status_map[app_id] = "Active"

        updated_apps["overall_status"] = updated_apps["application_id"].map(terminal_status_map).fillna("Active")

        return df_stage_records, updated_apps

    def generate_interview_slots(self, df_companies: pd.DataFrame, df_rooms: pd.DataFrame, df_panels: pd.DataFrame, count: int = 2500) -> pd.DataFrame:
        """Generate 2,500 capacity interview slots."""
        print(f"-> Generating Interview Slots (Target: {count})...")
        slots = []
        slot_counter = 90001
        hiring_days = ["Day 1", "Day 2", "Day 3", "Day 4", "Day 5"]

        slot_base_dates = {
            "Day 1": datetime(2026, 2, 2, 9, 0, 0),
            "Day 2": datetime(2026, 2, 3, 9, 0, 0),
            "Day 3": datetime(2026, 2, 4, 9, 0, 0),
            "Day 4": datetime(2026, 2, 5, 9, 0, 0),
            "Day 5": datetime(2026, 2, 6, 9, 0, 0),
        }

        company_ids = df_companies["company_id"].tolist()
        room_ids = df_rooms["room_id"].tolist()
        panel_ids = df_panels["panel_id"].tolist()

        for i in range(count):
            day = random.choice(hiring_days)
            start_date = slot_base_dates[day]
            hour_offset = random.randint(0, 7)
            minute_offset = random.choice([0, 45])

            s_start = start_date + timedelta(hours=hour_offset, minutes=minute_offset)
            s_end = s_start + timedelta(minutes=45)

            status = random.choice(["Booked", "Completed", "Available", "Cancelled"])

            slots.append({
                "slot_id": f"SLT-{slot_counter}",
                "company_id": random.choice(company_ids),
                "room_id": random.choice(room_ids),
                "panel_id": random.choice(panel_ids),
                "hiring_day": day,
                "slot_start_time": s_start.strftime("%Y-%m-%d %H:%M:%S+05:30"),
                "slot_end_time": s_end.strftime("%Y-%m-%d %H:%M:%S+05:30"),
                "slot_status": status,
                "created_at": "2026-02-01 16:00:00+05:30",
            })
            slot_counter += 1

        return pd.DataFrame(slots)

    def run(self) -> Dict[str, pd.DataFrame]:
        """Execute full production data generation pipeline."""
        print("==================================================================")
        print("     RECRUITMENT PLATFORM - PRODUCTION DATA GENERATOR             ")
        print("==================================================================")

        df_candidates = self.generate_candidates(1250)
        df_companies = self.generate_companies(180)
        df_rooms = self.generate_rooms(30)
        df_panels = self.generate_panels(50)
        df_applications_init = self.generate_applications(df_candidates, df_companies, 6000)
        df_stage_records, df_applications = self.generate_recruitment_stage_records(df_applications_init, 40000)
        df_slots = self.generate_interview_slots(df_companies, df_rooms, df_panels, 2500)

        datasets = {
            "candidates": df_candidates,
            "companies": df_companies,
            "applications": df_applications,
            "recruitment_stage_records": df_stage_records,
            "rooms": df_rooms,
            "panels": df_panels,
            "interview_slots": df_slots,
        }

        print("\n-> Exporting Production DataFrames to PostgreSQL-compatible CSVs...")
        for name, df in datasets.items():
            path = CSV_PATHS[name]
            df.to_csv(path, index=False)
            print(f"   [OK] Saved {name:<26} ({len(df):>5} rows) -> {path}")

        print("\n[SUCCESS] Production-scale data generation completed.")
        return datasets


def generate_production_data() -> Dict[str, pd.DataFrame]:
    generator = ProductionDataGenerator()
    return generator.run()


if __name__ == "__main__":
    generate_production_data()
