import streamlit as st
from utils.auth_utils import require_login
from utils.forms import macros_goal_form, update_macros_goal_form
from utils.db_utils import select_rows, get_latest_goal, get_last_created_goal
import pandas as pd
import plotly.express as px
from datetime import datetime

# Session states
if "show_macros_goal_form" not in st.session_state:
    st.session_state.show_macros_goal_form = True
if "latest_week" not in st.session_state:
    st.session_state.latest_week = 1

st.title("Weekly Macros 🎯")

st.sidebar.header("Macros Goal")
st.sidebar.write("Set your macros for the week and crush it!")

def is_goals_logged_this_week(verbose):
    todays_date = datetime.now().date()
    latest_goal = get_last_created_goal("macro_goal")

    # Extract the date from the goal (make sure it's not None)
    goal_date_str = latest_goal.get("date")
    if goal_date_str is None:
        return False  # No goal date to compare

    goal_date = datetime.fromisoformat(goal_date_str).date()
    days_difference = (todays_date - goal_date).days

    if verbose:
        print(f"Today's date: {todays_date}")
        print(f"Latest goal date: {goal_date}")
        print(f"Days since last goal: {days_difference}")

    return days_difference < 7

@ require_login
def macros_goal_main(verbose):
    resp = select_rows("macro_goal")
    data = resp.data or []
    
    if is_goals_logged_this_week(verbose):
        st.info("You have set your macros for this week. Keep it up!", icon="🔥")
    else:
        st.warning("Log your macros goal for this week to keep your streak going!", icon="💪")
        macros_goal_form("weekly_goal_form")

    latest_goal = get_latest_goal("macro_goal")
    if latest_goal:
        df = pd.DataFrame(data).drop(columns=["user_id", "created_at"])
        week, protein, carbs, fats, calories = latest_goal['week'], latest_goal['protein'], latest_goal['carbs'], latest_goal['fats'], latest_goal['calories']
        if week > st.session_state.latest_week:
            st.session_state.latest_week = week
        st.subheader(f"Goal for Week {week}")
        piechart = st.checkbox(f"Show goal", value=True)
        if piechart:
            fig = px.pie(
                names=["Protein", "Carbs", "Fat"],
                values=[protein, carbs, fats],
                color=["Protein", "Carbs", "Fat"],  # Match color key
                color_discrete_map={
                    "Carbs": "turquoise",
                    "Protein": "orange",
                    "Fat": "indigo"
                },
            )
            st.plotly_chart(fig)
    
    if data:
        st.subheader("Macros trend 📈")
        df = pd.DataFrame(data).drop(columns=["user_id", "created_at"])
        df = df.sort_values("week").set_index("week")
        # manipulate the (g) of each macro to their calroie equivalent
        df["protein"] = df["protein"] * 4
        df["carbs"] = df["carbs"] * 4
        df["fats"] = df["fats"] * 9
        df.rename(columns={"protein": "Protein (kcal)", "carbs": "Carbs (kcal)", "fats": "Fat (kcal)", "calories": "Calories (kcal)"}, inplace=True)

        macros = st.multiselect(
            "Choose macros to view", 
            ["Protein (kcal)", "Carbs (kcal)", "Fat (kcal)", "Calories (kcal)"],  
            ["Calories (kcal)"]  
        )
        if not macros:
            st.error("Please select at least one macro.")
        else:
            tab1, tab2 = st.tabs(["Line Chart", "Sheet"])
            tab1.subheader("Line Chart")
            with tab1:
                fig = px.line(
                df.reset_index(),  # "label" becomes a column again
                x="week",
                y=macros,
                markers=True,
                title="Macros Trend"
                )
                fig.update_layout(xaxis_title="Week", yaxis_title="Macros (kcal)")
                st.plotly_chart(fig, use_container_width=True)
            tab2.subheader("Sheet")
            with tab2:
                st.dataframe(df[macros])

        st.subheader("Alls Goals 🗓️")
        df = pd.DataFrame(data).drop(columns=["user_id", "created_at"])
        if verbose:
            st.write(df)
        for index, row in df.iterrows():
            goal_id, week, protein, carbs, fat, calories = row['id'], row['week'], row['protein'], row['carbs'], row['fats'], row['calories']
            with st.expander(f"Week {week} | Protein: {protein}g | Carbs: {carbs}g | Fat: {fat}g | Calories: {calories}"):
                update_macros_goal_form(goal_id, week, protein, carbs, fat, calories)
    else:
        st.info("No goals set yet.")
    
    st.write("Would you like to create a goal?")
    if st.button("Create Goal"):
        st.session_state.show_macros_goal_form = not st.session_state.show_macros_goal_form

    if st.session_state.show_macros_goal_form:
        macros_goal_form("macros_goal_form")

macros_goal_main(verbose=False)