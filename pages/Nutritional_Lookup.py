import streamlit as st
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
import time

from utils.auth_utils import require_login

load_dotenv()
API_NINJA_KEY = os.getenv("API_NINJA_KEY")

st.title("Nutritional Lookup")

st.sidebar.title("Macros look up")
st.sidebar.write("Enter the food item to look up its nutritional information.")

# initalise session state for food 
if "edamam_input" not in st.session_state:
    st.session_state.edamam_input = ""

def ninja_lookup():
    st.write("API call from NINJA API")
    with st.form("ninja_lookup_form"):
        food_query = st.text_input("Food to search:", key="food_item")
    
        submitted = st.form_submit_button("Search")
        if submitted:
            query = food_query.strip()
            api_url = 'https://api.api-ninjas.com/v1/nutrition?query={}'.format(query)
            response = requests.get(api_url, headers={'X-Api-Key': f'{API_NINJA_KEY}'})
            if response.status_code == requests.codes.ok:
                print(response.text)
                st.write(response.json())
            else:
                print("Error:", response.status_code, response.text)

@ require_login
def nutritional_lookup_main():
    ninja_lookup()

nutritional_lookup_main()