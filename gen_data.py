# NOT INCLUDED IN FINAL REPO

import pandas as pd
import numpy as np
import datetime

def generate_market_data(start_date, end_date, filename):
    # Generate a date range with 5-minute intervals
    date_range = pd.date_range(start=start_date, end=end_date, freq='5T')

    # Simulate Market Price (e.g., fluctuating between certain values)
    market_price = np.random.uniform(20, 50, len(date_range))

    # Simulate Weather Data
    temperature = np.random.uniform(10, 35, len(date_range))  # Temperature in Celsius
    cloud_cover = np.random.uniform(0, 100, len(date_range))  # Cloud cover percentage

    # Simulate Energy Demand (e.g., higher during daytime and peak hours)
    base_demand = np.random.uniform(500, 1000, len(date_range))
    demand_variation = 300 * np.sin(2 * np.pi * (date_range.hour + date_range.minute / 60) / 24)
    energy_demand = base_demand + demand_variation

    # Create a DataFrame
    data = pd.DataFrame({
        'Timestamp': date_range,
        'Market_Price': market_price,
        'Temperature': temperature,
        'Cloud_Cover': cloud_cover,
        'Energy_Demand': energy_demand
    })

    # Save to CSV
    data.to_csv(filename, index=False)

# Usage
generate_market_data(start_date='2024-01-01', end_date='2024-01-02', filename='train.csv')
