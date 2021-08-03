# Bonsai Twin Builder connector

A connector for using Ansys Twin Builder with [Microsoft Project Bonsai](https://azure.microsoft.com/en-us/services/project-bonsai/).

## Installation

In order to use this connector, you will need a Python 3.7 environment with the [required Python packages](TwinBuilderConnector/requirements.txt) installed. One way to do this is using a conda environment as follows:

```
conda create -n bonsai-twin-builder python=3.7
conda activate bonsai-twin-builder
pip install -r TwinBuilderConnector/requirements.txt
```

## Usage: Running a local simulator

This connector assumes you have already created a simulation using [Ansys Twin Builder](https://www.ansys.com/products/systems/ansys-twin-builder).

1. Create an empty brain on Bonsai.

   ```sh
   bonsai brain create -n <brain_name>
   ```

2. Update the brain with your inkling file.

    ```sh
    bonsai brain version update-inkling \   
        -n <brain_name> \
        -f <inkling_filename.ink>
    ```
3. Register your simulator by launching it locally.

   ```sh
   python main.py
   ```

4. Connect your registered sim to the brain:

   ```sh
   bonsai simulator unmanaged connect \                          
       -b <brain_name> \
       -a Train \
       -c <concept_name> \
       --simulator-name <simulator_name> 
   ```

## Usage: Scaling your simulator

Scale your simulator by building the image and pushing it to your registry.

   ```sh
   az acr build --registry <your_registry>
                --image cabinpressure:latest . 
                --file Dockerfile 
                --platform windows
   ```

## Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft 
trademarks or logos is subject to and must follow 
[Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general).
Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship.
Any use of third-party trademarks or logos are subject to those third-party's policies.
