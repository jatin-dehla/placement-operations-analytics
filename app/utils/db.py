"""
DuckDB Database Utility Module

Provides cached, thread-safe, read-only connections to the
placement_analytics.duckdb warehouse. Automatically registers
dialect compatibility macros and exposes query execution helpers.
"""

import os
from pathlib import Path
from typing import Optional, List, Any
import duckdb
import pandas as pd
import streamlit as st


def get_warehouse_path() -> str:
    """Resolve the absolute path to placement_analytics.duckdb."""
    cwd = Path.cwd()
    this_dir = Path(__file__).resolve().parent

    candidate_paths = [
        cwd / "database" / "duckdb" / "placement_analytics.duckdb",
        cwd / "recruitment-analytics" / "database" / "duckdb" / "placement_analytics.duckdb",
        this_dir.parent.parent / "database" / "duckdb" / "placement_analytics.duckdb",
        this_dir.parent.parent.parent / "database" / "duckdb" / "placement_analytics.duckdb",
        this_dir.parent.parent.parent / "recruitment-analytics" / "database" / "duckdb" / "placement_analytics.duckdb",
    ]

    for path in candidate_paths:
        if path.is_file():
            return str(path.resolve())

    raise FileNotFoundError(
        "Could not locate 'placement_analytics.duckdb'. "
        f"Searched in: {[str(p) for p in candidate_paths]}"
    )


@st.cache_resource
def get_duckdb_connection():
    """Establish and cache a read-only DuckDB connection."""
    db_path = get_warehouse_path()
    conn = duckdb.connect(database=db_path, read_only=True)

    # Register PostgreSQL compatibility macro for TO_CHAR if not already present
    try:
        conn.execute("""
            CREATE OR REPLACE MACRO to_char(ts, fmt) AS (
                strftime(ts, REPLACE(REPLACE(fmt, 'HH24:00', '%H:00'), 'HH24', '%H'))
            );
        """)
    except Exception:
        pass

    return conn


def get_warehouse_mtime() -> float:
    """Return the last modified timestamp of the DuckDB warehouse file for cache invalidation."""
    try:
        db_path = get_warehouse_path()
        return os.path.getmtime(db_path)
    except Exception:
        return 0.0


def clear_warehouse_cache():
    """Explicitly invalidate all cached query and connection resources."""
    st.cache_data.clear()
    st.cache_resource.clear()


@st.cache_data(ttl=300, show_spinner=False)
def _run_query_cached(query_sql: str, params_tuple: Optional[tuple], db_mtime: float) -> pd.DataFrame:
    """Execute cached analytical SQL query against DuckDB."""
    conn = get_duckdb_connection()
    try:
        if params_tuple:
            df = conn.execute(query_sql, list(params_tuple)).df()
        else:
            df = conn.execute(query_sql).df()
        return df
    except Exception as e:
        st.error(f"DuckDB Query Error: {e}")
        return pd.DataFrame()


def run_query(query_sql: str, params: Optional[List[Any]] = None) -> pd.DataFrame:
    """
    Execute an analytical SQL query against DuckDB and return a Pandas DataFrame.
    Automatically invalidates cache whenever the warehouse file is modified.
    """
    db_mtime = get_warehouse_mtime()
    params_tuple = tuple(params) if params else None
    return _run_query_cached(query_sql, params_tuple, db_mtime)


def check_warehouse_health() -> dict:
    """Verify record counts across all 7 warehouse tables."""
    conn = get_duckdb_connection()
    tables = [
        "candidates", "companies", "panels", "rooms",
        "applications", "recruitment_stage_records", "interview_slots"
    ]
    counts = {}
    total = 0
    for tbl in tables:
        try:
            cnt = conn.execute(f"SELECT COUNT(*) FROM {tbl}").fetchone()[0]
            counts[tbl] = cnt
            total += cnt
        except Exception as e:
            counts[tbl] = f"Error: {e}"
    counts["total_warehouse_records"] = total
    return counts
