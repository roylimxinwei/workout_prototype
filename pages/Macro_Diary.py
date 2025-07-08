import streamlit as st
from utils.auth_utils import require_login
from datetime import datetime, timedelta
from utils.forms import macro_diary_form, update_macros_diary_form
from utils.db_utils import select_rows
import pandas as pd

st.title("Macro diary 📔")

st.sidebar.header("Macro Diary")
st.sidebar.write("Track your macros for the day!")

# Session states
if "carousel_date" not in st.session_state:
    st.session_state.carousel_date = datetime.now().date()

@ require_login
def macro_diary_main(verbose=False):
    col1, col2, col3 = st.columns([1, 8, 1])
    with col1:
        if st.button("⬅️", key="prev"):
            st.session_state.carousel_date -= timedelta(days=1)
            st.rerun()
    with col3:
        if st.button("➡️", key="next"):
            st.session_state.carousel_date += timedelta(days=1)
            st.rerun()
    with col2:
        date = st.session_state.carousel_date
        date = st.date_input("Macros for", value=date, key="macro_diary_date")

    resp = select_rows("macro_diary", {'date': date.strftime("%Y-%m-%d")})
    data = resp.data or []

    if data:
        st.info(f"Viewing macros logged for {date}:", icon="📅")
        df = pd.DataFrame(data).drop(columns=["user_id", "created_at", "date"])
        row = df.iloc[0]
        diary_id, protein, carbs, fats, calories = row['id'], row['protein'], row['carbs'], row['fats'], row['calories']

        update_macros_diary_form(diary_id, date, protein, carbs, fats, calories)
        if verbose:
            st.write(data)
            st.write(df)

    else:
        # display the macro diary form if no macros logged for the date
        macro_diary_form(date)
    

macro_diary_main(verbose=False)