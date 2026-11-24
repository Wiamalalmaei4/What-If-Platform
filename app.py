
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="WHAT IF?",
    page_icon="💡",
    layout="wide"
)

st.title("💡 WHAT IF?")
st.caption("Engineering Decision Support Platform")

st.markdown(
    "### Scenario Lab\n"
    "Create alternatives, simulate their performance, "
    "and compare operational decisions."
)

# -------------------------
# SAMPLE DATA
# -------------------------

rooms_data = pd.DataFrame({
    "Room": ["R101", "R102", "R103"],
    "Capacity": [30, 50, 40]
})

base_lectures = pd.DataFrame({
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

scenario_b = base_lectures.copy()
scenario_b["Room"] = ["R101", "R102", "R102", "R103", "R102"]

scenario_c = base_lectures.copy()
scenario_c["Room"] = ["R101", "R102", "R103", "R101", "R102"]

# -------------------------
# SESSION STATE
# -------------------------

if "scenario_data" not in st.session_state:

    st.session_state.scenario_data = {
        "Scenario A - Current": base_lectures.copy(),
        "Scenario B - Alternative": scenario_b.copy(),
        "Scenario C - Proposed": scenario_c.copy()
    }

if "rooms_data" not in st.session_state:
    st.session_state.rooms_data = rooms_data.copy()

# -------------------------
# INPUT DATA
# -------------------------

st.header("1. Resource Setup")

rooms = st.data_editor(
    st.session_state.rooms_data,
    num_rows="dynamic",
    key="rooms_editor",
    use_container_width=True
)

st.session_state.rooms_data = rooms.copy()

st.divider()

st.header("2. Build Your Scenarios")

st.write(
    "Edit the classroom assignments, lecture times, "
    "or student numbers to test different alternatives."
)

scenario_names = list(st.session_state.scenario_data.keys())

edited_scenarios = {}

for name in scenario_names:

    with st.expander(name, expanded=(name == scenario_names[0])):

        edited = st.data_editor(
            st.session_state.scenario_data[name],
            num_rows="dynamic",
            key=f"editor_{name}",
            use_container_width=True
        )

        edited_scenarios[name] = edited.copy()

st.session_state.scenario_data = edited_scenarios

# -------------------------
# SIMULATION ENGINE
# -------------------------

def evaluate_scenario(lectures, rooms):

    conflicts = []
    capacity_issues = []
    data_errors = []

    total_hours = 0
    total_student_hours = 0
    total_capacity_hours = 0

    for _, lecture in lectures.iterrows():

        room_match = rooms[
            rooms["Room"] == lecture["Room"]
        ]

        if room_match.empty:
            data_errors.append(
                f"{lecture['Lecture']}: "
                f"Room {lecture['Room']} not found."
            )
            continue

        capacity = room_match.iloc[0]["Capacity"]

        duration = lecture["End"] - lecture["Start"]

        if duration <= 0:
            data_errors.append(
                f"{lecture['Lecture']}: "
                "Invalid lecture duration."
            )
            continue

        if lecture["Students"] < 0:
            data_errors.append(
                f"{lecture['Lecture']}: "
                "Invalid student count."
            )
            continue

        total_hours += duration

        total_student_hours += (
            lecture["Students"] * duration
        )

        total_capacity_hours += (
            capacity * duration
        )

        if lecture["Students"] > capacity:

            capacity_issues.append(
                f"{lecture['Lecture']} — "
                f"{lecture['Room']}: "
                f"{lecture['Students']} students, "
                f"capacity {capacity}"
            )

    # Detect room conflicts
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
                    f"{a['Room']} — {a['Day']}: "
                    f"{a['Lecture']} / {b['Lecture']}"
                )

    # KPIs
    available_room_hours = len(rooms) * 8 * 5

    room_utilization = (
        total_hours / available_room_hours * 100
        if available_room_hours > 0 else 0
    )

    seat_utilization = (
        total_student_hours / total_capacity_hours * 100
        if total_capacity_hours > 0 else 0
    )

    feasible = (
        len(capacity_issues) == 0
        and len(conflicts) == 0
        and len(data_errors) == 0
    )

    return {
        "feasible": feasible,
        "room_utilization": room_utilization,
        "seat_utilization": seat_utilization,
        "conflicts": conflicts,
        "capacity_issues": capacity_issues,
        "data_errors": data_errors,
        "total_hours": total_hours
    }

# -------------------------
# DECISION WEIGHTS
# -------------------------

st.divider()
st.header("3. Decision Criteria")

st.write(
    "Adjust the importance of each criterion. "
    "Only feasible scenarios can receive a recommendation."
)

weight_room = st.slider(
    "Room Utilization Importance",
    min_value=0,
    max_value=100,
    value=50
)

weight_seat = st.slider(
    "Seat Utilization Importance",
    min_value=0,
    max_value=100,
    value=50
)

weight_total = weight_room + weight_seat

if weight_total == 0:
    st.warning("At least one criterion must have a weight.")

# -------------------------
# RUN ALL SCENARIOS
# -------------------------

if st.button("▶ Run & Compare Scenarios", type="primary"):

    results = {}

    for name, data in st.session_state.scenario_data.items():

        results[name] = evaluate_scenario(
            data, st.session_state.rooms_data
        )

    # Calculate weighted scores for feasible scenarios
    for name, result in results.items():

        if result["feasible"] and weight_total > 0:

            score = (
                result["room_utilization"]
                * weight_room
                + result["seat_utilization"]
                * weight_seat
            ) / weight_total

            result["score"] = score

        else:
            result["score"] = None

    # -------------------------
    # RESULTS
    # -------------------------

    st.divider()
    st.header("4. Simulation Results")

    result_rows = []

    for name, result in results.items():

        result_rows.append({
            "Scenario": name,
            "Feasible": (
                "Yes" if result["feasible"] else "No"
            ),
            "Room Utilization (%)": round(
                result["room_utilization"], 2
            ),
            "Seat Utilization (%)": round(
                result["seat_utilization"], 2
            ),
            "Conflicts": len(result["conflicts"]),
            "Capacity Issues": len(
                result["capacity_issues"]
            ),
            "Score": (
                round(result["score"], 2)
                if result["score"] is not None
                else "N/A"
            )
        })

    results_df = pd.DataFrame(result_rows)

    st.dataframe(
        results_df,
        use_container_width=True,
        hide_index=True
    )

    # Detailed issues
    for name, result in results.items():

        if not result["feasible"]:

            with st.expander(f"⚠ Issues in {name}"):

                for issue in result["capacity_issues"]:
                    st.write("Capacity:", issue)

                for issue in result["conflicts"]:
                    st.write("Conflict:", issue)

                for issue in result["data_errors"]:
                    st.write("Data:", issue)

    # -------------------------
    # COMPARISON CHARTS
    # -------------------------

    st.subheader("Scenario Comparison")

    chart_df = results_df.set_index("Scenario")

    st.bar_chart(
        chart_df[
            ["Room Utilization (%)", "Seat Utilization (%)"]
        ]
    )

    # -------------------------
    # RECOMMENDATION
    # -------------------------

    valid_results = {
        name: result
        for name, result in results.items()
        if result["feasible"]
        and result["score"] is not None
    }

    st.header("5. Final Decision")

    if valid_results:

        best_name = max(
            valid_results,
            key=lambda name: valid_results[name]["score"]
        )

        best = valid_results[best_name]

        st.success(
            f"Recommended Scenario: {best_name}"
        )

        st.metric(
            "Decision Score",
            f"{best['score']:.2f}%"
        )

        st.write(
            "This scenario passed the feasibility checks "
            "and achieved the highest weighted score "
            "among the evaluated alternatives."
        )

    else:

        st.error(
            "No feasible scenario is available. "
            "Correct the constraints or input data "
            "before making a recommendation."
        )

    st.caption(
        "Results are based on demo data and the "
        "selected decision weights."
    )

st.divider()

st.caption(
    "WHAT IF? | Simulate. Compare. Decide."
)
