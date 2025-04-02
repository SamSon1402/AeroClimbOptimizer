import pandas as pd
import numpy as np

def get_sample_airport_data():
    """Return sample airport data for visualization"""
    return pd.DataFrame({
        'Airport': ['London Heathrow', 'Paris CDG', 'Amsterdam Schiphol', 'Frankfurt', 'Madrid Barajas'],
        'Code': ['EGLL', 'LFPG', 'EHAM', 'EDDF', 'LEMD'],
        'Latitude': [51.4700, 49.0097, 52.3105, 50.0379, 40.4983],
        'Longitude': [-0.4543, 2.5479, 4.7683, 8.5622, -3.5676],
        'Annual_CO2_Reduction': [3127, 896, 310, 650, 520],
        'Per_Flight_Reduction': [15.5, 4.3, 1.5, 3.1, 2.8]
    })

def get_yearly_trend_data():
    """Return sample yearly trend data for visualization"""
    years = list(range(2016, 2025))
    level_flight_pct = [0.0426, 0.0425, 0.0448, 0.0454, 0.0355, 0.0391, 0.0448, 0.0457, 0.0475]
    cco_success_rate = [0.747, 0.735, 0.720, 0.722, 0.763, 0.756, 0.735, 0.731, 0.724]
    
    return pd.DataFrame({
        'Year': years,
        'Level Flight %': level_flight_pct,
        'CCO Success Rate': cco_success_rate
    })

def get_feature_importance_data():
    """Return sample feature importance data"""
    features = ['Level Flight %', 'Number of Flights', 'Month', 'Airport UGTB', 'Airport UKKK', 'Airport EGLL']
    importance = [0.35, 0.28, 0.14, 0.09, 0.08, 0.06]
    
    return features, importance

def get_airport_impact_data():
    """Return sample impact data by airport"""
    airports = ["London Heathrow", "Paris CDG", "Frankfurt", "Madrid", "Amsterdam"]
    annual_co2 = [3127, 896, 650, 520, 310]
    
    return airports, annual_co2

def get_airport_details(airport_code):
    """Get detailed information for a specific airport"""
    airport_details = {
        'EGLL': {
            'name': 'London Heathrow',
            'country': 'United Kingdom',
            'annual_flights': 203000,
            'avg_level_flight_pct': 0.048,
            'avg_co2_per_flight': 27.5,
            'potential_savings_pct': 56
        },
        'LFPG': {
            'name': 'Paris Charles de Gaulle',
            'country': 'France',
            'annual_flights': 208000,
            'avg_level_flight_pct': 0.041,
            'avg_co2_per_flight': 9.8,
            'potential_savings_pct': 45
        },
        'EHAM': {
            'name': 'Amsterdam Schiphol',
            'country': 'Netherlands',
            'annual_flights': 207000,
            'avg_level_flight_pct': 0.039,
            'avg_co2_per_flight': 4.9,
            'potential_savings_pct': 32
        },
        'EDDF': {
            'name': 'Frankfurt Airport',
            'country': 'Germany',
            'annual_flights': 209000,
            'avg_level_flight_pct': 0.043,
            'avg_co2_per_flight': 9.1,
            'potential_savings_pct': 33
        },
        'LEMD': {
            'name': 'Madrid Barajas',
            'country': 'Spain',
            'annual_flights': 186000,
            'avg_level_flight_pct': 0.045,
            'avg_co2_per_flight': 10.2,
            'potential_savings_pct': 28
        }
    }
    
    return airport_details.get(airport_code, {})