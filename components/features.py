import streamlit as st
import plotly.graph_objects as go
import pandas as pd

def create_feature_importance_chart(features, importance):
    """Create horizontal bar chart showing feature importance"""
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=features,
        x=importance,
        orientation='h',
        marker_color=['#e0e0e0', '#d4d4d4', '#c8c8c8', '#bcbcbc', '#b0b0b0', '#a4a4a4'],
        text=[f"{i:.2f}" for i in importance],
        textposition='auto',
    ))
    
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        title="Feature Importance for CO₂ Prediction",
        xaxis_title="Importance Score",
        yaxis_title="",
        xaxis=dict(gridcolor='#333333'),
        height=400,
        margin=dict(l=0, r=20, t=50, b=0)
    )
    
    return fig

def render_feature_descriptions():
    """Render detailed descriptions of the most important features"""
    st.markdown(
        """
        <div class="feature-details">
            <div class="feature-card">
                <div class="feature-title">Level Flight % (0.35)</div>
                <div class="feature-description">
                    Percentage of climb distance flown level. Lower values indicate more efficient continuous climb operations.
                    This is the primary factor SITA's Opticlimb aims to optimize.
                </div>
            </div>
            <div class="feature-card">
                <div class="feature-title">Number of Flights (0.28)</div>
                <div class="feature-description">
                    Traffic volume impacts efficiency due to congestion and ATC constraints.
                    Busier airports typically have more complex departure procedures.
                </div>
            </div>
            <div class="feature-card">
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