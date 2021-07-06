from twin_runtime.twin_runtime_core import TwinRuntime
from twin_runtime.twin_runtime_core import LogLevel

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import csv
import os
import platform
import time
import pprint

CUR_DIR = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
pd.set_option('precision', 12)
pd.set_option('display.max_columns', 20)
pd.set_option('expand_frame_repr', False)


def load_data(twin_builder_inputs, twin_builder_results):

    # Clean CSV headers if exported from Twin builder
    def clean_column_names(column_names):
        for name_index in range(len(column_names)):
            clean_header = column_names[name_index].replace("\"", "").replace(" ", "").replace("]", "").replace("[","")
            name_components = clean_header.split(".", 1)
            # The column name should match the last word after the "." in each column
            column_names[name_index] = name_components[-1]

        return column_names

    ##### Data loading (into Pandas DataFrame) and pre-processing #######
    # C engine can't read rows with quotes, reading just the first row
    input_header_df = pd.read_csv(twin_builder_inputs, header=None, nrows=1, sep=',\s+',
                                  engine='python', quoting=csv.QUOTE_ALL)

    # C engine can't read rows with quotes, reading just the first row
    output_header_df = pd.read_csv(twin_builder_results, header=None, nrows=1, sep=',\s+',
                                   engine='python', quoting=csv.QUOTE_ALL)

    # Reading all values from the csv but skipping the first row
    twin_builder_inputs_df = pd.read_csv(twin_builder_inputs, header=None, skiprows=1)
    twin_builder_results_df = pd.read_csv(twin_builder_results, header=None, skiprows=1)

    # Parsing column names correctly
    inputs_header_values = input_header_df.iloc[0][0].split(',')
    output_header_values = output_header_df.iloc[0][0].split(',')

    # Cleaning csv column names to match the twin output names
    clean_column_names(inputs_header_values)
    clean_column_names(output_header_values)

    # Adding column names back
    twin_builder_results_df.columns = output_header_values
    twin_builder_inputs_df.columns = inputs_header_values

    return twin_builder_inputs_df, twin_builder_results_df


def run_simulation_step_by_step(twin_runtime, input_df, output_names,
                                print_step_output=True):

    data_dimensions = input_df.shape
    sim_output_list = []

    # Getting the outputs for 0 time
    initial_output = [0.0] + twin_runtime.twin_get_outputs()  # API CALL
    sim_output_list.append(initial_output)

    # Iterates over all datapoints in the dataframe
    for data_index in range(data_dimensions[0] - 1):

        # Gets the stop time of the current simulation step
        time_end = input_df.iloc[data_index + 1][0]

        # Sets the input values
        for column in input_df.columns[1::]:
            input_value = input_df[column][data_index]
            twin_runtime.twin_set_input_by_name(column, input_value)  # API CALL

        if print_step_output is True:
            inputs = input_df.iloc[data_index][1:].values.tolist()
            print("Simulating to: {} with inputs {}".format(time_end, inputs))

        # Advance simulation until the next timestep
        twin_runtime.twin_simulate(time_end)  # API CALL

        # Reads and stores the simulation results for the current timestep
        sim_output = [time_end] + twin_runtime.twin_get_outputs()  # API CALL
        sim_output_list.append(sim_output)

        if print_step_output is True:
            twin_runtime.print_outputs()  # API CALL
            print()

    # Returns a dataframe with the simulation results for all timesteps
    return pd.DataFrame(sim_output_list, columns=output_names, dtype=float)


def run_simulation_batch_mode_csv(twin_runtime, twin_file_name):
    # Running batch mode with csv files
    twin_runtime_batch_input = os.path.join(CUR_DIR, '{}_input.csv'.format(twin_file_name))
    twin_runtime_batch_result = os.path.join(CUR_DIR, '{}_batch_mode_output.csv'.format(twin_file_name))
    step_size = 0
    interpolate = 0
    twin_runtime.twin_simulate_batch_mode_csv(twin_runtime_batch_input, twin_runtime_batch_result,
                                              step_size, interpolate)  # API CALL
    batch_csv_result_df = pd.read_csv(twin_runtime_batch_result)
    return batch_csv_result_df


def run_simulation_batch_mode_2d_array(reference_df, twin_model_input_df, twin_runtime):
    # Running batch mode with pandas Dataframes
    step_size = 0
    interpolate = 0
    twin_model_input_df.set_index('Time', inplace=True)
    output_columns = reference_df.columns
    batch_2d_array_result_df = twin_runtime.twin_simulate_batch_mode(twin_model_input_df,
                                                                     output_columns, step_size,
                                                                     interpolate,
                                                                     time_as_index=True)  # API CALL
    return batch_2d_array_result_df


def plot_result_comparison(runtime_result_df, reference_df,
                           batch_csv_result_df, batch_2d_array_result_df):
    # Plotting the runtime output and comparing against the Twin Builder output
    columns = runtime_result_df.columns[1::]
    fig, ax = plt.subplots(ncols=4, nrows=len(columns), figsize=(18, 7))
    if len(columns) == 1:
        single_column = True
    else:
        single_column = False

    fig.subplots_adjust(hspace=0.5)
    fig.set_tight_layout({"pad": .0})
    # x_data = runtime_result_df.iloc[:, 0]

    for ind, col_name in enumerate(columns):
        # Plot runtime results
        if single_column:
            axes0 = ax[0]
            axes1 = ax[1]
            axes2 = ax[2]
            axes3 = ax[3]
        else:
            axes0 = ax[ind, 0]
            axes1 = ax[ind, 1]
            axes2 = ax[ind, 2]
            axes3 = ax[ind, 3]
        runtime_result_df.plot(x=0, y=col_name, ax=axes0, ls=":", color='g',
                               title='Twin Runtime - Step by Step')
        axes0.legend(loc=2)
        axes0.set_xlabel('Time [s]')

        # Plot Twin batch mode csv results
        batch_csv_result_df.plot(x=0, y=col_name, ax=axes1, ls="-.", color='g',
                                 title='Twin Runtime - Batch Mode CSV')
        axes1.legend(loc=2)
        axes1.set_xlabel('Time [s]')

        # Plot Twin batch mode 2d array results
        batch_2d_array_result_df.plot(x=0, y=col_name, ax=axes2, ls="--", color='g',
                                      title='Twin Runtime - Batch Mode 2D Array')
        axes2.legend(loc=2)
        axes2.set_xlabel('Time [s]')

        # Plot Twin Builder results
        reference_df.plot(x=0, y=col_name, ax=axes3, color='g', title='Twin Builder')
        axes3.legend(loc=2)
        axes3.set_xlabel('Time [s]')

        if ind > 0:
            axes0.set_title('')
            axes1.set_title('')
            axes2.set_title('')
            axes3.set_title('')
    

    # Show plot
    plt.style.use('seaborn')
    plt.show()
    plt.savefig(os.path.join(CUR_DIR, 'results.png'))    


def run(twin_file_name):

    # Input generated from Twin builder
    twin_builder_input = os.path.join(CUR_DIR, '{}_input.csv'.format(twin_file_name))

    # Simulation results exported from Twin Builder
    twin_builder_result = os.path.join(CUR_DIR, 'Reference.csv')

    twin_model_file = os.path.join(CUR_DIR, '{}.twin'.format(twin_file_name))
    runtime_log = os.path.join(CUR_DIR, '{}_{}.log'.format(twin_file_name, platform.system()))
    print('Loading model: {}'.format(twin_model_file))

    # Load input and reference data
    twin_model_input_df, reference_df = load_data(twin_builder_input, twin_builder_result)

    if platform.system() == 'Windows':
        lib_file = 'TwinRuntimeSDK.dll'
    else:
        lib_file = 'TwinRuntimeSDK.so'
    twin_runtime_lib = os.path.join(os.path.dirname(CUR_DIR), 'twin_runtime', lib_file)

    # Instantiate Twin Runtime
    twin_runtime = TwinRuntime(twin_model_file, runtime_log, log_level=LogLevel.TWIN_LOG_ERROR)  # API CALL
    twin_runtime.print_model_info(max_var_to_print=10)  # API CALL

    cross_platform = TwinRuntime.twin_is_cross_platform(twin_runtime_lib, twin_model_file)
    if cross_platform:
        print('Twin model is cross-platform')
    else:
        print('Twin model is Windows-only')

    if platform.system() == 'Linux':
        twin_dependencies_dict = TwinRuntime.twin_get_model_dependencies(twin_runtime_lib,
                                                                         twin_model_file)  # API CALL

        print('--- Twin Model Dependencies ---')
        pprint.pprint(twin_dependencies_dict)

    # Instantiating, setting start values for inputs and initializing
    twin_runtime.twin_instantiate()  # API CALL
    start_values = list(twin_model_input_df.iloc[0, 1:])
    twin_runtime.twin_set_inputs(start_values)
    twin_runtime.twin_initialize()  # API CALL

    # Simulate using all data points from the data frame, one datapoint at a time
    t_start = time.time()
    runtime_result_df = run_simulation_step_by_step(twin_runtime, twin_model_input_df,
                                                    reference_df.columns,
                                                    print_step_output=False)
    t_end = time.time()
    print('Step-by-step time: {}'.format(t_end-t_start))

    # Resetting Twin Runtime simulation to instantiation state
    twin_runtime.twin_close()
    twin_runtime.twin_load(log_level=LogLevel.TWIN_LOG_ERROR)

    # Instantiating, setting start values for inputs and initializing
    twin_runtime.twin_instantiate()  # API CALL
    start_values = list(twin_model_input_df.iloc[0, 1:])
    twin_runtime.twin_set_inputs(start_values)
    twin_runtime.twin_initialize()  # API CALL

    t_start = time.time()
    batch_csv_result_df = run_simulation_batch_mode_csv(twin_runtime, twin_file_name)
    t_end = time.time()
    print('Batch mode csv time: {}'.format(t_end - t_start))

    # Resetting Twin Runtime simulation to instantiation state
    twin_runtime.twin_close()
    twin_runtime.twin_load(log_level=LogLevel.TWIN_LOG_ERROR)

    # Instantiating, setting start values for inputs and initializing
    twin_runtime.twin_instantiate()  # API CALL
    start_values = list(twin_model_input_df.iloc[0, 1:])
    twin_runtime.twin_set_inputs(start_values)
    twin_runtime.twin_initialize()  # API CALL

    t_start = time.time()
    batch_2d_array_result_df = run_simulation_batch_mode_2d_array(reference_df,
                                                                  twin_model_input_df, twin_runtime)
    t_end = time.time()
    print('Batch mode 2D time: {}'.format(t_end - t_start))

    # Closing the TWIN model
    twin_runtime.twin_close()

    # Plotting all the results
    plot_result_comparison(runtime_result_df, reference_df, batch_csv_result_df,
                           batch_2d_array_result_df)


if __name__ == '__main__':
    run()
