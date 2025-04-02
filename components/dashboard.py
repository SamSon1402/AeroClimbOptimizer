import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def render_metrics_section():
    """Render the model performance metrics section"""
    metrics_col1, metrics_col2 = st.columns(2)
    with metrics_col1:
        st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
        st.metric("R² Score", "0.57", "Model Accuracy")
        st.markdown("</div>", unsafe_allow_html=True)
    with metrics_col2:
        st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
        st.metric("Mean Absolute Error", "2.65 kg", "Average Prediction Error")
        st.markdown("</div>", unsafe_allow_html=True)

def create_airport_map(airport_data):
    """Create a map visualization of airports and their CO2 reduction potential"""
    fig = px.scatter_mapbox(
        airport_data, 
        lat="Latitude", 
        lon="Longitude", 
        size="Annual_CO2_Reduction",
        color="Per_Flight_Reduction",
        color_continuous_scale=["#1a1a1a", "#4a4a4a", "#9a9a9a", "#e0e0e0"],
        size_max=25,
        hover_name="Airport",
        hover_data={"Annual_CO2_Reduction": True, "Per_Flight_Reduction": True, 
                   "Latitude": False, "Longitude": False},
        zoom=3, 
        center={"lat": 48.8566, "lon": 2.3522}
    )
    
    fig.update_layout(
        mapbox_style="carto-darkmatter",
        margin={"r":0,"t":0,"l":0,"b":0},
        height=500,
    )
    
    return fig

def create_yearly_trends_chart(trend_data):
    """Create a chart showing yearly trends in efficiency metrics"""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=trend_data['Year'], 
        y=trend_data['Level Flight %'],
        mode='lines+markers',
        name='Level Flight %',
        line=dict(color='#e0e0e0', width=3),
        marker=dict(size=8, symbol='circle')
    ))
    
    fig.add_trace(go.Scatter(
        x=trend_data['Year'], 
        y=trend_data['CCO Success Rate'],
        mode='lines+markers',
        name='CCO Success Rate',
        line=dict(color='#9a9a9a', width=3),
        marker=dict(size=8, symbol='circle'),
        yaxis='y2'
    ))
    
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        hovermode="x unified",
        xaxis=dict(
            title="",
            gridcolor='#333333',
            showgrid=True,
            zeroline=False
        ),
        yaxis=dict(
            title="Level Flight %",
            gridcolor='#333333',
            showgrid=True,
            zeroline=False,
            tickformat='.1%'
        ),
        yaxis2=dict(
            title="CCO Success Rate",
            overlaying='y',
            side='right',
            gridcolor='#333333',
            showgrid=False,
            zeroline=False,
            tickformat='.0%'
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            bgcolor='rgba(0,0,0,0.3)'
        ),
        height=400,
    )
    
    return fig