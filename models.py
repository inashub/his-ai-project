"""
models.py - Handles our database using Python's built-in "sqlite3" module.

WHAT IS SQLITE?
SQLite is a database that lives in a single file on your computer (his.db).
No separate database server needed - perfect for learning and for a
prototype like this.

WHAT IS THIS FILE DOING?
It defines small functions for: creating the patients table, adding a new
patient, getting one patient, and getting all patients. app.py calls these
functions - it never has to write raw SQL itself.
"""

import sqlite3

DB_NAME = "his.db"


def get_connection():
    """Opens a connection to the database file. Every function below uses this."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # lets us access columns by name, e.g. row["full_name"]
    return conn


def init_db():
    """
    Creates the 'patients' table if it doesn't already exist.
    Called once when the app starts.
    """
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            date_of_birth TEXT NOT NULL,
            gender TEXT,
            phone TEXT,
            chief_complaint TEXT NOT NULL,
            suggested_department TEXT
        )
    """)
    conn.commit()
    conn.close()


def add_patient(full_name, date_of_birth, gender, phone, chief_complaint, suggested_department):
    """Inserts one new patient row and returns its new ID."""
    conn = get_connection()
    cursor = conn.execute(
        """
        INSERT INTO patients (full_name, date_of_birth, gender, phone, chief_complaint, suggested_department)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (full_name, date_of_birth, gender, phone, chief_complaint, suggested_department),
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id


def get_all_patients():
    """Returns every patient, most recently registered first."""
    conn = get_connection()
    rows = conn.execute("SELECT * FROM patients ORDER BY id DESC").fetchall()
    conn.close()
    return rows


def get_patient(patient_id):
    """Returns one patient by ID, or None if it doesn't exist."""
    conn = get_connection()
    row = conn.execute("SELECT * FROM patients WHERE id = ?", (patient_id,)).fetchone()
    conn.close()
    return row


def count_patients():
    """Returns how many patients are registered - used on the homepage."""
    conn = get_connection()
    row = conn.execute("SELECT COUNT(*) as total FROM patients").fetchone()
    conn.close()
    return row["total"]
