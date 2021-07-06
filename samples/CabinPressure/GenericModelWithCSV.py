import os
import sys
import time
import struct

import pandas as pd
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from AnsysTwinConnector.twin_runtime_core import TwinRuntime
from AnsysTwinConnector.twin_runtime_core import LogLevel

class GenericTwinModelWithCSV():

    def __init__(self, twin_model_file, csv_file):
        self.state = {}
        self.twin_runtime = None #assigned in reset
        self.done = False
        self.twin_model_file = twin_model_file
        self.csv_file = csv_file
        self.csv_df = pd.read_csv(csv_file)
        self.index = 0
        self.step_size = 0
        self.columns = {}

        c_index = -1
        for s in self.csv_df.columns: #.split(','):   
            c_index = c_index+1         
            if not 'Time' in s:
                colName = s.replace('"','').replace('[]','').strip()
                colName = colName[colName.index('.')+1:]
                self.columns[colName] = c_index
        
        self.slim_df = None

        self.interface_config = None
        self.time_index = 0

    def reset(self,step_size):


        if step_size == 0:
            step_size = 1

        self.done = False
        self.index = 0
        self.step_size = step_size
        CUR_DIR = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))

        if not os.path.isabs(self.twin_model_file):
            self.twin_model_file = os.path.join(CUR_DIR, *self.twin_model_file.split(os.sep))

        if not os.path.isfile(self.twin_model_file):
            print('File does not exist: {}'.format(self.twin_model_file))
            sys.exit(1)

        runtime_log = self.twin_model_file.replace('.twin', '.log')

        # Load Twin, set the parameters values, initialize (and generate snapshots, output)
        self.twin_runtime = TwinRuntime(self.twin_model_file, runtime_log, log_level=LogLevel.TWIN_LOG_ALL)
        self.twin_runtime.print_model_info(max_var_to_print=10)
        self.twin_runtime.twin_instantiate()
        self.twin_runtime.twin_initialize()

        first_col = self.csv_df.columns[0]
        min = self.csv_df[first_col].min()
        max = self.csv_df[first_col].max()

        
        steps = (max-min)/step_size

        len_df = len(self.csv_df)-1

        df_step_size = int(len_df/steps)

        self.slim_df = pd.DataFrame(data=None, columns=self.csv_df.columns)

        for i in range(0,len_df,df_step_size):
            self.slim_df = self.slim_df.append(self.csv_df.iloc[i])

        for f in self.get_interface().description.state.fields:
            self.state[f.name] = 0

        self.time_index = 0

    def parse_df(self, df):
        fields = []

        print(df.columns)

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
        
        try:
            for f in self.interface_config.description.action.fields:
                #self.twin_runtime.twin_set_input_by_name("InputTorque", action["Torq1_tau"])
                if f.name in self.columns.keys():
                    print('{} is a key'.format(f.name))
                    self.twin_runtime.twin_set_input_by_name(f.name, self.slim_df.iloc[self.index][self.columns[f.name]])
                else:
                    print()
                    self.twin_runtime.twin_set_input_by_name(f.name, action[f.name])
            
            self.twin_runtime.twin_simulate(self.csv_df.iloc[self.index][0])

            for f in self.interface_config.description.state.fields:
                value = self.twin_runtime.twin_get_output_by_name(f.name).value
                print(value)
                self.state[f.name] = value

            self.index = self.index + 1

            if self.index == self.slim_df.shape[0]:
                self.done = True
        except Exception as ex:
            print("Exception {} occurred on step".format(type(ex).__name__))
            self.done = True
 
    def close(self):
        self.twin_runtime.twin_close()