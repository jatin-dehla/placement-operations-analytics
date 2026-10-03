"""
Validation Dataset Generator

Generates a realistic small-scale validation dataset (~50 candidates, 10 companies,
200 applications, ~1000 stage records, 10 rooms, 15 panels, 100 interview slots)
to verify schema correctness, foreign key integrity, and analytics viability.
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

from config.database_config import VALIDATION_SCALE, CSV_PATHS


def generate_validation_data(seed: int = 42) -> Dict[str, pd.DataFrame]:
    """Generate realistic validation datasets for all 7 approved entities."""

    fake = Faker()
    Faker.seed(seed)
    random.seed(seed)

    print("==================================================================")
    print("      RECRUITMENT PLATFORM - VALIDATION DATASET PIPELINE          ")
    print("==================================================================")

    # --------------------------------------------------------------------------
    # 1. GENERATE CANDIDATES (50 records)
    # --------------------------------------------------------------------------
    print("-> Generating Candidates (Target: 50)...")
    candidates_list = []
    degree_programs = ["B.Tech", "M.Tech", "Dual Degree (B.Tech + M.Tech)"]
    majors = [
        "Computer Science & Engineering",
        "Data Science & AI",
        "Electrical Engineering",
        "Mechanical Engineering",
        "Chemical Engineering",
    ]

    for i in range(1, VALIDATION_SCALE["CANDIDATES_COUNT"] + 1):
        c_id = f"CND-{1000 + i}"
        gpa = round(random.uniform(6.0, 10.0), 2)
        if gpa >= 8.5:
            cgpa_band = "High Distinction (8.5 - 10.0)"
        elif gpa >= 7.0:
            cgpa_band = "First Class (7.0 - 8.49)"
        else:
            cgpa_band = "Second Class (6.0 - 6.99)"

        candidates_list.append({
            "candidate_id": c_id,
            "full_name": fake.name(),
            "email": f"student_{i}@university.edu",
            "phone_number": f"+91-98{random.randint(10000000, 99999999)}",
            "degree_program": random.choice(degree_programs),
            "academic_major": random.choice(majors),
            "gpa": gpa,
            "cgpa_band": cgpa_band,
            "graduation_year": 2026,
            "gender": random.choice(["Female", "Male", "Non-Binary"]),
            "created_at": "2026-01-10 09:00:00+05:30",
        })

    df_candidates = pd.DataFrame(candidates_list)

    # --------------------------------------------------------------------------
    # 2. GENERATE COMPANIES (10 records)
    # --------------------------------------------------------------------------
    print("-> Generating Companies (Target: 10)...")
    companies_data = [
        ("CMP-101", "Acme Cloud Systems", "Enterprise Software", "Tier 1 (Dream Partner)", "campus@acmecloud.com"),
        ("CMP-102", "FinTech Analytics Corp", "Financial Technology", "Tier 1 (Dream Partner)", "careers@fintech.com"),
        ("CMP-103", "NexGen Cyber Security", "Cybersecurity", "Tier 2 (Super Dream)", "recruiting@nexgen.io"),
        ("CMP-104", "Global Retail Tech", "E-Commerce", "Tier 2 (Super Dream)", "campus@globalretail.com"),
        ("CMP-105", "DataMind Artificial Intelligence", "Data Science & AI", "Tier 1 (Dream Partner)", "hr@datamind.ai"),
        ("CMP-106", "Alpha Health Tech", "Healthcare & Biotech", "Tier 3 (Regular)", "careers@alphahealth.com"),
        ("CMP-107", "Quantum Robotics", "Robotics & Hardware", "Tier 2 (Super Dream)", "hiring@quantumrobotics.com"),
        ("CMP-108", "Apex Management Consulting", "Consulting", "Tier 1 (Dream Partner)", "campus@apexconsulting.com"),
        ("CMP-109", "CloudScale Infrastructure", "DevOps & Cloud", "Tier 3 (Regular)", "jobs@cloudscale.io"),
        ("CMP-110", "Veritas Financial Labs", "Financial Technology", "Tier 2 (Super Dream)", "hr@veritaslabs.com"),
    ]

    df_companies = pd.DataFrame(companies_data, columns=[
        "company_id", "company_name", "industry_sector", "priority_tier", "contact_email"
    ])
    df_companies["created_at"] = "2025-11-01 10:00:00+05:30"

    # --------------------------------------------------------------------------
    # 3. GENERATE ROOMS (10 records)
    # --------------------------------------------------------------------------
    print("-> Generating Rooms (Target: 10)...")
    rooms_list = []
    for i in range(1, VALIDATION_SCALE["ROOMS_COUNT"] + 1):
        r_mode = "In-Person" if i <= 7 else "Virtual"
        r_loc = "Student Activity Center" if r_mode == "In-Person" else "Online Conference Portal"
        rooms_list.append({
            "room_id": f"RM-10{i}",
            "room_name": f"Interview Desk {i}" if r_mode == "In-Person" else f"Virtual Zoom Desk {i - 7}",
            "building_location": r_loc,
            "interview_mode": r_mode,
            "seating_capacity": 4 if r_mode == "In-Person" else 2,
        })
    df_rooms = pd.DataFrame(rooms_list)

    # --------------------------------------------------------------------------
    # 4. GENERATE PANELS (15 records)
    # --------------------------------------------------------------------------
    print("-> Generating Panels (Target: 15)...")
    panels_list = []
    departments = ["Software Engineering", "Data Science & Analytics", "Product Management", "DevOps & Cloud"]
    for i in range(1, VALIDATION_SCALE["PANELS_COUNT"] + 1):
        dept = departments[(i - 1) % len(departments)]
        panels_list.append({
            "panel_id": f"PNL-10{i:02d}",
            "panel_code": f"{dept[:3].upper()}-Panel-{chr(65 + (i % 5))}",
            "department": dept,
            "max_daily_slots": 8 if dept == "Software Engineering" else 6,
        })
    df_panels = pd.DataFrame(panels_list)

    # --------------------------------------------------------------------------
    # 5. GENERATE APPLICATIONS (200 records)
    # --------------------------------------------------------------------------
    print("-> Generating Applications (Target: 200)...")
    applications_list = []
    roles = [
        "Software Development Engineer (SDE-1)",
        "Data Scientist Intern",
        "Business Analyst",
        "Product Management Associate",
        "DevOps Engineer",
    ]

    app_counter = 5001
    candidate_ids = df_candidates["candidate_id"].tolist()
    company_ids = df_companies["company_id"].tolist()

    # Each candidate applies to 4 companies on average
    for c_id in candidate_ids:
        assigned_companies = random.sample(company_ids, k=4)
        for comp_id in assigned_companies:
            applications_list.append({
                "application_id": f"APP-{app_counter}",
                "candidate_id": c_id,
                "company_id": comp_id,
                "applied_role": random.choice(roles),
                "overall_status": "Active",  # Will be updated by stage generator
                "application_date": "2026-02-01",
                "updated_at": "2026-02-01 10:00:00+05:30",
            })
            app_counter += 1

    df_applications = pd.DataFrame(applications_list)

    # --------------------------------------------------------------------------
    # 6. GENERATE RECRUITMENT STAGE RECORDS (~1000 records)
    # --------------------------------------------------------------------------
    print("-> Generating Recruitment Stage Records (Target: ~1000)...")
    stage_records_list = []
    stage_counter = 10001

    stage_definitions = [
        ("Applied", 1, 24),
        ("Shortlisted", 2, 48),
        ("OA", 3, 72),
        ("Technical", 4, 48),
        ("HR", 5, 24),
        ("Offer", 6, 72),
    ]

    # Progression pass probabilities per stage
    pass_probabilities = {
        1: 1.00,  # Applied -> Shortlisted
        2: 0.75,  # Shortlisted -> OA
        3: 0.40,  # OA -> Technical
        4: 0.45,  # Technical -> HR
        5: 0.80,  # HR -> Offer
        6: 0.75,  # Offer -> Joined/Accepted
    }

    base_time = datetime(2026, 2, 1, 9, 0, 0)

    for idx, app_row in df_applications.iterrows():
        app_id = app_row["application_id"]
        current_time = base_time + timedelta(hours=random.randint(0, 12))
        is_active = True

        for s_name, s_seq, s_sla in stage_definitions:
            if not is_active:
                break

            entry_time = current_time
            # Generate stage duration (12 to 60 hours)
            duration_hours = random.randint(12, 60)
            exit_time = entry_time + timedelta(hours=duration_hours)
            sla_breached = duration_hours > s_sla

            # Determine pass/fail
            prob = pass_probabilities[s_seq]
            passed = random.random() < prob

            if passed:
                s_status = "Passed"
                score = round(random.uniform(70.0, 98.0), 2)
            else:
                s_status = "Failed"
                score = round(random.uniform(35.0, 68.0), 2)
                is_active = False

            stage_records_list.append({
                "stage_record_id": f"SR-{stage_counter}",
                "application_id": app_id,
                "stage_name": s_name,
                "sequence_order": s_seq,
                "stage_entry_time": entry_time.strftime("%Y-%m-%d %H:%M:%S+05:30"),
                "stage_exit_time": exit_time.strftime("%Y-%m-%d %H:%M:%S+05:30"),
                "stage_status": s_status,
                "evaluation_score": score,
                "target_sla_hours": s_sla,
                "sla_breached_flag": sla_breached,
                "created_at": entry_time.strftime("%Y-%m-%d %H:%M:%S+05:30"),
            })

            stage_counter += 1
            # Next stage starts after exit time plus short break
            current_time = exit_time + timedelta(hours=random.randint(2, 12))

    df_stage_records = pd.DataFrame(stage_records_list)

    # Update application overall_status based on terminal stage
    terminal_status_map = {}
    for app_id, group in df_stage_records.groupby("application_id"):
        last_row = group.sort_values("sequence_order").iloc[-1]
        if last_row["stage_name"] == "Offer" and last_row["stage_status"] == "Passed":
            terminal_status_map[app_id] = "Hired"
        elif last_row["stage_status"] == "Failed":
            terminal_status_map[app_id] = "Rejected"
        else:
            terminal_status_map[app_id] = "Active"

    df_applications["overall_status"] = df_applications["application_id"].map(terminal_status_map).fillna("Active")

    # --------------------------------------------------------------------------
    # 7. GENERATE INTERVIEW SLOTS (100 records)
    # --------------------------------------------------------------------------
    print("-> Generating Interview Slots (Target: 100)...")
    slots_list = []
    slot_counter = 9001
    hiring_days = ["Day 1", "Day 2", "Day 3"]

    slot_base_dates = {
        "Day 1": datetime(2026, 2, 2, 9, 0, 0),
        "Day 2": datetime(2026, 2, 3, 9, 0, 0),
        "Day 3": datetime(2026, 2, 4, 9, 0, 0),
    }

    room_ids = df_rooms["room_id"].tolist()
    panel_ids = df_panels["panel_id"].tolist()

    for i in range(VALIDATION_SCALE["SLOTS_COUNT"]):
        day = random.choice(hiring_days)
        start_date = slot_base_dates[day]
        # Slots spaced across hours 9am - 5pm
        hour_offset = random.randint(0, 7)
        minute_offset = random.choice([0, 45])

        s_start = start_date + timedelta(hours=hour_offset, minutes=minute_offset)
        s_end = s_start + timedelta(minutes=45)

        status = random.choice(["Booked", "Completed", "Available"])

        slots_list.append({
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

    df_slots = pd.DataFrame(slots_list)

    # --------------------------------------------------------------------------
    # SAVE CSV FILES TO DATA/RAW/
    # --------------------------------------------------------------------------
    print("\n-> Exporting DataFrames to CSV files in data/raw/...")
    datasets = {
        "candidates": df_candidates,
        "companies": df_companies,
        "applications": df_applications,
        "recruitment_stage_records": df_stage_records,
        "rooms": df_rooms,
        "panels": df_panels,
        "interview_slots": df_slots,
    }

    for name, df in datasets.items():
        file_path = CSV_PATHS[name]
        df.to_csv(file_path, index=False)
        print(f"   [OK] Saved {name:<26} ({len(df):>4} rows) -> {file_path}")

    print("\n[SUCCESS] Validation dataset generation completed cleanly.")
    return datasets


if __name__ == "__main__":
    generate_validation_data()
