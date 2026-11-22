
import hashlib
import hmac
import os

from backend_v2.database import get_connection


ALLOWED_ROLES = {"Admin", "Nurse", "Staff"}


def hash_password(password):
    """Create a secure PBKDF2 password hash."""

    if not isinstance(password, str) or len(password) < 8:
        raise ValueError("Password must contain at least 8 characters.")

    salt = os.urandom(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        310000
    )

    return (
        "pbkdf2_sha256$310000$"
        + salt.hex()
        + "$"
        + password_hash.hex()
    )


def verify_password(password, stored_hash):
    """Verify a password against its stored hash."""

    try:
        algorithm, iterations, salt_hex, hash_hex = stored_hash.split("$")

        if algorithm != "pbkdf2_sha256":
            return False

        calculated_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            bytes.fromhex(salt_hex),
            int(iterations)
        )

        return hmac.compare_digest(
            calculated_hash.hex(),
            hash_hex
        )

    except (ValueError, TypeError, AttributeError):
        return False


def add_staff(full_name, username, password, role):
    """Create a new staff account."""

    full_name = str(full_name).strip()
    username = str(username).strip()
    role = str(role).strip()

    if not full_name:
        raise ValueError("Full name is required.")

    if not username:
        raise ValueError("Username is required.")

    if len(username) < 3:
        raise ValueError("Username must contain at least 3 characters.")

    if role not in ALLOWED_ROLES:
        raise ValueError("Invalid staff role.")

    password_hash = hash_password(password)

    with get_connection() as connection:
        try:
            cursor = connection.execute(
                """
                INSERT INTO staff (
                    full_name,
                    username,
                    password_hash,
                    role
                )
                VALUES (?, ?, ?, ?)
                """,
                (full_name, username, password_hash, role)
            )

            return cursor.lastrowid

        except Exception as error:
            if "UNIQUE constraint failed" in str(error):
                raise ValueError("Username already exists.") from error
            raise


def authenticate_staff(username, password):
    """Authenticate an active staff account."""

    username = str(username).strip()

    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT * FROM staff
            WHERE username = ? COLLATE NOCASE
              AND active = 1
            """,
            (username,)
        ).fetchone()

    if row is None:
        return None

    if not verify_password(password, row["password_hash"]):
        return None

    return {
        "id": row["id"],
        "full_name": row["full_name"],
        "username": row["username"],
        "role": row["role"],
        "active": row["active"]
    }


def get_all_staff(include_inactive=False):
    """List staff without exposing password hashes."""

    with get_connection() as connection:

        if include_inactive:
            rows = connection.execute(
                """
                SELECT id, full_name, username, role,
                       active, created_at
                FROM staff
                ORDER BY full_name
                """
            ).fetchall()

        else:
            rows = connection.execute(
                """
                SELECT id, full_name, username, role,
                       active, created_at
                FROM staff
                WHERE active = 1
                ORDER BY full_name
                """
            ).fetchall()

        return [dict(row) for row in rows]


def update_staff_role(staff_id, new_role):
    """Change a staff member's role."""

    new_role = str(new_role).strip()

    if new_role not in ALLOWED_ROLES:
        raise ValueError("Invalid staff role.")

    with get_connection() as connection:
        cursor = connection.execute(
            """
            UPDATE staff
            SET role = ?
            WHERE id = ?
            """,
            (new_role, staff_id)
        )

        if cursor.rowcount == 0:
            raise ValueError("Staff member not found.")


def deactivate_staff(staff_id):
    """Deactivate a staff account."""

    with get_connection() as connection:
        cursor = connection.execute(
            """
            UPDATE staff
            SET active = 0
            WHERE id = ?
            """,
            (staff_id,)
        )

        if cursor.rowcount == 0:
            raise ValueError("Staff member not found.")


def reactivate_staff(staff_id):
    """Reactivate a staff account."""

    with get_connection() as connection:
        cursor = connection.execute(
            """
            UPDATE staff
            SET active = 1
            WHERE id = ?
            """,
            (staff_id,)
        )

        if cursor.rowcount == 0:
            raise ValueError("Staff member not found.")
