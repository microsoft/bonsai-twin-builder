This package contains a sample Python code that interacts with the Ansys Twin Runtime SDK and performs the simulation of a Twin model. The 3 simulation modes supported by the Twin Runtime are demonstrated: step-by-step simulation, batch mode with inputs/output from CSV file, and batch mode with input/output from 2D arrays. The Python application uses Pandas dataframes for the batch mode with 2D arrays, and the Python wrapper converts them to 2D arrays compatible with the Twin Runtime.

Detailed contents of this package:

- README.md:                         This readme file
- run_windows.bat:                   Batch file for easy execution of the simulation under Windows
- run_linux.sh:                      Shell script file for easy execution of the simulation under Linux; LD_LIBRARY_PATH is automatically set in this script
- run.py:                            Main Python file that initializes the demonstration
- requirements.txt:                  List of required Python packages
- twin_runtime/
  - lib/:                         Folder containing the GCC6.3 library dependencies required by the Twin Runtime for Linux
  - TwinRuntimeSDK.dll:           Ansys Twin Runtime SDK for Windows
  - TwinRuntimeSDK.so:            Ansys Twin Runtime SDK for Linux
  - twin_runtime_core.py:         Python wrapper for the runtime
  - twin_runtime_error.py:        Wrapper exception classes
  - log_level.py:                 Wrapper log level enumerator


app/
  -- application.py                           Python application for the TwinROM example
  -- TwinModel.twin                           TWIN model
  -- TwinModel_input.csv                      Input data for the model
  -- Reference.csv                            Reference simulation results

*******************************************************

Requirements:
 - Python 3.5 or greater
 - Python libraries listed in the requirements.txt
    -> For easy installation, open a Windows prompt, and type: > pip install -r requirements.txt

*******************************************************

Running the demonstration on Windows:
 
  Double-click on the run_windows.bat file
   
                 or
                  
  Open a terminal/prompt and type: python run.py

Running the demonstration on Linux: 
  - Open a terminal, verify that the script has execution permission, and type: ./run_linux.sh
                

