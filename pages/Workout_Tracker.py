import streamlit as st
from utils.auth_utils import require_login
from datetime import datetime
import pandas as pd
from utils.forms import create_workout_routine_form
from utils.db_utils import select_rows
import time


def is_workout_logged_today():
    """Check if weight has been logged today"""
    resp = select_rows("workouts", {"routine_date": pd.to_datetime("today").date().isoformat()})
    data = resp.data or []
    if data:
        return True
    return False

@require_login
def workout_tracker(verbose=False):
    st.title("Workout Tracker")

    st.sidebar.header("Timer")
    seconds = st.sidebar.number_input("Rest duration (seconds)", min_value=1, value=60, step=10)

    if st.sidebar.button("Start Rest"):
        placeholder = st.sidebar.empty()
        for remaining in range(seconds, -1, -1):
            placeholder.metric("Time Remaining", f"{remaining} s")
            time.sleep(1)
        st.toast(f"🔔{seconds}s Rest complete!")

    resp = select_rows("workouts")
    data = resp.data or []

    # Initialize session state for exercises and exercise dataframes
    if "exercise_dfs" not in st.session_state:
        st.session_state.exercise_dfs = []

    if "routine_form_key" not in st.session_state:
        st.session_state.routine_form_key = 0

    # check if there is a workout logged today
    if not is_workout_logged_today():
        st.warning("Ready to start a workout?")
        create_workout_routine_form(st.session_state.exercise_dfs, expanded=True)
    else:
        st.info("You have logged your workout for today. Keep it up!", icon="🔥")
        create_workout_routine_form(st.session_state.exercise_dfs, expanded=False)

    st.subheader("Completed Workouts 💪")
    
    if data:
        for workout in sorted(data, key=lambda x: x.get("routine_date", ""), reverse=True):
            with st.expander(f"{workout.get('routine_name', 'Workout')} - {workout.get('routine_date', '')}"):
                exercises = workout.get("exercises", [])
                for idx, exercise in enumerate(exercises):
                    st.markdown(f"**{exercise.get('name')}**")
                    # If exercise is a list of sets/reps/weight
                    data = exercise.get("sets", [])
                    if isinstance(data, list) and data:
                        df = pd.DataFrame(data)
                        st.dataframe(df, use_container_width=True)
                    else:
                        st.write(exercise)
    else:
        st.info("Start logging your workouts to see them here!")
        
workout_tracker(verbose=True)
