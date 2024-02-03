import random

def act(
        max_charge_rate, 
        max_discharge_rate,
        last_action,
        last_profit,
        current_sate_of_charge,
        current_market_price,
    ):

    if current_market_price is None:
        return random.choice([max_charge_rate, -max_discharge_rate, 0]) * random.uniform(0, 1)

    if current_market_price > 35:
        return -max_discharge_rate
    elif current_market_price < 28:
        return max_charge_rate
    return 0