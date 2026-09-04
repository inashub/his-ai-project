"""
app.py - The main Flask application for our Healthcare Information System (HIS).

WHAT IS A "ROUTE"?
A route is just a rule that tells Flask: "when someone visits this web address
(URL), run this Python function and show the result." For example, the route
"/" is the homepage. The route "/register" is the registration page.

HOW TO RUN THIS FILE:
    python app.py
Then open your browser to: http://127.0.0.1:5000
"""

from flask import Flask, render_template, request, redirect, url_for, abort
import models

app = Flask(__name__)

# Create the database table the first time the app runs, if it doesn't exist yet.
models.init_db()


# --- Very simple "Hospital Receptionist AI" logic ---
# For Milestone 1, this is a small set of rules (not a machine learning model yet).
# It looks at the patient's "chief complaint" (their main reason for visiting)
# and suggests which department they should go to. Later milestones will make
# specialist AIs smarter and more central to the system.
def receptionist_suggest_department(chief_complaint: str) -> str:
    text = chief_complaint.lower()

    if any(word in text for word in ["chest pain", "breathless", "heart"]):
        return "Emergency Department (possible cardiac symptoms)"
    if any(word in text for word in ["fracture", "broken", "sprain", "fall"]):
        return "Orthopedics / Emergency Department"
    if any(word in text for word in ["fever", "cough", "cold", "flu"]):
        return "General Practice (GP)"
    if any(word in text for word in ["anxious", "depressed", "stress", "mental"]):
        return "Mental Health Services"
    if any(word in text for word in ["skin", "rash"]):
        return "Dermatology"
    return "General Practice (GP) - for initial assessment"


# --- Routes ---

@app.route("/")
def home():
    """Homepage: shows a welcome message and the navigation menu (in base.html)."""
    patient_count = models.count_patients()
    return render_template("home.html", patient_count=patient_count)


@app.route("/register", methods=["GET", "POST"])
def register():
    """
    Patient Registration page.
    GET  -> just show the empty form.
    POST -> the form was submitted, so save the new patient to the database.
    """
    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        date_of_birth = request.form.get("date_of_birth", "").strip()
        gender = request.form.get("gender", "").strip()
        phone = request.form.get("phone", "").strip()
        chief_complaint = request.form.get("chief_complaint", "").strip()

        if not full_name or not date_of_birth or not chief_complaint:
            return render_template(
                "register.html",
                error="Please fill in Full Name, Date of Birth, and Reason for Visit."
            )

        suggested_department = receptionist_suggest_department(chief_complaint)

        new_id = models.add_patient(
            full_name, date_of_birth, gender, phone, chief_complaint, suggested_department
        )

        return redirect(url_for("patient_record", patient_id=new_id))

    return render_template("register.html", error=None)


@app.route("/patients")
def patient_list():
    """Shows a simple list of all registered patients (links to each EPR)."""
    patients = models.get_all_patients()
    return render_template("patient_list.html", patients=patients)


@app.route("/patient/<int:patient_id>")
def patient_record(patient_id):
    """Electronic Patient Record (EPR) page for one patient."""
    patient = models.get_patient(patient_id)
    if patient is None:
        abort(404)
    return render_template("patient_record.html", patient=patient)


if __name__ == "__main__":
    app.run(debug=True)
