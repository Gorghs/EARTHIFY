# eco_calculator.py

"""
Eco Calculator Module

This module provides functions to calculate carbon footprint savings and economic benefits
from proper waste management practices such as recycling and composting.
"""

# Emission factors: kg CO2 equivalent saved per kg of waste through proper management
CARBON_FOOTPRINT_FACTORS = {
    'plastic': 2.5,  # Approximate kg CO2 saved per kg of plastic recycled
    'paper': 1.5,    # Approximate kg CO2 saved per kg of paper recycled
    'glass': 0.5,    # Approximate kg CO2 saved per kg of glass recycled
    'metal': 3.0,    # Approximate kg CO2 saved per kg of metal recycled
    'organic': 0.8   # Approximate kg CO2 saved per kg of organic waste composted
}

# Economic values: USD per kg from recycling/composting
ECONOMIC_VALUES = {
    'plastic': 0.20,  # Approximate revenue per kg of plastic recycled
    'paper': 0.10,    # Approximate revenue per kg of paper recycled
    'glass': 0.05,    # Approximate revenue per kg of glass recycled
    'metal': 1.00,    # Approximate revenue per kg of metal recycled
    'organic': 0.05   # Approximate value per kg of compost produced
}

def calculate_carbon_footprint(waste_type, quantity):
    """
    Calculate the carbon footprint savings from proper waste management.

    Args:
        waste_type (str): Type of waste ('plastic', 'paper', 'glass', 'metal', 'organic')
        quantity (float): Quantity of waste in kg

    Returns:
        float: Carbon footprint savings in kg CO2 equivalent
    """
    factor = CARBON_FOOTPRINT_FACTORS.get(waste_type.lower(), 0)
    return factor * quantity

def calculate_economic_value(waste_type, quantity):
    """
    Calculate the economic value from proper waste management.

    Args:
        waste_type (str): Type of waste ('plastic', 'paper', 'glass', 'metal', 'organic')
        quantity (float): Quantity of waste in kg

    Returns:
        float: Economic value in USD
    """
    value = ECONOMIC_VALUES.get(waste_type.lower(), 0)
    return value * quantity

def environmental_impact(waste_items):
    """
    Calculate the total environmental impact (carbon savings) from a list of waste items.

    Args:
        waste_items (list of dict): List of {'type': str, 'quantity': float} dicts

    Returns:
        float: Total carbon footprint savings in kg CO2 equivalent
    """
    total_savings = 0
    for item in waste_items:
        total_savings += calculate_carbon_footprint(item['type'], item['quantity'])
    return total_savings

def potential_economic_benefits(waste_items):
    """
    Calculate the total potential economic benefits from a list of waste items.

    Args:
        waste_items (list of dict): List of {'type': str, 'quantity': float} dicts

    Returns:
        float: Total economic benefits in USD
    """
    total_benefits = 0
    for item in waste_items:
        total_benefits += calculate_economic_value(item['type'], item['quantity'])
    return total_benefits

# Example usage
if __name__ == "__main__":
    waste_list = [
        {'type': 'plastic', 'quantity': 10},
        {'type': 'paper', 'quantity': 5},
        {'type': 'metal', 'quantity': 2}
    ]

    print(f"Total Carbon Savings: {environmental_impact(waste_list)} kg CO2")
    print(f"Total Economic Benefits: ${potential_economic_benefits(waste_list)}")