#!/usr/bin/env python3
import os
import sys
import json

# Add parent directory containing the TwinBuilderConnector folder to path.
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from TwinBuilderConnector.RunSession import RunSession

if __name__ == '__main__':
    twin_model_file = "./demo_package_online/Resources/python_runtime_demo/app/TwinModel.twin"

    # Locate twin_model_file if it is relative path from this file.
    CUR_DIR = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
    if not os.path.isabs(twin_model_file):
        twin_model_file = os.path.join(CUR_DIR, *twin_model_file.split(os.sep))

    if not os.path.isfile(twin_model_file):
        print('File does not exist: {}'.format(twin_model_file))
        sys.exit(1)

    RunSession(twin_model_file)
