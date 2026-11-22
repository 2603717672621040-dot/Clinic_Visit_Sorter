
import pytest

from backend_v2.database import get_connection
from backend_v2 import (
    register_visit,
    get_visit,
    get_all_visits,
    search_visits,
    save_ai_suggestion,
    update_nurse_review,
    update_visit_status,
    get_visit_counts,
    add_staff,
    authenticate_staff,
    get_all_staff,
    deactivate_staff,
    reactivate_staff,
    book_appointment,
    get_appointment,
    get_all_appointments,
    update_appointment_status,
    reschedule_appointment,
    get_appointments_by_date,
    validate_ai_result,
    read_complaints_csv,
    export_results_csv,
    get_csv_summary
)


@pytest.fixture(autouse=True)
def clean_database():
    """Keep each test independent using the new v2 database."""

    with get_connection() as connection:
        connection.execute("DELETE FROM visits")
        connection.execute("DELETE FROM staff")
        connection.execute("DELETE FROM appointments")
        connection.execute(
            "DELETE FROM sqlite_sequence WHERE name IN "
            "('visits', 'staff', 'appointments')"
        )


def test_register_and_get_visit():
    visit_id = register_visit(
        "Student One",
        "Twisted ankle",
        "ST001"
    )

    visit = get_visit(visit_id)

    assert visit["student_name"] == "Student One"
    assert visit["complaint"] == "Twisted ankle"
    assert visit["student_id"] == "ST001"


def test_empty_visit_is_rejected():
    with pytest.raises(ValueError):
        register_visit("", "Headache")


def test_search_visits():
    register_visit("Student Two", "Fever", "ST002")

    results = search_visits("Fever")

    assert len(results) == 1
    assert results[0]["student_name"] == "Student Two"


def test_save_ai_suggestion():
    visit_id = register_visit("Student Three", "Swollen ankle")

    save_ai_suggestion(
        visit_id,
        "injury",
        "today",
        "Swollen ankle reported"
    )

    visit = get_visit(visit_id)

    assert visit["category"] == "injury"
    assert visit["ai_priority"] == "today"
    assert visit["ai_reviewed"] == 0


def test_invalid_ai_category():
    visit_id = register_visit("Student Four", "Cough")

    with pytest.raises(ValueError):
        save_ai_suggestion(
            visit_id,
            "invalid",
            "today",
            "Test summary"
        )


def test_nurse_review():
    visit_id = register_visit("Student Five", "Pain")

    update_nurse_review(
        visit_id,
        "See Now",
        "Nurse review completed"
    )

    visit = get_visit(visit_id)

    assert visit["nurse_priority"] == "See Now"
    assert visit["ai_reviewed"] == 1


def test_visit_status():
    visit_id = register_visit("Student Six", "Cold")

    update_visit_status(visit_id, "Completed")

    assert get_visit(visit_id)["status"] == "Completed"


def test_visit_counts():
    register_visit("Student Seven", "Fever")

    counts = get_visit_counts()

    assert counts["total"] == 1
    assert counts["waiting"] == 1
    assert counts["completed"] == 0


def test_staff_login():
    add_staff(
        "Nurse One",
        "nurse_test",
        "SecurePass123",
        "Nurse"
    )

    staff = authenticate_staff(
        "NURSE_TEST",
        "SecurePass123"
    )

    assert staff is not None
    assert staff["role"] == "Nurse"


def test_wrong_password():
    add_staff(
        "Nurse Two",
        "nurse_wrong",
        "SecurePass123",
        "Nurse"
    )

    assert authenticate_staff(
        "nurse_wrong",
        "WrongPassword"
    ) is None


def test_duplicate_staff_username():
    add_staff(
        "Admin One",
        "admin_test",
        "SecurePass123",
        "Admin"
    )

    with pytest.raises(ValueError):
        add_staff(
            "Admin Two",
            "ADMIN_TEST",
            "SecurePass123",
            "Admin"
        )


def test_staff_password_is_not_exposed():
    add_staff(
        "Staff One",
        "staff_test",
        "SecurePass123",
        "Staff"
    )

    staff = get_all_staff()

    assert "password_hash" not in staff[0]


def test_deactivate_and_reactivate_staff():
    staff_id = add_staff(
        "Staff Two",
        "staff_active",
        "SecurePass123",
        "Staff"
    )

    deactivate_staff(staff_id)

    assert authenticate_staff(
        "staff_active",
        "SecurePass123"
    ) is None

    reactivate_staff(staff_id)

    assert authenticate_staff(
        "staff_active",
        "SecurePass123"
    ) is not None


def test_book_and_get_appointment():
    appointment_id = book_appointment(
        "Student Eight",
        "2026-12-01",
        "10:30",
        "ST008",
        "General visit"
    )

    appointment = get_appointment(appointment_id)

    assert appointment["student_name"] == "Student Eight"
    assert appointment["appointment_date"] == "2026-12-01"
    assert appointment["appointment_time"] == "10:30"


def test_invalid_appointment_date():
    with pytest.raises(ValueError):
        book_appointment(
            "Student Nine",
            "01-12-2026",
            "10:30"
        )


def test_appointment_status():
    appointment_id = book_appointment(
        "Student Ten",
        "2026-12-02",
        "11:00"
    )

    update_appointment_status(
        appointment_id,
        "Completed"
    )

    assert get_appointment(appointment_id)["status"] == "Completed"


def test_reschedule_appointment():
    appointment_id = book_appointment(
        "Student Eleven",
        "2026-12-03",
        "09:00"
    )

    reschedule_appointment(
        appointment_id,
        "2026-12-04",
        "12:00"
    )

    appointment = get_appointment(appointment_id)

    assert appointment["appointment_date"] == "2026-12-04"
    assert appointment["appointment_time"] == "12:00"
    assert appointment["status"] == "Rescheduled"


def test_get_appointments_by_date():
    book_appointment(
        "Student Twelve",
        "2026-12-05",
        "09:30"
    )

    results = get_appointments_by_date("2026-12-05")

    assert len(results) == 1


def test_csv_import():
    content = (
        "student_name,student_id,complaint\n"
        "Student A,ST101,Headache\n"
        "Student B,ST102,Ankle swelling\n"
    )

    records = read_complaints_csv(content)

    assert len(records) == 2
    assert records[0]["complaint"] == "Headache"


def test_csv_missing_complaint_column():
    content = "student_name,student_id\nStudent A,ST101"

    with pytest.raises(ValueError):
        read_complaints_csv(content)


def test_csv_export():
    results = [{
        "student_name": "Student A",
        "student_id": "ST101",
        "complaint": "Headache",
        "category": "illness",
        "priority": "today",
        "summary": "Headache reported"
    }]

    exported = export_results_csv(results)

    assert "Student A" in exported
    assert "Headache" in exported


def test_csv_summary():
    records = [
        {"complaint": "Fever"},
        {"complaint": ""},
        {"complaint": "Cough"}
    ]

    summary = get_csv_summary(records)

    assert summary["total_records"] == 3
    assert summary["valid_complaints"] == 2
    assert summary["empty_complaints"] == 1


def test_ai_result_validation():
    result = validate_ai_result({
        "category": "injury",
        "priority": "today",
        "summary": "Twisted ankle"
    })

    assert result["category"] == "injury"
    assert result["priority"] == "today"


def test_invalid_ai_result_defaults_safely():
    result = validate_ai_result({
        "category": "unknown_category",
        "priority": "urgent",
        "summary": "Test complaint"
    })

    assert result["category"] == "other"
    assert result["priority"] == "today"


