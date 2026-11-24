
import streamlit as st
import pandas as pd
import itertools

# -------------------------
# PAGE CONFIGURATION
# -------------------------

st.set_page_config(
    page_title="WHAT IF?",
    page_icon="💡",
    layout="wide"
)


# -------------------------
# BRAND IDENTITY & DESIGN
# -------------------------

st.markdown("""
<style>

/* Main background */
.stApp {
    background-color: #F5F7FA;
    color: #24364B;
}

/* Main content */
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1200px;
}

/* Typography */
html, body, [class*="css"] {
    font-family: "Arial", sans-serif;
}

h1, h2, h3 {
    color: #142B45 !important;
    font-weight: 700 !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #142B45;
}

[data-testid="stSidebar"] * {
    color: #FFFFFF !important;
}

[data-testid="stSidebar"] [role="radiogroup"] label {
    background-color: rgba(255,255,255,0.06);
    border-radius: 8px;
    padding: 10px;
    margin-bottom: 5px;
}

/* Buttons */
.stButton button,
.stFormSubmitButton button {
    border-radius: 9px;
    min-height: 45px;
    font-weight: 600;
    border: 1px solid #16A6A0;
    transition: 0.2s;
}

.stButton button[kind="primary"],
.stFormSubmitButton button[kind="primary"] {
    background-color: #16A6A0;
    color: white;
}

/* Metrics */
[data-testid="stMetric"] {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    padding: 18px;
    border-radius: 12px;
}

/* Input fields */
[data-testid="stTextInput"],
[data-testid="stNumberInput"],
[data-testid="stSelectbox"] {
    border-radius: 8px;
}

/* Data tables */
[data-testid="stDataFrame"] {
    background-color: #FFFFFF;
    border-radius: 10px;
}

/* Dividers */
hr {
    border-color: #E2E8F0;
}

/* Alerts */
[data-testid="stAlert"] {
    border-radius: 10px;
}

/* Footer */
.brand-footer {
    color: #718096;
    font-size: 12px;
    text-align: center;
    padding: 20px;
    letter-spacing: 1px;
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
# HEADER
# -------------------------

# -------------------------
# HEADER
# -------------------------

logo_col, tagline_col = st.columns([2, 1])

with logo_col:
    st.markdown("""
    <div style="padding: 8px 0;">
        <span style="
            font-size: 36px;
            font-weight: 800;
            color: #142B45;
            letter-spacing: -1px;">
            WHAT IF<span style="color:#16A6A0;">?</span>
        </span>
        <div style="
            color: #718096;
            font-size: 11px;
            letter-spacing: 2px;
            font-weight: 600;">
            ENGINEERING DECISION PLATFORM
        </div>
    </div>
    """, unsafe_allow_html=True)

with tagline_col:
    st.markdown("""
    <div style="
        text-align:right;
        padding-top:15px;
        color:#16A6A0;
        font-weight:600;
        font-size:14px;">
        SIMULATE. COMPARE. DECIDE.
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

# -------------------------
# FOOTER
# -------------------------

# -------------------------
# FOOTER
# -------------------------

st.markdown("""
<div class="brand-footer">
    WHAT IF? &nbsp; | &nbsp; ENGINEERING DECISION PLATFORM
    <br>
    SIMULATE. COMPARE. DECIDE.
</div>
""", unsafe_allow_html=True)

