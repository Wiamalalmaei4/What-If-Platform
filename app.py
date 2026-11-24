
import streamlit as st
import pandas as pd
import itertools

from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

# -------------------------
# PDF REPORT GENERATOR
# -------------------------

def create_pdf_report(analysis):

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=35,
        leftMargin=35,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph(
        "WHAT IF? - Analysis Report",
        styles["Title"]
    ))

    story.append(Paragraph(
        "Engineering Decision Support Platform",
        styles["Normal"]
    ))

    story.append(Spacer(1, 20))

    solutions = analysis["feasible"]
    best = solutions[0]

    summary_data = [
        ["Analysis Summary", "Result"],
        ["Allocations Tested", str(analysis["tested"])],
        ["Feasible Solutions", str(len(solutions))],
        ["Rejected Solutions", str(analysis["rejected"])],
        ["Best Seat Utilization", f"{best['score']:.2f}%"]
    ]

    summary_table = Table(summary_data, colWidths=[250, 200])

    summary_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#172A40")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 8),
    ]))

    story.append(summary_table)
    story.append(Spacer(1, 25))

    story.append(Paragraph(
        "Recommended Classroom Assignment",
        styles["Heading2"]
    ))

    assignment_data = [
        ["Lecture", "Day", "Start", "End", "Students", "Room"]
    ]

    for _, lecture in best["data"].iterrows():
        assignment_data.append([
            str(lecture["Lecture"]),
            str(lecture["Day"]),
            str(lecture["Start"]),
            str(lecture["End"]),
            str(lecture["Students"]),
            str(lecture["Room"])
        ])

    assignment_table = Table(
        assignment_data,
        repeatRows=1
    )

    assignment_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#172A40")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 6),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
    ]))

    story.append(assignment_table)
    story.append(Spacer(1, 25))

    story.append(Paragraph(
        "Top 5 Alternatives",
        styles["Heading2"]
    ))

    alternatives_data = [
        ["Rank", "Seat Utilization (%)"]
    ]

    for rank, solution in enumerate(solutions[:5], start=1):
        alternatives_data.append([
            str(rank),
            f"{solution['score']:.2f}%"
        ])

    alternatives_table = Table(
        alternatives_data,
        colWidths=[150, 200]
    )

    alternatives_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#172A40")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 8),
    ]))

    story.append(alternatives_table)
    story.append(Spacer(1, 20))

    story.append(Paragraph(
        "The recommended solution satisfies classroom capacity "
        "requirements and avoids overlapping lectures in the same room. "
        "It achieved the highest seat utilization among feasible solutions.",
        styles["Normal"]
    ))

    doc.build(story)

    return buffer.getvalue()
    
# -------------------------
# PAGE CONFIGURATION
# -------------------------

st.set_page_config(
    page_title="WHAT IF?",
    page_icon="💡",
    layout="wide"
)



# -------------------------
# DARK BRAND IDENTITY
# -------------------------

st.markdown("""
<style>

/* Main application */
.stApp {
    background: #101D30;
    color: #F3F6FA;
}

/* Main layout */
.block-container {
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Typography */
html, body, [class*="css"] {
    font-family: Arial, sans-serif;
}

h1, h2, h3, h4 {
    color: #F3F6FA !important;
    font-weight: 700 !important;
}

p, label, .stMarkdown {
    color: #D5DFEA;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #0B1728;
    border-right: 1px solid #263B52;
}

[data-testid="stSidebar"] * {
    color: #EAF2F8;
}

[data-testid="stSidebar"] [role="radiogroup"] label {
    background: #172A40;
    border-radius: 9px;
    padding: 10px;
    margin-bottom: 7px;
}

/* Buttons */
.stButton button,
.stFormSubmitButton button {
    border-radius: 9px;
    min-height: 45px;
    font-weight: 700;
    border: 1px solid #24C6B5;
    transition: 0.2s;
}

.stButton button[kind="primary"],
.stFormSubmitButton button[kind="primary"] {
    background: #24C6B5;
    color: #101D30;
}

.stButton button:hover,
.stFormSubmitButton button:hover {
    border-color: #64E4D5;
    color: #FFFFFF;
}

/* Metric cards */
[data-testid="stMetric"] {
    background: #172A40;
    border: 1px solid #2A4058;
    padding: 18px;
    border-radius: 12px;
}

[data-testid="stMetricLabel"] {
    color: #A8B9CC !important;
}

[data-testid="stMetricValue"] {
    color: #24C6B5 !important;
}

/* Input areas */
[data-testid="stTextInput"],
[data-testid="stNumberInput"],
[data-testid="stSelectbox"],
[data-testid="stDataEditor"] {
    border-radius: 9px;
}

/* Expanders */
[data-testid="stExpander"] {
    background: #172A40;
    border: 1px solid #2A4058;
    border-radius: 10px;
}

/* Alerts */
[data-testid="stAlert"] {
    border-radius: 10px;
}

/* Dividers */
hr {
    border-color: #2A4058;
}

/* Brand footer */
.brand-footer {
    text-align: center;
    color: #8295AA;
    font-size: 12px;
    padding: 25px;
    letter-spacing: 1.5px;
}

</style>
""", unsafe_allow_html=True)


# -------------------------
# SAMPLE DATA
# -------------------------

default_rooms = pd.DataFrame({
    "Room": ["R101", "R102", "R103"],
    "Capacity": [30, 50, 40]
})

default_lectures = pd.DataFrame({
    "Lecture": [
        "Industrial Engineering",
        "Statistics",
        "Operations Research",
        "Work Design",
        "Engineering Economy"
    ],
    "Day": [
        "Sunday", "Sunday", "Monday", "Monday", "Tuesday"
    ],
    "Start": [8.0, 9.0, 8.0, 10.0, 9.0],
    "End": [9.0, 10.0, 10.0, 11.0, 10.0],
    "Students": [25, 45, 35, 28, 38],
    "Room": ["R101", "R102", "R101", "R103", "R103"]
})

if "rooms" not in st.session_state:
    st.session_state.rooms = default_rooms.copy()

if "lectures" not in st.session_state:
    st.session_state.lectures = default_lectures.copy()

if "analysis" not in st.session_state:
    st.session_state.analysis = None

# -------------------------
# BRAND HEADER
# -------------------------

logo_col, tagline_col = st.columns([2, 1])

with logo_col:

    st.markdown("""
    <div style="
        display:flex;
        align-items:center;
        gap:13px;
        padding:8px 0 15px 0;">

        <div style="
            width:52px;
            height:52px;
            background:#1B344B;
            border:1px solid #24C6B5;
            border-radius:13px;
            display:flex;
            align-items:center;
            justify-content:center;
            font-size:28px;">
            💡
        </div>

        <div>
            <div style="
                color:#F3F6FA;
                font-size:34px;
                font-weight:800;
                letter-spacing:-1px;">
                WHAT IF<span style="color:#24C6B5;">?</span>
            </div>

            <div style="
                color:#8295AA;
                font-size:10px;
                letter-spacing:2px;
                font-weight:600;">
                ENGINEERING DECISION PLATFORM
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with tagline_col:

    st.markdown("""
    <div style="
        text-align:right;
        padding-top:20px;
        color:#24C6B5;
        font-size:13px;
        font-weight:700;
        letter-spacing:1px;">
        SIMULATE.<br>
        COMPARE.<br>
        DECIDE.
    </div>
    """, unsafe_allow_html=True)

st.divider()


# -------------------------
# NAVIGATION
# -------------------------

page = st.sidebar.radio(
    "NAVIGATION",
    ["Home", "New Analysis", "Results"]
)

st.sidebar.divider()
st.sidebar.caption("WHAT IF? | Decision Support")

# -------------------------
# HOME
# -------------------------

if page == "Home":

    st.subheader("Make Better Decisions.")

    st.write(
        "WHAT IF? helps you evaluate operational decisions "
        "before implementation by testing alternatives, "
        "checking constraints, and identifying better solutions."
    )

    st.markdown("### How it works")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("#### 01")
        st.write("**Define**")
        st.caption("Enter resources and operational data.")

    with col2:
        st.markdown("#### 02")
        st.write("**Analyze**")
        st.caption("Generate and evaluate possible alternatives.")

    with col3:
        st.markdown("#### 03")
        st.write("**Decide**")
        st.caption("Review the best feasible solution.")

    st.divider()

    st.subheader("Current Pilot")

    st.info(
        "Classroom Allocation: evaluating lecture schedules "
        "and classroom capacities to find suitable allocations."
    )

    st.write("**Ready to evaluate a decision?**")

    if st.button("Start New Analysis", type="primary"):
        st.session_state.analysis = None
        st.rerun()

# -------------------------
# NEW ANALYSIS
# -------------------------

elif page == "New Analysis":

    st.subheader("New Analysis")

    st.write(
        "Enter your classrooms and lecture information. "
        "The platform will evaluate possible allocations automatically."
    )

    with st.form("analysis_form"):

        st.markdown("### 1. Classroom Resources")

        rooms = st.data_editor(
            st.session_state.rooms,
            num_rows="dynamic",
            use_container_width=True,
            key="rooms_input"
        )

        st.markdown("### 2. Lecture Information")

        lectures = st.data_editor(
            st.session_state.lectures,
            num_rows="dynamic",
            use_container_width=True,
            key="lectures_input"
        )

        submitted = st.form_submit_button(
            "Analyze & Find Best Solution",
            type="primary",
            use_container_width=True
        )

    if submitted:

        st.session_state.rooms = rooms.copy()
        st.session_state.lectures = lectures.copy()

        # Validate input

        required_rooms = {"Room", "Capacity"}
        required_lectures = {
            "Lecture", "Day", "Start",
            "End", "Students", "Room"
        }

        if not required_rooms.issubset(rooms.columns):

            st.error("Please check the classroom data columns.")

        elif not required_lectures.issubset(lectures.columns):

            st.error("Please check the lecture data columns.")

        elif rooms.empty or lectures.empty:

            st.error("Please enter at least one room and one lecture.")

        else:

            try:

                rooms["Room"] = rooms["Room"].astype(str).str.strip()
                lectures["Room"] = lectures["Room"].astype(str).str.strip()

                rooms["Capacity"] = pd.to_numeric(
                    rooms["Capacity"], errors="raise"
                )

                for column in ["Start", "End", "Students"]:
                    lectures[column] = pd.to_numeric(
                        lectures[column], errors="raise"
                    )

                if (
                    rooms["Room"].eq("").any()
                    or rooms["Room"].duplicated().any()
                    or rooms["Capacity"].le(0).any()
                    or lectures["Lecture"].isna().any()
                    or lectures["Day"].isna().any()
                    or lectures["Room"].eq("").any()
                    or lectures["Start"].isna().any()
                    or lectures["End"].isna().any()
                    or lectures["Students"].isna().any()
                    or (lectures["Start"] < 0).any()
                    or (lectures["End"] > 24).any()
                    or (lectures["End"] <= lectures["Start"]).any()
                    or (lectures["Students"] < 0).any()
                ):

                    st.error(
                        "Some input values are invalid. "
                        "Check room names, capacities, times and student numbers."
                    )

                else:

                    room_names = rooms["Room"].tolist()
                    combinations = itertools.product(
                        room_names,
                        repeat=len(lectures)
                    )

                    feasible = []
                    tested = 0

                    progress = st.progress(0)

                    total = len(room_names) ** len(lectures)

                    for allocation in combinations:

                        tested += 1

                        candidate = lectures.copy()
                        candidate["Room"] = list(allocation)

                        issues = []

                        for _, lecture in candidate.iterrows():

                            room_capacity = rooms.loc[
                                rooms["Room"] == lecture["Room"],
                                "Capacity"
                            ].iloc[0]

                            if lecture["Students"] > room_capacity:
                                issues.append("Capacity violation")

                        for i in range(len(candidate)):

                            for j in range(i + 1, len(candidate)):

                                a = candidate.iloc[i]
                                b = candidate.iloc[j]

                                if (
                                    a["Room"] == b["Room"]
                                    and a["Day"] == b["Day"]
                                    and a["Start"] < b["End"]
                                    and b["Start"] < a["End"]
                                ):
                                    issues.append("Room conflict")

                        if not issues:

                            student_hours = sum(
                                row["Students"] * (
                                    row["End"] - row["Start"]
                                )
                                for _, row in candidate.iterrows()
                            )

                            capacity_hours = sum(
                                rooms.loc[
                                    rooms["Room"] == row["Room"],
                                    "Capacity"
                                ].iloc[0] * (
                                    row["End"] - row["Start"]
                                )
                                for _, row in candidate.iterrows()
                            )

                            seat_utilization = (
                                student_hours / capacity_hours * 100
                                if capacity_hours > 0 else 0
                            )

                            feasible.append({
                                "score": seat_utilization,
                                "data": candidate.copy()
                            })

                        if tested % max(1, total // 100) == 0:
                            progress.progress(tested / total)

                    progress.progress(1)

                    feasible.sort(
                        key=lambda x: x["score"],
                        reverse=True
                    )

                    st.session_state.analysis = {
                        "tested": tested,
                        "feasible": feasible,
                        "rejected": tested - len(feasible)
                    }

                    st.success(
                        "Analysis completed successfully. "
                        "Open Results to view the recommendation."
                    )

            except Exception as e:

                st.error(
                    f"Unable to analyze the data. Please check your inputs. Details: {e}"
                )

# -------------------------
# RESULTS
# -------------------------

elif page == "Results":

    st.subheader("Analysis Results")

    analysis = st.session_state.analysis

    if analysis is None:

        st.info(
            "No analysis is available yet. "
            "Start a new analysis to generate results."
        )

    elif not analysis["feasible"]:

        st.metric("Allocations Tested", analysis["tested"])
        st.metric("Feasible Solutions", 0)

        st.error(
            "No feasible allocation was found. "
            "Review classroom capacities and lecture schedules."
        )

    else:

        solutions = analysis["feasible"]
        best = solutions[0]

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Allocations Tested",
            analysis["tested"]
        )

        col2.metric(
            "Feasible Solutions",
            len(solutions)
        )

        col3.metric(
            "Rejected Solutions",
            analysis["rejected"]
        )

        st.divider()

        st.markdown("### Recommended Solution")

        st.success("Best feasible allocation identified.")

        st.metric(
            "Seat Utilization",
            f"{best['score']:.2f}%"
        )

        st.markdown("#### Recommended Classroom Assignment")

        st.dataframe(
            best["data"],
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        st.markdown("### Top 5 Alternatives")

        top_rows = []

        for rank, solution in enumerate(solutions[:5], start=1):

            row = {
                "Rank": rank,
                "Seat Utilization (%)": round(
                    solution["score"], 2
                )
            }

            for _, lecture in solution["data"].iterrows():
                row[lecture["Lecture"]] = lecture["Room"]

            top_rows.append(row)

        st.dataframe(
            pd.DataFrame(top_rows),
            use_container_width=True,
            hide_index=True
        )

        st.markdown("### Why was this solution selected?")

        st.write(
            "The recommended solution satisfies all classroom "
            "capacity requirements and avoids overlapping lectures "
            "in the same room. It achieved the highest seat utilization "
            "among the feasible allocations."
        )

        st.caption(
            "The analysis uses the entered data and evaluates "
            "all possible classroom assignments."
        )
        st.download_button(
            label="Download PDF Report",
            data=create_pdf_report(analysis),
            file_name="WHAT_IF_Analysis_Report.pdf",
            mime="application/pdf",
            type="primary",
            use_container_width=True
        )
# -------------------------
# FOOTER
# -------------------------

st.markdown("""
<div class="brand-footer">
    💡 WHAT IF? &nbsp; | &nbsp;
    ENGINEERING DECISION PLATFORM
    <br><br>
    SIMULATE. COMPARE. DECIDE.
</div>
""", unsafe_allow_html=True)
