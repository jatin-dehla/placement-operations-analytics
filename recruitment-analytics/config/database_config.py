"""
Database & Validation Pipeline Configuration

Defines directory paths, validation dataset scale targets, and file locations.
"""

import os
from typing import Dict

# Base Directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_DATA_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, "processed")

# Ensure raw data directory exists
os.makedirs(RAW_DATA_DIR, exist_ok=True)

# Validation Dataset Target Scales
VALIDATION_SCALE: Dict[str, int] = {
    "CANDIDATES_COUNT": 50,
    "COMPANIES_COUNT": 10,
    "APPLICATIONS_COUNT": 200,
    "STAGE_RECORDS_TARGET": 1000,
    "ROOMS_COUNT": 10,
    "PANELS_COUNT": 15,
    "SLOTS_COUNT": 100,
}

# Raw CSV File Paths
CSV_PATHS: Dict[str, str] = {
    "candidates": os.path.join(RAW_DATA_DIR, "candidates.csv"),
    "companies": os.path.join(RAW_DATA_DIR, "companies.csv"),
    "applications": os.path.join(RAW_DATA_DIR, "applications.csv"),
    "recruitment_stage_records": os.path.join(RAW_DATA_DIR, "recruitment_stage_records.csv"),
    "rooms": os.path.join(RAW_DATA_DIR, "rooms.csv"),
    "panels": os.path.join(RAW_DATA_DIR, "panels.csv"),
    "interview_slots": os.path.join(RAW_DATA_DIR, "interview_slots.csv"),
}
