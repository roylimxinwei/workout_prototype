import streamlit as st
from utils.db_utils import select_rows
from utils.auth_utils import require_login
from utils.forms import weight_log_form, update_weight_form
import pandas as pd
from collections import defaultdict
import plotly.express as px

# Session states
if 'show_weight_form' not in st.session_state:
    st.session_state.show_weight_form = True
if 'weight_latest_week' not in st.session_state:
    st.session_state.weight_latest_week = 1

st.title("Weight log")

st.sidebar.header("Weight Log")
st.sidebar.write("Log your weight and track your progress!")

def is_weight_logged_today():
    """Check if weight has been logged today"""
    resp = select_rows("weight", {"date": pd.to_datetime("today").date().isoformat()})
    data = resp.data or []
    if data:
        return True
    return False

@ require_login
def weight_log_main(verbose):
    resp = select_rows("weight")
    data = resp.data or []

    # to make the week = latest week on first run
    if data:
        df = pd.DataFrame(data).drop(columns=["user_id", "created_at"])
    if not df.empty and "week" in df.columns:
        st.session_state.weight_latest_week = int(df["week"].max())

    # Check if weight has been logged today
    if not is_weight_logged_today():
        st.warning("Log your weight to keep your streak going!", icon="💪")
        weight_log_form("daily_weight_form", st.session_state.weight_latest_week)
    else:
        st.info("You have logged your weight for today. Keep it up!", icon="🔥")
        
    # is_weight_logged_today()
    
    if data:
        if verbose:
            st.write(df)
        
        st.subheader("Weight trend 📈")
        # Define weekday order as a mapping
        day_order = {
            "Monday": 0,
            "Tuesday": 1,
            "Wednesday": 2,
            "Thursday": 3,
            "Friday": 4,
            "Saturday": 5,
            "Sunday": 6,
        }
        df["day_order"] = df["day"].map(day_order)

        # Create a sortable "timeline" key
        df["timeline"] = df["week"] + df["day_order"] / 10

        # Sort and create readable labels
        df = df.sort_values("timeline", ascending=True).copy()
        df["label"] = "Week " + df["week"].astype(str) + " - " + df["day"]

        # Final index + rename
        df.set_index("label", inplace=True)
        df.rename(columns={"weight": "Weight (kg)"}, inplace=True)

        # Update chart with current data
        fig = px.line(
            df.reset_index(),
            x="label",
            y="Weight (kg)",
            markers=True,
            title="Weight Trend"
        )
        fig.update_layout(xaxis_title="Weekday", yaxis_title="Weight (kg)")
        st.plotly_chart(fig, use_container_width=True)
    
        st.subheader("All Weight Entries 📊")
        if verbose:
            st.write(df)
        # Group weights by week
        weight_by_week = defaultdict(list)
        for index, row in df.iterrows():
            weight_id, week, day, weight_val, date = row['id'], row['week'], row['day'], row['Weight (kg)'], row['date']
            weight_by_week[week].append((weight_id, day, weight_val, date))
            if week > st.session_state.weight_latest_week:
                st.session_state.weight_latest_week = week
        
        for week in sorted(weight_by_week.keys(), reverse=True):
            with st.expander(f"Week {week}", expanded=False):
                for weight_id, day, weight_val, date in weight_by_week[week]:
                    update_weight_form(weight_id, week, day, weight_val, date)
    else:
        st.info("No weight entries found. Please log your first weight.")

    st.write("Would you like to log a weight?")
    if st.button("Log Weight"):
        st.session_state.show_weight_form = not st.session_state.show_weight_form

    if st.session_state.show_weight_form:
        weight_log_form("weight_form", st.session_state.weight_latest_week)
    
weight_log_main(verbose=False)