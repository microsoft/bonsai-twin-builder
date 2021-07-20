#!/usr/bin/env python3

"""
MSFT Bonsai SDK3 Template for Simulator Integration using
Copyright 2020 Microsoft
Usage:
  For registering simulator with the Bonsai service for training:
    python __main__.py --api-host https://api.bons.ai \
           --workspace <workspace_id> \
           --accesskey="<access_key> \
  Then connect your registered simulator to a Brain via UI
"""

import os
import sys
import logging
import json

from microsoft_bonsai_api.simulator.client import BonsaiClient, BonsaiClientConfig
from microsoft_bonsai_api.simulator.generated.models import (
    SimulatorInterface,
    SimulatorState,
    SimulatorSessionResponse,
)
import time
import argparse
import datetime

# Add parent directory containing the TwinBuilderConnector folder to path.
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from TwinBuilderConnector.RunSession import RunSession

log = logging.getLogger(__name__)


if __name__ == '__main__':
    twin_model_file = "./demo_package_online/Resources/python_runtime_demo/app/TwinModel.twin"
    CUR_DIR = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
    if not os.path.isabs(twin_model_file):
        twin_model_file = os.path.join(CUR_DIR, *twin_model_file.split(os.sep))
    if not os.path.isfile(twin_model_file):
        print('File does not exist: {}'.format(twin_model_file))
        sys.exit(1)

    RunSession(twin_model_file)
