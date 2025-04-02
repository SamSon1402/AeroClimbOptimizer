import streamlit as st
import pandas as pd
import numpy as np
import time
import requests
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image

# Set Mapbox token (this is a public token for demo purposes)
px.set_mapbox_access_token("pk.eyJ1Ijoic2hyZXlhc2thbWF0aCIsImEiOiJja2xyNGhxOW0xMzVvMnBudGF4ZzB3ZXJoIn0.jZSY4du3H9G-GZU59mTi3g")

# Set page configuration
st.set_page_config(
    page_title="Flight Efficiency Optimizer",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS directly inline (no file needed)
def load_css():
    css = """
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;700&display=swap');
    
    * { 
        font-family: 'Montserrat', sans-serif; 
        transition: all 0.3s ease-in-out;
    }
    
    /* Reset z-index stacking */
    .streamlit-container {
        width: 100%;
    }
    
    /* Artistic background with animation */
    .background-container {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        overflow: hidden;
        z-index: -10; /* Far behind all content */
    }
    
    .fluid-animation {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, #000000, #0a0a0a);
        z-index: -9;
    }
    
    .fluid-shape {
        position: absolute;
        border-radius: 50%;
        filter: blur(80px);
        opacity: 0.15; /* Reduced opacity */
        animation: float 20s ease-in-out infinite alternate;
    }
    
    .shape1 {
        background: #FFDD00;
        width: 600px;
        height: 600px;
        top: -150px;
        right: -150px;
        animation-delay: 0s;
    }
    
    .shape2 {
        background: #00A3FF;
        width: 500px;
        height: 500px;
        top: 40%;
        left: -150px;
        animation-delay: 2s;
    }
    
    .shape3 {
        background: #FF3B30;
        width: 400px;
        height: 400px;
        bottom: -100px;
        right: 25%;
        animation-delay: 4s;
    }
    
    .shape4 {
        background: #00FF7F;
        width: 300px;
        height: 300px;
        top: 20%;
        right: 15%;
        animation-delay: 6s;
    }
    
    .dark-overlay {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.75); /* Slightly more transparent */
        z-index: -8;
    }
    
    @keyframes float {
        0% {
            transform: translate(0px, 0px) scale(1);
        }
        50% {
            transform: translate(50px, 30px) scale(1.1);
        }
        100% {
            transform: translate(-30px, 20px) scale(0.9);
        }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in {
        animation: fadeIn 1s ease-out forwards;
        opacity: 0;
    }
    
    .title {
        font-size: 2.8rem !important;
        font-weight: 300 !important;
        margin-bottom: 0.5rem !important;
        color: rgba(255, 255, 255, 1.0) !important;
        letter-spacing: 4px !important;
        text-transform: uppercase !important;
    }
    
    .subtitle {
        font-size: 1.2rem !important;
        color: rgba(255, 255, 255, 0.8) !important;
        margin-bottom: 2rem !important;
        font-weight: 300 !important;
        letter-spacing: 1px !important;
    }
    
    .tab-header {
        font-size: 1.8rem !important;
        margin-bottom: 1rem !important;
        color: rgba(255, 255, 255, 1.0) !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.3);
        padding-bottom: 0.5rem;
        font-weight: 300 !important;
        letter-spacing: 3px !important;
        text-transform: uppercase !important;
    }
    
    .tab-description {
        font-size: 1rem !important;
        color: rgba(255, 255, 255, 0.8) !important;
        margin-bottom: 2rem !important;
        font-weight: 300 !important;
    }
    
    .section-header {
        font-size: 1.2rem !important;
        letter-spacing: 2px !important;
        margin-top: 2rem !important;
        margin-bottom: 1rem !important;
        color: rgba(255, 255, 255, 1.0) !important;
        font-weight: 400 !important;
        text-transform: uppercase !important;
    }
    
    /* Card Styles with fixed z-index */
    .glass-card {
        background: rgba(20, 20, 20, 0.7) !important;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        position: relative;
        z-index: 1; /* Ensure it's above background */
    }
    
    .metric-container {
        padding: 1.2rem;
        margin-bottom: 1rem;
    }
    
    .results-container {
        display: flex;
        justify-content: space-between;
        margin-top: 1rem;
        gap: 15px;
    }
    
    .result-card {
        padding: 1.2rem;
        width: 32%;
        text-align: center;
    }
    
    .result-value {
        font-size: 1.6rem;
        font-weight: 300;
        color: rgba(255, 255, 255, 1.0);
        margin-bottom: 0.5rem;
    }
    
    .result-label {
        font-size: 0.8rem;
        color: rgba(255, 255, 255, 0.8);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .feature-details {
        display: flex;
        flex-direction: column;
        gap: 1rem;
        margin-top: 2rem;
    }
    
    .feature-card {
        padding: 1.2rem;
    }
    
    .feature-title {
        font-size: 1.1rem;
        color: rgba(255, 255, 255, 1.0);
        margin-bottom: 0.5rem;
        font-weight: 400;
    }
    
    .feature-description {
        font-size: 0.9rem;
        color: rgba(255, 255, 255, 0.8);
        line-height: 1.5;
    }
    
    .impact-container {
        padding: 1.5rem;
        margin-bottom: 1rem;
        text-align: center;
        min-height: 150px;
    }
    
    .impact-value {
        font-size: 2rem;
        font-weight: 300;
        color: rgba(255, 255, 255, 1.0);
        margin-bottom: 0.5rem;
    }
    
    .impact-label {
        font-size: 1rem;
        color: rgba(255, 255, 255, 0.9);
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 1rem;
    }
    
    .impact-equivalent {
        font-size: 0.9rem;
        color: rgba(255, 255, 255, 0.7);
        font-style: italic;
    }
    
    .input-section {
        padding: 1.2rem;
        margin-bottom: 1rem;
    }
    
    /* Override Streamlit element styling */
    div[data-testid="stMetricLabel"] {
        font-size: 0.8rem !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        color: rgba(255, 255, 255, 0.8) !important;
    }
    
    div[data-testid="stMetricValue"] {
        font-weight: 300 !important;
        font-size: 1.8rem !important;
        color: rgba(255, 255, 255, 1.0) !important;
    }
    
    div[data-testid="stMetricDelta"] {
        color: #4ade80 !important;
    }
    
    /* Plot styling */
    .js-plotly-plot {
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        z-index: 1; /* Ensure plots are above background */
        position: relative;
    }
    
    /* Tab styling */
    button[role="tab"] {
        letter-spacing: 1px !important;
        font-weight: 400 !important;
        background-color: rgba(30, 30, 30, 0.7) !important;
        border-radius: 4px 4px 0 0 !important;
        color: rgba(255, 255, 255, 0.7) !important;
        position: relative;
        z-index: 1;
    }
    
    button[role="tab"][aria-selected="true"] {
        background-color: rgba(40, 40, 40, 0.9) !important;
        color: rgba(255, 255, 255, 1.0) !important;
        border-bottom-color: rgba(255, 255, 255, 0.5) !important;
    }
    
    /* Form inputs */
    input, select, textarea, .stSlider {
        background-color: rgba(30, 30, 30, 0.7) !important;
        border-color: rgba(255, 255, 255, 0.2) !important;
        color: rgba(255, 255, 255, 0.9) !important;
        border-radius: 4px !important;
        position: relative;
        z-index: 1;
    }
    
    /* Logo animation */
    .emoji {
        font-size: 3rem;
        animation: float 6s ease-in-out infinite;
        display: inline-block;
    }
    
    /* Make sure all Streamlit elements are above background */
    div.stTabs, div.stButton, div.stDownloadButton, 
    div.stSelectbox, div.stText, div.stMarkdown,
    div.element-container, div.stDataFrame, div.stNumber,
    div.stPlotlyChart, header {
        position: relative;
        z-index: 1;
    }
    
    /* Override plotly styles for better visibility */
    .main-svg {
        background-color: rgba(20, 20, 20, 0.8) !important;
    }
    
    .geo {
        position: relative;
        z-index: 2 !important; /* Force geo plots to be visible */
    }
    
    .modebar {
        background-color: rgba(20, 20, 20, 0.7) !important;
        z-index: 3 !important; /* Ensure controls are clickable */
    }
    
    .modebar-btn {
        color: rgba(255, 255, 255, 0.8) !important;
    }
    """
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

# Fade-in animation
def fade_in_animation(element, delay=0.1):
    # Apply CSS animation
    animated_element = f"""
    <div class="fade-in" style="animation-delay: {delay}s;">
        {element}
    </div>
    """
    return st.markdown(animated_element, unsafe_allow_html=True)

# Main application
def main():
    # Load CSS
    load_css()

    # Artistic animated background
    st.markdown(
        """
        <div class="background-container">
            <div class="fluid-animation">
                <div class="fluid-shape shape1"></div>
                <div class="fluid-shape shape2"></div>
                <div class="fluid-shape shape3"></div>
                <div class="fluid-shape shape4"></div>
                <div class="dark-overlay"></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Header with fade-in effect
    with st.container():
        col1, col2 = st.columns([1, 3])
        with col1:
            # Animated airplane emoji
            st.markdown("<div class='emoji'>✈️</div>", unsafe_allow_html=True)
        with col2:
            fade_in_animation("<h1 class='title'>FLIGHT EFFICIENCY OPTIMIZER</h1>")
            fade_in_animation("<p class='subtitle'>Reducing emissions through climb optimization</p>")

    # Navigation tabs with artistic animations
    tab1, tab2, tab3, tab4 = st.tabs([
        "DASHBOARD",
        "OPTIMIZATION SIMULATOR",
        "FEATURE IMPORTANCE",
        "SUSTAINABILITY IMPACT"
    ])

    # === DASHBOARD TAB ===
    with tab1:
        st.markdown("<div class='tab-header'>EXECUTIVE DASHBOARD</div>", unsafe_allow_html=True)

        # Model performance metrics
        metrics_col1, metrics_col2 = st.columns(2)
        with metrics_col1:
            st.markdown("<div class='glass-card metric-container'>", unsafe_allow_html=True)
            st.metric("R² Score", "0.57", "Model Accuracy")
            st.markdown("</div>", unsafe_allow_html=True)
        with metrics_col2:
            st.markdown("<div class='glass-card metric-container'>", unsafe_allow_html=True)
            st.metric("Mean Absolute Error", "2.65 kg", "Average Prediction Error")
            st.markdown("</div>", unsafe_allow_html=True)

        # Map visualization
        st.markdown("<div class='section-header'>CO₂ REDUCTION POTENTIAL BY AIRPORT</div>", unsafe_allow_html=True)

        # Sample airport data
        airport_data = pd.DataFrame({
            'Airport': ['London Heathrow', 'Paris CDG', 'Amsterdam Schiphol', 'Frankfurt', 'Madrid Barajas'],
            'Code': ['EGLL', 'LFPG', 'EHAM', 'EDDF', 'LEMD'],
            'Latitude': [51.4700, 49.0097, 52.3105, 50.0379, 40.4983],
            'Longitude': [-0.4543, 2.5479, 4.7683, 8.5622, -3.5676],
            'Annual_CO2_Reduction': [3127, 896, 310, 650, 520],
            'Per_Flight_Reduction': [15.5, 4.3, 1.5, 3.1, 2.8]
        })

        # Create map with better visibility settings
        fig = px.scatter_geo(
            airport_data,
            lat="Latitude",
            lon="Longitude",
            size="Annual_CO2_Reduction",
            color="Per_Flight_Reduction",
            color_continuous_scale=["#cfe2ff", "#6ea8fe", "#0d6efd", "#084298"],
            projection="natural earth",
            size_max=30,
            hover_name="Airport",
            hover_data={"Annual_CO2_Reduction": True, "Per_Flight_Reduction": True}
        )

        fig.update_layout(
            geo=dict(
                showland=True,
                landcolor="#1a1e24",
                countrycolor="#374151",
                coastlinecolor="#4b5563",
                showocean=True,
                oceancolor="#111827",
                showlakes=True,
                lakecolor="#111827",
                showcountries=True,
                projection_type="natural earth",
                bgcolor="rgba(20, 20, 20, 0.8)"
            ),
            paper_bgcolor='rgba(10, 10, 10, 0.9)',
            plot_bgcolor='rgba(10, 10, 10, 0.9)',
            height=500,
            margin=dict(l=0, r=0, t=0, b=0),
            coloraxis_colorbar=dict(
                title="CO₂ Reduction<br>per Flight (kg)",
                titlefont=dict(color="rgba(255, 255, 255, 0.9)"),
                tickfont=dict(color="rgba(255, 255, 255, 0.9)"),
                len=0.8,
                thickness=15,
                bgcolor="rgba(20, 20, 20, 0.8)",
                bordercolor="rgba(255, 255, 255, 0.3)",
                outlinecolor="rgba(255, 255, 255, 0.3)"
            )
        )

        st.plotly_chart(fig, use_container_width=True)

        # Yearly trends
        st.markdown("<div class='section-header'>EFFICIENCY TRENDS (2016-2024)</div>", unsafe_allow_html=True)

        # Sample yearly data
        years = list(range(2016, 2025))
        level_flight_pct = [0.0426, 0.0425, 0.0448, 0.0454, 0.0355, 0.0391, 0.0448, 0.0457, 0.0475]
        cco_success_rate = [0.747, 0.735, 0.720, 0.722, 0.763, 0.756, 0.735, 0.731, 0.724]

        trend_data = pd.DataFrame({
            'Year': years,
            'Level Flight %': level_flight_pct,
            'CCO Success Rate': cco_success_rate
        })

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=trend_data['Year'],
            y=trend_data['Level Flight %'],
            mode='lines+markers',
            name='Level Flight %',
            line=dict(color='#FFDD00', width=3),
            marker=dict(size=8, symbol='circle')
        ))

        fig.add_trace(go.Scatter(
            x=trend_data['Year'],
            y=trend_data['CCO Success Rate'],
            mode='lines+markers',
            name='CCO Success Rate',
            line=dict(color='#00A3FF', width=3),
            marker=dict(size=8, symbol='circle'),
            yaxis='y2'
        ))

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(10, 10, 10, 0.9)',
            plot_bgcolor='rgba(10, 10, 10, 0.9)',
            hovermode="x unified",
            xaxis=dict(
                title="",
                gridcolor='#444444',
                showgrid=True,
                zeroline=False,
                tickfont=dict(color="rgba(255, 255, 255, 0.9)")
            ),
            yaxis=dict(
                title="Level Flight %",
                gridcolor='#444444',
                showgrid=True,
                zeroline=False,
                tickformat='.1%',
                titlefont=dict(color="rgba(255, 255, 255, 0.9)"),
                tickfont=dict(color="rgba(255, 255, 255, 0.9)")
            ),
            yaxis2=dict(
                title="CCO Success Rate",
                overlaying='y',
                side='right',
                gridcolor='#444444',
                showgrid=False,
                zeroline=False,
                tickformat='.0%',
                titlefont=dict(color="rgba(255, 255, 255, 0.9)"),
                tickfont=dict(color="rgba(255, 255, 255, 0.9)")
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.5,
                bgcolor='rgba(20, 20, 20, 0.8)',
                font=dict(color="rgba(255, 255, 255, 0.9)")
            ),
            height=400,
        )

        st.plotly_chart(fig, use_container_width=True)

    # === OPTIMIZATION SIMULATOR ===
    with tab2:
        st.markdown("<div class='tab-header'>OPTIMIZATION SIMULATOR</div>", unsafe_allow_html=True)
        st.markdown("<p class='tab-description'>Simulate CO₂ reduction by optimizing climb profiles</p>", unsafe_allow_html=True)

        # Airport selection and parameters
        col1, col2 = st.columns([1, 2])

        with col1:
            st.markdown("<div class='glass-card input-section'>", unsafe_allow_html=True)
            selected_airport = st.selectbox(
                "Select Airport",
                ["London Heathrow (EGLL)", "Paris CDG (LFPG)", "Amsterdam (EHAM)",
                 "Frankfurt (EDDF)", "Madrid (LEMD)"]
            )

            current_level_pct = 0.048 if "London" in selected_airport else 0.041
            if "Amsterdam" in selected_airport:
                current_level_pct = 0.039
            elif "Frankfurt" in selected_airport:
                current_level_pct = 0.043
            elif "Madrid" in selected_airport:
                current_level_pct = 0.045

            monthly_flights = st.number_input(
                "Monthly Flights",
                min_value=100,
                max_value=20000,
                value=8000 if "London" in selected_airport else 5000,
                step=100
            )

            current_co2 = 27.5 if "London" in selected_airport else 9.8
            if "Amsterdam" in selected_airport:
                current_co2 = 4.9
            elif "Frankfurt" in selected_airport:
                current_co2 = 9.1
            elif "Madrid" in selected_airport:
                current_co2 = 10.2

            optimized_level_pct = st.slider(
                "Optimized Level Flight %",
                min_value=0.01,
                max_value=current_level_pct,
                value=current_level_pct * 0.5,
                format="%.3f"
            )

            # Calculate savings
            reduction_factor = 1 - (optimized_level_pct / current_level_pct)
            co2_savings_per_flight = current_co2 * reduction_factor
            monthly_savings = co2_savings_per_flight * monthly_flights
            annual_savings = monthly_savings * 12
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            # Results visualization
            fig = go.Figure()

            # Current vs Optimized bar chart
            fig.add_trace(go.Bar(
                x=['Current', 'Optimized'],
                y=[current_co2, current_co2 * (1 - reduction_factor)],
                text=[f"{current_co2:.1f} kg", f"{current_co2 * (1 - reduction_factor):.1f} kg"],
                textposition='auto',
                marker_color=['#FF3B30', '#00FF7F'],
                marker_line=dict(width=1, color='rgba(255, 255, 255, 0.5)'),
                name='CO₂ per Flight'
            ))

            fig.update_layout(
                template="plotly_dark",
                paper_bgcolor='rgba(10, 10, 10, 0.9)',
                plot_bgcolor='rgba(10, 10, 10, 0.9)',
                title="CO₂ Emissions per Flight",
                title_font=dict(color="rgba(255, 255, 255, 0.9)"),
                xaxis_title="",
                yaxis_title="CO₂ (kg)",
                yaxis=dict(
                    gridcolor='#444444',
                    tickfont=dict(color="rgba(255, 255, 255, 0.9)")
                ),
                xaxis=dict(
                    tickfont=dict(color="rgba(255, 255, 255, 0.9)")
                ),
                height=300,
                margin=dict(t=50, l=0, r=0, b=0)
            )

            st.plotly_chart(fig, use_container_width=True)

            # Results cards
            st.markdown(
                f"""
                <div class="results-container">
                    <div class="glass-card result-card">
                        <div class="result-value">{co2_savings_per_flight:.1f} kg</div>
                        <div class="result-label">CO₂ Saved per Flight</div>
                    </div>
                    <div class="glass-card result-card">
                        <div class="result-value">{annual_savings/1000:.1f} tonnes</div>
                        <div class="result-label">Annual CO₂ Reduction</div>
                    </div>
                    <div class="glass-card result-card">
                        <div class="result-value">{reduction_factor*100:.1f}%</div>
                        <div class="result-label">Efficiency Improvement</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    # === FEATURE IMPORTANCE ===
    with tab3:
        st.markdown("<div class='tab-header'>FEATURE IMPORTANCE</div>", unsafe_allow_html=True)
        st.markdown("<p class='tab-description'>Key factors affecting climb efficiency</p>", unsafe_allow_html=True)

        # Feature importance data
        features = ['Level Flight %', 'Number of Flights', 'Month', 'Airport UGTB', 'Airport UKKK', 'Airport EGLL']
        importance = [0.35, 0.28, 0.14, 0.09, 0.08, 0.06]

        # Bar chart
        fig = go.Figure()

        fig.add_trace(go.Bar(
            y=features,
            x=importance,
            orientation='h',
            marker_color=['#FFDD00', '#00A3FF', '#00FF7F', '#FF3B30', '#36A2EB', '#FF66D9'],
            marker_line=dict(width=1, color='rgba(255, 255, 255, 0.5)'),
            text=[f"{i:.2f}" for i in importance],
            textposition='auto',
            textfont=dict(size=14, color='rgba(255, 255, 255, 0.95)')
        ))

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(10, 10, 10, 0.9)',
            plot_bgcolor='rgba(10, 10, 10, 0.9)',
            title="Feature Importance for CO₂ Prediction",
            title_font=dict(color="rgba(255, 255, 255, 0.9)"),
            xaxis_title="Importance Score",
            yaxis_title="",
            xaxis=dict(
                gridcolor='#444444',
                tickfont=dict(color="rgba(255, 255, 255, 0.9)")
            ),
            yaxis=dict(
                tickfont=dict(color="rgba(255, 255, 255, 0.9)")
            ),
            height=400,
            margin=dict(l=0, r=20, t=50, b=0)
        )

        st.plotly_chart(fig, use_container_width=True)

        # Feature descriptions
        st.markdown(
            """
            <div class="feature-details">
                <div class="glass-card feature-card">
                    <div class="feature-title">Level Flight % (0.35)</div>
                    <div class="feature-description">
                        Percentage of climb distance flown level. Lower values indicate more efficient continuous climb operations.
                        This is the primary factor SITA's Opticlimb aims to optimize.
                    </div>
                </div>
                <div class="glass-card feature-card">
                    <div class="feature-title">Number of Flights (0.28)</div>
                    <div class="feature-description">
                        Traffic volume impacts efficiency due to congestion and ATC constraints.
                        Busier airports typically have more complex departure procedures.
                    </div>
                </div>
                <div class="glass-card feature-card">
                    <div class="feature-title">Airport-Specific Factors (0.23)</div>
                    <div class="feature-description">
                        Individual airport characteristics like terrain, airspace structure, and procedures
                        significantly impact climb efficiency and optimization potential.
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # === SUSTAINABILITY IMPACT ===
    with tab4:
        st.markdown("<div class='tab-header'>SUSTAINABILITY IMPACT</div>", unsafe_allow_html=True)
        st.markdown("<p class='tab-description'>Environmental benefits of climb optimization</p>", unsafe_allow_html=True)

        # Airport impact data
        airports = ["London Heathrow", "Paris CDG", "Frankfurt", "Madrid", "Amsterdam"]
        annual_co2 = [3127, 896, 650, 520, 310]

        # Annual impact visualization
        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=airports,
            y=annual_co2,
            marker_color=['#FFDD00', '#00A3FF', '#00FF7F', '#FF3B30', '#36A2EB'],
            marker_line=dict(width=1, color='rgba(255, 255, 255, 0.5)'),
            text=[f"{co2:.0f} tonnes" for co2 in annual_co2],
            textposition='auto',
            textfont=dict(size=14, color='rgba(255, 255, 255, 0.95)')
        ))

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(10, 10, 10, 0.9)',
            plot_bgcolor='rgba(10, 10, 10, 0.9)',
            title="Annual CO₂ Reduction Potential by Airport",
            title_font=dict(color="rgba(255, 255, 255, 0.9)"),
            xaxis_title="",
            yaxis_title="CO₂ (tonnes/year)",
            xaxis=dict(
                gridcolor='#444444',
                tickfont=dict(color="rgba(255, 255, 255, 0.9)")
            ),
            yaxis=dict(
                gridcolor='#444444',
                tickfont=dict(color="rgba(255, 255, 255, 0.9)")
            ),
            height=350,
        )

        st.plotly_chart(fig, use_container_width=True)

        # Equivalent metrics
        col1, col2 = st.columns(2)

        with col1:
            # Total potential
            total_potential = sum(annual_co2)
            trees_equivalent = total_potential * 45  # ~45 trees per tonne of CO2 annually

            st.markdown(
                f"""
                <div class="glass-card impact-container">
                    <div class="impact-value">{total_potential:,} tonnes</div>
                    <div class="impact-label">Annual CO₂ Reduction</div>
                    <div class="impact-equivalent">Equivalent to planting {trees_equivalent:,} trees</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:
            # Cars equivalent
            cars_equivalent = total_potential / 4.6  # ~4.6 tonnes per car annually

            st.markdown(
                f"""
                <div class="glass-card impact-container">
                    <div class="impact-value">{cars_equivalent:,.0f}</div>
                    <div class="impact-label">Cars Off the Road</div>
                    <div class="impact-equivalent">Annual emissions from {cars_equivalent:,.0f} passenger vehicles</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        # Cumulative impact
        st.markdown("<div class='section-header'>CUMULATIVE IMPACT (10 YEARS)</div>", unsafe_allow_html=True)

        # Cumulative data
        years = list(range(2025, 2035))
        cumulative = [total_potential * i for i in range(1, len(years)+1)]

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=years,
            y=cumulative,
            mode='lines+markers',
            line=dict(color='#00FF7F', width=3),
            fill='tozeroy',
            fillcolor='rgba(0, 255, 127, 0.2)',
        ))

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(10, 10, 10, 0.9)',
            plot_bgcolor='rgba(10, 10, 10, 0.9)',
            xaxis_title="Year",
            yaxis_title="Cumulative CO₂ Reduction (tonnes)",
            xaxis=dict(
                gridcolor='#444444',
                tickfont=dict(color="rgba(255, 255, 255, 0.9)")
            ),
            yaxis=dict(
                gridcolor='#444444',
                tickfont=dict(color="rgba(255, 255, 255, 0.9)")
            ),
            height=300,
        )

        st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()