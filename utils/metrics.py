def calculate_co2_savings(current_level_pct, optimized_level_pct, 
                          current_co2, monthly_flights):
    """
    Calculate CO2 savings from optimizing level flight percentage
    
    Parameters:
    current_level_pct (float): Current percentage of level flight during climb
    optimized_level_pct (float): Optimized percentage of level flight
    current_co2 (float): Current CO2 emissions per flight in kg
    monthly_flights (int): Number of flights per month
    
    Returns:
    dict: Dictionary with savings metrics
    """
    # Calculate reduction factor
    reduction_factor = 1 - (optimized_level_pct / current_level_pct)
    
    # Calculate emissions
    co2_savings_per_flight = current_co2 * reduction_factor
    optimized_co2 = current_co2 - co2_savings_per_flight
    
    # Calculate total savings
    monthly_savings = co2_savings_per_flight * monthly_flights
    annual_savings = monthly_savings * 12
    
    return {
        "reduction_factor": reduction_factor,
        "co2_savings_per_flight": co2_savings_per_flight,
        "optimized_co2": optimized_co2,
        "monthly_savings": monthly_savings,
        "annual_savings": annual_savings
    }

def calculate_environmental_equivalents(co2_tonnes):
    """
    Calculate environmental equivalents for CO2 reduction
    
    Parameters:
    co2_tonnes (float): CO2 reduction in tonnes
    
    Returns:
    dict: Dictionary with equivalent metrics
    """
    # Equivalency factors
    trees_per_tonne = 45  # Trees absorbing CO2 annually
    kg_co2_per_car_year = 4600  # 4.6 tonnes CO2 per car annually
    liters_fuel_per_tonne = 400  # Approximate fuel liters per tonne CO2
    
    return {
        "trees_equivalent": co2_tonnes * trees_per_tonne,
        "cars_equivalent": co2_tonnes * 1000 / kg_co2_per_car_year,
        "fuel_savings_liters": co2_tonnes * liters_fuel_per_tonne
    }