# Precision-Refrigerator
Code for controlling a Peltier thermoelectric device with two temperature sensors.

Run the daemon, FridgeServer.py and connect with some program using the methods in FridgeClient to fetch data and set a target temperature. 

A little beaker simulator (BeakerSim.py) allows testing of the daemon interface.

Written by Bonar Robb and Max Tyler for the DAH course project

# How To Use!
The FridgeServer.py class needs to be run on the computer that is connected to the peltier element and thermometer. This takes the readings and responds to the clients. 

Once the FridgeServer.py is running, you can connect from an interface. There are two written, using the functions defined in the FridgeClient class to communicate with the server: FridgeCLI and FridgeTK.
FridgeTK is the GUI to the FridgeServer, and connects to an address and a port that the server is running on. 
It plots the target temperature and current temperature of the water, and this data can be saved. 

The FridgeCLI program can set the target temperature of the server, and can also read its current state and outputs to the terminal. 

To get more specific help with each program, the -h flag can be used when running to print all available options. 

# Requirements
Here are the requirements for each class:
- FridgeServer.py
  - python-daemon
  - RPi.GPIO
  - w1thermsensor
- Test
