import streamlit as st
from typing import Any, Dict
from .auth_utils import supabase, get_current_user_id


# again, assume supabase: Client is initialized/imported here

def insert_row(table: str, payload: Dict[str, Any]) -> Any:
    uid = get_current_user_id()
    if not uid:
        return None
    try:
        payload["user_id"] = uid
        supabase.table(table).insert([payload]).execute()
    except Exception as e:
        st.error(f"Insert failed: {e}")

def update_row(table: str, record_id: int, updates: Dict[str, Any]) -> Any:
    uid = get_current_user_id()
    if not uid:
        return None
    # only update rows owned by this user
    res = (
        supabase
        .table(table)
        .update(updates)
        .eq("id", record_id)
        .execute()
    )
    return res

def delete_row(table: str, record_id: Any) -> Any:
    uid = get_current_user_id()
    if not uid:
        return None
    res = (
        supabase
        .table(table)
        .delete()
        .eq("id", record_id)
        .execute()
    )
    return res

def select_rows(table: str, filters: Dict[str, Any] = None) -> list[Dict]:
    uid = get_current_user_id()
    if not uid:
        return []
    query = supabase.table(table).select("*").eq("user_id", uid)
    if filters:
        for k, v in filters.items():
            query = query.eq(k, v)
    res = query.execute()
    return res

### macro_goal.py
def get_latest_goal(table: str) -> Dict[str, Any]:
    """Based on week column"""
    uid = get_current_user_id()
    if not uid:
        return []
    res = (
        supabase
        .table(table)
        .select("*")
        .eq("user_id", uid)
        .order("week", desc=True)
        .limit(1)
        .execute()
    )
    print(res)
    return res.data[0] if res.data else {}

def get_last_created_goal(table: str) -> Dict[str, Any]:
    """Based on date column"""
    uid = get_current_user_id()
    if not uid:
        return []
    res = (
        supabase
        .table(table)
        .select("*")
        .eq("user_id", uid)
        .order("date", desc=True)
        .limit(1)
        .execute()
    )
    return res.data[0] if res.data else {}