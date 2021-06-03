# This file must contain sample Inkling for a Bonsai brain that can be trained with the Cabin Pressure simulator.
#
# The purpose is to demonstrate that the simulator sample's states, actions, and configuration parameters
# work correctly and that training with the {SimPlatform} connector works correctly.
#
# It is not necessary for the brain to actually learn something realistic and useful, although the sample will be more interesting
# and compelling if does!

inkling "2.0"

using Math
using Goal

const SetTemp = 296
# Define a type that represents the per-iteration state returned by the simulator.
type SimState {
    PC: number,
    PCabin: number,
    ceiling_t: number,
    altitude_out: number,
    velocity_out: number,
    time_index:number
}
# Commenting out unused ObservableState
# type ObservableState {
#     PC: number,
#     PCabin: number,
#     ceiling_t: number,
#     altitude_out: number,
#     velocity_out: number
# }
# Define a type that represents the per-iteration action
# accepted by the simulator.
type SimAction {
    controlFlow: number<0 .. 6> ,
    outflow: number<0 .. 350>,
}
type SimConfig{
    step_size: number
}
simulator Simulator(action: SimAction, config: SimConfig): SimState {
   #package "ansys-tb2v1"
   package "ansys-tb3v1130"
}
# Define a concept graph
graph (input: SimState): SimAction {
    concept Concept1(input): SimAction {
        curriculum {
            # Add goals here describing what you want to teach the brain
            # See the Inkling documentation for goals syntax
            # https://docs.microsoft.com/bonsai/inkling/keywords/goal
           
             goal(s:SimState)
            {
                minimize pressure_overshoot:
                   Math.Abs(s.PCabin - s.PC) in Goal.Range(0,1000)
                #avoid overshoot_pressure:
                #    Math.Abs(s.PCabin - s.PC) in Goal.RangeAbove(3000) #within 10
                minimize temp_differences:
                    Math.Abs(s.ceiling_t - SetTemp) in Goal.RangeBelow(2)
            }
            lesson `step size`{
                scenario {
                    step_size: 0.9
                }
            }
        
             training {
                 EpisodeIterationLimit: 1000,
                 NoProgressIterationLimit: 5000000,
                 TotalIterationLimit: 50000000
             }
            # The source of training for this concept is a simulator
            # that takes an action as an input and outputs a state.
            source Simulator
        }
    }
}