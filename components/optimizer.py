import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.metrics import calculate_co2_savings

def render_airport_selector():
    """Render airport selection and parameter inputs"""
    selected_airport = st.selectbox(
        "Select Airport", 
        ["London Heathrow (EGLL)", "Paris CDG (LFPG)", "Amsterdam (EHAM)", 
         "Frankfurt (EDDF)", "Madrid (LEMD)"]
    )
    
    # Set default values based on selected airport
    airport_code = selected_airport.split("(")[1].replace(")", "")
    
    # Get current level flight percentage (different for each airport)
    current_level_pct = 0.048 if "London" in selected_airport else 0.041
    if "Amsterdam" in selected_airport:
        current_level_pct = 0.039
    elif "Frankfurt" in selected_airport:
        current_level_pct = 0.043
    elif "Madrid" in selected_airport:
        current_level_pct = 0.045
    
    # Get monthly flights
    monthly_flights = st.number_input(
        "Monthly Flights", 
        min_value=100, 
        max_value=20000, 
        value=8000 if "London" in selected_airport else 5000,
        step=100
    )
    
    # Get current CO2 per flight
    current_co2 = 27.5 if "London" in selected_airport else 9.8
    if "Amsterdam" in selected_airport:
        current_co2 = 4.9
    elif "Frankfurt" in selected_airport:
        current_co2 = 9.1
    elif "Madrid" in selected_airport:
        current_co2 = 10.2
    
    # Optimized level flight percentage slider
    optimized_level_pct = st.slider(
        "Optimized Level Flight %", 
        min_value=0.01, 
        max_value=current_level_pct,
        value=current_level_pct * 0.5,
        format="%.3f"
    )
    
    return {
        "airport": selected_airport,
        "airport_code": airport_code,
        "current_level_pct": current_level_pct,
        "optimized_level_pct": optimized_level_pct,
        "monthly_flights": monthly_flights,
        "current_co2": current_co2
    }

def create_comparison_chart(current_co2, optimized_co2):
    """Create a bar chart comparing current vs optimized CO2 emissions"""
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=['Current', 'Optimized'],
        y=[current_co2, optimized_co2],
        text=[f"{current_co2:.1f} kg", f"{optimized_co2:.1f} kg"],
        textposition='auto',
        marker_color=['#9a9a9a', '#e0e0e0'],
        name='CO₂ per Flight'
    ))
    
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        title="CO₂ Emissions per Flight",
        xaxis_title="",
        yaxis_title="CO₂ (kg)",
        yaxis=dict(gridcolor='#333333'),
        height=300,
        margin=dict(t=50, l=0, r=0, b=0)
    )
    
    return fig

def render_results_cards(co2_savings_per_flight, annual_savings, reduction_factor):
    """Render cards showing optimization results"""
    st.markdown(
        f"""
        <div class="results-container">
            <div class="result-card">
                <div class="result-value">{co2_savings_per_flight:.1f} kg</div>
                <div class="result-label">CO₂ Saved per Flight</div>
            </div>
            <div class="result-card">
                <div class="result-value">{annual_savings/1000:.1f} tonnes</div>
                <div class="result-label">Annual CO₂ Reduction</div>
            </div>
            <div class="result-card">
                <div class="result-value">{reduction_factor*100:.1f}%</div>
                <div class="result-label">Efficiency Improvement</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )