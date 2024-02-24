"""
This is an example of a more sophisticated policy.

The RollingAveragePolicy class is an example of a policy that uses historical market data 
to make decisions. It calculates a rolling average of market prices and decides whether 
to charge or discharge based on the current market price relative to this average.
This class serves as a more advanced template that contestants can use as a basis for their 
own policy implementations.
"""

from policies.policy import Policy
from collections import deque
import numpy as np

class RollingAveragePolicy(Policy):
    def __init__(self, window_size=50):
        """
        Initialize the RollingAveragePolicy with a parameter for the window size.
        The policy uses a rolling average of market prices to decide whether to charge or discharge.

        :param window_size: The size of the window for calculating the rolling average.
        """
        super().__init__()
        self.window_size = window_size
        self.past_prices = deque(maxlen=self.window_size)

    def act(self, market_observation, info):
        """
        Decide on an action based on the current market price and its rolling average.

        If the current market price is above the rolling average, the action will be to discharge.
        Otherwise, the action will be to charge.

        :param market_observation: A dictionary containing market data.
        :param info: A dictionary containing additional information.
        :return: The action to be taken, represented as a float.
        """
        current_price = market_observation.get('Market_Price')
        self.past_prices.append(current_price)

        rolling_average = np.mean(self.past_prices)

        # Decide action based on the comparison with the rolling average
        if current_price > rolling_average:
            return -info.get('max_discharge_rate')  # Discharge at maximum rate
        else:
            return info.get('max_charge_rate')  # Charge at maximum rate
