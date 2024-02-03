import matplotlib.pyplot as plt

def plot_results(actions, profits, socs, market_prices, save_path=None):
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

    if save_path:
        plt.savefig(save_path)
    else:
        plt.show()