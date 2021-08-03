# Ansys Twin Builder Connector

This directory contains helper classes for integrating an Ansys digital twin model with the Microsoft Project Bonsai service.

* [TwinBuilderSimulator.py](TwinBuilderSimulator.py) uses the twin runtime to load a digital twin model and supports the reset, step, and state functions needed to use the digital twin with Bonsai.
* [RunSession.py](RunSession.py) connects to the Bonsai service and runs training episodes using the digital twin.