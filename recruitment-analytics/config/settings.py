"""
Configuration Settings Module

Centralized parameters for recruitment analytics engine and scale benchmarks.
Approved Entities: candidates, companies, applications, recruitment_stages,
                   interview_slots, rooms, panels
"""

import os
from typing import Dict, Any


class Settings:
    """Central configuration class with updated scale assumptions."""

    # Database Defaults
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("DB_PORT", 5432))
    DB_NAME: str = os.getenv("DB_NAME", "recruitment_analytics")
    DB_USER: str = os.getenv("DB_USER", "postgres")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
    DB_SCHEMA: str = os.getenv("DB_SCHEMA", "public")

    # Approved Scale Assumptions
    TARGET_CANDIDATE_COUNT: int = 1250        # Range: 1000 - 1500
    TARGET_COMPANY_COUNT: int = 200          # Range: 150 - 300
    TARGET_APPLICATION_COUNT: int = 6000      # Range: 4000 - 8000
    TARGET_STAGE_RECORD_COUNT: int = 40000    # Range: 20000 - 60000

    # Path Settings
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR: str = os.path.join(BASE_DIR, "data")
    RAW_DATA_DIR: str = os.path.join(DATA_DIR, "raw")
    PROCESSED_DATA_DIR: str = os.path.join(DATA_DIR, "processed")
    OUTPUTS_DIR: str = os.path.join(BASE_DIR, "outputs")

    @classmethod
    def get_db_connection_url(cls) -> str:
        """Construct PostgreSQL SQLAlchemy Connection URL."""
        return f"postgresql://{cls.DB_USER}:{cls.DB_PASSWORD}@{cls.DB_HOST}:{cls.DB_PORT}/{cls.DB_NAME}"
