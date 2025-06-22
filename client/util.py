import requests
import streamlit as st
import os
from dotenv import load_dotenv
import datetime

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

def filter_daywise_pnl_by_range(daywise_pnl, selected_range):
    """
    Filters the daywise_pnl dict by the selected time range.
    daywise_pnl: dict of {date_str: pnl}
    selected_range: one of 'All', '5Y', '1Y', 'YTD', '6M', '1M', '5D', '1D'
    Returns a sorted list of (date, pnl) tuples.
    """
    time_options = {
        "All": None,
        "5Y": 5*365,
        "1Y": 365,
        "YTD": "ytd",
        "6M": 182,
        "1M": 30,
        "5D": 5,
        "1D": 1
    }
    today = datetime.date.today()
    date_pnl_pairs = [(datetime.datetime.strptime(date, "%Y-%m-%d").date(), pnl) for date, pnl in daywise_pnl.items()]
    date_pnl_pairs.sort()
    if time_options[selected_range] is None:
        filtered = date_pnl_pairs
    elif selected_range == "YTD":
        ytd_start = datetime.date(today.year, 1, 1)
        filtered = [(d, pnl) for d, pnl in date_pnl_pairs if d >= ytd_start and d <= today]
    else:
        days = time_options[selected_range]
        start_date = today - datetime.timedelta(days=days-1)
        filtered = [(d, pnl) for d, pnl in date_pnl_pairs if d >= start_date and d <= today]
    return filtered 

def get_daywise_pnl(person, country, strategy):
    payload = {"person": person, "country": country, "strategy": strategy}
    try:
        response = requests.post(f"{BASE_URL}/stats", json=payload)
        if response.status_code == 200:
            data = response.json()
            return data.get("daywise_pnl", {})
        else:
            st.error(f"Failed to fetch daywise pnl: {response.text}")
            return None
    except Exception as e:
        st.error(f"Error fetching daywise pnl: {e}")
        return None 