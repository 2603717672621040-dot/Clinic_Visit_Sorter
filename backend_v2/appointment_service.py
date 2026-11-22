
from datetime import datetime

from backend_v2.database import get_connection


APPOINTMENT_STATUSES = {
    "Booked",
    "Completed",
    "Cancelled",
    "Rescheduled"
}


def validate_date(date_text):
    """Validate date in YYYY-MM-DD format."""

    try:
        datetime.strptime(date_text, "%Y-%m-%d")
    except (ValueError, TypeError):
        raise ValueError("Date must use YYYY-MM-DD format.")


def validate_time(time_text):
    """Validate time in HH:MM 24-hour format."""

    try:
        datetime.strptime(time_text, "%H:%M")
    except (ValueError, TypeError):
        raise ValueError("Time must use HH:MM format.")


def book_appointment(
    student_name,
    appointment_date,
    appointment_time,
    student_id=None,
    purpose=""
):
    """Create a new appointment."""

    student_name = str(student_name).strip()
    appointment_date = str(appointment_date).strip()
    appointment_time = str(appointment_time).strip()

    if not student_name:
        raise ValueError("Student name is required.")

    validate_date(appointment_date)
    validate_time(appointment_time)

    student_id = (
        str(student_id).strip() or None
        if student_id is not None else None
    )

    purpose = str(purpose).strip()

    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO appointments (
                student_name,
                student_id,
                appointment_date,
                appointment_time,
                purpose
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                student_name,
                student_id,
                appointment_date,
                appointment_time,
                purpose
            )
        )

        return cursor.lastrowid


def get_appointment(appointment_id):
    """Get one appointment."""

    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT * FROM appointments
            WHERE id = ?
            """,
            (appointment_id,)
        ).fetchone()

        return dict(row) if row else None


def get_all_appointments():
    """Get all appointments in date and time order."""

    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT * FROM appointments
            ORDER BY appointment_date, appointment_time
            """
        ).fetchall()

        return [dict(row) for row in rows]


def update_appointment_status(appointment_id, status):
    """Change an appointment's status."""

    status = str(status).strip()

    if status not in APPOINTMENT_STATUSES:
        raise ValueError("Invalid appointment status.")

    with get_connection() as connection:
        cursor = connection.execute(
            """
            UPDATE appointments
            SET status = ?
            WHERE id = ?
            """,
            (status, appointment_id)
        )

        if cursor.rowcount == 0:
            raise ValueError("Appointment not found.")


def reschedule_appointment(
    appointment_id,
    new_date,
    new_time
):
    """Change the date and time of an appointment."""

    new_date = str(new_date).strip()
    new_time = str(new_time).strip()

    validate_date(new_date)
    validate_time(new_time)

    with get_connection() as connection:
        cursor = connection.execute(
            """
            UPDATE appointments
            SET appointment_date = ?,
                appointment_time = ?,
                status = 'Rescheduled'
            WHERE id = ?
            """,
            (new_date, new_time, appointment_id)
        )

        if cursor.rowcount == 0:
            raise ValueError("Appointment not found.")


def get_appointments_by_date(appointment_date):
    """Find appointments for a particular date."""

    appointment_date = str(appointment_date).strip()
    validate_date(appointment_date)

    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT * FROM appointments
            WHERE appointment_date = ?
            ORDER BY appointment_time
            """,
            (appointment_date,)
        ).fetchall()

        return [dict(row) for row in rows]
