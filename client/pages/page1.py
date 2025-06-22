import streamlit as st
from util import get_metadata
import requests
import os
from dotenv import load_dotenv
import plotly.graph_objs as go
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
        payload = {
            "person": person,
            "country": country,
            "strategy": strategy
        }
        try:
            response = requests.post(f"{BASE_URL}/stats", json=payload)
            if response.status_code == 200:
                st.success("Path sent to backend!")
                data = response.json()
                daywise_pnl = data.get("daywise_pnl", {})
                st.session_state['daywise_pnl'] = daywise_pnl
            else:
                st.error(f"Failed to send path: {response.text}")
        except Exception as e:
            st.error(f"Error sending path: {e}")

    # Always show toggles and chart if daywise_pnl is present
    daywise_pnl = st.session_state.get('daywise_pnl', {})
    if daywise_pnl:
        # --- Toggle Buttons for Time Ranges ---
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
        selected_range = st.radio("Select Time Range", list(time_options.keys()), horizontal=True)
        # --- Filter Data by Selected Range ---
        today = datetime.date.today()
        # Convert string dates to datetime.date
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
        # Prepare for plotting
        if filtered:
            plot_dates = [d.strftime("%Y-%m-%d") for d, _ in filtered]
            plot_pnls = [pnl for _, pnl in filtered]
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=plot_dates, y=plot_pnls, mode='lines+markers', name='Daily PNL'))
            fig.update_layout(title=f"Daily PNL Over Time ({selected_range})", xaxis_title="Date", yaxis_title="PNL")
            # Responsive width using columns
            if st.session_state.get('is_large_screen') is None:
                st.session_state['is_large_screen'] = False
            cols = st.columns([1,2,1]) if st.session_state['is_large_screen'] else st.columns([1,1])
            with cols[1 if st.session_state['is_large_screen'] else 0]:
                fig.update_layout(width=600 if st.session_state['is_large_screen'] else 400)
                st.plotly_chart(fig)
        else:
            st.info("No PNL data available for the selected time range.")

if __name__ == "__main__":
    page1() 