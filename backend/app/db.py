import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "monitoring.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS alert_config (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            psi_warning REAL NOT NULL DEFAULT 0.10,
            psi_critical REAL NOT NULL DEFAULT 0.20,
            precision_drop_warning REAL NOT NULL DEFAULT 0.03,
            precision_drop_critical REAL NOT NULL DEFAULT 0.08,
            recall_drop_warning REAL NOT NULL DEFAULT 0.05,
            recall_drop_critical REAL NOT NULL DEFAULT 0.12,
            quality_drift_warning REAL NOT NULL DEFAULT 0.20,
            business_impact_warning REAL NOT NULL DEFAULT 1000000
        )
        """
    )
    conn.execute(
        "INSERT OR IGNORE INTO alert_config (id, psi_warning, psi_critical, precision_drop_warning, precision_drop_critical, recall_drop_warning, recall_drop_critical, quality_drift_warning, business_impact_warning) VALUES (1, 0.10, 0.20, 0.03, 0.08, 0.05, 0.12, 0.20, 1000000)"
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS investigation_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            summary TEXT NOT NULL,
            classification TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()
