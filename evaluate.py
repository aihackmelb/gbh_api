import argparse
import yaml
import os
import random
import pandas as pd
from policies import policy_classes
from battery_env import BatteryEnv
from datetime import datetime
import numpy as np
import tqdm
import json

def load_config(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)['policy']

def set_seed(seed):
    random.seed(seed)
    np.random.seed(seed)

def run_trial(env, policy, start_step, episode_length):
    state, info = env.reset(start_step=start_step, episode_length=episode_length)
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

    return actions, profits, socs, market_prices

def parse_parameters(params_list):
    params = {}
    for item in params_list:
        key, value = item.split('=')
        params[key] = eval(value)
    return params

def main():
    parser = argparse.ArgumentParser(description='Evaluate a single energy market strategy.')
    parser.add_argument('--trials', type=int, default=100, help='Number of trials to run')
    parser.add_argument('--seed', type=int, default=42, help='Seed for randomness')
    parser.add_argument('--data', type=str, default='train.csv', help='Path to the market data csv file')
    parser.add_argument('--class_name', type=str, help='Policy class name. If not provided, the config.yaml policy will be used.')
    parser.add_argument('--param', action='append', help='Policy parameters as key=value pairs', default=[])
    args = parser.parse_args()

    if args.class_name:
        policy_config = {'class_name': args.class_name, 'parameters': parse_parameters(args.param)}
    else:
        policy_config = load_config('config.yaml')

    policy_class = policy_classes[policy_config['class_name']]
    policy = policy_class(**policy_config.get('parameters', {}))
    env = BatteryEnv(data=args.data)

    print(f'Running {args.trials} trials with policy {policy_config["class_name"]} and parameters {policy_config.get("parameters", {})}')

    results_dir = os.path.join('results', f'{datetime.now().strftime("%Y%m%d_%H%M%S")}_{policy_config["class_name"]}')
    os.makedirs(results_dir, exist_ok=True)
    runs_dir = os.path.join(results_dir, 'runs')
    os.makedirs(runs_dir, exist_ok=True)

    set_seed(args.seed)

    total_profits = []
    for trial in tqdm.tqdm(range(args.trials)):
        set_seed(args.seed + trial)

        start_step = random.randint(0, len(env.market_data) - 1)
        episode_length = random.randint(1, len(env.market_data) - start_step)
        actions, profits, socs, market_prices = run_trial(env, policy, start_step, episode_length)
        total_profits.extend(profits)

        results_df = pd.DataFrame({'Actions': actions, 'Profits': profits, 'SoC': socs, 'Market Prices': market_prices})
        results_df.to_csv(os.path.join(runs_dir, f'trial_{trial}.csv'), index=False)

    avg_profit = float(np.mean(total_profits))
    std_profit = float(np.std(total_profits))

    config_stats = {
        'class_name': policy_config['class_name'],
        'parameters': policy_config.get('parameters', {}),
        'mean_profit': avg_profit,
        'std_profit': std_profit,
        'num_runs': args.trials
    }

    print(f'Average profit ($): {avg_profit:.2f} ± {std_profit:.2f}')

    with open(os.path.join(results_dir, 'config_stats.yaml'), 'w') as file:
        yaml.dump(config_stats, file, default_flow_style=False)

if __name__ == '__main__':
    main()