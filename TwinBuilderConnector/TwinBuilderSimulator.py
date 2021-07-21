from typing import Dict, List

from twin_runtime.twin_runtime_core import TwinRuntime
from twin_runtime.twin_runtime_core import LogLevel

class TwinBuilderSimulator():
    def __init__(self, twin_model_file, state_variable_names: List):
        self.state = {}
        self.twin_runtime = None #assigned in reset
        self.done = False
        self.twin_model_file = twin_model_file
        self.state_variable_names = state_variable_names
        self.step_size = 0.5
        self.time_index = 0
        self.reset(self.step_size)

    def reset(self, step_size):
        self.done = False
        runtime_log = self.twin_model_file.replace('.twin', '.log')
        self.step_size = step_size

        if self.twin_runtime != None:
            self.twin_runtime.twin_close()

        # Load Twin, set the parameters values, initialize (and generate snapshots, output)
        self.twin_runtime = TwinRuntime(self.twin_model_file, runtime_log, log_level=LogLevel.TWIN_LOG_ALL)
        self.twin_runtime.twin_instantiate()
        self.twin_runtime.twin_initialize()

        for state_variable_name in self.state_variable_names:
            self.state[state_variable_name] = 0

        self.time_index = 0
        self.state['time_index'] = self.time_index
        # Start at average action values:
        self.episode_step({'controlFlow': (6.0-0.0)/2.0,\
            'outflow':(350.0-0.0)/2.0})

    def get_state(self) -> Dict[str, float]:
        """Called to retreive the current state of the simulator. """
        print(f"returning state: {self.state}")
        return self.state

    def halted(self) -> bool:
        """
        Should return True if the simulator cannot continue for some reason
        """
        return self.done

    def episode_start(self, config: Dict = None) -> None:
        """ Called at the start of each episode """
        self.reset(config["step_size"] or 0.5)
        
    def episode_step(self, action: Dict):
        """ Called for each step of the episode """
        #let the sim get a warm up
        if self.time_index == 0:
            for i in range(5):
                self.runloop(action)

        self.runloop(action)

    def runloop(self,action: Dict):
        for f in ['controlFlow','outflow']:
            self.twin_runtime.twin_set_input_by_name(f, action[f])

        self.twin_runtime.twin_simulate(self.time_index)

        for state_variable_name in self.state_variable_names:
            value = self.twin_runtime.twin_get_output_by_name(state_variable_name).value
            print(value)
            self.state[state_variable_name] = value

        self.state['time_index'] = self.time_index
        #increase the index
        self.time_index = self.time_index + self.step_size
 
    def episode_finish(self):
        """ Called at the end of each episode """
        self.twin_runtime.twin_close()
