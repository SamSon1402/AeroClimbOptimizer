import pandas as pd
import numpy as np

class FlightEfficiencyModel:
    def __init__(self):
        """Initialize the flight efficiency prediction model"""
        # This is a simplified model for demonstration purposes
        # In a real application, this would load a trained ML model
        self.feature_importance = {
            'level_flight_pct': 0.35,
            'num_flights': 0.28,
            'month': 0.14,
            'airport_ugtb': 0.09,
            'airport_ukkk': 0.08,
            'airport_egll': 0.06
        }
        
        # Base CO2 emissions by airport (kg)
        self.base_co2 = {
            'EGLL': 20.0,  # London Heathrow
            'LFPG': 8.5,   # Paris CDG
            'EHAM': 4.2,   # Amsterdam
            'EDDF': 8.0,   # Frankfurt
            'LEMD': 9.5,   # Madrid
        }
        
        # Level flight sensitivity factor by airport
        self.level_flight_sensitivity = {
            'EGLL': 156.2,  # London has higher sensitivity
            'LFPG': 92.7,
            'EHAM': 67.9,
            'EDDF': 85.1,
            'LEMD': 78.4,
        }

    def predict_co2(self, airport_code, level_flight_pct, num_flights=1):
        """
        Predict CO2 emissions based on airport and level flight percentage
        
        Parameters:
        airport_code (str): ICAO code of the airport
        level_flight_pct (float): Percentage of climb in level flight (0.01-0.1)
        num_flights (int): Number of flights
        
        Returns:
        float: Predicted CO2 emissions in kg
        """
        if airport_code not in self.base_co2:
            # Default values for unknown airports
            base = 10.0
            sensitivity = 100.0
        else:
            base = self.base_co2[airport_code]
            sensitivity = self.level_flight_sensitivity[airport_code]
        
        # Calculate CO2 based on level flight percentage
        # Higher level flight % = higher emissions
        co2 = base + (level_flight_pct * sensitivity)
        
        # Scale by number of flights
        return co2 * num_flights
    
    def get_feature_importance(self):
        """Return feature importance from the model"""
        return self.feature_importance
    
    def get_r2_score(self):
        """Return R2 score of the model (simulated)"""
        return 0.57
    
    def get_mae(self):
        """Return Mean Absolute Error of the model (simulated)"""
        return 2.65