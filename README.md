# Bonsai Twin Builder connector

A connector for using Ansys Twin Builder with [Microsoft Project Bonsai](https://azure.microsoft.com/en-us/services/project-bonsai/).

## Installation

In order to use this connector, you will need a Python 3.7 environment with the [required Python packages](TwinBuilderConnector/requirements.txt) installed. One way to do this is using a conda environment as follows:

```
conda create -n bonsai-twin-builder python=3.7
conda activate bonsai-twin-builder
pip install -r TwinBuilderConnector/requirements.txt
```

## CabinPressure sample

The [CabinPressure sample](samples/CabinPressure/README.md) demonstrates how to use Bonsai with an Ansys Twin Builder model. It shows how to train a Bonsai brain that uses a digital twin to control the cabin pressure and temperature of an avionics system.

## CabinPressureTwin model

The Twin Builer model in samples/CabinPressure/CabinPressureTwin contains a twin model, runtime, and code that are copyrighted example files from ANSYS, Inc. and is licensed by the terms outlined in [samples/CabinPressure/CabinPressureTwin/LICENSE.txt](samples/CabinPressure/CabinPressureTwin/LICENSE.txt).

## Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft 
trademarks or logos is subject to and must follow 
[Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general).
Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship.
Any use of third-party trademarks or logos are subject to those third-party's policies.
