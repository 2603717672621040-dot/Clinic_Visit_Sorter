
from pathlib import Path
import sqlite3

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATABASE = PROJECT_DIR / "clinic_v2.db"


def get_connection():
    connection = sqlite3.connect(str(DATABASE), timeout=30)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database():
    with get_connection() as connection:

        connection.execute("""
            CREATE TABLE IF NOT EXISTS visits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_name TEXT NOT NULL,
                student_id TEXT,
                complaint TEXT NOT NULL,
                arrival_time TEXT NOT NULL,
                category TEXT DEFAULT 'unknown',
                ai_priority TEXT DEFAULT 'pending_review',
                ai_summary TEXT DEFAULT '',
                ai_reviewed INTEGER DEFAULT 0,
                nurse_priority TEXT DEFAULT 'Pending',
                nurse_notes TEXT DEFAULT '',
                status TEXT DEFAULT 'Waiting',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS staff (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                username TEXT NOT NULL UNIQUE COLLATE NOCASE,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL,
                active INTEGER DEFAULT 1,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS appointments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_name TEXT NOT NULL,
                student_id TEXT,
                appointment_date TEXT NOT NULL,
                appointment_time TEXT NOT NULL,
                purpose TEXT DEFAULT '',
                status TEXT DEFAULT 'Booked',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        connection.execute("""
            CREATE INDEX IF NOT EXISTS idx_visits_arrival
            ON visits(arrival_time)
        """)

        connection.execute("""
            CREATE INDEX IF NOT EXISTS idx_visits_status
            ON visits(status)
        """)

        connection.execute("""
            CREATE INDEX IF NOT EXISTS idx_appointments_date
            ON appointments(appointment_date)
        """)


def database_health():
    with get_connection() as connection:
        connection.execute("SELECT 1")
        return {
            "status": "connected",
            "database": str(DATABASE)
        }


initialize_database()
