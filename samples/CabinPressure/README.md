# Cabin Pressure

The Cabin Pressure Control System (CPCS) is an avionics system designed to minimize the rate of change of cabin temperature and pressure. The purpose of the CPCS is to ensure the safety of the airframe and passengers while maximizing comfort during all phases of flight. ANSYS Twin Builder models the CPCS components (actuators, sensors, etc.) to enable optimization and validation of the component choices with the system response. 

In this example, the goal is to optimize the control of two flow rate valves that regulate cabin temperature and pressure. Comfort is characterized by meeting the set point temperature (296K), while safety is achieved by matching a variable cabin pressure controller set point. Ultimately, the controller should learn to balance safety and comfort as the altitude and velocity of the airframe changes throughout the duration of the flight.


## States

> | State                    | Range         | Notes |
> | ------------------------ | ------------- | ----- |
> | PC                | []   | Cabin pressure controller set point. |
> | PCabin                | []   | Cabin pressure. |
> | ceiling_t                | []   | Cabin temperature at ceiling level. |
> | altitude_out                | []   | Altitude of airplane. |
> | velocity_out                | []   | Velocity of airplane. |

## Actions

> | Action                    | Range         | Notes |
> | ------------------------ | ------------- | ----- |
> | controlFlow                | [0 .. 6]   |  |
> | outflow                | [0 .. 345]   |  |


## Configuration Parameters

> | Config                    | Range         | Notes |
> | ------------------------ | ------------- | ----- |
> | step_size                | [0 .. 1]   |  |

## Usage: Running a local simulator

1. Run a single instance of the simulator locally:
    ```
    python main.py
    ```
    It should connect to the Bonsai service and print messages showing that it is idling.

2. In a separate command window, create a brain and start training using either the UI in your Bonsai workspace or the following CLI commands:
    ```
    bonsai brain create -n CabinPressure
    bonsai brain version update-inkling -f CabinPressure.ink -n CabinPressure
    bonsai brain version start-training -n CabinPressure
    bonsai simulator unmanaged connect -b CabinPressure -a Train -c ControlTemperatureAndPressure --simulator-name cabin_pressure
    ```
    Your simulation should run epsiodes with states and actions that appear in the Bonsai training graph.
