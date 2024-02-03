import pandas as pd
import random
import matplotlib.pyplot as plt

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
        power = min(power, self.charge_rate)
        energy_added = power * (duration / 60) * self.efficiency
        self.state_of_charge = min(self.state_of_charge + energy_added, self.capacity)

    def discharge(self, power, duration):
        """
        Discharge the battery with a specified power over a duration.

        :param power: Power in kW to discharge the battery.
        :param duration: Duration in minutes for which the battery is discharged.
        """
        power = min(power, self.discharge_rate)
        energy_removed = power * (duration / 60) / self.efficiency
        self.state_of_charge = max(self.state_of_charge - energy_removed, 0)

    def get_state_of_charge(self):
        """
        Return the current state of charge of the battery.

        :return: State of charge in kWh.
        """
        return self.state_of_charge

class BatteryEnv:
    def __init__(self, capacity=100, charge_rate=50, discharge_rate=50, initial_charge=50, data='test_data.csv'):
        """
        Environment for simulating battery operation in a market context.
        """
        self.battery = Battery(capacity, charge_rate, discharge_rate, initial_charge)
        self.market_data = pd.read_csv(data)
        self.reset()

    def reset(self):
        self.current_step = 0
        self.total_profit = 0
        self.battery.reset()
        return self.market_data.iloc[self.current_step], self.get_info()

    def step(self, action):
        if self.current_step >= len(self.market_data) - 1:
            return None, None

        market_price = self.market_data.iloc[self.current_step]['Market_Price']
        profit_delta = self.process_action(action, market_price)
        self.current_step += 1

        return self.market_data.iloc[self.current_step], self.get_info(profit_delta)

    def process_action(self, action, market_price):
        duration = 5
        if action > 0:
            self.battery.charge(action, duration)
            return -action * (duration / 60) * market_price
        elif action < 0:
            self.battery.discharge(-action, duration)
            return -action * (duration / 60) * market_price
        return 0

    def get_info(self, profit_delta=0):
        self.total_profit += profit_delta
        remaining_steps = len(self.market_data) - self.current_step - 1
        return {
            'total_profit': self.total_profit,
            'profit_delta': profit_delta,
            'battery_soc': self.battery.get_state_of_charge(),
            'remaining_steps': remaining_steps
        }

def random_action(max_charge_rate, max_discharge_rate):
    return random.choice([max_charge_rate, -max_discharge_rate, 0]) * random.uniform(0, 1)

def plot_results(actions, profits, socs, market_prices):
    """
    Plot the results of the simulation including actions, market prices, battery state of charge, and cumulative profits.

    :param actions: List of actions taken at each step.
    :param profits: List of total profits at each step.
    :param socs: List of battery state of charge at each step.
    :param market_prices: List of market prices at each step.
    """
    # Number of steps in the simulation
    steps = list(range(1, len(actions) + 1))

    # Setting up the plot
    plt.figure(figsize=(7, 7))

    # Plotting Actions
    plt.subplot(4, 1, 1)
    plt.plot(steps, actions, label='Actions', color='blue')
    plt.ylabel('Action (kW)')
    plt.title('Battery Actions Over Time')

    # Plotting Market Prices
    plt.subplot(4, 1, 2)
    plt.plot(steps, market_prices, label='Market Price', color='green')
    plt.ylabel('Market Price ($/kWh)')
    plt.title('Market Price Over Time')

    # Plotting Total Profit
    plt.subplot(4, 1, 3)
    plt.plot(steps, profits, label='Total Profit', color='red')
    plt.axhline(y=0, color='r', linestyle='--')
    plt.ylabel('Total Profit ($)')
    plt.title('Total Profit Over Time')

    # Plotting Battery State of Charge
    plt.subplot(4, 1, 4)
    plt.plot(steps, socs, label='Battery SoC', color='purple')
    plt.xlabel('Time Step')
    plt.ylabel('State of Charge (kWh)')
    plt.title('Battery State of Charge Over Time')

    plt.tight_layout()
    plt.show()


def main():
    env = BatteryEnv()
    step_data, info = env.reset()

    actions, profits, socs, market_prices = [], [], [], []

    while True:
        action = random_action(env.battery.charge_rate, env.battery.discharge_rate)
        step_data, info = env.step(action)

        if step_data is None:
            break

        actions.append(action)
        profits.append(info['total_profit'])
        socs.append(info['battery_soc'])
        market_prices.append(step_data['Market_Price'])

    plot_results(actions, profits, socs, market_prices)




if __name__ == "__main__":
    main()
