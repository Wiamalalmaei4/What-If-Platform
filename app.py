
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="WHAT IF?",
    page_icon="💡",
    layout="wide"
)

st.title("💡 WHAT IF?")
st.caption("Engineering Decision Support & Simulation Platform")

st.markdown(
    "Test your scenarios, analyze their performance, "
    "and discover better operational decisions."
)

st.divider()

# -----------------------------
# DEMO DATA
# -----------------------------

rooms_data = pd.DataFrame({
    "Room": ["R101", "R102", "R103"],
    "Capacity": [30, 50, 40]
})

lectures_data = pd.DataFrame({
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

# -----------------------------
# EDITABLE INPUTS
# -----------------------------

st.header("1. Scenario Setup")

scenario_name = st.text_input(
    "Scenario Name",
    "Scenario 1 - Current Allocation"
)

st.subheader("Available Classrooms")

rooms = st.data_editor(
    rooms_data,
    num_rows="dynamic",
    use_container_width=True,
    key="rooms_table"
)

st.subheader("Lecture Schedule")

lectures = st.data_editor(
    lectures_data,
    num_rows="dynamic",
    use_container_width=True,
    key="lectures_table"
)

# -----------------------------
# SIMULATION ENGINE
# -----------------------------

if st.button("▶ Run Simulation", type="primary"):

    errors = []
    capacity_issues = []
    conflicts = []

    # Check room capacities
    for _, lecture in lectures.iterrows():

        room_match = rooms[
            rooms["Room"] == lecture["Room"]
        ]

        if room_match.empty:
            errors.append(
                f"{lecture['Lecture']}: Room not found."
            )
            continue

        capacity = room_match.iloc[0]["Capacity"]

        if lecture["Students"] > capacity:
            capacity_issues.append(
                f"{lecture['Lecture']} - "
                f"{lecture['Room']}: "
                f"{lecture['Students']} students, "
                f"capacity {capacity}"
            )

    # Check room scheduling conflicts
    for i in range(len(lectures)):

        for j in range(i + 1, len(lectures)):

            a = lectures.iloc[i]
            b = lectures.iloc[j]

            same_room = a["Room"] == b["Room"]
            same_day = a["Day"] == b["Day"]

            overlap = (
                a["Start"] < b["End"]
                and b["Start"] < a["End"]
            )

            if same_room and same_day and overlap:

                conflicts.append(
                    f"{a['Room']} on {a['Day']}: "
                    f"{a['Lecture']} overlaps with "
                    f"{b['Lecture']}"
                )

    # Calculate performance metrics
    total_lectures = len(lectures)

    scheduled_hours = (
        lectures["End"] - lectures["Start"]
    ).sum()

    total_room_hours = len(rooms) * 8 * 5

    utilization = (
        scheduled_hours / total_room_hours * 100
        if total_room_hours > 0 else 0
    )

    total_students = lectures["Students"].sum()

    seats_available = 0

    for _, lecture in lectures.iterrows():

        room_match = rooms[
            rooms["Room"] == lecture["Room"]
        ]

        if not room_match.empty:

            seats_available += (
                room_match.iloc[0]["Capacity"]
            )

    unused_seats = max(
        seats_available - total_students, 0
    )

    feasible = (
        len(errors) == 0
        and len(capacity_issues) == 0
        and len(conflicts) == 0
    )

    # -----------------------------
    # RESULTS
    # -----------------------------

    st.divider()
    st.header("2. Simulation Results")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Room Utilization",
        f"{utilization:.1f}%"
    )

    col2.metric(
        "Capacity Violations",
        len(capacity_issues)
    )

    col3.metric(
        "Schedule Conflicts",
        len(conflicts)
    )

    if feasible:

        st.success(
            "Scenario Status: FEASIBLE ✓"
        )

        st.write(
            f"**{scenario_name}** passed all "
            "basic scheduling checks."
        )

    else:

        st.error(
            "Scenario Status: NOT FEASIBLE"
        )

    # Capacity warnings
    if capacity_issues:

        st.warning("Capacity Issues")

        for issue in capacity_issues:
            st.write("- " + issue)

    # Scheduling conflicts
    if conflicts:

        st.warning("Scheduling Conflicts")

        for conflict in conflicts:
            st.write("- " + conflict)

    # Missing rooms
    if errors:

        st.warning("Data Issues")

        for error in errors:
            st.write("- " + error)

    # Additional metrics
    st.subheader("3. Performance Analysis")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Lectures",
        total_lectures
    )

    col2.metric(
        "Scheduled Hours",
        f"{scheduled_hours:.1f}"
    )

    col3.metric(
        "Unused Seats",
        unused_seats
    )

    # Charts
    if not lectures.empty:

        st.subheader("Students per Lecture")

        chart_data = lectures[
            ["Lecture", "Students"]
        ].set_index("Lecture")

        st.bar_chart(chart_data)

        st.subheader("Room Allocation")

        room_counts = lectures["Room"].value_counts()

        st.bar_chart(room_counts)

    st.caption(
        "Demo results are based on sample data "
        "and simplified operating assumptions."
    )

st.divider()

st.caption(
    "WHAT IF? | Simulate. Compare. Decide."
)
