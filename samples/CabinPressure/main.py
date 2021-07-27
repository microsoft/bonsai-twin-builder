#!/usr/bin/env python3
import os
import sys

# Add parent directory containing the TwinBuilderConnector folder to path.
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
# Add CabinPressureTwin directory containing twin_runtime to the path.
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "CabinPressureTwin"))

print(f"path is {sys.path}")

from TwinBuilderConnector.RunSession import RunSession

if __name__ == '__main__':
    twin_model_file = "./CabinPressureTwin/TwinModel.twin"

    # Locate twin_model_file if it is relative path from this file.
    CUR_DIR = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
    if not os.path.isabs(twin_model_file):
        twin_model_file = os.path.join(CUR_DIR, *twin_model_file.split(os.sep))

    if not os.path.isfile(twin_model_file):
        print('File does not exist: {}'.format(twin_model_file))
        sys.exit(1)

    state_variable_names = ['PC', 'PCabin', 'ceiling_t', 'altitude_out', 'velocity_out']
    action_variable_names = ['controlFlow', 'outflow']
    action_variable_values = [(6.0-0.0)/2.0, (350.0-0.0)/2.0] # start at average action values
    RunSession(twin_model_file, state_variable_names, action_variable_names, 5, action_variable_values)
