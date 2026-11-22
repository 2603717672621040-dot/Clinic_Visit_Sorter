# CLINIQ - Smart Clinic Management System

## 1. Project Overview

CLINIQ is an AI-assisted student clinic visit and queue management application.
It helps clinic staff register student visits, organise administrative queues,
manage appointments and review visit information.

AI classifications are suggestions for administrative prioritisation only.
Qualified nurses retain full responsibility for reviewing every student.

## 2. Technologies Used

- Python
- Streamlit
- Google Gemini API
- SQLite
- Pandas
- CSV and JSON

## 3. AI Models

- Primary model: Gemini 3.8 Flash
- Backup model: Gemini 3.5 Flash Lite

If the primary model fails after retrying, CLINIQ automatically attempts
classification using the backup model. If both models fail, a conservative
fallback result is used.

## 4. Main Features

- Secure staff login
- Student visit registration
- Student queue management
- AI-assisted complaint classification
- Emergency red-flag priority checks
- Nurse review and priority assignment
- Appointment booking and management
- Staff management
- Visit details and history
- CSV upload and AI processing
- Nurse queue and summary report generation
- Clinic reports and analytics
- API performance and cost monitoring

## 5. System Requirements

- Python 3.10 or later
- Internet connection for live Gemini AI features
- VS Code or another Python editor
- Google Gemini API key
- Minimum 4 GB RAM recommended

## 6. Installation

Open the project folder in PowerShell.

Install the required packages:

    python -m pip install -r requirements.txt

## 7. API Key Configuration

Configure GEMINI_API_KEY securely using Streamlit secrets.

The key should be stored in:

    .streamlit/secrets.toml

Never publish your API key or secrets.toml file.
Never place API keys directly inside Python source code.

## 8. Run the Application

From the project folder, run:

    python -m streamlit run app.py

Open the local URL displayed in the terminal.

## 9. Testing

Run backend tests:

    python -m pytest test_backend_v2.py -v

Run assignment evaluation:

    python test_assignment_eval.py

The backend test suite contains 24 tests.

The assignment evaluation checks:
- Five normal classification cases
- Three red-team cases

These tests evaluate software behaviour and do not establish clinical safety
or medical accuracy.

## 10. API Performance and Cost Monitoring

CLINIQ records:
- API attempts and successful responses
- Failed API requests
- API call latency
- Gemini model used
- Input and output token counts
- Estimated API cost in USD and INR

Cost figures are estimates based on configured token pricing.
They are not actual invoices. Currency conversion is indicative.

## 11. Important Safety Notice

CLINIQ is an administrative queue-support system.

It must not:
- Diagnose diseases
- Prescribe medicines or recommend treatment
- Replace qualified nursing judgement
- Automatically remove students from the queue

The nurse must review every visit and make all clinical decisions.

## 12. Project Documents

- SPECIFICATION.md
- JUDGMENT_FRAMEWORK.md
- README_BACKEND_V2.txt
- requirements.txt
- test_assignment_eval.py
- test_backend_v2.py

