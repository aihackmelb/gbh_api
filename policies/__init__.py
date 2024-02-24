"""
IMPORTANT: DO NOT MODIFY THIS FILE

This script is crucial for dynamically loading and registering policy classes from
Python files in this directory. It is an integral part of the evaluation process for submissions.
Any modifications to this file may disrupt the evaluation system and are strongly discouraged.

The script automatically imports all policy classes defined in separate files within
the same directory, making them available for use in evaluations.
"""

import os
import importlib
from policies.policy import Policy

# Dictionary to hold the class names and references of the dynamically imported policies
policy_classes = {}

# Gather all .py files in the current directory, excluding '__init__.py'
policy_files = [f[:-3] for f in os.listdir(os.path.dirname(__file__))
                if f.endswith('.py') and f != '__init__.py']

# Dynamically import each policy file and extract policy classes
for file in policy_files:
    module = importlib.import_module('.' + file, package='policies')
    for attr in dir(module):
        attr_value = getattr(module, attr)
        # Check if the attribute is a class and is a subclass of Policy
        if isinstance(attr_value, type) and issubclass(attr_value, Policy) and attr != 'Policy':
            policy_classes[attr] = attr_value
