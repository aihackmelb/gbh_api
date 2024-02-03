import datetime
import sys
import random

from batteryenv import BatteryEnv
from plotting import plot_results
from algo import act

data = sys.argv[1]
version = sys.argv[2]

date_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

env = BatteryEnv(data=data)
step_data, info = env.reset()

actions, profits, historical_state_of_charge, market_prices = [], [], [], []

last_action = None
last_profit = None
current_state_of_charge = None
current_market_price = None

while True:
    action = act(
        max_charge_rate=env.battery.charge_rate, 
        max_discharge_rate=env.battery.discharge_rate, 
        last_action=last_action,
        last_profit=last_profit,
        current_sate_of_charge=current_state_of_charge,
        current_market_price=current_market_price,
    )

    step_data, info = env.step(action)

    if step_data is None:
        break
    
    last_action = action
    last_profit = info['total_profit']
    current_state_of_charge = info['battery_soc']
    current_market_price = step_data['Market_Price']

    actions.append(action)
    profits.append(last_profit)
    historical_state_of_charge.append(current_state_of_charge)
    market_prices.append(current_market_price)


plot_results(actions, profits, historical_state_of_charge, market_prices, save_path=f'{version}-{date_time}.png')