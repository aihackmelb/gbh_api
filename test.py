import pandas as pd
import random

class Battery:
    def __init__(self, capacity, charge_rate, discharge_rate, initial_charge=0, efficiency=0.9):
        """
        Initialize the battery instance.
        
        :param capacity: Maximum energy capacity of the battery in kWh.
        :param charge_rate: Maximum charging rate in kW.
        :param discharge_rate: Maximum discharging rate in kW.
        :param initial_charge: Initial state of charge of the battery in kWh.
        :param efficiency: Round-trip efficiency of the battery.
        """
        self.capacity = capacity
        self.charge_rate = charge_rate
        self.discharge_rate = discharge_rate
        self.efficiency = efficiency
        self.state_of_charge = min(initial_charge, capacity)  # Ensure initial SoC is within capacity

    def charge(self, power, duration):
        """
        Charge the battery with a specified power over a duration.
        
        :param power: Power in kW to charge the battery.
        :param duration: Duration in minutes for which the battery is charged.
        """
        power = min(power, self.charge_rate)  # Limit power to max charge rate
        energy_added = power * (duration / 60)  # Convert power and time to kWh
        self.state_of_charge += energy_added * self.efficiency  # Adjust for efficiency
        self.state_of_charge = min(self.state_of_charge, self.capacity)  # Limit to max capacity

    def discharge(self, power, duration):
        """
        Discharge the battery with a specified power over a duration.
        
        :param power: Power in kW to discharge the battery.
        :param duration: Duration in minutes for which the battery is discharged.
        """
        power = min(power, self.discharge_rate)  # Limit power to max discharge rate
        energy_removed = power * (duration / 60)  # Convert power and time to kWh
        self.state_of_charge -= energy_removed / self.efficiency  # Adjust for efficiency
        self.state_of_charge = max(self.state_of_charge, 0)  # Ensure SoC doesn't go below 0

    def get_state_of_charge(self):
        """
        Return the current state of charge of the battery.
        """
        return self.state_of_charge

class TimeSeriesAPI:
    def __init__(self, battery, market_data):
        """
        Initialize the time series API.
        
        :param battery: An instance of the Battery class.
        :param market_data: Time series data of the market, like energy demand, prices.
        """
        self.battery = battery
        self.market_data = market_data
        self.current_step = 0
        self.total_profit = 0  # Initialize total profit

    def get_next_step(self):
        """
        Dispenses the next row of data along with the current battery state of charge.
        
        :return: A dictionary containing market data and battery SoC for the current step.
        """
        if self.current_step < len(self.market_data):
            step_data = {
                'data': self.market_data.iloc[self.current_step],
                'battery_soc': self.battery.get_state_of_charge(),
                'total_profit': self.total_profit
            }
            self.current_step += 1
            return step_data
        else:
            return "End of data series"

    def apply_action(self, action):
        """
        Apply an action to the battery. Positive action values indicate charging,
        negative values indicate discharging, and zero indicates no action.
        
        :param action: Power level for the action in kW (positive for charge, negative for discharge).
        """
        duration = 5  # Duration is 5 minutes
        market_price = self.market_data.iloc[self.current_step - 1]['Market_Price']
        profit_delta = 0

        if action > 0:  # Charging
            self.battery.charge(action, duration)
            cost = action * (duration / 60) * market_price
            self.total_profit -= cost  # Charging costs money
            profit_delta = -cost

        elif action < 0:  # Discharging
            self.battery.discharge(-action, duration)
            revenue = -action * (duration / 60) * market_price
            self.total_profit += revenue  # Discharging earns money
            profit_delta = revenue

        return profit_delta

# Function to read market data
def read_market_data(filename):
    return pd.read_csv(filename)

# Random decision-making function
def random_decision(battery):
    """
    Randomly decide to charge, discharge, or hold. The magnitude of the action is also random.
    """
    action = random.choice([battery.charge_rate, -battery.discharge_rate, 0])  # Choose action type
    magnitude = random.uniform(0, 1)  # Random magnitude from 0 to 1
    return action * magnitude

def run_simulation(api, market_data):
    for index, row in market_data.iterrows():
        step_data = api.get_next_step()  # Fetching the current step data
        if isinstance(step_data, dict):  # Check if it's the end of the series
            action = random_decision(api.battery)
            profit_delta = api.apply_action(action)
            print(f"Step: {api.current_step:>5} | Action: {action:>7.2f} kW | Profit Delta: {profit_delta:>8.2f} | Total Profit: ${api.total_profit:>10.2f} | Battery SoC: {api.battery.get_state_of_charge():>5.2f} kWh")
        else:
            print(step_data)
            break

# Main execution
market_data = read_market_data('market_data.csv')
battery = Battery(capacity=100, charge_rate=50, discharge_rate=50, initial_charge=0)
api = TimeSeriesAPI(battery, market_data)

run_simulation(api, market_data)