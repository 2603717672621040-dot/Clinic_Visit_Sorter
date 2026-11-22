
import csv
import io
from collections import Counter
from datetime import datetime

from backend_v2.ai_service import fallback_result


# =========================================================
# CSV SETTINGS
# =========================================================

MIN_CSV_ROWS = 20
MAX_CSV_ROWS = 100

REQUIRED_VISIT_COLUMNS = {"id", "time", "note"}

PRIORITY_ORDER = {
    "see_now": 0,
    "today": 1,
    "routine": 2
}

ALLOWED_CATEGORIES = {
    "injury",
    "fever_cold",
    "stomach",
    "pain",
    "allergy",
    "other"
}


# =========================================================
# ARRIVAL TIME SORTING
# =========================================================

def get_time_sort_key(value):
    """Convert arrival time into a sortable value."""

    value = str(value).strip()

    formats = [
        "%H:%M",
        "%H:%M:%S",
        "%I:%M %p",
        "%I:%M:%S %p",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S"
    ]

    for time_format in formats:
        try:
            parsed = datetime.strptime(value, time_format)
            return (0, parsed.hour, parsed.minute,
                    parsed.second, value)
        except ValueError:
            continue

    return (1, 0, 0, 0, value.lower())


# =========================================================
# READ ASSIGNMENT CSV
# =========================================================

def read_visits_csv(file_content):
    """
    Read visits.csv using id,time,note format.
    Supports UTF-8 and Tamil text.
    """

    if isinstance(file_content, bytes):
        try:
            file_content = file_content.decode("utf-8-sig")
        except UnicodeDecodeError:
            raise ValueError("CSV must use UTF-8 encoding.")

    if not isinstance(file_content, str) or not file_content.strip():
        raise ValueError("CSV file is empty.")

    reader = csv.DictReader(io.StringIO(file_content))

    if not reader.fieldnames:
        raise ValueError("CSV must contain a header row.")

    reader.fieldnames = [
        str(name).strip().lower() if name else ""
        for name in reader.fieldnames
    ]

    if len(reader.fieldnames) != len(set(reader.fieldnames)):
        raise ValueError("CSV contains duplicate column names.")

    missing = REQUIRED_VISIT_COLUMNS - set(reader.fieldnames)

    if missing:
        raise ValueError(
            "Missing required columns: "
            + ", ".join(sorted(missing))
        )

    records = []

    for row_number, row in enumerate(reader, start=2):

        if row_number > MAX_CSV_ROWS + 1:
            raise ValueError(
                f"Maximum allowed visits: {MAX_CSV_ROWS}."
            )

        visit_id = str(row.get("id") or "").strip()
        visit_time = str(row.get("time") or "").strip()
        note = str(row.get("note") or "").strip()

        if not visit_id and not visit_time and not note:
            continue

        if not visit_id or not visit_time or not note:
            raise ValueError(
                f"Row {row_number}: ID, time and note are required."
            )

        records.append({
            "id": visit_id,
            "time": visit_time,
            "note": note
        })

    if len(records) < MIN_CSV_ROWS:
        raise ValueError(
            f"At least {MIN_CSV_ROWS} valid visit notes are required. "
            f"Found {len(records)}."
        )

    if len({record["id"] for record in records}) != len(records):
        raise ValueError("Visit IDs must be unique.")

    return records


# =========================================================
# CLASSIFY ALL VISITS
# =========================================================

def process_visit_records(records, classifier):
    """
    Classify every visit.
    Keep every original note.
    Sort by priority and arrival time.
    """

    if not isinstance(records, list):
        raise ValueError("Records must be a list.")

    if not callable(classifier):
        raise ValueError("A valid AI classifier is required.")

    results = []

    for record in records:

        note = str(record.get("note", "")).strip()

        try:
            ai_result = classifier(note)

            if not isinstance(ai_result, dict):
                raise ValueError("Invalid classifier response.")

            category = str(
                ai_result.get("category", "other")
            ).strip().lower()

            priority = str(
                ai_result.get("priority", "today")
            ).strip().lower()

            summary = str(
                ai_result.get("summary", "Nurse review required")
            ).strip()

            if category not in ALLOWED_CATEGORIES:
                category = "other"

            if priority not in PRIORITY_ORDER:
                priority = "today"

        except Exception:
            # Never remove a visit if classification fails.
            ai_result = fallback_result(note)

            category = ai_result["category"]
            priority = ai_result["priority"]
            summary = ai_result["summary"]

        results.append({
            "id": str(record.get("id", "")),
            "time": str(record.get("time", "")),
            "note": note,
            "category": category,
            "priority": priority,
            "summary": summary
        })

    # Most urgent first, then arrival time.
    results.sort(
        key=lambda item: (
            PRIORITY_ORDER.get(item["priority"], 1),
            get_time_sort_key(item["time"])
        )
    )

    return results


# =========================================================
# OUTPUT 1: NURSE QUEUE CSV
# =========================================================

def export_nurse_queue_csv(results):
    """
    Generate nurse_queue.csv.

    Contains every visit and original complaint.
    Most urgent visits appear first.
    """

    if not isinstance(results, list):
        raise ValueError("Results must be a list.")

    sorted_results = sorted(
        results,
        key=lambda item: (
            PRIORITY_ORDER.get(item.get("priority"), 1),
            get_time_sort_key(item.get("time", ""))
        )
    )

    output = io.StringIO()

    fieldnames = [
        "id",
        "time",
        "note",
        "category",
        "priority",
        "summary"
    ]

    writer = csv.DictWriter(
        output,
        fieldnames=fieldnames,
        extrasaction="ignore"
    )

    writer.writeheader()

    for item in sorted_results:
        writer.writerow({
            field: item.get(field, "")
            for field in fieldnames
        })

    return output.getvalue()


# Backward compatibility with the previous function name.
def export_processed_visits_csv(results):
    """Legacy function name; returns the new nurse queue CSV."""

    return export_nurse_queue_csv(results)


# =========================================================
# OUTPUT 2: SUMMARY TEXT
# =========================================================

def build_summary_report(results):
    """
    Generate summary.txt.

    Includes priority, category and arrival-hour counts.
    Does not include original student notes.
    """

    if not isinstance(results, list):
        raise ValueError("Results must be a list.")

    priority_counts = Counter()
    category_counts = Counter()
    hour_counts = Counter()

    for item in results:

        priority = item.get("priority", "today")
        category = item.get("category", "other")

        priority_counts[priority] += 1
        category_counts[category] += 1

        time_value = str(item.get("time", "")).strip()
        time_key = get_time_sort_key(time_value)

        if time_key[0] == 0:
            hour_counts[time_key[1]] += 1
        else:
            hour_counts["Unknown"] += 1

    lines = [
        "CLINIC VISIT SORTER - SUMMARY REPORT",
        "=" * 45,
        "",
        f"Total visits processed: {len(results)}",
        "",
        "1. PRIORITY COUNTS",
        "-" * 30,
        f"See Now: {priority_counts.get('see_now', 0)}",
        f"Today: {priority_counts.get('today', 0)}",
        f"Routine: {priority_counts.get('routine', 0)}",
        "",
        "2. CATEGORY COUNTS",
        "-" * 30
    ]

    for category in [
        "injury",
        "fever_cold",
        "stomach",
        "pain",
        "allergy",
        "other"
    ]:
        lines.append(
            f"{category}: {category_counts.get(category, 0)}"
        )

    lines.extend([
        "",
        "3. ARRIVAL COUNTS BY HOUR",
        "-" * 30
    ])

    for hour in range(24):
        lines.append(
            f"{hour:02d}:00 - {hour:02d}:59: "
            f"{hour_counts.get(hour, 0)}"
        )

    if hour_counts.get("Unknown", 0):
        lines.append(
            f"Unknown arrival time: {hour_counts['Unknown']}"
        )

    lines.extend([
        "",
        "SAFETY NOTICE",
        "-" * 30,
        "AI classifications are administrative suggestions only.",
        "A qualified nurse must review every visit.",
        "Potential emergency warning signs require immediate",
        "human attention.",
        "",
        "This report contains counts only and no student notes.",
        ""
    ])

    return "\n".join(lines)


# =========================================================
# BACKWARD COMPATIBILITY
# =========================================================

REQUIRED_COLUMNS = {"complaint"}

OPTIONAL_COLUMNS = {
    "student_name",
    "student_id",
    "arrival_time"
}


def read_complaints_csv(file_content):
    """Read the older complaint CSV format."""

    if isinstance(file_content, bytes):
        try:
            file_content = file_content.decode("utf-8-sig")
        except UnicodeDecodeError:
            raise ValueError("CSV file must use UTF-8 encoding.")

    if not isinstance(file_content, str) or not file_content.strip():
        raise ValueError("CSV file is empty.")

    reader = csv.DictReader(io.StringIO(file_content))

    if not reader.fieldnames:
        raise ValueError("CSV must contain a header row.")

    reader.fieldnames = [
        str(name).strip().lower() if name else ""
        for name in reader.fieldnames
    ]

    missing = REQUIRED_COLUMNS - set(reader.fieldnames)

    if missing:
        raise ValueError(
            "Missing required CSV column: "
            + ", ".join(sorted(missing))
        )

    records = []

    for row_number, row in enumerate(reader, start=2):

        if row_number > MAX_CSV_ROWS + 1:
            raise ValueError(
                f"CSV cannot contain more than {MAX_CSV_ROWS} data rows."
            )

        complaint = str(row.get("complaint") or "").strip()

        if not complaint:
            continue

        records.append({
            "student_name": str(
                row.get("student_name") or "Unknown"
            ).strip(),
            "student_id": str(
                row.get("student_id") or ""
            ).strip(),
            "arrival_time": str(
                row.get("arrival_time") or ""
            ).strip(),
            "complaint": complaint
        })

    return records


def export_results_csv(results):
    """Export results in the older CLINIQ format."""

    if not isinstance(results, list):
        raise ValueError("Results must be a list.")

    output = io.StringIO()

    fieldnames = [
        "student_name",
        "student_id",
        "arrival_time",
        "complaint",
        "category",
        "priority",
        "summary"
    ]

    writer = csv.DictWriter(
        output,
        fieldnames=fieldnames,
        extrasaction="ignore"
    )

    writer.writeheader()

    for result in results:
        writer.writerow({
            field: result.get(field, "")
            for field in fieldnames
        })

    return output.getvalue()


def get_csv_summary(records):
    """Return basic statistics for imported records."""

    if not isinstance(records, list):
        raise ValueError("Records must be a list.")

    return {
        "total_records": len(records),
        "valid_complaints": sum(
            1 for record in records
            if str(record.get("complaint", "")).strip()
        ),
        "empty_complaints": sum(
            1 for record in records
            if not str(record.get("complaint", "")).strip()
        )
    }

# =========================================================
# ASSIGNMENT REQUIRED FUNCTIONS
# =========================================================

def load_visits(file_content):
    """Assignment-required name for loading visit records."""
    return read_visits_csv(file_content)


def write_reports(results, output_dir="."):
    """Write the nurse queue and management summary files."""

    from pathlib import Path

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    nurse_csv = export_nurse_queue_csv(results)
    summary_text = build_summary_report(results)

    nurse_file = output_path / "nurse_queue.csv"
    summary_file = output_path / "summary.txt"

    nurse_file.write_text(
        nurse_csv,
        encoding="utf-8-sig"
    )

    summary_file.write_text(
        summary_text,
        encoding="utf-8"
    )

    return {
        "nurse_queue": str(nurse_file),
        "summary": str(summary_file)
    }
