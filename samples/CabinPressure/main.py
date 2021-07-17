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
from typing import Any, Dict, List
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
from TwinBuilderConnector.GenericTwinBuilderSimulator import GenericTwinBuilderSimulator


log = logging.getLogger(__name__)


def CreateSession(
    registration_info: SimulatorInterface, config_client: BonsaiClientConfig
):
    """Creates a new Simulator Session and returns new session, sequenceId
    """

    try:
        print(
            "config: {}, {}".format(config_client.server, config_client.workspace)
        )
        registered_session: SimulatorSessionResponse = client.session.create(
            workspace_name=config_client.workspace, body=registration_info
        )
        print("Registered simulator. {}".format(registered_session.session_id))

        return registered_session, 1
    except HttpResponseError as ex:
        print(
            "HttpResponseError in Registering session: StatusCode: {}, Error: {}, Exception: {}".format(
                ex.status_code, ex.error.message, ex
            )
        )
        raise ex
    except Exception as ex:
        print(
            "UnExpected error: {}, Most likely, it's some network connectivity issue, make sure you are able to reach bonsai platform from your network.".format(
                ex
            )
        )
        raise ex
            
if __name__ == '__main__':

    # Configure client to interact with Bonsai service
    config_client = BonsaiClientConfig()
    client = BonsaiClient(config_client)

    # Create simulator session and init sequence id
    twin_model_file = "./demo_package_online/Resources/python_runtime_demo/app/TwinModel.twin"
    CUR_DIR = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
    if not os.path.isabs(twin_model_file):
        twin_model_file = os.path.join(CUR_DIR, *twin_model_file.split(os.sep))
    if not os.path.isfile(twin_model_file):
        print('File does not exist: {}'.format(twin_model_file))
        sys.exit(1)

    sim = GenericTwinBuilderSimulator(twin_model_file)
    # With CSV file
    # csv_file = "./sim/altitude_velocity.csv"
    # sim = GenericTwinBuilderSimulator(twin_model_file, csv_file)
    
    # Load json file as simulator integration config type file
    with open("interface.json") as file:
        interface = json.load(file)

    # Create simulator session and init sequence id
    registration_info = SimulatorInterface(
        name="cabin_pressure",
        timeout=60,
        simulator_context=config_client.simulator_context,
        description=interface["description"],
    )
    registered_session, sequence_id = CreateSession(registration_info, config_client)

    episode = 0
    iteration = 0

    try:
        while True:
            # Advance by the new state depending on the event type
            # TODO: it's risky not doing doing `get_state` without first initializing the sim
            sim_state = SimulatorState(
                sequence_id=sequence_id, state=sim.get_state(), halted=sim.halted(),
            )
            try:
                event = client.session.advance(
                    workspace_name=config_client.workspace,
                    session_id=registered_session.session_id,
                    body=sim_state,
                )
                sequence_id = event.sequence_id
                print(
                    "[{}] Last Event: {}".format(time.strftime("%H:%M:%S"), event.type)
                )
            except HttpResponseError as ex:
                print(
                    "HttpResponseError in Advance: StatusCode: {}, Error: {}, Exception: {}".format(
                        ex.status_code, ex.error.message, ex
                    )
                )
                # This can happen in network connectivity issue, though SDK has retry logic, but even after that request may fail,
                # if your network has some issue, or sim session at platform is going away..
                # So let's re-register sim-session and get a new session and continue iterating. :-)
                registered_session, sequence_id = CreateSession(
                    registration_info, config_client
                )
                continue
            except Exception as err:
                print("Unexpected error in Advance: {}".format(err))
                # Ideally this shouldn't happen, but for very long-running sims It can happen with various reasons, let's re-register sim & Move on.
                # If possible try to notify Bonsai team to see, if this is platform issue and can be fixed.
                registered_session, sequence_id = CreateSession(
                    registration_info, config_client
                )
                continue

            # Event loop
            if event.type == "Idle":
                time.sleep(event.idle.callback_time)
                print("Idling...")
            elif event.type == "EpisodeStart":
                print(event.episode_start.config)
                sim.episode_start(event.episode_start.config)
                episode += 1
            elif event.type == "EpisodeStep":
                iteration += 1
                sim.episode_step(event.episode_step.action)
            elif event.type == "EpisodeFinish":
                print("Episode Finishing...")
                iteration = 0
            elif event.type == "Unregister":
                print("Simulator Session unregistered by platform, Registering again!")
                registered_session, sequence_id = CreateSession(
                    registration_info, config_client
                )
                continue
            else:
                pass
    except KeyboardInterrupt:
        # Gracefully unregister with keyboard interrupt
        client.session.delete(
            workspace_name=config_client.workspace,
            session_id=registered_session.session_id,
        )
        print("Unregistered simulator.")
    except Exception as err:
        # Gracefully unregister for any other exceptions
        client.session.delete(
            workspace_name=config_client.workspace,
            session_id=registered_session.session_id,
        )
        print("Unregistered simulator because: {}".format(err))