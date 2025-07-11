import streamlit as st
import os
import sys
from utils.forms import sign_up_form, login_form
from utils.auth_utils import supabase, init_session, sign_in, sign_up, sign_out
import time

pages = {
    "Nutrition": [
        st.Page("pages/Macro_Diary.py", title="Macro Diary", icon="📝"),
        st.Page("pages/Macros_Goal.py", title= "Weekly Macros Goal", icon="📊"),
        st.Page("pages/Nutritional_Lookup.py", title="Nutrion Finder", icon="🍽️"),
        st.Page("pages/Food _Prediction_Estimation.py", title="AI calorie scanner", icon="📷"),
    ],
    "Fitness": [
        st.Page("pages/Weight_Log.py", title="Weight Log", icon="📉"),
        st.Page("pages/Workout_Tracker.py", title="Workout Tracker", icon="🏋️"),
    ],
    "Well Being":[
        st.Page('pages/Ask_AI.py', title="Chat Bot", icon="🤖")],
}

# 1) initialize session  
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "utils")))
init_session()

# 2) sign up / login 
def auth_screen():
    st.title("Log-In/ Sign-Up")
    option = st.selectbox("Select an option", ["Log In", "Sign Up"])
    st.info("For slightly better experience, use a desktop browser.", icon="ℹ️")
    if option == "Sign Up":
        username, email, password = sign_up_form()
        if username and email and password:
            res = sign_up(email, password, username)
            if getattr(res, "user", None):
                st.success("✅ Sign up successful – Check your email for verification and log in again!")
                time.sleep(5)
                st.rerun()
    else:
        email, password = login_form()
        if email and password:
            res = sign_in(email, password)
            if getattr(res, "user", None):
                response = supabase.auth.get_user()
                st.session_state.user_info = response
                st.rerun()

# 3) check if user is logged in
if not st.session_state.user_info:
    auth_screen()
    st.stop()
    
pg = st.navigation(pages)
pg.run()

st.write(f"🎉 Successfully logged in as {st.session_state.user_info.user.email}!")

st.sidebar.button("Sign Out", on_click=sign_out)
if st.button("logout"):
    sign_out()
    st.rerun()
