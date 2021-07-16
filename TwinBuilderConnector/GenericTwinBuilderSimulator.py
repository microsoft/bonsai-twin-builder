from typing import Dict, List

from GenericModel import GenericTwinModel
from GenericModelWithCSV import GenericTwinModelWithCSV


class GenericTwinBuilderSimulator():
    def __init__(self, twin_model_file, csv_file=None):
        # super().__init__()
        self.simulator = None
        
        if csv_file == None:
            self.simulator = GenericTwinModel(twin_model_file)
        else:
            self.simulator = GenericTwinModelWithCSV(twin_model_file, csv_file)
      
        
    def get_state(self) -> Dict[str, float]:
        """Called to retreive the current state of the simulator. """
        print("returning state:")
        print(self.simulator.state)
        return self.simulator.state
       

    def halted(self) -> bool:
        """
        Should return True if the simulator cannot continue for some reason
        """
        return False #self.simulator.done

    def episode_start(self, config: Dict = None) -> None:
        """ Called at the start of each episode """
        self.simulator.reset(config["step_size"] or 0.5)
        
    def episode_step(self, action: Dict):
        """ Called for each step of the episode """
        self.simulator.step(action)
        
        state = self.get_state()

    def episode_finish(self, action: Dict):
        """ Called for each step of the episode """
        self.simulator.close()
