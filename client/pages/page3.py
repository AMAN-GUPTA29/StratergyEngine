import streamlit as st

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

def page3():
    st.header("Page 3: Placeholder")
    st.write("This is Page 3.")

if __name__ == "__main__":
    page3() 