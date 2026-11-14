
import streamlit as st
import pandas as pd
import backend
import io
import html
from datetime import datetime, date


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="CLINIQ | Smart Clinic",
    page_icon="✚",
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
# LOGIN - NO PASSWORD
# =========================================================

if not st.session_state.authenticated:

    st.markdown("<br><br>", unsafe_allow_html=True)

    left, right = st.columns([1.1, 1], gap="large")

    with left:
        st.markdown("# ✚ CLINIQ")
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
        st.subheader("Staff Login")
        st.caption("Enter your details to continue.")

        with st.form("login_form"):
            username = st.text_input("Username")

            selected_role = st.selectbox(
                "Select Role",
                ["Admin", "Nurse", "Staff"]
            )

            submitted = st.form_submit_button(
                "Enter CLINIQ",
                width="stretch"
            )

        if submitted:
            if not username.strip():
                st.error("Please enter your username.")
            else:
                st.session_state.authenticated = True
                st.session_state.username = username.strip()
                st.session_state.role = selected_role
                st.session_state.staff_id = None
                st.rerun()

    st.stop()




# =========================================================
# CUSTOM DESIGN
# =========================================================

st.markdown("""
<style>

/* Main application */
.stApp {
    background-color: #f3f7fb;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #10243a;
}

[data-testid="stSidebar"] * {
    color: white;
}

/* Main headings */
.main-title {
    font-size: 34px;
    font-weight: 800;
    color: #10243a;
}

.section-caption {
    color: #718096;
    font-size: 14px;
}

/* Dashboard welcome banner */
.dashboard-hero {
    background: linear-gradient(120deg, #10243a, #176b78);
    padding: 30px;
    border-radius: 18px;
    color: white;
    margin-bottom: 25px;
}

.dashboard-hero h2 {
    color: white;
    font-size: 30px;
    margin-bottom: 8px;
}

.dashboard-hero p {
    color: #e0f2f1;
    font-size: 15px;
}

/* Dashboard section headings */
.dashboard-section {
    color: #10243a;
    font-size: 21px;
    font-weight: 750;
    margin-top: 20px;
    margin-bottom: 12px;
}

/* Metric cards */
.metric-card {
    background: white;
    padding: 22px;
    min-height: 110px;
    border-radius: 15px;
    border: 1px solid #e5edf4;
    box-shadow: 0 4px 14px rgba(20, 45, 70, 0.06);
}

.metric-label {
    color: #718096;
    font-size: 14px;
}

.metric-value {
    color: #10243a;
    font-size: 30px;
    font-weight: 800;
}

/* Priority cards */
.priority-card {
    background: white;
    padding: 18px;
    border-radius: 14px;
    border: 1px solid #e5edf4;
    text-align: center;
}

.priority-number {
    font-size: 28px;
    font-weight: 800;
    color: #10243a;
}

/* Buttons */
div.stButton > button,
div.stFormSubmitButton > button {
    border-radius: 9px;
    font-weight: 600;
}

/* Page spacing */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
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

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Visit ID:**", get_value(visit, "id"))
        st.write("**Student Name:**", get_value(visit, "student_name"))
        st.write("**Student ID:**", get_value(visit, "student_id"))

    with col2:
        st.write("**Status:**", get_value(visit, "status"))
        st.write("**Nurse Priority:**", get_value(visit, "nurse_priority", "Not assigned"))
        st.write("**Created:**", get_value(visit, "created_at"))

    st.write("**Student Complaint:**")
    st.write(get_value(visit, "complaint"))


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

    st.markdown("# ✚ CLINIQ")
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
            "Visit Details",
            "Appointment Management",
            "Clinic Reports",
            "Visit History"
        ]

    else:

        pages = [
            "Dashboard",
            "Student Queue",
            "Visit Details",
            "Appointment Management",
            "Clinic Reports",
            "Visit History"
        ]

    default_page = st.session_state.pop(
        "dashboard_navigation",
        "Dashboard"
    )

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
    visits = backend.get_all_visits() or []
except Exception as error:
    visits = []
    st.error(f"Unable to load visits: {error}")



# =========================================================
# DASHBOARD
# =========================================================

if page == "Dashboard":

    # -----------------------------------------------------
    # WELCOME HEADER
    # -----------------------------------------------------

    current_time = datetime.now()
    current_hour = current_time.hour

    if current_hour < 12:
        greeting = "Good Morning"
    elif current_hour < 17:
        greeting = "Good Afternoon"
    else:
        greeting = "Good Evening"

    st.markdown(
        f"""
        <div class="dashboard-hero">
            <h2>{greeting}, {html.escape(st.session_state.username)}! 👋</h2>
            <p>
                Welcome to CLINIQ Smart Clinic Management System.
                Here's your clinic activity overview.
            </p>
            <p>
                📅 {current_time.strftime("%A, %d %B %Y")}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # -----------------------------------------------------
    # PROCESS VISIT DATA
    # -----------------------------------------------------

    today = date.today()

    today_visits = []

    for visit in visits:
        created = get_value(visit, "created_at")

        try:
            visit_date = pd.to_datetime(created).date()

            if visit_date == today:
                today_visits.append(visit)

        except Exception:
            pass

    total = len(visits)

    waiting = get_status_count(visits, "Waiting")

    consultation = get_status_count(
        visits,
        "In Consultation"
    )

    completed = get_status_count(
        visits,
        "Completed"
    )

    # -----------------------------------------------------
    # STATISTICS CARDS
    # -----------------------------------------------------

    st.markdown(
        '<div class="dashboard-section">Clinic Statistics</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        metric_card("📋 Total Visits", total)

    with col2:
        metric_card("📅 Today's Visits", len(today_visits))

    with col3:
        metric_card("⏳ Waiting", waiting)

    with col4:
        metric_card("✓ Completed", completed)

    # -----------------------------------------------------
    # ADDITIONAL STATISTICS
    # -----------------------------------------------------

    st.markdown(
        '<div class="dashboard-section">Activity Overview</div>',
        unsafe_allow_html=True
    )

    activity1, activity2, activity3 = st.columns(3)

    with activity1:
        metric_card(
            "🩺 In Consultation",
            consultation
        )

    with activity2:
        metric_card(
            "👩‍⚕️ Nurse Reviews",
            sum(
                1 for visit in visits
                if not get_value(visit, "nurse_priority")
            )
        )

    with activity3:
        completion_rate = (
            round((completed / total) * 100, 1)
            if total > 0 else 0
        )

        metric_card(
            "📊 Completion Rate",
            f"{completion_rate}%"
        )

    # -----------------------------------------------------
    # NURSE PRIORITY OVERVIEW
    # -----------------------------------------------------

    st.markdown("---")

    st.markdown(
        '<div class="dashboard-section">Nurse Priority Overview</div>',
        unsafe_allow_html=True
    )

    st.caption(
        "Priority values are assigned by the nurse, "
        "not automatically by the system."
    )

    p1, p2, p3 = st.columns(3)

    with p1:
        metric_card(
            "🔴 See Now",
            get_priority_count(visits, "See Now")
        )

    with p2:
        metric_card(
            "🟠 Today",
            get_priority_count(visits, "Today")
        )

    with p3:
        metric_card(
            "🟢 Routine",
            get_priority_count(visits, "Routine")
        )

    # -----------------------------------------------------
    # CHARTS
    # -----------------------------------------------------

    st.markdown("---")

    st.markdown(
        '<div class="dashboard-section">Clinic Analytics</div>',
        unsafe_allow_html=True
    )

    chart1, chart2 = st.columns(2)

    with chart1:

        st.subheader("Visit Status")

        status_data = pd.DataFrame({
            "Status": [
                "Waiting",
                "In Consultation",
                "Completed"
            ],
            "Visits": [
                waiting,
                consultation,
                completed
            ]
        })

        st.bar_chart(
            status_data.set_index("Status"),
            height=300,
            width="stretch"
        )

    with chart2:

        st.subheader("Nurse Priority Distribution")

        priority_data = pd.DataFrame({
            "Priority": [
                "See Now",
                "Today",
                "Routine"
            ],
            "Visits": [
                get_priority_count(visits, "See Now"),
                get_priority_count(visits, "Today"),
                get_priority_count(visits, "Routine")
            ]
        })

        st.bar_chart(
            priority_data.set_index("Priority"),
            height=300,
            width="stretch"
        )

    # -----------------------------------------------------
    # RECENT STUDENT VISITS
    # -----------------------------------------------------

    st.markdown("---")

    st.markdown(
        '<div class="dashboard-section">Recent Student Visits</div>',
        unsafe_allow_html=True
    )

    st.caption(
        "The latest registered student visits."
    )

    if visits:

        recent = sorted(
            visits,
            key=lambda x: str(
                get_value(x, "created_at")
            ),
            reverse=True
        )[:10]

        recent_df = pd.DataFrame(recent)

        display_columns = [
            column for column in [
                "id",
                "student_name",
                "student_id",
                "nurse_priority",
                "status",
                "created_at"
            ]
            if column in recent_df.columns
        ]

        if display_columns:

            recent_display = recent_df[
                display_columns
            ].copy()

            if "created_at" in recent_display.columns:
                recent_display["created_at"] = (
                    pd.to_datetime(
                        recent_display["created_at"],
                        errors="coerce"
                    ).dt.strftime("%d %b %Y, %I:%M %p")
                )

                recent_display["created_at"] = (
                    recent_display["created_at"]
                    .fillna("Unknown")
                )

            recent_display = recent_display.rename(
                columns={
                    "id": "Visit ID",
                    "student_name": "Student Name",
                    "student_id": "Student ID",
                    "nurse_priority": "Nurse Priority",
                    "status": "Visit Status",
                    "created_at": "Registered At"
                }
            )

            st.dataframe(
                recent_display,
                width="stretch",
                hide_index=True
            )

        else:
            st.info(
                "Visit records are available, "
                "but the expected display columns were not found."
            )

    else:

        st.info(
            "No student visits have been registered yet. "
            "Register your first visit to see dashboard statistics."
        )

    # -----------------------------------------------------
    # QUICK ACTIONS
    # -----------------------------------------------------

    st.markdown("---")

    st.markdown(
        '<div class="dashboard-section">Quick Actions</div>',
        unsafe_allow_html=True
    )

    action1, action2, action3 = st.columns(3)

    with action1:
        if st.button(
            "➕ Register New Visit",
            width="stretch"
        ):
            st.session_state.dashboard_navigation = "Register Visit"
            st.rerun()

    with action2:
        if st.button(
            "📋 Open Student Queue",
            width="stretch"
        ):
            st.session_state.dashboard_navigation = "Student Queue"
            st.rerun()

    with action3:
        if st.button(
            "📅 Manage Appointments",
            width="stretch"
        ):
            st.session_state.dashboard_navigation = "Appointment Management"
            st.rerun()



# =========================================================
# REGISTER VISIT
# =========================================================

elif page == "Register Visit":

    st.title("✚ Register Student Visit")
    st.caption(
        "Register a student visit and add it to the clinic queue."
    )

    st.markdown("---")

    # -----------------------------------------------------
    # REGISTRATION INFORMATION
    # -----------------------------------------------------

    left, right = st.columns([1.5, 1], gap="large")

    with left:

        st.subheader("Student Information")

        st.write(
            "Enter the student's details carefully."
        )

        with st.form("registration_form", clear_on_submit=True):

            student_name = st.text_input(
                "Student Full Name",
                placeholder="Example: Rohith Parasuram"
            )

            student_id = st.text_input(
                "Student ID",
                placeholder="Enter college ID"
            )

            st.markdown("---")

            st.subheader("Visit Information")

            complaint = st.text_area(
                "Reason for Clinic Visit",
                placeholder=(
                    "Enter the reason provided by the student..."
                ),
                height=150
            )

            st.caption(
                "Describe the student's stated concern. "
                "Do not enter an AI-generated diagnosis."
            )

            submitted = st.form_submit_button(
                "➕ Register Student Visit",
                width="stretch"
            )



            if submitted:

                if not student_name.strip():
                    st.error("Please enter the student's name.")

                elif not student_id.strip():
                    st.error("Please enter the student ID.")

                elif not complaint.strip():
                    st.error("Please enter the reason for the visit.")

                else:
                    try:
                        visit_id = backend.register_visit(
                            student_name.strip(),
                            student_id.strip(),
                            complaint.strip()
                        )

                        st.success(
                            f"Student visit registered successfully! "
                            f"Visit ID: {visit_id}"
                        )

                        st.rerun()

                    except Exception as error:
                        st.error(
                            f"Unable to register student visit: {error}"
                        )



    # -----------------------------------------------------
    # INFORMATION PANEL
    # -----------------------------------------------------

    with right:

        st.subheader("Registration Guide")

        st.info(
            "New student visits are added to the clinic system "
            "for administrative queue management."
        )

        st.markdown("**Registration steps**")

        st.write("1. Enter the student's full name.")
        st.write("2. Enter the college student ID.")
        st.write("3. Record the student's stated concern.")
        st.write("4. Submit the registration form.")

        st.markdown("---")

        st.subheader("Important Information")

        st.warning(
            "Clinical priority is not assigned during registration. "
            "A nurse must review the visit and assign its priority."
        )

        st.markdown("---")

        st.markdown("**Available nurse priorities**")

        st.write("🔴 See Now")
        st.write("🟠 Today")
        st.write("🟢 Routine")

        st.caption(
            "These priorities are assigned by the nurse only."
        )

    # -----------------------------------------------------
    # REGISTRATION RECEIPT
    # -----------------------------------------------------

    receipt_data = st.session_state.get(
        "registration_receipt"
    )

    if receipt_data:

        st.markdown("---")

        st.subheader("✓ Registration Confirmation")

        receipt_col1, receipt_col2 = st.columns(2)

        with receipt_col1:

            st.write(
                "**Student Name:**",
                receipt_data["student_name"]
            )

            st.write(
                "**Student ID:**",
                receipt_data["student_id"]
            )

        with receipt_col2:

            st.write(
                "**Registered At:**",
                receipt_data["registered_at"]
            )

            st.write("**Initial Status:** Waiting for nurse review")

        st.write("**Visit Concern:**")

        st.write(receipt_data["complaint"])

        receipt_text = f"""
CLINIQ - STUDENT VISIT RECEIPT

Student Name: {receipt_data['student_name']}
Student ID: {receipt_data['student_id']}

Visit Concern:
{receipt_data['complaint']}

Registered At:
{receipt_data['registered_at']}

Note:
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

    st.title("Student Visit Queue")
    st.caption(
        "Monitor registered visits and manage the clinic queue."
    )

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
        metric_card("⏳ Waiting", waiting_count)

    with q3:
        metric_card("🩺 In Consultation", consultation_count)

    with q4:
        metric_card("✓ Completed", completed_count)

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
                            "In Consultation",
                            "Completed"
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
                            backend.nurse_review(
                                visit_id,
                                new_priority
                            )

                            backend.update_status(
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

    st.title("Visit Details")
    st.caption("View individual student visit information.")

    if visits:

        visit_options = {
            f"Visit #{get_value(v, 'id')} - "
            f"{get_value(v, 'student_name')}": get_value(v, "id")
            for v in visits
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

    st.title("📅 Appointment Management")
    st.caption(
        "Schedule and manage student appointments at the clinic."
    )

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
        "➕ Book Appointment",
        "📋 Appointment Records"
    ])

    # -----------------------------------------------------
    # BOOK APPOINTMENT
    # -----------------------------------------------------

    with booking_tab:

        st.subheader("Book a New Appointment")

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
                            student_name.strip(),
                            student_id.strip(),
                            appointment_date.isoformat(),
                            appointment_time.strftime("%H:%M"),
                            purpose.strip()
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

        st.subheader("Appointment Records")

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
                        "Scheduled",
                        "Completed",
                        "Cancelled"
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
                    "⬇ Download Appointment Report",
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

    st.title("📊 Clinic Reports & Analytics")
    st.caption(
        "Administrative overview of student visits and clinic activity."
    )

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

        st.subheader("Report Date Range")

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

        st.subheader("Visit Status Analysis")

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

        st.subheader("Nurse Priority Analysis")

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

        st.subheader("Daily Visit Trend")

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

        st.subheader("Detailed Visit Records")

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
            "⬇ Download Clinic Report (CSV)",
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

    st.title("👥 Staff Management")
    st.caption(
        "Manage clinic staff accounts and access roles."
    )

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

    st.subheader("Staff Overview")

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
        "➕ Add Staff",
        "📋 Staff Directory"
    ])

    # -----------------------------------------------------
    # ADD STAFF
    # -----------------------------------------------------

    with add_tab:

        st.subheader("Create Staff Account")

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
                "➕ Create Staff Account",
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

        st.subheader("Registered Staff")

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

elif page == "Visit History":

    st.title("🗂️ Visit History")
    st.caption(
        "Search and review previously registered student visits."
    )

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

        st.subheader("Search Visit Records")

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
                "⬇ Download Visit History (CSV)",
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
        **✚ CLINIQ | Smart Clinic Management**

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
