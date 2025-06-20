import streamlit as st
import time
import os
from dotenv import load_dotenv
from util import get_metadata

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

# Load environment variables from .env
load_dotenv()
API_URL = os.getenv("API_URL", "http://localhost")
PORT = os.getenv("PORT", "8000")
BASE_URL = f"{API_URL}:{PORT}"

# Global cache for metadata
if 'global_metadata' not in st.session_state:
    st.session_state['global_metadata'] = None

def main():
    # Fetch metadata on first load
    if "metadata" not in st.session_state or st.session_state["metadata"] is None:
        with st.spinner("Loading metadata from server..."):
            metadata = get_metadata()
            if metadata:
                st.session_state["metadata"] = metadata
                st.session_state["global_metadata"] = metadata
                st.success("Metadata loaded. Redirecting to Page 1...")
                time.sleep(1)
                st.switch_page("pages/page1.py")
            else:
                st.stop()
    else:
        st.switch_page("pages/page1.py")

if __name__ == "__main__":
    main() 