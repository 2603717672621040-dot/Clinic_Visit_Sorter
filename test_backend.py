import pytest
import backend


@pytest.fixture
def setup_db(tmp_path, monkeypatch):
	test_db = tmp_path / "test_clinic.db"
	monkeypatch.setattr(backend, "DATABASE", str(test_db))
	backend.create_table()


def test_register_visit(setup_db):
	visit_id = backend.register_visit("Rahul", "ST101", "Headache")
	visit = backend.get_visit(visit_id)

	assert visit["student_name"] == "Rahul"
	assert visit["student_id"] == "ST101"
	assert visit["complaint"] == "Headache"


def test_empty_registration(setup_db):
	with pytest.raises(ValueError):
		backend.register_visit("", "ST101", "Headache")


def test_get_all_visits(setup_db):
	backend.register_visit("Rahul", "ST101", "Headache")
	visits = backend.get_all_visits()

	assert len(visits) == 1


def test_nurse_review(setup_db):
	visit_id = backend.register_visit("Rahul", "ST101", "Headache")
	backend.nurse_review(visit_id, "Today")

	visit = backend.get_visit(visit_id)
	assert visit["nurse_priority"] == "Today"


def test_update_status(setup_db):
	visit_id = backend.register_visit("Rahul", "ST101", "Headache")
	backend.update_status(visit_id, "Completed")

	visit = backend.get_visit(visit_id)
	assert visit["status"] == "Completed"


def test_invalid_priority(setup_db):
	with pytest.raises(ValueError):
		backend.nurse_review(1, "Urgent")


def test_invalid_status(setup_db):
	with pytest.raises(ValueError):
		backend.update_status(1, "Unknown")


def test_invalid_ai_suggestion(setup_db):
	with pytest.raises(ValueError):
		backend.save_ai_suggestion(1, "Urgent")

def test_empty_complaint_completeness():
    result = backend.check_complaint_completeness("")
    assert result["completeness"] == "Incomplete"


def test_short_complaint_completeness():
    result = backend.check_complaint_completeness("Headache")
    assert result["completeness"] == "Needs clarification"


def test_complete_complaint_completeness():
    result = backend.check_complaint_completeness(
        "I have a headache since this morning."
    )
    assert result["completeness"] == "Submitted"
