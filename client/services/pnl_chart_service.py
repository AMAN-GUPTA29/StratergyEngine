import streamlit as st
import plotly.graph_objs as go
from util import filter_daywise_pnl_by_range

def render_pnl_chart(daywise_pnl):
    """
    Render PNL chart with time range selection and filtering
    
    Args:
        daywise_pnl (dict): Dictionary containing daily PNL data
    """
    if not daywise_pnl:
        return
    
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
    
    # --- Filter Data by Selected Range using util ---
    filtered = filter_daywise_pnl_by_range(daywise_pnl, selected_range)
    
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