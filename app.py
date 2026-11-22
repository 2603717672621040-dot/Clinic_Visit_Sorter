
import streamlit as st
import pandas as pd
import backend_v2 as backend
import io
import html
import json
import re
from datetime import datetime, date


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="CLINIQ | Smart Clinic",
    page_icon="\u2728",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.info(
    "CLINIQ is an administrative queue-management system. "
    "It does not diagnose medical conditions or recommend treatment. "
    "All clinical priority decisions are made by the nurse."
)


# =========================================================
# SESSION STATE
# =========================================================

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "role" not in st.session_state:
    st.session_state.role = ""

if "staff_id" not in st.session_state:
    st.session_state.staff_id = None




# =========================================================
# LOGIN - SECURE STAFF AUTHENTICATION
# =========================================================

if not st.session_state.authenticated:

    st.markdown("<br><br>", unsafe_allow_html=True)

    left, right = st.columns([1.1, 1], gap="large")

    with left:
        st.markdown("# CLINIQ")
        st.caption("SMART CLINIC MANAGEMENT SYSTEM")

        st.markdown("### A smarter way to manage clinic visits")

        st.write(
            "CLINIQ helps clinic staff organise student visits, "
            "manage appointments and maintain an organised queue."
        )

        st.markdown("**Main Features**")
        st.write("- Student visit registration")
        st.write("- Nurse-managed priority queue")
        st.write("- Appointment management")
        st.write("- Clinic activity reports")
        st.write("- Staff management")

    
    
    with right:
        st.subheader("Welcome to CLINIQ")



        login_tab, register_tab = st.tabs([
            "Staff Login",
            "Create New Account"
        ])

        with login_tab:
            st.caption("Enter your registered username and password.")

            with st.form("login_form"):
                username = st.text_input("Username")
                password = st.text_input(
                    "Password",
                    type="password"
                )
                submitted = st.form_submit_button(
                    "Enter CLINIQ",
                    width="stretch"
                )

            if submitted:
                if not username.strip() or not password:
                    st.error("Please enter both username and password.")
                else:
                    try:
                        staff = backend.authenticate_staff(
                            username.strip(), password
                        )
                        if staff:
                            st.session_state.authenticated = True
                            st.session_state.username = staff["username"]
                            st.session_state.role = staff["role"]
                            st.session_state.staff_id = staff["id"]
                            st.success("Login successful.")
                            st.rerun()
                        else:
                            st.error("Invalid username or password.")
                    except Exception as error:
                        st.error(f"Login failed: {error}")

        with register_tab:
            st.caption("Create your own CLINIQ staff account.")

            with st.form("create_account_form"):
                full_name = st.text_input("Full Name")
                new_username = st.text_input("Create Username")
                new_password = st.text_input(
                    "Create Password", type="password"
                )
                confirm_password = st.text_input(
                    "Confirm Password", type="password"
                )
                register_submitted = st.form_submit_button(
                    "Create Account",
                    width="stretch"
                )

            if register_submitted:
                if not full_name.strip():
                    st.error("Please enter your full name.")
                elif not new_username.strip():
                    st.error("Please create a username.")
                elif not re.fullmatch(
                    r"[A-Za-z0-9._@-]{3,50}", new_username.strip()
                ):
                    st.error("Invalid username format.")
                elif len(new_password) < 8:
                    st.error("Password must contain at least 8 characters.")
                elif new_password != confirm_password:
                    st.error("Passwords do not match.")
                else:
                    try:
                        backend.add_staff(
                            full_name.strip(),
                            new_username.strip(),
                            new_password,
                            "Staff"
                        )
                        st.success(
                            "Account created! You can now log in."
                        )
                    except Exception as error:
                        st.error(f"Unable to create account: {error}")

    st.stop()






# =========================================================
# CUSTOM DESIGN
# =========================================================


st.markdown("""
<style>

/* =========================================
   CLINIQ MODERN DESIGN SYSTEM
========================================= */

:root {
    --navy: #10243A;
    --navy-light: #193B56;
    --teal: #0D9488;
    --teal-light: #14B8A6;
    --page-bg: #F4F7FB;
    --card-bg: #FFFFFF;
    --text-main: #172B42;
    --text-muted: #718096;
    --border: #E2EAF1;
}

/* MAIN APPLICATION */

.stApp {
    background: var(--page-bg);
    color: var(--text-main);
}

.block-container {
    max-width: 1500px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* SIDEBAR */

[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #10243A 0%,
        #173B55 100%
    );
    border-right: 1px solid #24465F;
}

[data-testid="stSidebar"] * {
    color: #F1F7FB;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label {
    padding: 9px 12px;
    border-radius: 9px;
    transition: background 0.2s ease;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
    background: rgba(255,255,255,0.12);
}

/* HEADINGS */

h1, h2, h3 {
    color: var(--navy);
    font-weight: 750;
    letter-spacing: -0.4px;
}

.main-title {
    font-size: 34px;
    font-weight: 800;
    color: var(--navy);
}

.section-caption {
    color: var(--text-muted);
    font-size: 14px;
}

/* DASHBOARD HERO */

.dashboard-hero {
    background: linear-gradient(
        120deg,
        #10243A,
        #087F8C
    );
    padding: 34px;
    border-radius: 20px;
    color: white;
    margin-bottom: 26px;
    box-shadow: 0 10px 30px rgba(16,36,58,0.14);
}

.dashboard-hero h2 {
    color: white !important;
    font-size: 30px;
    font-weight: 800;
}

.dashboard-hero p {
    color: #E0F7FA !important;
    font-size: 15px;
}

/* METRIC CARDS */

div[data-testid="stMetric"] {
    background: var(--card-bg);
    padding: 20px;
    border: 1px solid var(--border);
    border-radius: 17px;
    box-shadow: 0 5px 18px rgba(16,36,58,0.055);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

div[data-testid="stMetric"]:hover {
    transform: translateY(-3px);
    box-shadow: 0 9px 22px rgba(16,36,58,0.09);
}

div[data-testid="stMetricLabel"] {
    color: var(--text-muted);
    font-weight: 650;
}

div[data-testid="stMetricValue"] {
    color: var(--navy);
    font-size: 30px;
    font-weight: 800;
}

/* CUSTOM CARDS */

.metric-card,
.priority-card {
    background: white;
    padding: 22px;
    border-radius: 17px;
    border: 1px solid var(--border);
    box-shadow: 0 5px 18px rgba(16,36,58,0.05);
}

.metric-label {
    color: var(--text-muted);
    font-size: 14px;
}

.metric-value,
.priority-number {
    color: var(--navy);
    font-size: 29px;
    font-weight: 800;
}

/* BUTTONS */

div[data-testid="stButton"] > button,
div[data-testid="stFormSubmitButton"] > button {
    border-radius: 11px;
    min-height: 44px;
    font-weight: 700;
    border: 1px solid #D6E4EA;
    transition: all 0.2s ease;
}

div[data-testid="stButton"] > button:hover,
div[data-testid="stFormSubmitButton"] > button:hover {
    border-color: var(--teal);
    color: var(--teal);
}

/* INPUT FIELDS */

div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea,
div[data-testid="stNumberInput"] input {
    border-radius: 10px;
    border-color: #D8E3EC;
}

div[data-testid="stTextInput"] input:focus,
div[data-testid="stTextArea"] textarea:focus {
    border-color: var(--teal);
    box-shadow: 0 0 0 2px rgba(13,148,136,0.12);
}

/* FORMS */

[data-testid="stForm"] {
    background: white;
    padding: 22px;
    border: 1px solid var(--border);
    border-radius: 16px;
}

/* TABS */

button[data-baseweb="tab"] {
    font-weight: 650;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: var(--teal);
}

/* DATA TABLES */

div[data-testid="stDataFrame"] {
    border: 1px solid var(--border);
    border-radius: 13px;
    overflow: hidden;
}

/* ALERTS */

div[data-testid="stAlert"] {
    border-radius: 12px;
}

/* DIVIDERS */

hr {
    border-color: var(--border);
}

/* RESPONSIVE SPACING */

@media (max-width: 768px) {
    .block-container {
        padding: 1rem;
    }

    .dashboard-hero {
        padding: 22px;
    }

    .dashboard-hero h2 {
        font-size: 24px;
    }
}


/* DASHBOARD POLISH */

/* CLINIQ DASHBOARD ALIGNMENT */
.dashboard-section {
    margin: 26px 0 16px 0;
    padding-bottom: 10px;
    border-bottom: 1px solid #E5EDF3;
    color: #10243A;
    font-size: 19px;
    font-weight: 750;
    letter-spacing: -0.3px;
}

.metric-card {
    min-height: 112px;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    box-sizing: border-box;
}

div[data-testid="stMetric"] {
    height: 112px;
    box-sizing: border-box;
}

[data-testid="stHorizontalBlock"] {
    align-items: stretch;
}

[data-testid="stPlotlyChart"],
[data-testid="stVegaLiteChart"] {
    width: 100%;
    box-sizing: border-box;
    overflow: hidden;
}

[data-testid="stDataFrame"] {
    width: 100%;
    border: 1px solid #E2EAF1;
    border-radius: 14px;
    overflow: hidden;
}

div.stButton > button {
    min-height: 44px;
    border-radius: 11px;
    font-weight: 650;
}

@media (max-width: 768px) {
    .dashboard-section {
        margin-top: 20px;
        font-size: 17px;
    }

    .metric-card,
    div[data-testid="stMetric"] {
        min-height: 90px;
        height: auto;
    }
}

[data-testid="stVerticalBlock"] > [data-testid="stHorizontalBlock"] {
    gap: 16px;
}

div[data-testid="stMetric"] {
    min-height: 95px;
    justify-content: center;
}

[data-testid="stPlotlyChart"],
[data-testid="stVegaLiteChart"] {
    background: #FFFFFF;
    border: 1px solid #E2EAF1;
    border-radius: 15px;
    padding: 12px;
    box-shadow: 0 4px 14px rgba(16,36,58,0.04);
}

[data-testid="stSubheader"] {
    color: #10243A;
    font-weight: 750;
}

[data-testid="stCaptionContainer"] {
    color: #718096;
}

.stProgress > div > div {
    background-color: #0D9488;
}



/* CLINIQ DASHBOARD FINAL REFINEMENT */

.dashboard-hero {
    position: relative;
    overflow: hidden;
    padding: 36px;
    border: 1px solid rgba(255,255,255,0.12);
}

.dashboard-hero h2 {
    margin-bottom: 10px;
    letter-spacing: -0.6px;
}

.dashboard-section {
    display: block;
    padding: 0 0 11px 2px;
    margin-top: 30px;
    margin-bottom: 17px;
    border-bottom: 1px solid #E2EAF1;
}

.metric-card {
    min-height: 118px;
    padding: 22px;
    border-radius: 16px;
    transition: box-shadow 0.2s ease, transform 0.2s ease;
}

.metric-card:hover {
    box-shadow: 0 9px 24px rgba(16,36,58,0.09);
    transform: translateY(-2px);
}

.metric-label {
    font-size: 13px;
    font-weight: 650;
    letter-spacing: 0.2px;
    margin-bottom: 9px;
}

.metric-value {
    color: #10243A;
    font-size: 29px;
    font-weight: 800;
    line-height: 1.2;
}

[data-testid="stDataFrame"] {
    border: 1px solid #E2EAF1;
    border-radius: 14px;
    overflow: hidden;
}

[data-testid="stPlotlyChart"],
[data-testid="stVegaLiteChart"] {
    border: 1px solid #E2EAF1;
    border-radius: 15px;
    padding: 12px;
    background: #FFFFFF;
}

@media (max-width: 768px) {
    .dashboard-hero {
        padding: 23px;
    }

    .metric-card {
        min-height: 95px;
        padding: 17px;
    }

    .metric-value {
        font-size: 24px;
    }
}

</style>
""", unsafe_allow_html=True)






# =========================================================
# HELPER FUNCTIONS
# =========================================================

def get_value(record, key, default=""):
    if isinstance(record, dict):
        return record.get(key, default)
    return default


def safe_dataframe(records):
    if not records:
        return pd.DataFrame()
    return pd.DataFrame(records)


def metric_card(label, value):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{html.escape(str(label))}</div>
            <div class="metric-value">{html.escape(str(value))}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def get_priority_count(visits, priority):
    return sum(
        1 for visit in visits
        if get_value(visit, "nurse_priority") == priority
    )


def get_status_count(visits, status):
    return sum(
        1 for visit in visits
        if get_value(visit, "status") == status
    )


def show_detail(visit):
    st.markdown("### Visit Information")

    st.html("""
    <div style="
        background:#F0F7FA;
        border:1px solid #DCE9EF;
        border-radius:13px;
        padding:13px 17px;
        margin-bottom:15px;
        color:#34536A;
        font-size:13px;
    ">
        Review registered information carefully. Clinical decisions and
        priority assignments remain the responsibility of qualified nurses.
    </div>
    """)

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Visit ID:**", get_value(visit, "id"))
        st.write("**Student Name:**", get_value(visit, "student_name"))
        st.write("**Student ID:**", get_value(visit, "student_id"))

    with col2:
        st.write("**Status:**", get_value(visit, "status"))
        st.write("**Nurse Priority:**", get_value(visit, "nurse_priority", "Not assigned"))
        st.write("**Created:**", get_value(visit, "created_at"))

    st.markdown("#### Original Student Complaint")

    complaint = get_value(visit, "complaint", "No complaint recorded.")

    st.info(str(complaint))

def format_created_at(value):
    if not value:
        return "Unknown"

    try:
        return pd.to_datetime(value).strftime("%d %b %Y, %I:%M %p")
    except Exception:
        return str(value)



# =========================================================
# SIDEBAR NAVIGATION
# =========================================================

with st.sidebar:

    st.markdown("# \u2728 CLINIQ")
    st.caption("SMART CLINIC MANAGEMENT")

    st.divider()

    st.write("**Logged in as**")
    st.write(st.session_state.username)

    st.write("**Role**")
    st.write(st.session_state.role)

    st.divider()

    role = st.session_state.role

    if role == "Admin":

        pages = [
            "Dashboard",
            "Register Visit",
            "Student Queue",
            "CSV Upload & AI Processing",
            "Visit Details",
            "Appointment Management",
            "Clinic Reports",
            "Staff Management",
            "Visit History"
        ]

    elif role == "Nurse":

        pages = [
            "Dashboard",
            "Register Visit",
            "Student Queue",
            "CSV Upload & AI Processing",
            "Visit Details",
            "Appointment Management",
            "Clinic Reports",
            "Visit History"
        ]

   
    else:
        pages = [
            "Dashboard",
            "Register Visit",
            "Student Queue",
            "CSV Upload & AI Processing",
            "Visit Details",
            "Appointment Management",
            "Clinic Reports",
            "Visit History"
        ]


    requested_page = st.session_state.pop("dashboard_navigation", None)

    if requested_page in pages:
        st.session_state["main_navigation"] = requested_page

    default_page = st.session_state.get("main_navigation", "Dashboard")

    if default_page not in pages:
        default_page = "Dashboard"

    page = st.radio(
        "NAVIGATION",
        pages,
        index=pages.index(default_page),
        label_visibility="collapsed",
        key="main_navigation"
    )

    st.divider()

    if st.button("Logout", width="stretch"):

        for key in [
            "authenticated",
            "username",
            "role",
            "staff_id",
            "main_navigation",
            "dashboard_navigation"
        ]:
            st.session_state.pop(key, None)

        st.rerun()

# =========================================================
# LOAD VISITS
# =========================================================

try:

    # -------------------------------------------------
    # API PERFORMANCE & COST MONITORING
    # -------------------------------------------------

    st.markdown("### API Performance & Cost Monitoring")
    st.caption(
        "Gemini API request activity, response time and estimated "
        "paid-tier token cost."
    )

    api_log_path = "api_usage.jsonl"
    api_records = []

    try:
        with open(api_log_path, "r", encoding="utf-8") as api_file:
            for line in api_file:
                try:
                    record = json.loads(line.strip())
                    if isinstance(record, dict):
                        api_records.append(record)
                except (json.JSONDecodeError, ValueError):
                    continue
    except FileNotFoundError:
        pass
    except OSError:
        st.warning("API usage log could not be read.")

    today_api_records = []

    for record in api_records:
        try:
            record_time = datetime.fromisoformat(
                record.get("timestamp", "")
            )

            if record_time.date() == date.today():
                today_api_records.append(record)

        except (TypeError, ValueError):
            continue

    api_attempts = len(today_api_records)

    api_responses = sum(
        1 for record in today_api_records
        if record.get("api_success") is True
    )

    api_latencies = [
        float(record.get("latency_seconds", 0))
        for record in today_api_records
        if isinstance(record.get("latency_seconds"), (int, float))
    ]

    average_api_latency = (
        sum(api_latencies) / len(api_latencies)
        if api_latencies else 0
    )

    api_failures = api_attempts - api_responses

    successful_api_records = [
        record for record in today_api_records
        if record.get("api_success") is True
    ]

    today_api_cost_usd = sum(
        float(record.get("estimated_paid_cost_usd", 0) or 0)
        for record in successful_api_records
    )

    today_input_tokens = sum(
        int(record.get("input_tokens", 0) or 0)
        for record in today_api_records
    )

    today_output_tokens = sum(
        int(record.get("output_tokens", 0) or 0)
        for record in today_api_records
    )

    # Indicative USD-INR reference rate for display.
    usd_inr_rate = 92.89
    today_api_cost_inr = today_api_cost_usd * usd_inr_rate

    api_metric_columns = st.columns(5)

    with api_metric_columns[0]:
        metric_card("API Attempts Today", api_attempts)

    with api_metric_columns[1]:
        metric_card("Successful Requests", api_responses)

    with api_metric_columns[2]:
        metric_card("Failed Requests", api_failures)

    with api_metric_columns[3]:
        metric_card(
            "Average API Call Time",
            f"{average_api_latency:.2f} sec"
            if api_latencies else "No data"
        )

    with api_metric_columns[4]:
        metric_card(
            "Estimated Daily Cost",
            f"${today_api_cost_usd:.6f}"
        )

    st.caption(
        f"Estimated INR equivalent: INR {today_api_cost_inr:.4f} "
        f"| Reference rate: INR {usd_inr_rate:.2f} per USD."
    )

    token_col1, token_col2 = st.columns(2)

    with token_col1:
        metric_card("Input Tokens Today", today_input_tokens)

    with token_col2:
        metric_card("Output Tokens Today", today_output_tokens)

    if not today_api_records:
        st.info(
            "No Gemini API requests have been recorded today. "
            "Usage metrics will appear after AI classification requests."
        )

    elif today_input_tokens == 0 and today_output_tokens == 0:
        st.warning(
            "API requests were recorded, but token usage metadata was "
            "not returned. Cost may therefore be understated."
        )

    if today_api_records:
        with st.expander("View today's API request details"):
            api_detail_rows = []

            for record in reversed(today_api_records[-20:]):
                api_detail_rows.append({
                    "Time": str(record.get("timestamp", ""))[:19],
                    "Model": record.get("model", "Unknown"),
                    "Response Received": (
                        "Yes" if record.get("api_success") else "No"
                    ),
                    "Response Time (sec)": record.get(
                        "latency_seconds", 0
                    ),
                    "Input Tokens": record.get("input_tokens", 0),
                    "Output Tokens": record.get("output_tokens", 0),
                    "Estimated Cost (USD)": record.get(
                        "estimated_paid_cost_usd", 0
                    )
                })

            st.dataframe(
                pd.DataFrame(api_detail_rows),
                width="stretch",
                hide_index=True
            )

    st.caption(
        "Cost is an estimated paid-tier equivalent based on recorded token "
        "usage, not an actual invoice. Free-tier usage may be charged at "
        "zero within applicable limits. INR conversion is indicative."
    )

    st.markdown("---")

    visits = backend.get_all_visits() or []
except Exception as error:
    visits = []
    st.error(f"Unable to load visits: {error}")




# =========================================================
# DASHBOARD
# =========================================================

if page == "Dashboard":

    # =====================================================
    # CLINIQ QUEUE DASHBOARD - INSPIRED BY THE REFERENCE UI
    # Uses existing CLINIQ visit and appointment data only.
    # =====================================================

    st.html("""
    <style>
    /* Dashboard canvas and compact header */
    [data-testid="stAppViewContainer"] { background: #F3F6FA; }
    [data-testid="stAppViewBlockContainer"] {
        max-width: 1600px !important;
        padding-top: 0.8rem !important;
        padding-bottom: 1.5rem !important;
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg,#0B1830 0%,#102744 100%);
        border-right: 1px solid #1D3554;
    }
    [data-testid="stSidebar"] * { color: #EAF2FC; }
    [data-testid="stSidebar"] [data-testid="stRadio"] label {
        padding: 8px 10px; border-radius: 8px;
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
        background: rgba(255,255,255,.10);
    }
    .cl-topbar {
        display:flex; justify-content:space-between; align-items:center;
        background:#FFFFFF; border:1px solid #E6ECF2; border-radius:10px;
        padding:11px 17px; margin:0 0 13px 0;
        color:#15263E; font-size:13px; font-weight:750;
        box-shadow:0 2px 8px rgba(20,40,65,.035);
    }
    .cl-topbar small { color:#8492A4; font-weight:500; }
    /* Main live queue banner */
    .cl-live-hero {
        display:grid; grid-template-columns:1.05fr 1.15fr .48fr;
        gap:18px; align-items:stretch;
        background:linear-gradient(112deg,#0A1934 0%,#102544 58%,#0C2945 100%);
        color:white; border:1px solid #203B5C; border-radius:11px;
        padding:19px 22px; min-height:145px;
        box-shadow:0 7px 18px rgba(9,25,49,.14);
        margin-bottom:14px;
    }
    .cl-live-label {
        color:#22C7BE; font-size:10px; letter-spacing:1.4px;
        font-weight:850; text-transform:uppercase; margin-bottom:5px;
    }
    .cl-live-token {
        color:#FFFFFF; font-size:48px; line-height:1.05;
        font-weight:900; letter-spacing:-1.6px;
    }
    .cl-live-at { color:#5DD8D0; font-size:10px; font-weight:800; margin:5px 0 2px; }
    .cl-live-counter { color:#20C5BD; font-size:20px; font-weight:850; }
    .cl-live-dept { color:#C7D4E3; font-size:12px; margin-top:2px; }
    .cl-wait-list { border-left:1px solid rgba(210,230,250,.17);
        border-right:1px solid rgba(210,230,250,.17); padding:0 17px; }
    .cl-wait-row {
        display:flex; justify-content:space-between; gap:12px;
        padding:5px 0; border-bottom:1px solid rgba(210,230,250,.10);
        color:#EAF2FC; font-size:11px;
    }
    .cl-wait-row span:last-child { color:#27C7BE; font-weight:750; }
    .cl-live-time { text-align:center; display:flex; flex-direction:column;
        justify-content:center; color:#FFFFFF; }
    .cl-live-time .clock { font-size:22px; font-weight:850; }
    .cl-live-time .date { color:#B8C7D8; font-size:10px; margin-top:4px; }
    .cl-live-time .thanks { color:#28C9BE; font-size:11px; font-weight:800; margin-top:15px; }
    /* White dashboard panels */
    .cl-panel {
        background:#FFFFFF; border:1px solid #E4EAF1; border-radius:10px;
        padding:14px 15px; box-shadow:0 3px 12px rgba(20,40,65,.045);
        min-height:100px; margin-bottom:12px;
    }
    .cl-panel-title { color:#172A42; font-size:13px; font-weight:850; margin-bottom:3px; }
    .cl-panel-sub { color:#91A0B0; font-size:10px; margin-bottom:10px; }
    .cl-stat-grid { display:grid; grid-template-columns:repeat(4,1fr); gap:9px; }
    .cl-stat { text-align:center; padding:8px 4px; border-right:1px solid #EEF1F5; }
    .cl-stat:last-child { border-right:0; }
    .cl-stat-icon { width:29px; height:29px; margin:0 auto 5px; border-radius:50%;
        display:flex; align-items:center; justify-content:center; font-size:14px; }
    .cl-stat-value { color:#172A42; font-size:20px; font-weight:900; line-height:1.1; }
    .cl-stat-label { color:#65758A; font-size:10px; font-weight:700; margin-top:3px; }
    .cl-stat-caption { color:#98A5B3; font-size:9px; }
    .cl-chip { display:inline-block; padding:3px 8px; border-radius:20px;
        background:#E7F7F3; color:#16866F; font-size:9px; font-weight:800; }
    .cl-table-row { display:flex; justify-content:space-between; gap:8px;
        border-bottom:1px solid #EEF2F6; padding:7px 0; font-size:10px; color:#526276; }
    .cl-table-row strong { color:#26384F; font-weight:750; }
    .cl-empty { padding:18px 10px; text-align:center; border:1px dashed #D7E0E9;
        border-radius:8px; color:#8A98A8; font-size:11px; }
    @media(max-width:900px) {
        .cl-live-hero { grid-template-columns:1fr; }
        .cl-wait-list { border:0; border-top:1px solid rgba(210,230,250,.17);
            border-bottom:1px solid rgba(210,230,250,.17); padding:12px 0; }
        .cl-stat-grid { grid-template-columns:repeat(2,1fr); }
    }

    /* FINAL DASHBOARD VISUAL POLISH */
    .cl-topbar {
        min-height: 48px;
        padding: 12px 20px;
        border-radius: 12px;
    }

    .cl-live-hero {
        border-radius: 14px;
        padding: 23px 25px;
        min-height: 158px;
        box-shadow: 0 9px 25px rgba(9,25,49,.16);
    }

    .cl-panel {
        border-radius: 13px;
        padding: 17px;
        box-shadow: 0 4px 15px rgba(20,40,65,.055);
    }

    .cl-panel-title {
        font-size: 14px;
        letter-spacing: .1px;
    }

    .cl-stat {
        padding: 12px 5px;
    }

    .cl-stat-icon {
        width: 34px;
        height: 34px;
        font-size: 17px;
    }

    .cl-stat-value {
        font-size: 23px;
    }

    [data-testid="stVegaLiteChart"],
    [data-testid="stPlotlyChart"],
    [data-testid="stArrowVegaLiteChart"] {
        background: #FFFFFF;
        border: 1px solid #E4EAF1;
        border-radius: 12px;
        padding: 10px;
        box-shadow: 0 3px 12px rgba(20,40,65,.04);
    }

    [data-testid="stDataFrame"] {
        border: 1px solid #E4EAF1;
        border-radius: 10px;
        overflow: hidden;
    }

    [data-testid="stButton"] button {
        min-height: 43px;
        border-radius: 9px;
        font-weight: 700;
    }

    @media(max-width: 900px) {
        .cl-live-hero {
            padding: 17px;
        }
        .cl-stat-grid {
            grid-template-columns: repeat(2, minmax(0, 1fr));
        }
    }

    /* CLINIQ PROFESSIONAL DASHBOARD */
    .cl-topbar {
        min-height: 54px;
        padding: 14px 22px;
        border-radius: 12px;
        font-size: 14px;
        box-shadow: 0 4px 14px rgba(16,36,58,.06);
    }

    .cl-live-hero {
        grid-template-columns: 1fr 1.2fr .65fr;
        gap: 22px;
        min-height: 175px;
        padding: 25px 28px;
        border-radius: 16px;
        box-shadow: 0 10px 28px rgba(9,25,49,.17);
    }

    .cl-live-token {
        font-size: 54px;
        letter-spacing: -1px;
    }

    .cl-live-label {
        font-size: 11px;
        letter-spacing: 1.5px;
    }

    .cl-panel {
        padding: 19px;
        min-height: 115px;
        border: 1px solid #E1E8F0;
        border-radius: 14px;
        box-shadow: 0 5px 18px rgba(16,36,58,.055);
        margin-bottom: 14px;
    }

    .cl-panel-title {
        font-size: 15px;
        font-weight: 800;
        color: #10243A;
        margin-bottom: 5px;
    }

    .cl-panel-sub {
        font-size: 11px;
        color: #77869A;
        margin-bottom: 13px;
    }

    .cl-stat-grid {
        gap: 14px;
    }

    .cl-stat {
        padding: 14px 7px;
    }

    .cl-stat-icon {
        width: 38px;
        height: 38px;
        font-size: 18px;
        margin-bottom: 9px;
    }

    .cl-stat-value {
        font-size: 26px;
        font-weight: 850;
    }

    .cl-stat-label {
        font-size: 12px;
        font-weight: 750;
        color: #40536A;
    }

    .cl-stat-caption {
        font-size: 10px;
    }

    .cl-empty {
        padding: 25px 14px;
        background: #F8FAFC;
        border: 1px dashed #CBD7E3;
        border-radius: 11px;
        color: #718096;
        font-size: 12px;
    }

    [data-testid="stDataFrame"] {
        border: 1px solid #E1E8F0;
        border-radius: 11px;
        overflow: hidden;
    }

    [data-testid="stButton"] button {
        min-height: 44px;
        border-radius: 10px;
        font-size: 13px;
        font-weight: 750;
    }

    [data-testid="stAlert"] {
        border-radius: 11px;
    }

    @media(max-width: 900px) {
        .cl-live-hero {
            grid-template-columns: 1fr;
            gap: 15px;
        }
        .cl-stat-grid {
            grid-template-columns: repeat(2, minmax(0, 1fr));
        }
    }

    /* FINAL CHART PANEL FINISH */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background: #FFFFFF;
        border: 1px solid #E1E8F0 !important;
        border-radius: 14px !important;
        padding: 15px 17px 12px 17px;
        box-shadow: 0 5px 18px rgba(16,36,58,.05);
    }

    [data-testid="stVerticalBlockBorderWrapper"] h4 {
        color: #10243A;
        font-size: 15px;
        font-weight: 800;
        margin-bottom: 2px;
    }

    [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stCaptionContainer"] {
        color: #7B899B;
        font-size: 11px;
    }

    [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stVegaLiteChart"],
    [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stArrowVegaLiteChart"] {
        border: 0;
        box-shadow: none;
        padding: 0;
    }

    /* =========================================
       CLINIQ FINAL DASHBOARD REFINEMENT
    ========================================= */

    .cl-topbar {
        color: #10243A;
        font-size: 14px;
        font-weight: 750;
    }

    .cl-topbar small {
        font-size: 12px;
    }

    .cl-live-hero {
        gap: 24px;
        padding: 27px 30px;
    }

    .cl-live-label {
        color: #A9C4D9;
        font-weight: 800;
    }

    .cl-live-token {
        line-height: 1.15;
        font-weight: 850;
    }

    .cl-live-time .clock {
        font-size: 27px;
        font-weight: 800;
    }

    .cl-panel {
        background: #FFFFFF;
        transition: box-shadow .2s ease, transform .2s ease;
    }

    .cl-panel-title {
        font-size: 16px;
        letter-spacing: -0.2px;
    }

    .cl-panel-sub {
        font-size: 12px;
        line-height: 1.5;
    }

    .cl-stat-grid {
        align-items: stretch;
        gap: 16px;
    }

    .cl-stat {
        min-width: 0;
        padding: 16px 8px;
    }

    .cl-stat-value {
        font-size: 28px;
        line-height: 1.25;
    }

    .cl-stat-label {
        font-size: 13px;
        line-height: 1.4;
    }

    .cl-stat-caption {
        font-size: 11px;
        line-height: 1.4;
        margin-top: 3px;
    }

    .cl-empty {
        min-height: 115px;
        display: flex;
        align-items: center;
        justify-content: center;
        line-height: 1.6;
    }

    /* Dashboard chart and lower-panel headings */
    [data-testid="stVerticalBlockBorderWrapper"] h4 {
        font-size: 16px;
        letter-spacing: -0.2px;
    }

    [data-testid="stVerticalBlockBorderWrapper"]
    [data-testid="stCaptionContainer"] {
        font-size: 12px;
        line-height: 1.5;
    }

    /* Dashboard tables */
    [data-testid="stDataFrame"] {
        border-radius: 12px;
        border-color: #DCE6EF;
    }

    /* Quick action buttons */
    div[data-testid="stButton"] > button {
        min-height: 48px;
        font-size: 14px;
        font-weight: 750;
        border-radius: 12px;
        transition: all .2s ease;
    }

    div[data-testid="stButton"] > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 14px rgba(16,36,58,.09);
    }

    /* Responsive dashboard */
    @media (max-width: 900px) {
        .cl-live-hero {
            padding: 20px;
        }

        .cl-live-token {
            font-size: 42px;
        }

        .cl-stat-grid {
            gap: 8px;
        }
    }

    @media (max-width: 600px) {
        .cl-topbar {
            flex-wrap: wrap;
            gap: 8px;
            padding: 12px;
        }

        .cl-live-hero {
            padding: 17px;
            gap: 14px;
        }

        .cl-stat-grid {
            grid-template-columns: repeat(2, minmax(0, 1fr));
        }

        .cl-stat {
            border-right: 0;
            border-bottom: 1px solid #EEF1F5;
        }

        .cl-stat-value {
            font-size: 24px;
        }
    }

    </style>
    """)

    current_time = datetime.now()
    today = date.today()

    try:
        visits = backend.get_all_visits() or []
    except Exception as error:
        visits = []
        st.error(f"Unable to load clinic visits: {error}")

    try:
        appointments = backend.get_all_appointments() or []
    except Exception:
        appointments = []

    # Normalise visit dates and calculate dashboard figures.
    dated_visits = []
    today_visits = []
    for visit in visits:
        created = pd.to_datetime(get_value(visit, "created_at", ""), errors="coerce")
        if pd.notna(created):
            dated_visits.append((created, visit))
            if created.date() == today:
                today_visits.append(visit)

    waiting_visits = [
        v for v in visits
        if str(get_value(v, "status", "")).strip().lower() == "waiting"
    ]
    completed_visits = [
        v for v in visits
        if str(get_value(v, "status", "")).strip().lower() == "completed"
    ]
    consultation_visits = [
        v for v in visits
        if str(get_value(v, "status", "")).strip().lower()
        in ("in consultation", "in-consultation", "consulting")
    ]
    pending_reviews = [
        v for v in visits if not get_value(v, "nurse_priority")
    ]

    def _esc(value):
        return html.escape(str(value if value not in (None, "") else "—"))

    # Most recent waiting record is displayed as the current queue token.
    latest_waiting = sorted(
        waiting_visits,
        key=lambda v: str(get_value(v, "created_at", "")),
        reverse=True
    )
    now_serving = (
        get_value(latest_waiting[0], "id", "—") if latest_waiting else "—"
    )
    username = _esc(st.session_state.get("username", "Staff"))
    role_name = _esc(st.session_state.get("role", "Staff"))

    st.html(f"""
    <div class="cl-topbar">
        <span>CLINIQ <small>/ Smart Clinic Management</small></span>
        <span>{username} &nbsp; <small>{role_name}</small></span>
    </div>
    """)

    wait_rows = ""
    if latest_waiting:
        for item in latest_waiting[:8]:
            token = _esc(get_value(item, "id", "—"))
            priority = _esc(get_value(item, "nurse_priority", "Awaiting nurse review") or "Awaiting nurse review")
            wait_rows += f'<div class="cl-wait-row"><span>{token}</span><span>{priority}</span></div>'
    else:
        wait_rows = '<div class="cl-wait-row"><span>No waiting visits</span><span>Queue clear</span></div>'

    st.html(f"""
    <section class="cl-live-hero">
        <div>
            <div class="cl-live-label">LATEST WAITING QUEUE</div>
            <div class="cl-live-token">{_esc(now_serving)}</div>
            <div class="cl-live-at">QUEUE STATUS</div>
            <div class="cl-live-counter">WAITING / REVIEW</div>
            <div class="cl-live-dept">Latest waiting visit token</div>
        </div>
        <div class="cl-wait-list">
            <div class="cl-live-label">WAITING TOKENS</div>
            {wait_rows}
        </div>
        <div class="cl-live-time">
            <div>◷</div>
            <div class="clock">{current_time.strftime("%I:%M %p")}</div>
            <div class="date">{current_time.strftime("%d %b %Y")}<br>{current_time.strftime("%A")}</div>
            <div class="thanks">CLINIQ / THANK YOU</div>
            <div class="date">Please keep your visit details ready</div>
        </div>
    </section>
    """)

    # Main overview row, styled to match the reference dashboard.
    stat_items = [
        (chr(0x1F465), len(visits), "Total Visits", "All registered", "#E8F1FB", "#3779B8"),
        (chr(0x1F4C5), len(today_visits), "Today's Visits", "Registered today", "#EAF3FF", "#397CC0"),
        (chr(0x23F3), len(waiting_visits), "Waiting", "Currently in queue", "#FFF4DF", "#D89A32"),
        (chr(0x2713), len(completed_visits), "Completed", "Marked completed", "#E8F7F0", "#269A70"),
    ]
    stat_html = ""
    for icon, value, label, caption, bg, fg in stat_items:
        stat_html += f"""
        <div class="cl-stat">
            <div class="cl-stat-icon" style="background:{bg};color:{fg}">{icon}</div>
            <div class="cl-stat-value">{value}</div>
            <div class="cl-stat-label">{label}</div>
            <div class="cl-stat-caption">{caption}</div>
        </div>
        """

    st.html(f"""
    <div class="cl-panel">
        <div class="cl-panel-title">Live Overview</div>
        <div class="cl-panel-sub">Current clinic activity at a glance</div>
        <div class="cl-stat-grid">{stat_html}</div>
    </div>
    """)

    left_chart, right_chart = st.columns([0.92, 1.55], gap="medium")

    with left_chart:
        with st.container(border=True):
            st.markdown("#### Visit Queue Summary")
            st.caption("Current clinic workflow by visit status")

            if visits:
                status_summary = pd.DataFrame({
                    "Visit Status": ["Waiting", "In Consultation", "Completed"],
                    "Count": [
                        len(waiting_visits),
                        len(consultation_visits),
                        len(completed_visits)
                    ]
                }).set_index("Visit Status")

                st.bar_chart(
                    status_summary,
                    height=245,
                    color="#0D9488",
                    horizontal=True
                )
            else:
                st.markdown(
                    '<div class="cl-empty">Visit status analytics will appear '
                    'after student visits are registered.</div>',
                    unsafe_allow_html=True
                )

    with right_chart:
        with st.container(border=True):
            st.markdown("#### Visit Activity")
            st.caption("Daily registrations across the latest seven available days")

            if dated_visits:
                activity = pd.DataFrame([
                    {"Date": created.date().isoformat(), "Visits": 1}
                    for created, _ in dated_visits
                ])

                activity = (
                    activity.groupby("Date", as_index=False)["Visits"]
                    .sum()
                    .sort_values("Date")
                    .tail(7)
                )

                activity["Date"] = pd.to_datetime(
                    activity["Date"]
                ).dt.strftime("%d %b")

                st.bar_chart(
                    activity,
                    x="Date",
                    y="Visits",
                    height=245,
                    color="#0D9488"
                )
            else:
                st.markdown(
                    '<div class="cl-empty">Your clinic activity chart will '
                    'appear here after visits are registered.</div>',
                    unsafe_allow_html=True
                )

    # Professional lower dashboard panels
    q1, q2, q3 = st.columns([1, 1, 1.25], gap="medium")

    with q1:
        with st.container(border=True):
            st.markdown("#### Nurse Priority")
            st.caption("Staff-assigned visit priorities")

            priority_table = pd.DataFrame({
                "Priority": ["See Now", "Today", "Routine", "Not assigned"],
                "Visits": [
                    get_priority_count(visits, "See Now"),
                    get_priority_count(visits, "Today"),
                    get_priority_count(visits, "Routine"),
                    len(pending_reviews)
                ]
            })
            st.dataframe(
                priority_table,
                hide_index=True,
                width="stretch",
                height=190
            )

    with q2:
        with st.container(border=True):
            st.markdown("#### Department Queue")
            st.caption("Visit distribution by student department")

            department_counts = {}
            for visit in visits:
                department = (
                    get_value(visit, "department", "")
                    or get_value(visit, "student_department", "")
                    or "Not specified"
                )
                department_counts[str(department)] = (
                    department_counts.get(str(department), 0) + 1
                )

            if department_counts and any(
                name != "Not specified" for name in department_counts
            ):
                department_df = pd.DataFrame([
                    {"Department": name, "Visits": count}
                    for name, count in sorted(
                        department_counts.items(),
                        key=lambda x: x[1],
                        reverse=True
                    )
                ])
                st.bar_chart(
                    department_df.set_index("Department"),
                    height=190,
                    color="#397CC0"
                )
            else:
                st.markdown(
                    '<div class="cl-empty">Department information will appear '
                    'when available in visit records.</div>',
                    unsafe_allow_html=True
                )

    with q3:
        with st.container(border=True):
            st.markdown("#### Recent Student Visits")
            st.caption("Latest six registered clinic visits")

            recent = sorted(
                visits,
                key=lambda v: str(get_value(v, "created_at", "")),
                reverse=True
            )[:6]

            if recent:
                recent_rows = []
                for item in recent:
                    recent_rows.append({
                        "Student": get_value(item, "student_name", "?"),
                        "Status": get_value(item, "status", "?"),
                        "Priority": get_value(item, "nurse_priority", "?") or "?"
                    })

                st.dataframe(
                    pd.DataFrame(recent_rows),
                    hide_index=True,
                    width="stretch",
                    height=190
                )
            else:
                st.markdown(
                    '<div class="cl-empty">No student visits registered yet.</div>',
                    unsafe_allow_html=True
                )

    st.caption(
        f"Appointments recorded: {len(appointments)} | "
        f"Nurse reviews pending: {len(pending_reviews)} | "
        "Clinical decisions remain with qualified clinic staff."
    )

    st.markdown("### Quick Actions")
    st.caption("Open important clinic workflows directly from your dashboard.")

    def dashboard_go_to(target_page):
        st.session_state["dashboard_navigation"] = target_page

    action1, action2, action3 = st.columns(3, gap="medium")

    with action1:
        st.button(
            "Register New Visit",
            key="dashboard_register_action",
            width="stretch",
            on_click=dashboard_go_to,
            args=("Register Visit",)
        )

    with action2:
        st.button(
            "Open Student Queue",
            key="dashboard_queue_action",
            width="stretch",
            on_click=dashboard_go_to,
            args=("Student Queue",)
        )

    with action3:
        st.button(
            "Manage Appointments",
            key="dashboard_appointments_action",
            width="stretch",
            on_click=dashboard_go_to,
            args=("Appointment Management",)
        )

    st.info(
        "CLINIQ is an administrative support system. AI classifications "
        "are not diagnoses or medical advice. Qualified nurses must "
        "review every visit and make all clinical decisions."
    )


elif page == "Register Visit":

    # -----------------------------------------------------
    # PREMIUM PAGE STYLING
    # -----------------------------------------------------

    st.html("""
    <style>
    .cliniq-hero {
        background: linear-gradient(120deg,#10243A,#164E63);
        color: white;
        padding: 34px;
        border-radius: 20px;
        margin-bottom: 25px;
        box-shadow: 0 12px 30px rgba(16,36,58,.13);
    }
    .cliniq-kicker {
        color:#99F6E4;
        font-size:11px;
        font-weight:800;
        letter-spacing:2px;
    }
    .cliniq-heading {
        font-size:32px;
        font-weight:850;
        margin:12px 0 8px;
    }
    .cliniq-subtitle {
        color:#D5E8F0;
        font-size:14px;
        line-height:1.7;
    }
    .cliniq-pill {
        display:inline-block;
        margin-top:18px;
        padding:8px 13px;
        border:1px solid #5EEAD4;
        border-radius:30px;
        color:#99F6E4;
        font-size:11px;
        font-weight:750;
    }
    .cliniq-section {
        color:#0D9488;
        font-size:11px;
        font-weight:850;
        letter-spacing:1.5px;
    }
    .cliniq-title {
        color:#10243A;
        font-size:23px;
        font-weight:800;
        margin:5px 0;
    }
    .cliniq-description {
        color:#718096;
        font-size:13px;
        line-height:1.7;
        margin-bottom:17px;
    }
    .cliniq-info {
        background:#F0FDFA;
        border:1px solid #CCFBF1;
        border-left:4px solid #0D9488;
        border-radius:10px;
        padding:15px;
        color:#285E59;
        font-size:13px;
        line-height:1.7;
        margin:12px 0;
    }
    .cliniq-warning {
        background:#FFFAEB;
        border:1px solid #F6E3AE;
        border-radius:12px;
        padding:16px;
        color:#805B16;
        font-size:13px;
        line-height:1.7;
    }
    .cliniq-step {
        display:flex;
        align-items:center;
        gap:13px;
        padding:13px 0;
        border-bottom:1px solid #EDF2F7;
    }
    .cliniq-step-number {
        min-width:38px;
        height:38px;
        display:flex;
        align-items:center;
        justify-content:center;
        background:#E6FFFA;
        color:#0D9488;
        border-radius:11px;
        font-size:12px;
        font-weight:850;
    }
    .cliniq-step-title {
        color:#243B53;
        font-size:13px;
        font-weight:750;
    }
    .cliniq-step-description {
        color:#718096;
        font-size:11px;
        margin-top:3px;
    }
    .cliniq-priority {
        display:flex;
        align-items:center;
        gap:12px;
        padding:13px 0;
        border-bottom:1px solid #EDF2F7;
    }
    .cliniq-dot {
        width:12px;
        height:12px;
        border-radius:50%;
        flex-shrink:0;
    }
    .cliniq-priority-name {
        color:#243B53;
        font-size:13px;
        font-weight:750;
    }
    .cliniq-priority-description {
        color:#718096;
        font-size:11px;
        margin-top:3px;
    }
    .cliniq-workflow {
        background:linear-gradient(135deg,#F0FDFA,#F8FAFC);
        border:1px solid #D7F0EB;
        border-radius:13px;
        padding:17px;
        margin:12px 0;
    }
    .cliniq-workflow-title {
        color:#10243A;
        font-size:13px;
        font-weight:800;
    }
    .cliniq-workflow-description {
        color:#64748B;
        font-size:12px;
        line-height:1.6;
        margin-top:5px;
    }
    [data-testid="stVerticalBlockBorderWrapper"] {
        background:white !important;
        border:1px solid #E2EAF1 !important;
        border-radius:17px !important;
        box-shadow:0 5px 20px rgba(16,36,58,.055) !important;
    }
    .stTextInput input,.stTextArea textarea {
        background:#F8FAFC !important;
        border:1px solid #DCE5ED !important;
        border-radius:10px !important;
        font-size:14px !important;
    }
    .stTextInput input:focus,.stTextArea textarea:focus {
        border-color:#0D9488 !important;
        box-shadow:0 0 0 3px rgba(13,148,136,.12) !important;
        background:white !important;
    }
    div[data-testid="stFormSubmitButton"] button {
        background:linear-gradient(120deg,#0D9488,#0F766E) !important;
        color:white !important;
        border:0 !important;
        border-radius:11px !important;
        min-height:49px !important;
        font-weight:800 !important;
        box-shadow:0 5px 14px rgba(13,148,136,.2) !important;
    }
    div[data-testid="stFormSubmitButton"] button:hover {
        transform:translateY(-2px);
        box-shadow:0 8px 20px rgba(13,148,136,.25) !important;
    }
    
/* CLINIQ RESPONSIVE PROFESSIONAL POLISH */

html, body {
    font-size: 16px;
}

[data-testid="stMarkdownContainer"] p {
    font-size: 0.9rem;
    line-height: 1.55;
}

[data-testid="stWidgetLabel"] p,
[data-testid="stTextInput"] label,
[data-testid="stTextArea"] label {
    font-size: 0.88rem !important;
    font-weight: 600 !important;
}

[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea {
    font-size: 0.92rem !important;
    border-radius: 9px !important;
}

@media (max-width: 900px) {
    [data-testid="stHorizontalBlock"] {
        flex-direction: column !important;
        gap: 18px !important;
    }

    [data-testid="column"] {
        width: 100% !important;
        min-width: 100% !important;
        flex: 1 1 100% !important;
    }

    [data-testid="stVerticalBlockBorderWrapper"] {
        width: 100% !important;
    }
}

@media (max-width: 600px) {
    [data-testid="stAppViewContainer"] .main .block-container {
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }

    [data-testid="stMarkdownContainer"] p {
        font-size: 0.88rem;
    }
}

/* CLINIQ PERFECT ALIGNMENT */

[data-testid="stAppViewBlockContainer"] {
    max-width: 1500px !important;
    padding-top: 1.5rem !important;
    padding-bottom: 2rem !important;
}

[data-testid="stHorizontalBlock"] {
    align-items: flex-start !important;
    gap: 22px !important;
}

[data-testid="column"] {
    min-width: 0 !important;
    box-sizing: border-box !important;
}

[data-testid="stVerticalBlockBorderWrapper"] {
    box-sizing: border-box !important;
    border-radius: 12px !important;
    border-color: #D8E1EA !important;
}

[data-testid="stVerticalBlock"] {
    gap: 14px !important;
}

[data-testid="stTextInput"],
[data-testid="stTextArea"],
[data-testid="stForm"] {
    width: 100% !important;
}

[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea {
    width: 100% !important;
    box-sizing: border-box !important;
}

[data-testid="stFormSubmitButton"] button {
    width: 100% !important;
    min-height: 42px !important;
    border-radius: 9px !important;
    font-weight: 700 !important;
}

[data-testid="stMarkdownContainer"] h1,
[data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3 {
    line-height: 1.3 !important;
    margin-top: 0.2rem !important;
    margin-bottom: 0.45rem !important;
}

@media (max-width: 900px) {
    [data-testid="stHorizontalBlock"] {
        flex-direction: column !important;
        align-items: stretch !important;
        gap: 16px !important;
    }

    [data-testid="column"] {
        width: 100% !important;
        min-width: 100% !important;
        flex: 1 1 100% !important;
    }
}

@media (max-width: 600px) {
    [data-testid="stAppViewBlockContainer"] {
        padding-left: 0.8rem !important;
        padding-right: 0.8rem !important;
    }
}
</style>
    """)

    # -----------------------------------------------------
    # HERO
    # -----------------------------------------------------

    st.html("""
    <div class="cliniq-hero">
        <div class="cliniq-kicker">
            CLINIQ / SMART CLINIC MANAGEMENT
        </div>
        <div class="cliniq-heading">
            Student Visit Registration
        </div>
        <div class="cliniq-subtitle">
            A professional registration workspace for recording
            student visits and organising the clinic queue.
        </div>
        <div class="cliniq-pill">
            ● REGISTRATION PORTAL ACTIVE
        </div>
    </div>
    """)

    # -----------------------------------------------------
    # MAIN WORKSPACE
    # -----------------------------------------------------

    left, right = st.columns([1.65, 1], gap="large")

    with left:

        with st.container(border=True):

            st.html("""
            <div class="cliniq-section">01 / STUDENT PROFILE</div>
            <div class="cliniq-title">Student Information</div>
            <div class="cliniq-description">
                Enter the student's identifying information
                carefully before recording the visit.
            </div>
            """)

            with st.form(
                "registration_form",
                clear_on_submit=True
            ):

                student_name = st.text_input(
                    "Student Full Name",
                    placeholder="Enter student's full name"
                )

                student_id = st.text_input(
                    "Student ID",
                    placeholder="Enter college registration ID"
                )

                st.markdown("---")

                st.html("""
                <div class="cliniq-section">
                    02 / VISIT RECORD
                </div>
                <div class="cliniq-title">
                    Visit Information
                </div>
                <div class="cliniq-description">
                    Record the concern as stated by the student.
                    Use clear, factual language.
                </div>
                """)

                complaint = st.text_area(
                    "Reason for Clinic Visit",
                    placeholder=(
                        "Example: Student reports a headache "
                        "since this morning..."
                    ),
                    height=180
                )

                st.caption(
                    "Record the student's stated concern only. "
                    "Do not enter a diagnosis or treatment recommendation."
                )

                st.html("""
                <div class="cliniq-info">
                    <b>Privacy and data-entry reminder</b><br>
                    Record only information needed for clinic
                    registration and queue management. Keep
                    student information confidential.
                </div>
                """)

                submitted = st.form_submit_button(
                    "✚  Register Student Visit",
                    width="stretch",
                    type="primary"
                )

                # -----------------------------------------
                # VALIDATION AND BACKEND REGISTRATION
                # -----------------------------------------

                if submitted:

                    if not student_name.strip():
                        st.error(
                            "Please enter the student's full name."
                        )

                    elif not student_id.strip():
                        st.error(
                            "Please enter the student ID."
                        )

                    elif not complaint.strip():
                        st.error(
                            "Please enter the reason for the visit."
                        )

                    else:
                        try:
                            visit_id = backend.register_visit(
                                student_name=student_name.strip(),
                                complaint=complaint.strip(),
                                student_id=student_id.strip()
                            )

                            st.session_state[
                                "registration_receipt"
                            ] = {
                                "visit_id": visit_id,
                                "student_name": student_name.strip(),
                                "student_id": student_id.strip(),
                                "complaint": complaint.strip(),
                                "registered_at": datetime.now().strftime(
                                    "%d %b %Y, %I:%M %p"
                                )
                            }

                            st.rerun()

                        except Exception as error:
                            st.error(
                                f"Unable to register student visit: {error}"
                            )

    # -----------------------------------------------------
    # INFORMATION CENTRE
    # -----------------------------------------------------

    with right:

        # REGISTRATION PROCESS
        with st.container(border=True):

            st.html("""
            <div class="cliniq-section">REGISTRATION GUIDE</div>
            <div class="cliniq-title">
                Registration Process
            </div>
            <div class="cliniq-description">
                Four simple steps to create a clinic visit record.
            </div>
            """)

            steps = [
                ("01", "Student profile",
                 "Enter the student's full name."),
                ("02", "College identification",
                 "Record the correct student ID."),
                ("03", "Visit documentation",
                 "Record the student's stated concern."),
                ("04", "Registration",
                 "Submit the form to create the visit.")
            ]

            for number, heading, description in steps:

                st.html(f"""
                <div class="cliniq-step">
                    <div class="cliniq-step-number">
                        {number}
                    </div>
                    <div>
                        <div class="cliniq-step-title">
                            {heading}
                        </div>
                        <div class="cliniq-step-description">
                            {description}
                        </div>
                    </div>
                </div>
                """)

        # WHAT HAPPENS NEXT
        with st.container(border=True):

            st.html("""
            <div class="cliniq-section">VISIT WORKFLOW</div>
            <div class="cliniq-title">
                What Happens Next?
            </div>
            <div class="cliniq-description">
                The administrative registration process.
            </div>

            <div class="cliniq-workflow">
                <div class="cliniq-workflow-title">
                    01 · Visit Registered
                </div>
                <div class="cliniq-workflow-description">
                    Student information and stated concern
                    are recorded in the clinic system.
                </div>
            </div>

            <div class="cliniq-workflow">
                <div class="cliniq-workflow-title">
                    02 · Added to Queue
                </div>
                <div class="cliniq-workflow-description">
                    The visit becomes available for
                    administrative queue management.
                </div>
            </div>

            <div class="cliniq-workflow">
                <div class="cliniq-workflow-title">
                    03 · Nurse Review
                </div>
                <div class="cliniq-workflow-description">
                    A nurse reviews the visit and makes
                    the clinical priority decision.
                </div>
            </div>
            """)

        # SAFETY INFORMATION
        with st.container(border=True):

            st.html("""
            <div class="cliniq-section">
                CLINICAL SAFETY
            </div>
            <div class="cliniq-title">
                Nurse Review Required
            </div>
            <div class="cliniq-warning">
                <b>Important:</b><br>
                Registration does not assign clinical priority.
                A qualified nurse must review the visit and make
                all clinical decisions. This system does not
                diagnose, prescribe or replace professional
                judgement.
            </div>
            """)

        # NURSE PRIORITY GUIDE
        with st.container(border=True):

            st.html("""
            <div class="cliniq-section">
                PRIORITY REFERENCE
            </div>
            <div class="cliniq-title">
                Nurse Priority Guide
            </div>
            <div class="cliniq-description">
                These priority categories are assigned by
                the nurse, not during registration.
            </div>
            """)

            priorities = [
                ("#EF4444", "See Now",
                 "Requires immediate nurse review."),
                ("#F97316", "Today",
                 "Requires review during the day."),
                ("#10B981", "Routine",
                 "For routine nurse review.")
            ]

            for color, name, description in priorities:

                st.html(f"""
                <div class="cliniq-priority">
                    <div class="cliniq-dot"
                         style="background:{color};"></div>
                    <div>
                        <div class="cliniq-priority-name">
                            {name}
                        </div>
                        <div class="cliniq-priority-description">
                            {description}
                        </div>
                    </div>
                </div>
                """)

    # -----------------------------------------------------
    # DIGITAL REGISTRATION RECEIPT
    # -----------------------------------------------------

    receipt_data = st.session_state.get(
        "registration_receipt"
    )

    if receipt_data:

        st.markdown("---")

        st.html("""
        <div class="cliniq-section">
            REGISTRATION COMPLETE
        </div>
        <div class="cliniq-title">
            Visit Registration Confirmation
        </div>
        <div class="cliniq-description">
            The administrative registration record is ready.
        </div>
        """)

        with st.container(border=True):

            st.success("Student visit registered successfully.")

            receipt_col1, receipt_col2 = st.columns(2)

            with receipt_col1:

                st.markdown("**STUDENT PROFILE**")

                st.write(
                    "**Student Name:**",
                    receipt_data["student_name"]
                )

                st.write(
                    "**Student ID:**",
                    receipt_data["student_id"]
                )

            with receipt_col2:

                st.markdown("**VISIT RECORD**")

                st.write(
                    "**Visit ID:**",
                    receipt_data.get("visit_id", "Not available")
                )

                st.write(
                    "**Registered At:**",
                    receipt_data["registered_at"]
                )

                st.write(
                    "**Initial Status:** Waiting for nurse review"
                )

            st.markdown("---")

            st.markdown("**RECORDED VISIT CONCERN**")
            st.write(receipt_data["complaint"])

            receipt_text = f"""
CLINIQ - STUDENT VISIT RECEIPT

Visit ID: {receipt_data.get('visit_id', 'Not available')}

Student Name: {receipt_data['student_name']}
Student ID: {receipt_data['student_id']}

Visit Concern:
{receipt_data['complaint']}

Registered At:
{receipt_data['registered_at']}

Initial Status:
Waiting for nurse review

Clinical priority and care decisions are made by the nurse.
This receipt is an administrative registration confirmation.
"""

            st.download_button(
                "⬇ Download Registration Receipt",
                data=receipt_text,
                file_name="CLINIQ_Visit_Receipt.txt",
                mime="text/plain",
                width="stretch"
            )



# =========================================================
# STUDENT QUEUE
# =========================================================

elif page == "Student Queue":

    st.html("""
    <style>
    .queue-hero {
        background: linear-gradient(120deg, #10243A 0%, #087F8C 100%);
        padding: 28px 32px;
        border-radius: 18px;
        margin: 8px 0 24px 0;
        color: white;
        box-shadow: 0 8px 24px rgba(16,36,58,0.12);
    }
    .queue-hero h2 {
        color: white;
        font-size: 27px;
        font-weight: 750;
        margin: 0 0 8px 0;
    }
    .queue-hero p {
        color: #E1F3F4;
        font-size: 14px;
        margin: 0;
    }
    div[data-testid="stExpander"] {
        border: 1px solid #DFE8EF;
        border-radius: 14px;
        margin-bottom: 12px;
        background: white;
    }
    div[data-testid="stExpander"] summary {
        font-weight: 650;
        color: #10243A;
    }
    div[data-testid="stSelectbox"],
    div[data-testid="stTextInput"] {
        padding-bottom: 6px;
    }
    div[data-testid="stForm"] {
        background: #F7FAFC;
        border: 1px solid #E5EDF3;
        border-radius: 13px;
        padding: 16px;
    }
    

/* CLINIQ PREMIUM METRIC CARD DESIGN */

.metric-card {
    position: relative;
    overflow: hidden;
    min-height: 126px;
    padding: 22px 23px;
    background: linear-gradient(135deg, #FFFFFF 0%, #F0FAFA 100%);
    border: 1px solid #D7E8E9;
    border-left: 5px solid #0D9488;
    border-radius: 15px;
    box-shadow: 0 5px 16px rgba(16,36,58,0.07);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.metric-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 25px rgba(13,148,136,0.13);
}

.metric-label {
    color: #607789;
    font-size: 12px;
    font-weight: 750;
    letter-spacing: 0.7px;
    margin-bottom: 12px;
}

.metric-value {
    color: #10243A;
    font-size: 34px;
    font-weight: 850;
    line-height: 1.15;
}

@media (max-width: 768px) {
    .metric-card {
        min-height: 105px;
        padding: 17px;
    }

    .metric-value {
        font-size: 27px;
    }
}

</style>
    <div class="queue-hero">
        <h2>Student Visit Queue</h2>
        <p>Monitor registered visits, review nurse-assigned priorities and manage visit progress.</p>
    </div>
    """)

    st.write("")

    # -----------------------------------------------------
    # QUEUE SUMMARY
    # -----------------------------------------------------

    waiting_count = get_status_count(visits, "Waiting")
    consultation_count = get_status_count(
        visits, "In Consultation"
    )
    completed_count = get_status_count(visits, "Completed")

    q1, q2, q3, q4 = st.columns(4)

    with q1:
        metric_card("📋 Total Visits", len(visits))

    with q2:
        metric_card("Waiting", waiting_count)

    with q3:
        metric_card("🩺 In Consultation", consultation_count)

    with q4:
        metric_card("\u2713 Completed", completed_count)

    st.markdown("---")

    # -----------------------------------------------------
    # SEARCH AND FILTERS
    # -----------------------------------------------------

    st.subheader("Find Student Visits")

    filter1, filter2, filter3 = st.columns(3)

    with filter1:
        status_filter = st.selectbox(
            "Visit Status",
            [
                "All",
                "Waiting",
                "In Consultation",
                "Completed"
            ],
            key="queue_status_filter"
        )

    with filter2:
        priority_filter = st.selectbox(
            "Nurse Priority",
            [
                "All",
                "See Now",
                "Today",
                "Routine",
                "Not Assigned"
            ],
            key="queue_priority_filter"
        )

    with filter3:
        search = st.text_input(
            "Search Student",
            placeholder="Enter name or student ID",
            key="queue_search"
        )

    # -----------------------------------------------------
    # FILTER VISITS
    # -----------------------------------------------------

    filtered = []

    for visit in visits:

        visit_status = get_value(visit, "status")
        visit_priority = get_value(
            visit, "nurse_priority"
        )

        if (
            status_filter != "All"
            and visit_status != status_filter
        ):
            continue

        if priority_filter == "Not Assigned":
            if visit_priority:
                continue

        elif (
            priority_filter != "All"
            and visit_priority != priority_filter
        ):
            continue

        search_text = (
            str(get_value(visit, "student_name")) + " " +
            str(get_value(visit, "student_id"))
        ).lower()

        if search and search.lower() not in search_text:
            continue

        filtered.append(visit)

    # -----------------------------------------------------
    # SORT QUEUE
    # -----------------------------------------------------

    priority_order = {
        "See Now": 0,
        "Today": 1,
        "Routine": 2
    }

    filtered.sort(
        key=lambda visit: (
            priority_order.get(
                get_value(visit, "nurse_priority"), 3
            ),
            str(get_value(visit, "created_at"))
        )
    )

    st.markdown("---")

    st.subheader("Registered Visits")

    st.write(
        f"Showing **{len(filtered)}** matching visit(s)."
    )

    # -----------------------------------------------------
    # DISPLAY VISITS
    # -----------------------------------------------------

    if filtered:

        for visit in filtered:

            visit_id = get_value(visit, "id")
            student_name = get_value(
                visit, "student_name", "Unknown"
            )

            priority = get_value(
                visit, "nurse_priority"
            ) or "Not Assigned"

            status = get_value(
                visit, "status", "Unknown"
            )

            created_at = format_created_at(
                get_value(visit, "created_at")
            )

            with st.expander(
                f"Visit #{visit_id} | {student_name} | "
                f"{priority} | {status}"
            ):

                show_detail(visit)

                st.caption(
                    f"Registered: {created_at}"
                )

                # -----------------------------------------
                # NURSE REVIEW
                # -----------------------------------------

                if role in ["Admin", "Nurse"]:

                    st.markdown("---")
                    st.subheader("Nurse Review")

                    with st.form(
                        f"queue_review_{visit_id}"
                    ):

                        priority_options = [
                            "See Now",
                            "Today",
                            "Routine"
                        ]
                        status_options = [
                           "Waiting",
                           "In Review",
                           "Completed",
                           "Cancelled"
                        ]
                        
                        

                        current_priority_index = (
                            priority_options.index(priority)
                            if priority in priority_options
                            else 0
                        )

                        current_status_index = (
                            status_options.index(status)
                            if status in status_options
                            else 0
                        )

                        new_priority = st.selectbox(
                            "Nurse-assigned Priority",
                            priority_options,
                            index=current_priority_index
                        )

                        new_status = st.selectbox(
                            "Visit Status",
                            status_options,
                            index=current_status_index
                        )

                        save_review = st.form_submit_button(
                            "Save Nurse Review",
                            width="stretch"
                        )

                    
                    if save_review:

                        try:
                            backend.update_nurse_review(
                                visit_id,
                                new_priority
                            )

                            backend.update_visit_status(
                                visit_id,
                                new_status
                            )

                            st.success(
                                "Visit information updated."
                            )

                            st.rerun()

                        except Exception as error:
                            st.error(
                                f"Unable to update visit: {error}"
                            )

                else:

                    st.info(
                        "Read-only access: only Admin or Nurse "
                        "can update clinical priority and visit status."
                    )

    else:

        st.info(
            "No student visits match your search or filters."
        )

    # -----------------------------------------------------
    # QUEUE INFORMATION
    # -----------------------------------------------------

    st.markdown("---")

    st.caption(
        "Important: CLINIQ does not automatically determine "
        "clinical urgency. Only the nurse assigns visit priority. "
        "The system does not diagnose, recommend treatment, "
        "or remove students from the queue."
    )


# =========================================================
# VISIT DETAILS
# =========================================================

elif page == "Visit Details":

    st.html("""
    <div style="
        background:linear-gradient(120deg,#10243A 0%,#087F8C 100%);
        padding:29px 32px;
        border-radius:18px;
        margin:8px 0 24px 0;
        box-shadow:0 8px 24px rgba(16,36,58,0.13);
    ">
        <div style="
            color:#9DE5DE;
            font-size:12px;
            font-weight:800;
            letter-spacing:2px;
            margin-bottom:10px;
        ">CLINIQ / PATIENT RECORDS</div>
        <div style="
            color:white;
            font-size:28px;
            font-weight:800;
            margin-bottom:8px;
        ">Student Visit Details</div>
        <div style="
            color:#E1F3F4;
            font-size:14px;
            line-height:1.6;
        ">Access individual visit records and review registered student information.</div>
    </div>
    """)

    if visits:

        search_term = st.text_input(
            "Search student or visit",
            placeholder="Enter student name, student ID or visit ID...",
            key="visit_details_search"
        )

        filtered_visits = [
            v for v in visits
            if search_term.strip().lower() in " ".join([
                str(get_value(v, "id", "")),
                str(get_value(v, "student_name", "")),
                str(get_value(v, "student_id", ""))
            ]).lower()
        ]

        filtered_visits = sorted(
            filtered_visits,
            key=lambda v: str(get_value(v, "created_at", "")),
            reverse=True
        )

        if not filtered_visits:
            st.warning("No matching student visits found.")
            st.stop()

        st.caption(f"{len(filtered_visits)} matching visit(s) found.")

        visit_options = {
            f"Visit #{get_value(v, 'id')} - "
            f"{get_value(v, 'student_name')}": get_value(v, "id")
            for v in filtered_visits
        }

        selected_label = st.selectbox(
            "Select Student Visit",
            list(visit_options.keys())
        )

        selected_id = visit_options[selected_label]

        try:
            selected_visit = backend.get_visit(selected_id)

            if selected_visit:
                show_detail(selected_visit)
            else:
                st.warning("Visit details could not be found.")

        except Exception as error:
            st.error(f"Unable to load visit: {error}")

    else:
        st.info("No visit records are available.")



# =========================================================
# APPOINTMENT MANAGEMENT
# =========================================================

elif page == "Appointment Management":

    st.html("""
    <div style="
        background:linear-gradient(120deg,#10243A 0%,#087F8C 100%);
        padding:29px 32px;
        border-radius:18px;
        margin:8px 0 24px 0;
        box-shadow:0 8px 24px rgba(16,36,58,0.13);
    ">
        <div style="color:#9DE5DE;font-size:12px;font-weight:800;
                    letter-spacing:2px;margin-bottom:10px;">
            CLINIQ / SCHEDULING CENTRE
        </div>
        <div style="color:white;font-size:28px;font-weight:800;
                    margin-bottom:8px;">
            Appointment Management
        </div>
        <div style="color:#E1F3F4;font-size:14px;line-height:1.6;">
            Book student appointments, monitor schedules and manage
            appointment records in one place.
        </div>
    </div>
    """)

    appointments = backend.get_all_appointments() or []

    # -----------------------------------------------------
    # APPOINTMENT SUMMARY
    # -----------------------------------------------------

    total_appointments = len(appointments)

    scheduled_count = sum(
        1 for a in appointments
        if str(a.get("status", "")).lower() == "scheduled"
    )

    completed_count = sum(
        1 for a in appointments
        if str(a.get("status", "")).lower() == "completed"
    )

    cancelled_count = sum(
        1 for a in appointments
        if str(a.get("status", "")).lower() == "cancelled"
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        metric_card("Total Appointments", total_appointments)

    with c2:
        metric_card("Scheduled", scheduled_count)

    with c3:
        metric_card("Completed", completed_count)

    with c4:
        metric_card("Cancelled", cancelled_count)

    st.markdown("---")

    # -----------------------------------------------------
    # APPOINTMENT TABS
    # -----------------------------------------------------

    booking_tab, records_tab = st.tabs([
        "\u2795 Book Appointment",
        "📋 Appointment Records"
    ])

    # -----------------------------------------------------
    # BOOK APPOINTMENT
    # -----------------------------------------------------

    with booking_tab:

        st.html("""
        <div style="
            background:#F0F7FA;
            border:1px solid #DCE9EF;
            border-left:5px solid #0D9488;
            border-radius:12px;
            padding:16px 20px;
            margin:8px 0 20px 0;
        ">
            <div style="color:#10243A;font-size:19px;font-weight:750;">
                New Appointment Booking
            </div>
            <div style="color:#64788A;font-size:13px;margin-top:5px;">
                Enter the student's details and choose a suitable clinic date and time.
            </div>
        </div>
        """)

        left, right = st.columns([1.5, 1], gap="large")

        with left:

            with st.form("appointment_booking_form"):

                student_name = st.text_input(
                    "Student Full Name",
                    placeholder="Enter student name"
                )

                student_id = st.text_input(
                    "Student ID",
                    placeholder="Enter college ID"
                )

                appointment_date = st.date_input(
                    "Appointment Date",
                    min_value=date.today()
                )

                appointment_time = st.time_input(
                    "Appointment Time"
                )

                purpose = st.text_area(
                    "Appointment Purpose",
                    placeholder="Enter the purpose of the appointment...",
                    height=120
                )

                submitted = st.form_submit_button(
                    "📅 Confirm Appointment",
                    width="stretch"
                )

            if submitted:

                if not student_name.strip():
                    st.error("Please enter the student's name.")

                elif not student_id.strip():
                    st.error("Please enter the student ID.")

                elif not purpose.strip():
                    st.error("Please enter the appointment purpose.")

                else:

                    
                    try:
                        appointment_id = backend.book_appointment(
                            student_name=student_name.strip(),
                            appointment_date=appointment_date.isoformat(),
                            appointment_time=appointment_time.strftime("%H:%M"),
                            student_id=student_id.strip(),
                            purpose=purpose.strip()
                        )

                        st.success(
                            f"Appointment booked successfully! "
                            f"Appointment ID: {appointment_id}"
                        )

                        st.rerun()

                    except Exception as error:
                        st.error(
                            f"Unable to book appointment: {error}"
                        )


        with right:

            st.info(
                "Use this form to schedule a clinic appointment "
                "for a student."
            )

            st.markdown("### Booking Guidelines")

            st.write("1. Enter the student's name.")
            st.write("2. Enter the student ID.")
            st.write("3. Select the appointment date.")
            st.write("4. Choose the appointment time.")
            st.write("5. Enter the appointment purpose.")
            st.write("6. Confirm the booking.")

            st.warning(
                "Appointment booking does not replace immediate "
                "clinical assessment. Students with urgent concerns "
                "should be referred to the nurse."
            )

    # -----------------------------------------------------
    # APPOINTMENT RECORDS
    # -----------------------------------------------------

    with records_tab:

        st.html("""
        <div style="
            background:#F0F7FA;
            border:1px solid #DCE9EF;
            border-left:5px solid #0D9488;
            border-radius:12px;
            padding:16px 20px;
            margin:8px 0 20px 0;
        ">
            <div style="color:#10243A;font-size:19px;font-weight:750;">
                Appointment Records
            </div>
            <div style="color:#64788A;font-size:13px;margin-top:5px;">
                Search bookings, filter by status, update records and export appointment reports.
            </div>
        </div>
        """)

        if appointments:

            search_text = st.text_input(
                "🔎 Search by student name or ID",
                key="appointment_search"
            )

            status_filter = st.selectbox(
                "Filter by appointment status",
                [
                    "All",
                    "Scheduled",
                    "Completed",
                    "Cancelled"
                ],
                key="appointment_status_filter"
            )

            filtered_appointments = []

            for appointment in appointments:

                name = str(appointment.get("student_name", ""))
                student_id = str(appointment.get("student_id", ""))
                status = str(appointment.get("status", ""))

                matches_search = (
                    search_text.lower() in name.lower()
                    or search_text.lower() in student_id.lower()
                )

                matches_status = (
                    status_filter == "All"
                    or status.lower() == status_filter.lower()
                )

                if matches_search and matches_status:
                    filtered_appointments.append(appointment)

            st.caption(
                f"Showing {len(filtered_appointments)} appointment(s)"
            )

            if filtered_appointments:

                appointment_df = pd.DataFrame(
                    filtered_appointments
                )

                st.dataframe(
                    appointment_df,
                    width="stretch",
                    hide_index=True
                )

                st.markdown("### Update Appointment Status")

                appointment_options = {
                    str(a.get("id")): (
                        f"{a.get('student_name', 'Student')} "
                        f"— {a.get('appointment_date', 'Date')} "
                        f"({a.get('status', 'Unknown')})"
                    )
                    for a in filtered_appointments
                }

                selected_id = st.selectbox(
                    "Select an appointment",
                    list(appointment_options.keys()),
                    format_func=lambda x: appointment_options[x]
                )

                
                new_status = st.selectbox(
                    "New Status",
                    [
                        "Booked",
                        "Completed",
                        "Cancelled",
                        "Rescheduled"
                    ],
                    key="new_appointment_status"
                )

                if st.button(
                    "Update Appointment",
                    width="stretch"
                ):

                    try:

                        backend.update_appointment_status(
                            int(selected_id),
                            new_status
                        )

                        st.success(
                            "Appointment status updated successfully."
                        )

                        st.rerun()

                    except Exception as error:

                        st.error(
                            f"Unable to update appointment: {error}"
                        )

                # CSV EXPORT

                csv_data = appointment_df.to_csv(index=False)

                st.download_button(
                    "\u2B07 Download Appointment Report",
                    data=csv_data,
                    file_name="CLINIQ_Appointment_Report.csv",
                    mime="text/csv",
                    width="stretch"
                )

            else:

                st.info(
                    "No appointments match your search or filter."
                )

        else:

            st.info(
                "No appointments have been booked yet."
            )



# =========================================================
# CLINIC REPORTS
# =========================================================

elif page == "Clinic Reports":

    st.html("""
    <div style="
        background:linear-gradient(120deg,#10243A 0%,#087F8C 100%);
        padding:29px 32px;
        border-radius:18px;
        margin:8px 0 24px 0;
        box-shadow:0 8px 24px rgba(16,36,58,0.13);
    ">
        <div style="color:#9DE5DE;font-size:12px;font-weight:800;
                    letter-spacing:2px;margin-bottom:10px;">
            CLINIQ / INSIGHTS & PERFORMANCE
        </div>
        <div style="color:white;font-size:28px;font-weight:800;
                    margin-bottom:8px;">
            Clinic Reports & Analytics
        </div>
        <div style="color:#E1F3F4;font-size:14px;line-height:1.6;">
            Explore clinic activity, review visit trends and generate
            administrative insights using recorded visit data.
        </div>
    </div>
    """)

    visits = backend.get_all_visits() or []

    if not visits:

        st.info("No student visit records are available yet.")

    else:

        report_df = pd.DataFrame(visits)

        # -------------------------------------------------
        # PREPARE REPORT DATA
        # -------------------------------------------------

        if "created_at" in report_df.columns:

            report_df["Report Date"] = pd.to_datetime(
                report_df["created_at"],
                errors="coerce"
            )

            report_df = report_df.dropna(
                subset=["Report Date"]
            )

            report_df["Date Only"] = (
                report_df["Report Date"].dt.date
            )

        else:

            st.error(
                "Visit date information is unavailable."
            )
            st.stop()

        # -------------------------------------------------
        # DATE FILTER
        # -------------------------------------------------

        st.html("""
        <div style="
            background:#F0F7FA;
            border:1px solid #DCE9EF;
            border-left:5px solid #0D9488;
            border-radius:12px;
            padding:16px 20px;
            margin:8px 0 18px 0;
        ">
            <div style="color:#10243A;font-size:19px;font-weight:750;">
                Report Date Range
            </div>
            <div style="color:#64788A;font-size:13px;margin-top:5px;">
                Select a reporting period to filter clinic visit analytics.
            </div>
        </div>
        """)

        min_date = report_df["Date Only"].min()
        max_date = report_df["Date Only"].max()

        date_col1, date_col2 = st.columns(2)

        with date_col1:

            start_date = st.date_input(
                "Start Date",
                value=min_date,
                min_value=min_date,
                max_value=max_date,
                key="report_start_date"
            )

        with date_col2:

            end_date = st.date_input(
                "End Date",
                value=max_date,
                min_value=min_date,
                max_value=max_date,
                key="report_end_date"
            )

        if start_date > end_date:

            st.error("Start date cannot be after end date.")
            st.stop()

        filtered_df = report_df[
            (report_df["Date Only"] >= start_date)
            & (report_df["Date Only"] <= end_date)
        ].copy()

        st.markdown("---")

        if filtered_df.empty:

            st.info(
                "No visits were recorded during this date range."
            )
            st.stop()

        # -------------------------------------------------
        # SUMMARY METRICS
        # -------------------------------------------------

        total_visits = len(filtered_df)

        waiting_visits = (
            filtered_df["status"].astype(str).str.lower()
            == "waiting"
        ).sum() if "status" in filtered_df.columns else 0

        consultation_visits = (
            filtered_df["status"].astype(str).str.lower()
            == "in consultation"
        ).sum() if "status" in filtered_df.columns else 0

        completed_visits = (
            filtered_df["status"].astype(str).str.lower()
            == "completed"
        ).sum() if "status" in filtered_df.columns else 0

        metric_columns = st.columns(4)

        with metric_columns[0]:
            metric_card("Total Visits", total_visits)

        with metric_columns[1]:
            metric_card("Waiting", int(waiting_visits))

        with metric_columns[2]:
            metric_card("In Consultation", int(consultation_visits))

        with metric_columns[3]:
            metric_card("Completed", int(completed_visits))

        st.markdown("---")

        # -------------------------------------------------
        # STATUS ANALYSIS
        # -------------------------------------------------

        st.markdown("### Visit Status Analysis")
        st.caption("Understand how student visits are distributed across clinic workflow statuses.")

        if "status" in filtered_df.columns:

            status_data = (
                filtered_df["status"]
                .fillna("Unknown")
                .value_counts()
                .rename_axis("Status")
                .reset_index(name="Visits")
            )

            chart_col1, chart_col2 = st.columns(2)

            with chart_col1:

                st.markdown("**Visit Status Distribution**")

                st.bar_chart(
                    status_data.set_index("Status"),
                    width="stretch"
                )

            with chart_col2:

                st.markdown("**Visit Status Details**")

                st.dataframe(
                    status_data,
                    width="stretch",
                    hide_index=True
                )

        st.markdown("---")

        # -------------------------------------------------
        # NURSE PRIORITY ANALYSIS
        # -------------------------------------------------

        st.markdown("### Nurse Priority Analysis")
        st.caption("Review priority categories recorded by nurses for administrative monitoring.")

        if "priority" in filtered_df.columns:

            priority_data = (
                filtered_df["priority"]
                .fillna("Not Assigned")
                .replace("", "Not Assigned")
                .value_counts()
                .rename_axis("Nurse Priority")
                .reset_index(name="Visits")
            )

            priority_col1, priority_col2 = st.columns(2)

            with priority_col1:

                st.markdown("**Priority Distribution**")

                st.bar_chart(
                    priority_data.set_index("Nurse Priority"),
                    width="stretch"
                )

            with priority_col2:

                st.dataframe(
                    priority_data,
                    width="stretch",
                    hide_index=True
                )

            st.caption(
                "Priority categories are recorded from nurse reviews. "
                "These charts do not independently assess clinical urgency."
            )

        else:

            st.info(
                "Nurse priority information is not available."
            )

        st.markdown("---")

        # -------------------------------------------------
        # DAILY VISIT TREND
        # -------------------------------------------------

        st.markdown("### Daily Visit Trend")
        st.caption("Track the number of registered student visits across the selected dates.")

        daily_data = (
            filtered_df.groupby("Date Only")
            .size()
            .reset_index(name="Total Visits")
        )

        daily_data["Date"] = daily_data["Date Only"].astype(str)

        st.line_chart(
            daily_data.set_index("Date")["Total Visits"],
            width="stretch"
        )

        st.markdown("---")

        # -------------------------------------------------
        # REPORT TABLE
        # -------------------------------------------------

        st.html("""
        <div style="
            background:#F0F7FA;
            border:1px solid #DCE9EF;
            border-left:5px solid #0D9488;
            border-radius:12px;
            padding:16px 20px;
            margin:8px 0 18px 0;
        ">
            <div style="color:#10243A;font-size:19px;font-weight:750;">
                Detailed Visit Records
            </div>
            <div style="color:#64788A;font-size:13px;margin-top:5px;">
                Review registered visit information for the selected reporting period.
            </div>
        </div>
        """)

        display_columns = [
            column for column in [
                "id",
                "student_name",
                "student_id",
                "complaint",
                "priority",
                "status",
                "created_at"
            ]
            if column in filtered_df.columns
        ]

        st.dataframe(
            filtered_df[display_columns],
            width="stretch",
            hide_index=True
        )

        # -------------------------------------------------
        # DOWNLOAD REPORT
        # -------------------------------------------------

        st.markdown("---")

        export_df = filtered_df.drop(
            columns=["Date Only"],
            errors="ignore"
        )

        csv_report = export_df.to_csv(index=False)

        st.download_button(
            "\u2B07 Download Clinic Report (CSV)",
            data=csv_report,
            file_name="CLINIQ_Clinic_Report.csv",
            mime="text/csv",
            width="stretch"
        )

        st.success(
            f"Report prepared for {len(filtered_df)} visit record(s)."
        )



# =========================================================
# STAFF MANAGEMENT
# =========================================================

elif page == "Staff Management":

    st.html("""
    <div style="
        background:linear-gradient(120deg,#10243A 0%,#087F8C 100%);
        padding:29px 32px;
        border-radius:18px;
        margin:8px 0 24px 0;
        box-shadow:0 8px 24px rgba(16,36,58,0.13);
    ">
        <div style="color:#9DE5DE;font-size:12px;font-weight:800;
                    letter-spacing:2px;margin-bottom:10px;">
            CLINIQ / ADMINISTRATION
        </div>
        <div style="color:white;font-size:28px;font-weight:800;
                    margin-bottom:8px;">
            Staff Management
        </div>
        <div style="color:#E1F3F4;font-size:14px;line-height:1.6;">
            Manage clinic team accounts, assign access roles and
            maintain the staff directory securely.
        </div>
    </div>
    """)

    if role != "Admin":

        st.error(
            "Access denied. Only administrators can manage staff."
        )
        st.stop()

    # -----------------------------------------------------
    # LOAD STAFF
    # -----------------------------------------------------

    try:
        staff_records = backend.get_all_staff() or []

    except Exception as error:
        st.error(f"Unable to load staff records: {error}")
        st.stop()

    total_staff = len(staff_records)

    admin_count = sum(
        1 for staff in staff_records
        if str(staff.get("role", "")).lower() == "admin"
    )

    nurse_count = sum(
        1 for staff in staff_records
        if str(staff.get("role", "")).lower() == "nurse"
    )

    other_count = total_staff - admin_count - nurse_count

    # -----------------------------------------------------
    # STAFF SUMMARY
    # -----------------------------------------------------

    st.markdown("### Staff Overview")
    st.caption("A quick summary of registered clinic team members and their assigned roles.")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        metric_card("Total Staff", total_staff)

    with col2:
        metric_card("Administrators", admin_count)

    with col3:
        metric_card("Nurses", nurse_count)

    with col4:
        metric_card("Other Staff", other_count)

    st.markdown("---")

    # -----------------------------------------------------
    # STAFF MANAGEMENT TABS
    # -----------------------------------------------------

    add_tab, records_tab = st.tabs([
        "\u2795 Add Staff",
        "📋 Staff Directory"
    ])

    # -----------------------------------------------------
    # ADD STAFF
    # -----------------------------------------------------

    with add_tab:

        st.html("""
        <div style="
            background:#F0F7FA;
            border:1px solid #DCE9EF;
            border-left:5px solid #0D9488;
            border-radius:12px;
            padding:16px 20px;
            margin:8px 0 18px 0;
        ">
            <div style="color:#10243A;font-size:19px;font-weight:750;">
                Create Staff Account
            </div>
            <div style="color:#64788A;font-size:13px;margin-top:5px;">
                Register an authorised team member and assign their clinic access role.
            </div>
        </div>
        """)

        st.info(
            "Create a unique username and assign an appropriate "
            "clinic role to each staff member."
        )

        with st.form("add_staff_form", clear_on_submit=True):

            full_name = st.text_input(
                "Staff Full Name",
                placeholder="Enter full name"
            )

            username = st.text_input(
                "Username",
                placeholder="Create a username"
            )

            password = st.text_input(
                "Password",
                type="password",
                placeholder="Create a password"
            )

            staff_role = st.selectbox(
                "Staff Role",
                ["Admin", "Nurse", "Staff"]
            )

            add_submitted = st.form_submit_button(
                "\u2795 Create Staff Account",
                width="stretch"
            )

        if add_submitted:

            if not full_name.strip():
                st.error("Please enter the staff member's name.")

            elif not username.strip():
                st.error("Please enter a username.")

            elif not password.strip():
                st.error("Please enter a password.")

            else:

                try:

                    backend.add_staff(
                        full_name.strip(),
                        username.strip(),
                        password,
                        staff_role
                    )

                    st.success(
                        "Staff account created successfully."
                    )

                    st.rerun()

                except Exception as error:

                    st.error(
                        f"Unable to create staff account: {error}"
                    )

    # -----------------------------------------------------
    # STAFF DIRECTORY
    # -----------------------------------------------------

    with records_tab:

        st.html("""
        <div style="
            background:#F0F7FA;
            border:1px solid #DCE9EF;
            border-left:5px solid #0D9488;
            border-radius:12px;
            padding:16px 20px;
            margin:8px 0 18px 0;
        ">
            <div style="color:#10243A;font-size:19px;font-weight:750;">
                Registered Staff Directory
            </div>
            <div style="color:#64788A;font-size:13px;margin-top:5px;">
                Search clinic team members and review their registered account details and access roles.
            </div>
        </div>
        """)

        if staff_records:

            search_staff = st.text_input(
                "🔎 Search staff by name or username",
                key="staff_search"
            )

            filtered_staff = []

            for staff in staff_records:

                name = str(staff.get("full_name", ""))
                username_value = str(staff.get("username", ""))

                if (
                    search_staff.lower() in name.lower()
                    or search_staff.lower() in username_value.lower()
                ):
                    filtered_staff.append(staff)

            st.caption(
                f"Showing {len(filtered_staff)} staff member(s)"
            )

            if filtered_staff:

                safe_staff = []

                for staff in filtered_staff:

                    safe_staff.append({
                        "Staff ID": staff.get("id", ""),
                        "Full Name": staff.get("full_name", ""),
                        "Username": staff.get("username", ""),
                        "Role": staff.get("role", ""),
                      "Status": (
                          "Active"
                          if staff.get("active") in (1, True, "1")
                         else "Inactive"
                         )
                    })

                st.dataframe(
                    pd.DataFrame(safe_staff),
                    width="stretch",
                    hide_index=True
                )

                st.markdown("---")

                st.subheader("Update Staff Role")

                staff_with_ids = [
                    staff for staff in filtered_staff
                    if staff.get("id") is not None
                ]

                if staff_with_ids:

                    staff_options = {
                        str(staff["id"]): (
                            f"{staff.get('full_name', 'Staff')} "
                            f"({staff.get('username', '')})"
                        )
                        for staff in staff_with_ids
                    }

                    selected_staff_id = st.selectbox(
                        "Select Staff Member",
                        list(staff_options.keys()),
                        format_func=lambda x: staff_options[x]
                    )

                    selected_staff = next(
                        staff for staff in staff_with_ids
                        if str(staff["id"]) == selected_staff_id
                    )

                    current_role = selected_staff.get("role", "Staff")

                    role_options = ["Admin", "Nurse", "Staff"]

                    if current_role not in role_options:
                        current_role = "Staff"

                    new_role = st.selectbox(
                        "New Role",
                        role_options,
                        index=role_options.index(current_role),
                        key="staff_new_role"
                    )

                    if st.button(
                        "Update Staff Role",
                        width="stretch"
                    ):

                        try:

                            backend.update_staff_role(
                                int(selected_staff_id),
                                new_role
                            )

                            st.success("Staff role updated.")
                            st.rerun()

                        except Exception as error:

                            st.error(
                                f"Unable to update role: {error}"
                            )

                    # -------------------------------------
                    # DEACTIVATE STAFF
                    # -------------------------------------

                    st.markdown("---")

                    st.subheader("Deactivate Staff Account")

                    st.warning(
                        "Deactivation may prevent the selected staff "
                        "member from accessing the system."
                    )

                    if st.button(
                        "Deactivate Selected Staff",
                        type="secondary",
                        width="stretch"
                    ):

                        try:

                            if (
                                str(selected_staff_id)
                                == str(st.session_state.get("staff_id"))
                            ):

                                st.error(
                                    "You cannot deactivate your own account."
                                )

                            else:

                                backend.deactivate_staff(
                                    int(selected_staff_id)
                                )

                                st.success(
                                    "Staff account deactivated."
                                )

                                st.rerun()

                        except Exception as error:

                            st.error(
                                f"Unable to deactivate staff: {error}"
                            )

            else:

                st.info("No staff members match your search.")

        else:

            st.info("No staff records are available.")




# =========================================================
# VISIT HISTORY
# =========================================================



# =========================================================
# CSV UPLOAD & AI PROCESSING - ASSIGNMENT VERSION
# =========================================================

elif page == "CSV Upload & AI Processing":

    from backend_v2.ai_service import classify_complaint
    from backend_v2.csv_service import (
        read_visits_csv,
        process_visit_records,
        export_nurse_queue_csv,
        build_summary_report
    )

    st.html("""
    <div style="
        background: linear-gradient(120deg, #10243A 0%, #087F8C 100%);
        padding: 30px 32px;
        border-radius: 18px;
        margin: 8px 0 24px 0;
        box-shadow: 0 8px 24px rgba(16,36,58,0.13);
    ">
        <div style="
            color: #9DE5DE;
            font-size: 12px;
            font-weight: 800;
            letter-spacing: 2px;
            margin-bottom: 10px;
        ">CLINIQ  /  INTELLIGENT CLINIC MANAGEMENT</div>
        <div style="
            color: white;
            font-size: 29px;
            font-weight: 800;
            margin-bottom: 9px;
        ">AI Visit Classification Centre</div>
        <div style="
            color: #E1F3F4;
            font-size: 14px;
            line-height: 1.6;
        ">Upload student visit records, organise administrative priority
        suggestions, and prepare structured reports for nurse review.</div>
    </div>
    """)

    st.warning(
        "SAFETY NOTICE: AI suggestions are not diagnoses or medical "
        "advice. A qualified nurse must review every visit and make "
        "the final priority decision. Potential emergency warning "
        "signs require immediate human attention."
    )

    # -----------------------------------------------------
    # 1. UPLOAD CSV
    # -----------------------------------------------------

    st.html("""
    <div style="
        background: #FFFFFF;
        border: 1px solid #DFE8EF;
        border-left: 5px solid #0D9488;
        border-radius: 14px;
        padding: 20px 23px;
        margin: 8px 0 18px 0;
    ">
        <div style="font-size:19px;font-weight:750;color:#10243A;margin-bottom:8px;">
            01 / Upload Student Visit Records
        </div>
        <div style="font-size:14px;color:#64748B;line-height:1.6;margin-bottom:15px;">
            Import a CSV file containing student visit information.
            Review the records before starting AI-assisted administrative classification.
        </div>
        <div style="font-size:13px;font-weight:700;color:#10243A;margin-bottom:9px;">
            REQUIRED CSV COLUMNS
        </div>
        <div style="display:flex;flex-wrap:wrap;gap:9px;">
            <span style="background:#EAF2F8;padding:8px 13px;border-radius:8px;color:#10243A;font-size:13px;">
                <b>id</b> ? Visit ID
            </span>
            <span style="background:#EAF2F8;padding:8px 13px;border-radius:8px;color:#10243A;font-size:13px;">
                <b>time</b> ? Arrival time
            </span>
            <span style="background:#EAF2F8;padding:8px 13px;border-radius:8px;color:#10243A;font-size:13px;">
                <b>note</b> ? Original complaint
            </span>
        </div>
        <div style="font-size:12px;color:#718096;margin-top:13px;">
            Supports English, Tamil and Tanglish notes. Use the sample CSV below as a template.
        </div>
    </div>
    """)

    st.subheader("Download a sample file")

    sample_csv = """id,time,note
V001,09:00,I have a high fever and headache
V002,09:05,I twisted my ankle while playing football
V003,09:10,Enakku stomach pain irukku
V004,09:15,I have a severe headache
V005,09:20,I got a small cut on my finger
V006,09:25,I am feeling dizzy
V007,09:30,Enakku cold and cough irukku
V008,09:35,I have a skin rash and itching
V009,09:40,I feel like vomiting
V010,09:45,I have pain in my left knee
V011,09:50,I am having difficulty breathing
V012,09:55,Enakku kannu vali irukku
V013,10:00,I have a toothache
V014,10:05,I fainted in the classroom
V015,10:10,I have a mild sore throat
V016,10:15,My hand is swollen after an insect bite
V017,10:20,Enakku romba tired ah irukku
V018,10:25,I have back pain after carrying my bag
V019,10:30,I have chest pain
V020,10:35,I have a mild stomach ache after lunch
"""

    st.download_button(
        "Download 20-visit sample CSV",
        data=sample_csv.encode("utf-8-sig"),
        file_name="visits.csv",
        mime="text/csv",
        width="stretch"
    )

    uploaded_csv = st.file_uploader(
        "Choose visits.csv",
        type=["csv"],
        key="assignment_visits_upload"
    )

    if uploaded_csv is not None:

        try:
            uploaded_content = uploaded_csv.getvalue()

            records = read_visits_csv(uploaded_content)

            st.success(
                f"Successfully loaded {len(records)} visit notes."
            )

            # -------------------------------------------------
            # 2. INPUT PREVIEW
            # -------------------------------------------------

            st.subheader("2. Input Preview")

            input_df = pd.DataFrame(records)

            st.dataframe(
                input_df,
                width="stretch",
                hide_index=True
            )

            st.info(
                "Check the uploaded notes before starting AI processing."
            )

            # -------------------------------------------------
            # 3. AI CLASSIFICATION
            # -------------------------------------------------

            st.subheader("3. AI Classification")

            if st.button(
                "Start AI Classification",
                type="primary",
                width="stretch",
                key="assignment_run_ai"
            ):

                with st.spinner(
                    "Processing all student visits. Please wait..."
                ):

                    results = process_visit_records(
                        records,
                        classify_complaint
                    )

                    st.session_state[
                        "assignment_csv_results"
                    ] = results

                    st.session_state[
                        "assignment_csv_content"
                    ] = uploaded_content

                st.success(
                    "Classification completed. "
                    "All results require nurse review."
                )

            # -------------------------------------------------
            # DISPLAY RESULTS AND DOWNLOADS
            # -------------------------------------------------

            if (
                "assignment_csv_results" in st.session_state
                and st.session_state.get(
                    "assignment_csv_content"
                ) == uploaded_content
            ):

                results = st.session_state[
                    "assignment_csv_results"
                ]

                st.html("""
                <div style="
                    background:#FFFFFF;
                    border:1px solid #DFE8EF;
                    border-left:5px solid #0D9488;
                    border-radius:14px;
                    padding:19px 22px;
                    margin:22px 0 16px 0;
                ">
                    <div style="font-size:19px;font-weight:750;color:#10243A;">
                        03 / AI Classification Results
                    </div>
                    <div style="font-size:13px;color:#718096;margin-top:6px;">
                        Review the administrative classification suggestions for every uploaded visit.
                    </div>
                </div>
                """)

                results_df = pd.DataFrame(results)

                st.dataframe(
                    results_df[
                        [
                            "id",
                            "time",
                            "category",
                            "priority",
                            "summary"
                        ]
                    ],
                    width="stretch",
                    hide_index=True
                )

                # Priority counts
                priority_counts = {
                    "see_now": 0,
                    "today": 0,
                    "routine": 0
                }

                for item in results:
                    priority = item["priority"]

                    if priority in priority_counts:
                        priority_counts[priority] += 1

                st.markdown("#### Priority Distribution")

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric(
                        label="See Now",
                        value=priority_counts["see_now"],
                        help="Highest administrative priority suggestion. Nurse review is required."
                    )

                with col2:
                    st.metric(
                        label="Today",
                        value=priority_counts["today"],
                        help="Administrative suggestion for review today."
                    )

                with col3:
                    st.metric(
                        label="Routine",
                        value=priority_counts["routine"],
                        help="Routine administrative review suggestion."
                    )

                st.info(
                    "Priority order is an administrative suggestion. "
                    "A nurse must independently review every visit."
                )

                # -------------------------------------------------
                # 4. OUTPUT FILES
                # -------------------------------------------------

                st.html("""
                <div style="
                    background:#FFFFFF;
                    border:1px solid #DFE8EF;
                    border-left:5px solid #0D9488;
                    border-radius:14px;
                    padding:19px 22px;
                    margin:22px 0 16px 0;
                ">
                    <div style="font-size:19px;font-weight:750;color:#10243A;">
                        04 / Download Clinic Reports
                    </div>
                    <div style="font-size:13px;color:#718096;margin-top:6px;">
                        Export the processed nurse queue and clinic summary.
                    </div>
                </div>
                """)

                st.markdown(
                    """
                    **Output 1 - nurse_queue.csv**

                    Contains every visit, the original complaint,
                    category, priority and summary.
                    For nurse review only.

                    **Output 2 - summary.txt**

                    Contains counts by priority, category and
                    arrival hour. It does not contain student notes.
                    """
                )

                nurse_queue_data = export_nurse_queue_csv(results)

                summary_data = build_summary_report(results)

                col1, col2 = st.columns(2)

                with col1:
                    st.download_button(
                        label="Download nurse_queue.csv",
                        data=nurse_queue_data.encode("utf-8-sig"),
                        file_name="nurse_queue.csv",
                        mime="text/csv",
                        width="stretch",
                        key="download_nurse_queue"
                    )

                with col2:
                    st.download_button(
                        label="Download summary.txt",
                        data=summary_data.encode("utf-8"),
                        file_name="summary.txt",
                        mime="text/plain",
                        width="stretch",
                        key="download_clinic_summary"
                    )

                st.success(
                    "Both assignment output files are ready for download."
                )

                st.caption(
                    "CLINIQ Academic Project Prototype | "
                    "All clinical decisions belong to qualified nurses."
                )

        except Exception as error:

            st.error(
                f"CSV processing error: {error}"
            )


elif page == "Visit History":

    st.html("""
    <div style="
        background:linear-gradient(120deg,#10243A 0%,#087F8C 100%);
        padding:29px 32px;
        border-radius:18px;
        margin:8px 0 24px 0;
        box-shadow:0 8px 24px rgba(16,36,58,0.13);
    ">
        <div style="color:#9DE5DE;font-size:12px;font-weight:800;
                    letter-spacing:2px;margin-bottom:10px;">
            CLINIQ / RECORDS ARCHIVE
        </div>
        <div style="color:white;font-size:28px;font-weight:800;
                    margin-bottom:8px;">
            Visit History
        </div>
        <div style="color:#E1F3F4;font-size:14px;line-height:1.6;">
            Search previous student visits, review recorded statuses
            and priorities, and export administrative records.
        </div>
    </div>
    """)

    try:
        history_visits = backend.get_all_visits() or []

    except Exception as error:
        st.error(f"Unable to load visit history: {error}")
        st.stop()

    if not history_visits:
        st.info("No visit history is available yet.")

    else:

        history_df = pd.DataFrame(history_visits)

        # ---------------------------------------------
        # SEARCH AND FILTERS
        # ---------------------------------------------

        st.html("""
        <div style="
            background:#F0F7FA;
            border:1px solid #DCE9EF;
            border-left:5px solid #0D9488;
            border-radius:12px;
            padding:16px 20px;
            margin:8px 0 18px 0;
        ">
            <div style="color:#10243A;font-size:19px;font-weight:750;">
                Search & Filter Visit Records
            </div>
            <div style="color:#64788A;font-size:13px;margin-top:5px;">
                Find student records using a name, student ID, visit status or nurse-assigned priority.
            </div>
        </div>
        """)

        search_col, status_col, priority_col = st.columns(3)

        with search_col:
            history_search = st.text_input(
                "Search student name or ID",
                key="history_search"
            )

        with status_col:
            history_status = st.selectbox(
                "Visit Status",
                [
                    "All",
                    "Waiting",
                    "In Consultation",
                    "Completed"
                ],
                key="history_status"
            )

        with priority_col:
            history_priority = st.selectbox(
                "Nurse Priority",
                [
                    "All",
                    "See Now",
                    "Today",
                    "Routine",
                    "Not Assigned"
                ],
                key="history_priority"
            )

        filtered_history = []

        for visit in history_visits:

            name = str(visit.get("student_name", ""))
            student_id = str(visit.get("student_id", ""))
            status = str(visit.get("status", ""))
            priority = str(visit.get("priority", "") or "Not Assigned")

            matches_search = (
                history_search.lower() in name.lower()
                or history_search.lower() in student_id.lower()
            )

            matches_status = (
                history_status == "All"
                or status.lower() == history_status.lower()
            )

            matches_priority = (
                history_priority == "All"
                or priority.lower() == history_priority.lower()
            )

            if matches_search and matches_status and matches_priority:
                filtered_history.append(visit)

        st.markdown("---")

        # ---------------------------------------------
        # HISTORY SUMMARY
        # ---------------------------------------------

        total_records = len(filtered_history)

        completed_records = sum(
            1 for visit in filtered_history
            if str(visit.get("status", "")).lower() == "completed"
        )

        waiting_records = sum(
            1 for visit in filtered_history
            if str(visit.get("status", "")).lower() == "waiting"
        )

        review_records = sum(
            1 for visit in filtered_history
            if not visit.get("priority")
        )

        summary_cols = st.columns(4)

        with summary_cols[0]:
            metric_card("Matching Records", total_records)

        with summary_cols[1]:
            metric_card("Completed", completed_records)

        with summary_cols[2]:
            metric_card("Waiting", waiting_records)

        with summary_cols[3]:
            metric_card("Priority Not Assigned", review_records)

        st.markdown("---")

        # ---------------------------------------------
        # HISTORY TABLE
        # ---------------------------------------------

        st.subheader("Visit Records")

        if filtered_history:

            history_display = pd.DataFrame(filtered_history)

            preferred_columns = [
                "id",
                "student_name",
                "student_id",
                "complaint",
                "priority",
                "status",
                "created_at"
            ]

            visible_columns = [
                column for column in preferred_columns
                if column in history_display.columns
            ]

            st.dataframe(
                history_display[visible_columns],
                width="stretch",
                hide_index=True
            )

            # -----------------------------------------
            # INDIVIDUAL VISIT DETAILS
            # -----------------------------------------

            st.subheader("Individual Visit Details")

            for index, visit in enumerate(filtered_history):

                visit_id = visit.get("id", index)
                student_name = visit.get("student_name", "Unknown Student")
                visit_status = visit.get("status", "Unknown")

                with st.expander(
                    f"Visit #{visit_id} — {student_name} — {visit_status}"
                ):

                    detail_col1, detail_col2 = st.columns(2)

                    with detail_col1:
                        st.write("**Student Name:**", student_name)
                        st.write(
                            "**Student ID:**",
                            visit.get("student_id", "Not available")
                        )
                        st.write(
                            "**Registered At:**",
                            visit.get("created_at", "Not available")
                        )

                    with detail_col2:
                        st.write(
                            "**Nurse Priority:**",
                            visit.get("priority") or "Not assigned"
                        )
                        st.write(
                            "**Visit Status:**",
                            visit_status
                        )

                    st.write("**Visit Concern:**")
                    st.write(
                        visit.get("complaint", "No concern recorded.")
                    )

            # -----------------------------------------
            # EXPORT HISTORY
            # -----------------------------------------

            st.markdown("---")

            export_history = pd.DataFrame(filtered_history)

            history_csv = export_history.to_csv(index=False)

            st.download_button(
                "\u2B07 Download Visit History (CSV)",
                data=history_csv,
                file_name="CLINIQ_Visit_History.csv",
                mime="text/csv",
                width="stretch"
            )

        else:

            st.info(
                "No visit records match the selected search and filters."
            )

    st.caption(
        "Visit history is for administrative review. "
        "Clinical decisions remain with the nurse."
    )

# =========================================================
# CLINIQ APPLICATION FOOTER
# =========================================================

st.markdown("---")

footer_left, footer_right = st.columns(2)

with footer_left:
    st.markdown(
        """
        **\u2728 CLINIQ | Smart Clinic Management**

        <small>Student Clinic Visit Management System</small>
        """,
        unsafe_allow_html=True
    )

with footer_right:
    st.markdown(
        """
        <div style="text-align:right;">
            <small>Academic Project Prototype</small><br>
            <small>Version 1.0 | Built with Python & Streamlit</small>
        </div>
        """,
        unsafe_allow_html=True
    )

st.caption(
    "CLINIQ is an administrative prototype. "
    "All clinical decisions must be made by qualified healthcare staff."
)

# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.caption(
    "CLINIQ | Smart Clinic Management System | "
    "Administrative queue management only. "
    "Clinical decisions remain with qualified clinic staff."
)

