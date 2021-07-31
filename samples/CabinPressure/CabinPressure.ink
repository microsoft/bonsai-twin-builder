# Sample Inkling for a Bonsai brain that can be trained with the Cabin Pressure simulator.
inkling "2.0"

using Math
using Goal

# Temperature set point constant
const SetTemp = 296

# State received from the simulator after each iteration
type SimState {
    PC: number,
    PCabin: number,
    ceiling_t: number,
    altitude_out: number,
    velocity_out: number,
    time_index:number
}

# Action provided as output by brain and sent as input to the simulator
type SimAction {
    controlFlow: number<0 .. 6> ,
    outflow: number<0 .. 350>,
}

# Per-episode configuration sent to the simulator.
type SimConfig {
    step_size: number
}

# Concept graph with a single concept
graph (input: SimState): SimAction {
    concept ControlTemperatureAndPressure(input): SimAction {
        curriculum {
            # The source of training for this concept is a simulator that takes
            # an action as an input and outputs a state
            source simulator Simulator(action: SimAction, config: SimConfig): SimState {
            }

            goal(s:SimState) {
                # Minimize difference between cabin pressure and controller set point
                minimize pressure_difference:
                   Math.Abs(s.PCabin - s.PC) in Goal.Range(0, 1000)

                # Minimize difference between cabin temperature and constant set point
                minimize temperature_difference:
                    Math.Abs(s.ceiling_t - SetTemp) in Goal.RangeBelow(2)
            }

            # Configure simulation to use a step size of 0.9
            lesson step_size {
                scenario {
                    step_size: 0.9
                }
            }
        
            training {
                EpisodeIterationLimit: 1000,
                NoProgressIterationLimit: 1000000,
                TotalIterationLimit: 5000000
            }
       }
    }
}
