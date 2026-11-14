
import json
import sqlite3
import hashlib
import hmac
import secrets

from contextlib import contextmanager
from datetime import datetime
from pathlib import Path

import streamlit as st

try:
    from google import genai
except ImportError:
    genai = None


# ==========================================
# DATABASE CONFIGURATION
# ==========================================

DATABASE = str(Path(__file__).resolve().parent / "clinic.db")

ALLOWED_CATEGORIES = ["Pending"]

ALLOWED_PRIORITIES = ["See Now", "Today", "Routine"]

ALLOWED_STATUSES = [
    "Waiting",
    "In Consultation",
    "Completed"
]

ALLOWED_ROLES = ["Admin", "Nurse", "Staff"]

ALLOWED_APPOINTMENT_STATUSES = [
    "Scheduled",
    "Completed",
    "Cancelled"
]


# ==========================================
# DATABASE CONNECTION
# ==========================================

@contextmanager
def connect_db():
    """Open a safe SQLite connection."""

    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row

    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


# ==========================================
# CREATE DATABASE TABLES
# ==========================================

def create_table():
    """Create all CLINIQ database tables."""

    with connect_db() as connection:

        # Student visits
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS visits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_name TEXT NOT NULL,
                student_id TEXT NOT NULL,
                complaint TEXT NOT NULL,
                created_at TEXT NOT NULL,
                ai_suggestion TEXT DEFAULT 'Pending',
                nurse_priority TEXT DEFAULT 'Pending Review',
                status TEXT DEFAULT 'Waiting'
            )
            """
        )

        # Clinic staff
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS staff (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL,
                active INTEGER NOT NULL DEFAULT 1,
                created_at TEXT NOT NULL
            )
            """
        )

        # Clinic appointments
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS appointments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_name TEXT NOT NULL,
                student_id TEXT NOT NULL,
                appointment_date TEXT NOT NULL,
                appointment_time TEXT NOT NULL,
                purpose TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Scheduled',
                created_at TEXT NOT NULL
            )
            """
        )


# ==========================================
# STUDENT VISIT MANAGEMENT
# ==========================================

def register_visit(student_name, student_id, complaint):
    """Register a new student visit."""

    values = [student_name, student_id, complaint]

    if not all(isinstance(value, str) for value in values):
        raise ValueError("All fields must be text.")

    student_name = student_name.strip()
    student_id = student_id.strip()
    complaint = complaint.strip()

    if not student_name or not student_id or not complaint:
        raise ValueError("All fields are required.")

    if len(student_name) > 100:
        raise ValueError("Student name is too long.")

    if len(student_id) > 30:
        raise ValueError("Student ID is too long.")

    if len(complaint) > 1000:
        raise ValueError("Complaint is too long.")

    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with connect_db() as connection:
        cursor = connection.execute(
            """
            INSERT INTO visits
            (student_name, student_id, complaint, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (student_name, student_id, complaint, created_at)
        )

        return cursor.lastrowid


def get_all_visits():
    """Return all visits, newest first."""

    with connect_db() as connection:
        rows = connection.execute(
            "SELECT * FROM visits ORDER BY id DESC"
        ).fetchall()

        return [dict(row) for row in rows]


def get_visit(visit_id):
    """Return one visit."""

    with connect_db() as connection:
        row = connection.execute(
            "SELECT * FROM visits WHERE id = ?",
            (int(visit_id),)
        ).fetchone()

        return dict(row) if row else None


def save_ai_suggestion(visit_id, suggestion):
    """Save an administrative AI category."""

    if suggestion not in ALLOWED_CATEGORIES:
        raise ValueError("Invalid AI suggestion.")

    with connect_db() as connection:
        cursor = connection.execute(
            """
            UPDATE visits
            SET ai_suggestion = ?
            WHERE id = ?
            """,
            (suggestion, int(visit_id))
        )

        if cursor.rowcount == 0:
            raise ValueError("Visit not found.")


# ==========================================
# AI ADMINISTRATIVE ASSISTANT
# ==========================================

def classify_complaint(complaint):
    """
    Administrative suggestion only.
    AI does not diagnose or determine urgency.
    """

    complaint = str(complaint).strip()

    if not complaint or genai is None:
        return "Pending"

    try:
        api_key = st.secrets.get("GEMINI_API_KEY")

        if not api_key:
            return "Pending"

        client = genai.Client(api_key=api_key)

        prompt = f"""
You are an administrative assistant for a college clinic.

Review the text only for administrative clarity.
Do not diagnose, assess symptoms, determine urgency,
recommend treatment, or assign clinical priority.

The only permitted category is Pending.
Return JSON with category set to Pending.

Student complaint:
{complaint}
"""

        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_json_schema": {
                    "type": "OBJECT",
                    "properties": {
                        "category": {
                            "type": "STRING",
                            "enum": ["Pending"]
                        }
                    },
                    "required": ["category"]
                }
            }
        )

        result = json.loads(response.text or "{}")

        return "Pending"

    except Exception:
        return "Pending"


def check_complaint_completeness(complaint):
    """Check administrative completeness only."""

    complaint = str(complaint or "").strip()

    if not complaint:
        return {
            "completeness": "Incomplete",
            "message": "Complaint details are required."
        }

    if len(complaint) < 10:
        return {
            "completeness": "Needs clarification",
            "message": "The complaint description is very brief."
        }

    return {
        "completeness": "Submitted",
        "message": "Complaint recorded for nurse review."
    }


# ==========================================
# NURSE REVIEW AND VISIT STATUS
# ==========================================

def nurse_review(visit_id, priority):
    """Store the priority independently selected by the nurse."""

    if priority not in ALLOWED_PRIORITIES:
        raise ValueError("Invalid nurse priority.")

    with connect_db() as connection:
        cursor = connection.execute(
            """
            UPDATE visits
            SET nurse_priority = ?
            WHERE id = ?
            """,
            (priority, int(visit_id))
        )

        if cursor.rowcount == 0:
            raise ValueError("Visit not found.")


def update_status(visit_id, status):
    """Update student visit status."""

    if status not in ALLOWED_STATUSES:
        raise ValueError("Invalid visit status.")

    with connect_db() as connection:
        cursor = connection.execute(
            """
            UPDATE visits
            SET status = ?
            WHERE id = ?
            """,
            (status, int(visit_id))
        )

        if cursor.rowcount == 0:
            raise ValueError("Visit not found.")


# ==========================================
# STAFF MANAGEMENT
# ==========================================

def hash_password(password):
    """Hash a password using PBKDF2."""

    salt = secrets.token_bytes(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        200000
    )

    return salt.hex() + ":" + password_hash.hex()


def verify_password(password, stored_hash):
    """Verify a staff password."""

    try:
        salt_hex, hash_hex = stored_hash.split(":")

        salt = bytes.fromhex(salt_hex)

        calculated = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            200000
        )

        return hmac.compare_digest(
            calculated.hex(),
            hash_hex
        )

    except (ValueError, TypeError):
        return False


def add_staff(full_name, username, password, role):
    """Register a new clinic staff account."""

    full_name = str(full_name).strip()
    username = str(username).strip().lower()

    if not full_name or not username or not password:
        raise ValueError("All staff fields are required.")

    if len(full_name) > 100:
        raise ValueError("Name is too long.")

    if len(username) > 50:
        raise ValueError("Username is too long.")

    if role not in ALLOWED_ROLES:
        raise ValueError("Invalid staff role.")

    if len(password) < 8:
        raise ValueError(
            "Password must contain at least 8 characters."
        )

    password_hash = hash_password(password)

    with connect_db() as connection:
        connection.execute(
            """
            INSERT INTO staff
            (full_name, username, password_hash, role, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                full_name,
                username,
                password_hash,
                role,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
        )


def get_all_staff():
    """Get staff records without password hashes."""

    with connect_db() as connection:
        rows = connection.execute(
            """
            SELECT
                id,
                full_name,
                username,
                role,
                active,
                created_at
            FROM staff
            ORDER BY id DESC
            """
        ).fetchall()

        return [dict(row) for row in rows]


def update_staff_role(staff_id, role):
    """Update a staff member's role."""

    if role not in ALLOWED_ROLES:
        raise ValueError("Invalid staff role.")

    with connect_db() as connection:
        cursor = connection.execute(
            """
            UPDATE staff
            SET role = ?
            WHERE id = ?
            """,
            (role, int(staff_id))
        )

        if cursor.rowcount == 0:
            raise ValueError("Staff member not found.")


def deactivate_staff(staff_id):
    """Deactivate a staff account."""

    with connect_db() as connection:
        cursor = connection.execute(
            """
            UPDATE staff
            SET active = 0
            WHERE id = ?
            """,
            (int(staff_id),)
        )

        if cursor.rowcount == 0:
            raise ValueError("Staff member not found.")


def authenticate_staff(username, password):
    """Authenticate an active staff account."""

    username = str(username).strip().lower()

    with connect_db() as connection:
        row = connection.execute(
            """
            SELECT *
            FROM staff
            WHERE username = ? AND active = 1
            """,
            (username,)
        ).fetchone()

        if not row:
            return None

        if verify_password(password, row["password_hash"]):
            return {
                "id": row["id"],
                "full_name": row["full_name"],
                "username": row["username"],
                "role": row["role"]
            }

        return None


# ==========================================
# APPOINTMENT MANAGEMENT
# ==========================================

def book_appointment(
    student_name,
    student_id,
    appointment_date,
    appointment_time,
    purpose
):
    """Save a new clinic appointment."""

    student_name = str(student_name).strip()
    student_id = str(student_id).strip()
    appointment_date = str(appointment_date).strip()
    appointment_time = str(appointment_time).strip()
    purpose = str(purpose).strip()

    if not all([
        student_name,
        student_id,
        appointment_date,
        appointment_time,
        purpose
    ]):
        raise ValueError("All appointment fields are required.")

    if len(student_name) > 100:
        raise ValueError("Student name is too long.")

    if len(student_id) > 30:
        raise ValueError("Student ID is too long.")

    if len(purpose) > 300:
        raise ValueError("Appointment purpose is too long.")

    try:
        datetime.strptime(appointment_date, "%Y-%m-%d")
        datetime.strptime(appointment_time, "%H:%M")
    except ValueError:
        raise ValueError("Invalid appointment date or time.")

    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with connect_db() as connection:
        cursor = connection.execute(
            """
            INSERT INTO appointments (
                student_name,
                student_id,
                appointment_date,
                appointment_time,
                purpose,
                status,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, 'Scheduled', ?)
            """,
            (
                student_name,
                student_id,
                appointment_date,
                appointment_time,
                purpose,
                created_at
            )
        )

        return cursor.lastrowid


def get_all_appointments():
    """Return appointments in date and time order."""

    with connect_db() as connection:
        rows = connection.execute(
            """
            SELECT * FROM appointments
            ORDER BY appointment_date ASC, appointment_time ASC
            """
        ).fetchall()

        return [dict(row) for row in rows]


def get_appointment(appointment_id):
    """Retrieve one appointment."""

    with connect_db() as connection:
        row = connection.execute(
            "SELECT * FROM appointments WHERE id = ?",
            (int(appointment_id),)
        ).fetchone()

        return dict(row) if row else None


def update_appointment_status(appointment_id, status):
    """Update an appointment's administrative status."""

    if status not in ALLOWED_APPOINTMENT_STATUSES:
        raise ValueError("Invalid appointment status.")

    with connect_db() as connection:
        cursor = connection.execute(
            """
            UPDATE appointments
            SET status = ?
            WHERE id = ?
            """,
            (status, int(appointment_id))
        )

        if cursor.rowcount == 0:
            raise ValueError("Appointment not found.")


# ==========================================
# INITIALIZE DATABASE
# ==========================================

create_table()
