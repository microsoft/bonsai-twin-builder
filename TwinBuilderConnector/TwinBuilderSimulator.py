from typing import Dict, List
from demo_package_online.Resources.python_runtime_demo.twin_runtime.twin_runtime_core import TwinRuntime
from demo_package_online.Resources.python_runtime_demo.twin_runtime.twin_runtime_core import LogLevel

class TwinBuilderSimulator():
    def __init__(self, twin_model_file):
        self.state = {}
        self.twin_runtime = None #assigned in reset
        self.done = False
        self.twin_model_file = twin_model_file
        self.step_size = 0.5
        self.time_index = 0
        self.reset(self.step_size)

    def reset(self, step_size):
        self.done = False

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
        self.episode_step({'controlFlow': (6.0-0.0)/2.0,\
            'outflow':(350.0-0.0)/2.0})

    def get_state(self) -> Dict[str, float]:
        """Called to retreive the current state of the simulator. """
        print("returning state:")
        print(self.state)
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
 
    def episode_finish(self):
        """ Called at the end of each episode """
        self.twin_runtime.twin_close()
