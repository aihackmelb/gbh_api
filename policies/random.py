"""
This is an example implementation of a policy.

The RandomActionPolicy class randomly decides whether to charge, discharge, or do nothing.
Contestants can use this as a template for developing their own policy classes.
"""


from policies.policy import Policy
import random

class RandomActionPolicy(Policy):
    def __init__(self):
        """
        Initialize the RandomActionPolicy. This policy makes random decisions to charge, discharge, or do nothing.
        """
        super().__init__()

    def act(self, market_observation, info):
        """
        Select an action randomly, either charging, discharging, or doing nothing.

        :param market_observation: A dictionary containing market data.
        :param info: A dictionary containing additional information, including 'max_charge_rate' and 'max_discharge_rate'.
        :return: The action to be taken, represented as a float.
        """
        max_charge_rate = info.get('max_charge_rate')
        max_discharge_rate = info.get('max_discharge_rate')

        # Randomly choose an action: charge, discharge, or no action
        action = random.choice([max_charge_rate, -max_discharge_rate, 0])
        # Scale the action randomly between 0 and the chosen rate
        return action * random.uniform(0, 1)