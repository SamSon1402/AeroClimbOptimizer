import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def create_airport_impact_chart(airports, annual_co2):
    """Create bar chart showing CO2 reduction potential by airport"""
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=airports,
        y=annual_co2,
        marker_color='#9a9a9a',
        text=[f"{co2:.0f} tonnes" for co2 in annual_co2],
        textposition='auto',
    ))
    
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        title="Annual CO₂ Reduction Potential by Airport",
        xaxis_title="",
        yaxis_title="CO₂ (tonnes/year)",
        xaxis=dict(gridcolor='#333333'),
        yaxis=dict(gridcolor='#333333'),
        height=350,
    )
    
    return fig

def render_impact_summary(total_potential):
    """Render impact summary with equivalent metrics"""
    col1, col2 = st.columns(2)
    
    # Calculate equivalents
    trees_equivalent = total_potential * 45  # ~45 trees per tonne of CO2 annually
    cars_equivalent = total_potential / 4.6  # ~4.6 tonnes per car annually
    
    with col1:
        st.markdown(
            f"""
            <div class="impact-container">
                <div class="impact-value">{total_potential:,} tonnes</div>
                <div class="impact-label">Annual CO₂ Reduction</div>
                <div class="impact-equivalent">Equivalent to planting {trees_equivalent:,} trees</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            f"""
            <div class="impact-container">
                <div class="impact-value">{cars_equivalent:,.0f}</div>
                <div class="impact-label">Cars Off the Road</div>
                <div class="impact-equivalent">Annual emissions from {cars_equivalent:,.0f} passenger vehicles</div>
            </div>
            """,
            unsafe_allow_html=True
        )

def create_cumulative_impact_chart(total_potential, years_range=10):
    """Create line chart showing cumulative CO2 savings over time"""
    years = list(range(2025, 2025 + years_range))
    cumulative = [total_potential * i for i in range(1, len(years)+1)]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=years,
        y=cumulative,
        mode='lines+markers',
        line=dict(color='#e0e0e0', width=3),
        fill='tozeroy',
        fillcolor='rgba(224, 224, 224, 0.2)',
    ))
    
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_title="Year",
        yaxis_title="Cumulative CO₂ Reduction (tonnes)",
        xaxis=dict(gridcolor='#333333'),
        yaxis=dict(gridcolor='#333333'),
        height=300,
    )
    
    return fig