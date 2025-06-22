import streamlit as st
from util import get_metadata, get_daywise_pnl
from services.pnl_chart_service import render_pnl_chart
import requests
import os
from dotenv import load_dotenv
import streamlit.components.v1 as components
import sys
import datetime

st.set_page_config(
    page_title="Strategy Evaluation Engine",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={"Get Help": None, "Report a bug": None, "About": None}
)

st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {display: none;}
        [data-testid="collapsedControl"] {display: none;}
    </style>
    """,
    unsafe_allow_html=True
)

load_dotenv()
API_URL = os.getenv("API_URL", "http://localhost")
PORT = os.getenv("PORT", "8000")
BASE_URL = f"{API_URL}:{PORT}"

def page1():
    # Always show reload button at the top
    if st.button("Reload Metadata"):
        new_metadata = get_metadata()
        if new_metadata:
            st.session_state["metadata"] = new_metadata
            st.session_state["global_metadata"] = new_metadata
            st.success("Metadata reloaded!")
            st.rerun()
        else:
            st.error("Failed to reload metadata.")

    # Use global_metadata as fallback if metadata is missing
    metadata = st.session_state.get("metadata")
    if not metadata:
        metadata = st.session_state.get("global_metadata")

    if not metadata:
        st.warning("No metadata loaded. Please reload metadata.")
        st.stop()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="dropdown-label">Person</div>', unsafe_allow_html=True)
        person = st.selectbox(" ", list(metadata.keys()), key="person_select", label_visibility="collapsed")
    with col2:
        st.markdown('<div class="dropdown-label">Country</div>', unsafe_allow_html=True)
        country = st.selectbox("  ", list(metadata[person].keys()), key="country_select", label_visibility="collapsed")
    with col3:
        st.markdown('<div class="dropdown-label">Strategy</div>', unsafe_allow_html=True)
        strategy = st.selectbox("   ", metadata[person][country], key="strategy_select", label_visibility="collapsed")

    st.session_state["selected_path"] = {
        "person": person,
        "country": country,
        "strategy": strategy
    }
    st.success(f"Selected: {person} / {country} / {strategy}")

    # Button to send path to backend and plot PNL
    if st.button("Send Path to Backend and Plot PNL"):
        daywise_pnl = get_daywise_pnl(person, country, strategy)
        if daywise_pnl is not None:
            st.session_state['daywise_pnl'] = daywise_pnl

    # Always show toggles and chart if daywise_pnl is present
    daywise_pnl = st.session_state.get('daywise_pnl', {})
    if daywise_pnl:
        # Use the PNL chart service component
        render_pnl_chart(daywise_pnl)

if __name__ == "__main__":
    page1() 