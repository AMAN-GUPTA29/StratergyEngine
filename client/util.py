import requests
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()
API_URL = os.getenv("API_URL", "http://localhost")
PORT = os.getenv("PORT", "8000")
BASE_URL = f"{API_URL}:{PORT}"

def get_metadata():
    response = requests.get(f"{BASE_URL}/metadata")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch metadata from server.")
        return None

def get_data(person, country, strategy):
    params = {"person": person, "country": country, "strategy": strategy}
    response = requests.get(f"{BASE_URL}/data", params=params)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch data from server.")
        return None 