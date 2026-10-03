"""
DuckDB Analytics Warehouse Ingestion & Build Pipeline

Initializes the embedded DuckDB analytics warehouse, establishes table schemas
matching the production specification, loads all raw CSV datasets with exact data types,
verifies row counts and referential integrity, and tests analytical SQL queries.

Target Database: database/duckdb/placement_analytics.duckdb
"""

import os
import sys
import csv
import logging
from pathlib import Path
from typing import Dict, List, Tuple, Any
import duckdb

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("build_warehouse")

# Project Directory Resolution
SCRIPT_DIR = Path(__file__).resolve().parent
BASE_DIR = SCRIPT_DIR.parents[1]  # recruitment-analytics directory
DB_DIR = BASE_DIR / "database" / "duckdb"
DB_PATH = DB_DIR / "placement_analytics.duckdb"
RAW_DATA_DIR = BASE_DIR / "data" / "raw"
SQL_DIR = BASE_DIR / "sql"

# Ingestion Order: Dimension tables first, followed by fact/bridge tables
INGESTION_TABLES: List[Tuple[str, str]] = [
    ("candidates", "candidates.csv"),
    ("companies", "companies.csv"),
    ("rooms", "rooms.csv"),
    ("panels", "panels.csv"),
    ("applications", "applications.csv"),
    ("recruitment_stage_records", "recruitment_stage_records.csv"),
    ("interview_slots", "interview_slots.csv"),
]

# DDL Schema Definitions with Strict Typing and Primary/Foreign Keys
DDL_STATEMENTS = """
-- 1. Candidates Dimension
CREATE TABLE IF NOT EXISTS candidates (
    candidate_id VARCHAR PRIMARY KEY,
    full_name VARCHAR NOT NULL,
    email VARCHAR NOT NULL UNIQUE,
    phone_number VARCHAR,
    degree_program VARCHAR NOT NULL,
    academic_major VARCHAR NOT NULL,
    gpa DECIMAL(4, 2) NOT NULL,
    cgpa_band VARCHAR NOT NULL,
    graduation_year INTEGER NOT NULL,
    gender VARCHAR,
    created_at TIMESTAMPTZ NOT NULL
);

-- 2. Companies Dimension
CREATE TABLE IF NOT EXISTS companies (
    company_id VARCHAR PRIMARY KEY,
    company_name VARCHAR NOT NULL,
    industry_sector VARCHAR NOT NULL,
    priority_tier VARCHAR NOT NULL,
    contact_email VARCHAR NOT NULL,
    created_at TIMESTAMPTZ NOT NULL
);

-- 3. Rooms Dimension
CREATE TABLE IF NOT EXISTS rooms (
    room_id VARCHAR PRIMARY KEY,
    room_name VARCHAR NOT NULL,
    building_location VARCHAR,
    interview_mode VARCHAR NOT NULL,
    seating_capacity INTEGER NOT NULL
);

-- 4. Panels Dimension
CREATE TABLE IF NOT EXISTS panels (
    panel_id VARCHAR PRIMARY KEY,
    panel_code VARCHAR NOT NULL UNIQUE,
    department VARCHAR NOT NULL,
    max_daily_slots INTEGER NOT NULL DEFAULT 8
);

-- 5. Applications Fact / Bridge
CREATE TABLE IF NOT EXISTS applications (
    application_id VARCHAR PRIMARY KEY,
    candidate_id VARCHAR NOT NULL REFERENCES candidates(candidate_id),
    company_id VARCHAR NOT NULL REFERENCES companies(company_id),
    applied_role VARCHAR NOT NULL,
    overall_status VARCHAR NOT NULL,
    application_date DATE NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL
);

-- 6. Recruitment Stage Records (Funnel & SLA Fact)
CREATE TABLE IF NOT EXISTS recruitment_stage_records (
    stage_record_id VARCHAR PRIMARY KEY,
    application_id VARCHAR NOT NULL REFERENCES applications(application_id),
    stage_name VARCHAR NOT NULL,
    sequence_order INTEGER NOT NULL,
    stage_entry_time TIMESTAMPTZ NOT NULL,
    stage_exit_time TIMESTAMPTZ,
    stage_status VARCHAR NOT NULL,
    evaluation_score DECIMAL(5, 2),
    target_sla_hours INTEGER NOT NULL,
    sla_breached_flag BOOLEAN NOT NULL,
    created_at TIMESTAMPTZ NOT NULL
);

-- 7. Interview Slots (Capacity & Scheduling Fact)
CREATE TABLE IF NOT EXISTS interview_slots (
    slot_id VARCHAR PRIMARY KEY,
    company_id VARCHAR NOT NULL REFERENCES companies(company_id),
    room_id VARCHAR NOT NULL REFERENCES rooms(room_id),
    panel_id VARCHAR NOT NULL REFERENCES panels(panel_id),
    hiring_day VARCHAR NOT NULL,
    slot_start_time TIMESTAMPTZ NOT NULL,
    slot_end_time TIMESTAMPTZ NOT NULL,
    slot_status VARCHAR NOT NULL,
    created_at TIMESTAMPTZ NOT NULL
);
"""

# PostgreSQL compatibility macro for date/time formatting
COMPATIBILITY_MACROS = """
CREATE OR REPLACE MACRO to_char(ts, fmt) AS strftime(ts, 
    replace(replace(replace(replace(replace(fmt, 'YYYY', '%Y'), 'MM', '%m'), 'DD', '%d'), 'HH24', '%H'), 'MI', '%M')
);
"""


def count_csv_rows(csv_path: Path) -> int:
    """Count data rows in a CSV file excluding header."""
    with open(csv_path, mode="r", encoding="utf-8", errors="replace") as f:
        reader = csv.reader(f)
        try:
            next(reader)  # skip header
        except StopIteration:
            return 0
        return sum(1 for _ in reader)


def build_warehouse(db_path: Path = DB_PATH) -> Dict[str, Any]:
    """
    Initialize DuckDB database, apply DDL, ingest CSVs, and verify results.
    """
    logger.info("=" * 70)
    logger.info("Initializing DuckDB Analytics Warehouse Ingestion Pipeline")
    logger.info(f"Target Database: {db_path}")
    logger.info(f"Source Data Dir: {RAW_DATA_DIR}")
    logger.info("=" * 70)

    # Ensure parent directory exists
    db_path.parent.mkdir(parents=True, exist_ok=True)

    # Remove existing database file if recreating to ensure clean state
    if db_path.exists():
        logger.info("Existing database file found. Recreating for clean build...")
        try:
            db_path.unlink()
        except PermissionError:
            logger.warning(f"Could not delete {db_path}, opening existing database.")

    # Connect to DuckDB
    con = duckdb.connect(str(db_path))

    # 1. Apply Compatibility Macros
    logger.info("Registering PostgreSQL compatibility macros (to_char)...")
    con.execute(COMPATIBILITY_MACROS)

    # 2. Execute DDL Schema
    logger.info("Applying DDL schemas for 7 core entities...")
    con.execute(DDL_STATEMENTS)

    # 3. Ingest CSV Data
    audit_results: List[Dict[str, Any]] = []

    for table_name, csv_filename in INGESTION_TABLES:
        csv_file_path = RAW_DATA_DIR / csv_filename
        if not csv_file_path.exists():
            logger.error(f"Source file not found: {csv_file_path}")
            audit_results.append({
                "table": table_name,
                "csv_file": csv_filename,
                "expected_rows": 0,
                "loaded_rows": 0,
                "status": "FAILED (File Not Found)"
            })
            continue

        expected_rows = count_csv_rows(csv_file_path)
        logger.info(f"Ingesting '{table_name}' from {csv_filename} (Expected: {expected_rows:,} rows)...")

        # Load data using DuckDB native read_csv into strongly typed schema
        fpath_str = str(csv_file_path).replace("\\", "/")
        con.execute(f"INSERT INTO {table_name} SELECT * FROM read_csv('{fpath_str}', header=True)")

        # Verify row count
        actual_rows = con.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
        status = "SUCCESS" if actual_rows == expected_rows else f"MISMATCH ({actual_rows} != {expected_rows})"

        audit_results.append({
            "table": table_name,
            "csv_file": csv_filename,
            "expected_rows": expected_rows,
            "loaded_rows": actual_rows,
            "status": status
        })

    # Close connection to persist and unlock file
    con.close()

    # Generate and display validation report
    print("\n" + "=" * 78)
    print("                      WAREHOUSE VALIDATION REPORT")
    print("=" * 78)
    header = f"{'Table Name':<28} | {'CSV Rows':<10} | {'Loaded Rows':<12} | {'Load Status':<16}"
    print(header)
    print("-" * 78)
    all_success = True
    total_loaded = 0

    for res in audit_results:
        print(f"{res['table']:<28} | {res['expected_rows']:<10,} | {res['loaded_rows']:<12,} | {res['status']:<16}")
        total_loaded += res["loaded_rows"]
        if "SUCCESS" not in res["status"]:
            all_success = False

    print("-" * 78)
    print(f"{'TOTAL ROWS LOADED':<28} | {'':<10} | {total_loaded:<12,} | {'ALL PASSED' if all_success else 'ERRORS OCCURRED'}")
    print("=" * 78 + "\n")

    return {
        "db_path": str(db_path),
        "audit_results": audit_results,
        "total_rows": total_loaded,
        "success": all_success
    }


def verify_sql_scripts(db_path: Path = DB_PATH) -> bool:
    """
    Execute all analytical SQL files against the DuckDB database to ensure compatibility.
    """
    logger.info("=" * 70)
    logger.info("Executing Analytical SQL Verification Against DuckDB Warehouse")
    logger.info("=" * 70)

    con = duckdb.connect(str(db_path), read_only=True)

    sql_files = [
        SQL_DIR / "capacity" / "capacity_metrics.sql",
        SQL_DIR / "funnel" / "funnel_metrics.sql",
        SQL_DIR / "process_efficiency" / "process_metrics.sql",
    ]

    all_passed = True

    for sql_file in sql_files:
        rel_path = sql_file.relative_to(BASE_DIR)
        if not sql_file.exists():
            logger.warning(f"SQL file not found: {rel_path}")
            continue

        print(f"\nEvaluating: {rel_path}")
        print("-" * 60)

        with open(sql_file, "r", encoding="utf-8") as f:
            raw_sql = f.read()

        # Split multiple queries by semicolon
        queries = [q.strip() for q in raw_sql.split(";") if q.strip()]

        for idx, query in enumerate(queries, 1):
            try:
                result = con.execute(query).fetchall()
                print(f"  Query {idx:02d}: PASSED ({len(result):,} rows returned)")
            except Exception as e:
                print(f"  Query {idx:02d}: FAILED -> {e}")
                all_passed = False

    con.close()
    print("-" * 60)
    logger.info(f"SQL Verification Complete: {'All Queries Executed Successfully!' if all_passed else 'Some Queries Failed.'}")
    return all_passed


if __name__ == "__main__":
    result = build_warehouse()
    if result["success"]:
        sql_ok = verify_sql_scripts()
        if not sql_ok:
            sys.exit(1)
    else:
        sys.exit(1)
