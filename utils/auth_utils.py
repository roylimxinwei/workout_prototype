import os
import streamlit as st
from dotenv import load_dotenv
from functools import wraps
from supabase import create_client, Client

#--- 1. Supabase setup ---
load_dotenv()
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

#––– 2. Session bootstrap –––
def init_session():
    if "user_info" not in st.session_state:
        st.session_state.user_info = None

def get_current_user_id() -> str | None:
    if st.session_state.user_info is None:
        return None
    return st.session_state.user_info.user.id 

#––– 3. Auth functions –––
def sign_up(email, password, username):
    try:
        user = supabase.auth.sign_up({"email": email, "password": password, "options": {"data": {"username": username}}})
        return user
    except Exception as e:
        st.error(f"Error signing up: {e}")

def sign_in(email, password):
    try:
        user = supabase.auth.sign_in_with_password({"email": email, "password": password})
        return user
    except Exception as e:
        st.error(f"Error signing in: {e}")

def sign_out():
    try:
        supabase.auth.sign_out()
        st.session_state.user_info = None
        st.rerun()
    except Exception as e:
        st.error(f"Error signing out: {e}")
        
#––– 4. Optional decorator for per-page locking –––
def require_login(fn):
    @wraps(fn)
    def wrapped(*args, **kwargs):
        if not st.session_state.get("user_info"):
            st.error("Login required", icon="🚫")
            st.stop()
        return fn(*args, **kwargs)
    return wrapped