"""
IMPORTANT: DO NOT MODIFY THIS FILE

This Policy class is a critical component of the evaluation framework.
All contest submissions must extend this class without altering its structure.
Modifications to this class may result in disqualification or incorrect evaluations.
"""

from abc import ABC, abstractmethod

class Policy(ABC):
    def __init__(self, **kwargs):
        """
        Constructor for the Policy class. It can take flexible parameters.
        Contestants are free to maintain internal state and use any auxiliary data or information
        within this class. Policies will be evaluated using market data from late April to early May 2024.
        """
        super().__init__()

    @abstractmethod
    def act(self, market_observation, info):
        """
        Select an action based on the current market observation and additional info.

        Market Observation: A dictionary containing real-time market data. Example keys might include:
            - 'Market_Price' (float, $/kWh): Current price in the energy market.
            - 'Temperature' (float, degrees Celsius): Current temperature.
            - 'Cloud_Cover' (float, percentage): Current cloud cover.
            - 'Energy_Demand' (float, kW): Current energy demand.

        Info: A dictionary containing additional information relevant to the policy. Example keys might include:
            - 'total_profit' (float, $): Cumulative profit so far.
            - 'profit_delta' (float, $): Change in profit from the last action.
            - 'battery_soc' (float, kWh): Current state of charge of the battery.
            - 'remaining_steps' (int): Number of steps remaining in the simulation.
            - 'max_charge_rate' (float, kW): Maximum rate at which the battery can be charged.
            - 'max_discharge_rate' (float, kW): Maximum rate at which the battery can be discharged.

        Your policy should use these inputs to decide on an action to take, which could be charging, 
        discharging, or doing nothing. The action is represented as a float:
            - Positive values indicate charging (kW),
            - Negative values indicate discharging (kW),
            - Zero indicates no action.

        :param market_observation: A dictionary containing market data.
        :param info: A dictionary containing additional information relevant to decision-making.
        :return: The action to be taken.
        """
        pass

# Contestant Instructions:
# - Implement your policy by extending the Policy class.
# - Use the 'act' method to make decisions based on market conditions and battery information.
# - Your policy will be evaluated on market data from late April to early May 2024.
