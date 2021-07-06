import os
import sys
import time
import struct

import pandas as pd
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from AnsysTwinConnector.twin_runtime_core import TwinRuntime
from AnsysTwinConnector.twin_runtime_core import LogLevel

class GenericTwinModel():

    def __init__(self, twin_model_file):
        self.state = {}
        self.twin_runtime = None #assigned in reset
        self.done = False
        self.twin_model_file = twin_model_file
        self.step_size = 0.5
       
        self.interface_config = None
        self.time_index = 0
        self.reset(self.step_size)

    def reset(self, step_size):
        self.done = False
        CUR_DIR = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))

        if not os.path.isabs(self.twin_model_file):
            self.twin_model_file = os.path.join(CUR_DIR, *self.twin_model_file.split(os.sep))

        if not os.path.isfile(self.twin_model_file):
            print('File does not exist: {}'.format(self.twin_model_file))
            sys.exit(1)

        runtime_log = self.twin_model_file.replace('.twin', '.log')

        self.step_size = step_size

        # Load Twin, set the parameters values, initialize (and generate snapshots, output)
        self.twin_runtime = TwinRuntime(self.twin_model_file, runtime_log, log_level=LogLevel.TWIN_LOG_ALL)

        self.twin_runtime.twin_instantiate()

        self.twin_runtime.twin_initialize()

        self.state['PC'] = 0
        self.state['PCabin'] = 0
        self.state['ceiling_t'] = 0
        self.state['altitude_out'] = 0
        self.state['velocity_out'] = 0

        self.time_index = 0
        self.state['time_index'] = self.time_index
        # Start at average action values:
        self.step({'controlFlow': (6.0-0.0)/2.0,\
            'outflow':(350.0-0.0)/2.0})


    def parse_df(self, df):
        fields = []

        for i in range(0, len(df)):
            ft = FieldType(category=Category.Number)
            
            if df.iloc[i]['Description'] != 'TWIN_VARPROP_NOTDEFINED': 
                ft.comment = df.iloc[i]['Description']

            if df.iloc[i]['Start'] != 'TWIN_VARPROP_NOTDEFINED': 
                ft.start = df.iloc[i]['Start']

            if df.iloc[i]['Max'] != 'TWIN_VARPROP_NOTDEFINED': 
                ft.stop = df.iloc[i]['Max']

            f = Field(name=df.iloc[i]['Name'], field_type=ft)
            
            fields.append(f)

        return fields


    def step(self, action:dict):
        
        #let the sim get a warm up
        if self.time_index == 0:
            for i in range(5):
                self.runloop(action)

        self.runloop(action)

 
    def runloop(self,action:dict):
            for f in ['controlFlow','outflow']:
                self.twin_runtime.twin_set_input_by_name(f, action[f])

            self.twin_runtime.twin_simulate(self.time_index)

            for f in ['PC','PCabin','ceiling_t','altitude_out','velocity_out']:
                value = self.twin_runtime.twin_get_output_by_name(f).value
                print(value)
                self.state[f] = value

            self.state['time_index'] = self.time_index
            #increase the index
            self.time_index = self.time_index + self.step_size
 
    def close(self):
        self.twin_runtime.twin_close()