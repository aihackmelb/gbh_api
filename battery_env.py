"""
IMPORTANT: DO NOT MODIFY THIS FILE

This file contains core functionality for the battery simulation environment and its interaction with policies.
It is a critical component of the evaluation framework for the National Energy Market Hackathon.
Altering this file can disrupt the proper functioning of the simulation and evaluation process.
Please adhere to the provided structure and use the defined classes as they are.
"""

import pandas as pd
from plotting import plot_results

class Battery:
    def __init__(self, capacity, charge_rate, discharge_rate, initial_charge, efficiency=0.9):
        """
        A simple model of a battery with charging and discharging capabilities.

        :param capacity: Maximum energy capacity of the battery in kWh.
        :param charge_rate: Maximum charging rate in kW.
        :param discharge_rate: Maximum discharging rate in kW.
        :param initial_charge: Initial state of charge of the battery in kWh.
        :param efficiency: Charging and discharging efficiency of the battery.
        """
        self.capacity = capacity
        self.initial_charge = initial_charge
        self.charge_rate = charge_rate
        self.discharge_rate = discharge_rate
        self.efficiency = efficiency
        self.state_of_charge = min(self.initial_charge, self.capacity)

    def reset(self):
        """
        Reset the battery to its initial state of charge.
        """
        self.state_of_charge = min(self.initial_charge, self.capacity)

    def charge(self, power, duration):
        """
        Charge the battery with a specified power over a duration.

        :param power: Power in kW to charge the battery.
        :param duration: Duration in minutes for which the battery is charged.
        """
        assert power <= self.charge_rate, "Charging power cannot exceed the maximum charging rate."
        power = min(power, self.charge_rate)
        energy_add_order = power * (duration / 60) * self.efficiency
        energy_added = min(energy_add_order, self.capacity - self.state_of_charge)
        self.state_of_charge = min(self.state_of_charge + energy_add_order, self.capacity)
        return energy_added

    def discharge(self, power, duration):
        """
        Discharge the battery with a specified power over a duration.

        :param power: Power in kW to discharge the battery.
        :param duration: Duration in minutes for which the battery is discharged.
        """
        assert power <= self.discharge_rate, "Discharging power cannot exceed the maximum discharging rate."
        power = min(power, self.discharge_rate)
        energy_remove_order = power * (duration / 60) / self.efficiency
        energy_removed = min(energy_remove_order, self.state_of_charge)
        self.state_of_charge = max(self.state_of_charge - energy_remove_order, 0)
        return energy_removed

    def get_state_of_charge(self):
        """
        Return the current state of charge of the battery.

        :return: State of charge in kWh.
        """
        return self.state_of_charge

class BatteryEnv:
    def __init__(self, capacity=100, charge_rate=50, discharge_rate=50, initial_charge=50, data='train.csv'):
        """
        Environment for simulating battery operation in a market context.

        :param capacity: Maximum capacity of the battery in kWh.
        :param charge_rate: Maximum charging rate of the battery in kW.
        :param discharge_rate: Maximum discharging rate of the battery in kW.
        :param initial_charge: Initial state of charge of the battery in kWh.
        :param data: Path to the CSV file containing market data.
        """
        self.battery = Battery(capacity, charge_rate, discharge_rate, initial_charge)
        self.market_data = pd.read_csv(data)
        self.total_profit = 0
        self.current_step = 0
        self.episode_length = len(self.market_data)  # Default to full length

    def reset(self, start_step=0, episode_length=None, initial_soc=None):
        """
        Reset the environment with specified starting step, episode length, and initial state of charge.

        :param start_step: Starting step for the episode.
        :param episode_length: Length of the episode in steps.
        :param initial_soc: Initial state of charge of the battery.
        """
        self.current_step = start_step
        self.total_profit = 0
        self.episode_length = episode_length if episode_length else len(self.market_data) - start_step
        initial_soc = initial_soc if initial_soc is not None else self.battery.initial_charge
        self.battery.state_of_charge = min(initial_soc, self.battery.capacity)
        return self.market_data.iloc[self.current_step], self.get_info()

    def step(self, action):
        if self.current_step >= len(self.market_data) - 1:
            return None, None
        market_price = self.market_data.iloc[self.current_step]['Market_Price']
        profit_delta = self.process_action(action, market_price)
        self.current_step += 1
        market_data = self.market_data.iloc[self.current_step]
        return market_data, self.get_info(profit_delta)

    def process_action(self, action, market_price):
        duration = 5
        if action > 0:
            energy_added = self.battery.charge(action, duration)
            return -energy_added * (duration / 60) * market_price
        elif action < 0:
            energy_removed = self.battery.discharge(-action, duration)
            return energy_removed * (duration / 60) * market_price
        return 0

    def get_info(self, profit_delta=0):
        self.total_profit += profit_delta
        remaining_steps = len(self.market_data) - self.current_step - 1
        return {
            'total_profit': self.total_profit,
            'profit_delta': profit_delta,
            'battery_soc': self.battery.get_state_of_charge(),
            'max_charge_rate': self.battery.charge_rate,
            'max_discharge_rate': self.battery.discharge_rate,
            'remaining_steps': remaining_steps
        }


def main():
    # Example usage of the BatteryEnv class with a random strategy
    from policies import policy_classes

    policy = policy_classes.get('RandomActionPolicy')()
    env = BatteryEnv()

    state, info = env.reset()
    actions, profits, socs, market_prices = [], [], [], []

    while True:
        action = policy.act(state, info)
        state, info = env.step(action)

        if state is None:
            break

        actions.append(action)
        profits.append(info['total_profit'])
        socs.append(info['battery_soc'])
        market_prices.append(state['Market_Price'])

    plot_results(actions, profits, socs, market_prices)


if __name__ == "__main__":
    main()
