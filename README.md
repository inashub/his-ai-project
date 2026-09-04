# Intelligent Healthcare Information System (HIS) - Educational Prototype

This is a student project built for the "Introduction of AI in Healthcare" course.
It is an **educational prototype only** - not a real medical system. Do not use
real, identifiable patient information with it.

## Milestone 1 (current)
- Flask-based web app
- Patient Registration form
- Electronic Patient Record (EPR) module
- Homepage and navigation
- Basic Hospital Receptionist AI (rule-based department suggestion)

## How to run this project

1. Install Python 3.10 or newer.
2. Open a terminal in this folder.
3. (Recommended) create a virtual environment:
   - Windows: `python -m venv venv` then `venv\Scripts\activate`
   - Mac/Linux: `python3 -m venv venv` then `source venv/bin/activate`
4. Install the required package:
   `pip install -r requirements.txt`
5. Run the app:
   `python app.py`
6. Open your browser to: http://127.0.0.1:5000

## Project structure
- `app.py` - Flask routes (homepage, registration, patient list, EPR view)
- `models.py` - Database functions (SQLite, built into Python)
- `templates/` - HTML pages
- `static/style.css` - Basic styling
- `his.db` - Auto-created local database file (not uploaded to GitHub)

## Roadmap
See the full 12-milestone roadmap document for the complete project plan.
