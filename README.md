# National Energy Market Hackathon Competition Guide

## Competition Overview

Welcome to the National Energy Market (NEM) Hackathon! In this competition, you'll develop innovative strategies to optimize battery operations within an energy market simulation. Your challenge is to create algorithms, or policies, that expertly manage battery charging and discharging in response to real-time market data.

## Competition Goal

Maximize profits in a simulated energy market by strategically managing battery operations. Your policy will be evaluated over 1000 trials with varying starting conditions, including charge levels, times, and durations.

## Key Components of the Repository

- **battery_env.py**: The simulation environment for battery-market interactions.
- **evaluate.py**: Tool for testing and evaluating your market strategy.
- **plotting.py**: Utility to visualize outcomes like actions taken, market prices, battery SoC, and profits.
- **policies/**: Folder containing different policy classes for battery operation.
  - **policy.py**: Base class for all strategies.
  - **random.py**: A simple policy making random decisions.
  - **rolling_average.py**: A more complex policy based on market price averages.
  - **starter_code.py**: A template for developing your own policy.
  - **__init__.py**: Script to automatically load and register policy classes.

### Additional Note

- **gen_data.py**: Used for generating synthetic market data, not included in the final repository.

## Getting Started: Building Your Strategy

### Step 1: Develop Your Policy
Create your custom policy by extending the `Policy` class in `policies/your_policy.py`. Your policy should define a continuous action strategy, ranging from minimum discharge to maximum charge rate.

### Step 2: Test and Evaluate
Utilize `evaluate.py` to run simulations of your policy under various market conditions. This will help you understand the effectiveness of your strategy.

### Step 3: Visualize and Refine
Employ `plotting.py` to graphically analyze the performance of your policy. Use these insights to refine and improve your approach.

## Submission and Evaluation

### Dataset Information

- **Development Set**: Market data from April 2023.
- **Training Set**: Entire market data from 2023.
- **Testing Set**: Live market data from late April to early May.

### Submission Guidelines

- Tag your commits with 'submission' to enter them into the competition.
- Keep in mind the limited time frame of the test data when developing your strategy.
- Trial results and other data will be posted on our website (link TBD).

### Important Dates

- **Submission Deadline**: [Insert Deadline Date]
- Ensure your model is properly entered using the submission workflow.

## Final Notes

- Your `config.yaml` file will be crucial for the submission.
- Though dev test results are not part of the official grading, they are valuable for ensuring your model is correctly entered and functioning.

Best of luck to all participants! We eagerly anticipate your creative and effective solutions in this challenging competition.
