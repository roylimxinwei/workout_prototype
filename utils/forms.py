import streamlit as st
from utils.db_utils import insert_row, update_row, delete_row
import time
from datetime import datetime

### main.py
def sign_up_form():
    with st.form("sign_up_form"):
        st.subheader("Sign Up")
        username = st.text_input("Username", key="sign_up_username")
        email = st.text_input("Email", key="sign_up_email")
        password = st.text_input("Password", type="password", key="sign_up_password")
        submitted = st.form_submit_button("Sign Up")
        if submitted:
            return username, email, password
    return None, None, None

def login_form():
    with st.form("login_form"):
        st.subheader("Log In")
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        submitted = st.form_submit_button("Log In")
        if submitted:
            return email, password
    return None, None

### weight_log.py
def weight_log_form(form_name, latest_week):
    with st.form(form_name):
        # columns for week and calories
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            week = st.number_input("Week:", min_value=1, max_value=52, value=latest_week)
        with col2:
            day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            day_index = datetime.today().weekday()
            day = st.selectbox("Day", day_names, index=day_index)
        with col3:
            date = st.date_input("Date")
        with col4:
            weight = st.number_input("Weight (kg)", step=0.1)
        submitted = st.form_submit_button("Add")
        if submitted:
            date_str = date.strftime("%Y-%m-%d")  # Convert to ISO 8601 format
            insert_row("weight", {"week": week, "day": day, "weight": weight, "date": date_str})
            st.success("Weight added successfully!")
            time.sleep(1)
            st.rerun()

def update_weight_form(weight_id, week, day, weight_val, date):
    with st.form(f"update_{weight_id}weight_form"):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            new_week = st.number_input("Week", min_value=1, max_value=52, value=week, key=f"week_{weight_id}")
        with col2:
            day_index = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"].index(day)
            new_day = st.selectbox("Day", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                                   index=day_index, key=f"day_{weight_id}")
        with col3:
            if isinstance(date, str):
                try:
                    date = datetime.strptime(date, "%Y-%m-%d").date()
                except ValueError:
                    date = date.today() 
            new_date = st.date_input("Date", value=date, key=f"date_{weight_id}")
            new_date_str = new_date.strftime("%Y-%m-%d")
        with col4:
            new_weight = st.number_input("Weight (kg)", value=weight_val, step=0.1, key=f"weight_{weight_id}")
        update = st.form_submit_button("Update")
        if update:
            update_row("weight", weight_id, {"week": new_week, "day": new_day, "weight": new_weight, "date": new_date_str})
            st.success(f"Updating weight for week {new_week}, {new_day}...")
            time.sleep(1)
            st.rerun()
    # DELETE button (outside form to avoid submit conflict)
    if st.button("Delete", key=f"delete_{weight_id}"):
        delete_row("weight", weight_id)
        st.warning(f"Deleting weight for week {week}, {day}...")
        time.sleep(1)
        st.rerun()

### macros_goal.py
def macros_goal_form(form_name):
    with st.form(form_name):
        # columns for week and calories
        col1, col2 = st.columns(2)
        with col1:
            week = st.number_input("Goal for week:", min_value=1, max_value=52)
        with col2:
            calories = st.number_input("Daily calorie goal (kcal):", min_value=0, step=100)
        # columns for protein, carbs, and fat
        col1, col2, col3 = st.columns(3)
        with col1:
            protein = st.number_input("Protein (g):", min_value=0, max_value=1000, step=10)
        with col2:
            carbs = st.number_input("Carbs (g):", min_value=0, max_value=1000, step=10)
        with col3:
            fats = st.number_input("Fat (g):", min_value=0, max_value=1000, step=10)
        submitted = st.form_submit_button("Add Goal")
        if submitted:
            if form_name == 'weekly_goal_form':
                insert_row("macro_goal", {
                    "week": week,
                    "calories": calories,
                    "protein": protein,
                    "carbs": carbs,
                    "fats": fats,
                    "date": datetime.now().strftime("%Y-%m-%d")  # Add current timestamp
                })
            else:
                insert_row("macro_goal", {"week": week, "calories": calories, "protein": protein, "carbs": carbs, "fats": fats})
            st.success("Goal added successfully!")
            time.sleep(1)
            st.rerun()

def update_macros_goal_form(goal_id, week, protein, carbs, fat, calories):
    with st.form(f"edit_goal_{goal_id}"):
        # week and calories
        col1, col2 = st.columns(2)
        with col1:
            new_week = st.number_input("Week", value=week, min_value=1, max_value=52, key=f"week_{goal_id}")
        with col2:
            new_calories = st.number_input("Calories", value=calories, key=f"calories_{goal_id}")
        # protein, carbs, and fat
        col1, col2, col3 = st.columns(3)
        with col1:
            new_protein = st.number_input("Protein", value=protein, key=f"protein_{goal_id}")
        with col2:
            new_carbs = st.number_input("Carbs", value=carbs, key=f"carbs_{goal_id}")
        with col3:
            new_fat = st.number_input("Fat", value=fat, key=f"fat_{goal_id}")
        update = st.form_submit_button("Update")
        if update:
            update_row("macro_goal", goal_id, {
                "week": new_week,
                "calories": new_calories,
                "protein": new_protein,
                "carbs": new_carbs,
                "fats": new_fat
            })
            st.success(f"Updating goal for week {new_week}...")
            time.sleep(1)
            st.rerun()
    # DELETE button
    if st.button("Delete", key=f"delete_{goal_id}"):
        delete_row("macro_goal", goal_id)
        st.warning(f"Deleting goal for week {week}...")
        time.sleep(1)
        st.rerun()

### macro_diary.py
def macro_diary_form(date):
    st.warning(f"Would you like to log your macros for {date}?", icon="📅")
    with st.form("macro_diary_form"):
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                protein = st.number_input("Protein (g)", min_value=0, step=10, key="protein")
            with col2:
                carbs = st.number_input("Carbs (g)", min_value=0, step=10, key="carbs")
            with col3:
                fats = st.number_input("Fats (g)", min_value=0, step=10, key="fats")
            with col4:
                calories = st.number_input("Total Calories (kcal)", min_value=0, step=100, key="calories")
            submitted = st.form_submit_button("Log Macros")
            if submitted:
                insert_row("macro_diary", {
                        "date": date.strftime("%Y-%m-%d"),
                        "calories": calories,
                        "protein": protein,
                        "carbs": carbs,
                        "fats": fats
                    })
                st.success(f"Macros for {date} logged successfully!")
                time.sleep(1)
                st.rerun()

def update_macros_diary_form(diary_id, date, protein, carbs, fats, calories):
    with st.form(f"edit_diary_{diary_id}"):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            new_protein = st.number_input("Protein", value=protein, key=f"protein_{diary_id}")
        with col2:
            new_carbs = st.number_input("Carbs", value=carbs, key=f"carbs_{diary_id}")
        with col3:
            new_fat = st.number_input("Fat", value=fats, key=f"fat_{diary_id}")
        with col4:
            new_calories = st.number_input("Calories", value=calories, key=f"calories_{diary_id}")
        update = st.form_submit_button("Update")
        if update:
            update_row("macro_diary", diary_id, {
                "calories": new_calories,
                "protein": new_protein,
                "carbs": new_carbs,
                "fats": new_fat
            })
            st.success(f"Updating goal for {date}...")
            time.sleep(1)
            st.rerun()
    # DELETE button
    if st.button("Delete", key=f"delete_{diary_id}"):
        delete_row("macro_diary", diary_id)
        st.warning(f"Deleting diary for {date}...")
        time.sleep(1)
        st.rerun()
