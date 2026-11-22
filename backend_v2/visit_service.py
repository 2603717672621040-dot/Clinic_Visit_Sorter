
from datetime import datetime

from backend_v2.database import get_connection


AI_CATEGORIES = {"injury", "illness", "other", "unknown"}

AI_PRIORITIES = {
    "see_now",
    "today",
    "routine",
    "pending_review"
}

NURSE_PRIORITIES = {
    "Pending",
    "See Now",
    "Today",
    "Routine"
}

VISIT_STATUSES = {
    "Waiting",
    "In Review",
    "Completed",
    "Cancelled"
}


def register_visit(student_name, complaint, student_id=None):
    """Register a new student visit."""

    student_name = str(student_name).strip()
    complaint = str(complaint).strip()

    if not student_name:
        raise ValueError("Student name is required.")

    if not complaint:
        raise ValueError("Complaint is required.")

    if student_id is not None:
        student_id = str(student_id).strip() or None

    arrival_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO visits (
                student_name,
                student_id,
                complaint,
                arrival_time
            )
            VALUES (?, ?, ?, ?)
            """,
            (student_name, student_id, complaint, arrival_time)
        )

        return cursor.lastrowid


def get_visit(visit_id):
    """Get one visit using its ID."""

    with get_connection() as connection:
        row = connection.execute(
            "SELECT * FROM visits WHERE id = ?",
            (visit_id,)
        ).fetchone()

        return dict(row) if row else None


def get_all_visits():
    """Get all visits, newest arrivals first."""

    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT * FROM visits
            ORDER BY arrival_time DESC, id DESC
            """
        ).fetchall()

        return [dict(row) for row in rows]


def search_visits(search_text):
    """Search visits by student name, ID, or complaint."""

    search_text = str(search_text).strip()

    if not search_text:
        return get_all_visits()

    pattern = f"%{search_text}%"

    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT * FROM visits
            WHERE student_name LIKE ?
               OR student_id LIKE ?
               OR complaint LIKE ?
            ORDER BY arrival_time DESC, id DESC
            """,
            (pattern, pattern, pattern)
        ).fetchall()

        return [dict(row) for row in rows]


def save_ai_suggestion(
    visit_id,
    category,
    priority,
    summary
):
    """Save an AI suggestion without changing nurse decisions."""

    category = str(category).strip().lower()
    priority = str(priority).strip().lower()
    summary = str(summary).strip()

    if category not in AI_CATEGORIES:
        raise ValueError("Invalid AI category.")

    if priority not in AI_PRIORITIES:
        raise ValueError("Invalid AI priority.")

    if not summary:
        raise ValueError("AI summary is required.")

    with get_connection() as connection:
        cursor = connection.execute(
            """
            UPDATE visits
            SET category = ?,
                ai_priority = ?,
                ai_summary = ?,
                ai_reviewed = 0
            WHERE id = ?
            """,
            (category, priority, summary, visit_id)
        )

        if cursor.rowcount == 0:
            raise ValueError("Visit not found.")


def update_nurse_review(
    visit_id,
    priority,
    notes=""
):
    """Save the nurse's independent final review."""

    priority = str(priority).strip()

    if priority not in NURSE_PRIORITIES:
        raise ValueError("Invalid nurse priority.")

    with get_connection() as connection:
        cursor = connection.execute(
            """
            UPDATE visits
            SET nurse_priority = ?,
                nurse_notes = ?,
                ai_reviewed = 1
            WHERE id = ?
            """,
            (priority, str(notes).strip(), visit_id)
        )

        if cursor.rowcount == 0:
            raise ValueError("Visit not found.")


def update_visit_status(visit_id, status):
    """Update the administrative visit status."""

    status = str(status).strip()

    if status not in VISIT_STATUSES:
        raise ValueError("Invalid visit status.")

    with get_connection() as connection:
        cursor = connection.execute(
            """
            UPDATE visits
            SET status = ?
            WHERE id = ?
            """,
            (status, visit_id)
        )

        if cursor.rowcount == 0:
            raise ValueError("Visit not found.")


def get_visit_counts():
    """Return simple visit dashboard counts."""

    with get_connection() as connection:
        total = connection.execute(
            "SELECT COUNT(*) FROM visits"
        ).fetchone()[0]

        waiting = connection.execute(
            "SELECT COUNT(*) FROM visits WHERE status = 'Waiting'"
        ).fetchone()[0]

        completed = connection.execute(
            "SELECT COUNT(*) FROM visits WHERE status = 'Completed'"
        ).fetchone()[0]

        return {
            "total": total,
            "waiting": waiting,
            "completed": completed
        }
