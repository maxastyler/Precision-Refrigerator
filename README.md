# Precision-Refrigerator
Code for controlling a Peltier thermoelectric device with two temperature sensors.

Requirements are python-daemon and TKinter (for the FridgeTK program)

Run the daemon, FridgeServer.py and connect with some program using the methods in FridgeClient to fetch, set data. 

A little beaker simulator (BeakerSim.py) allows testing of the daemon interfaces

Written by Bonar Robb and Max Tyler for the DAH course project

# How To Use!
The FridgeServer.py class needs to be run on the computer that is connected to the peltier element and thermometer. This takes the readings and responds to the clients. 

Once the FridgeServer.py is running, you can connect from an interface. There are two: FridgeCLI and FridgeTK.
FridgeTK is the GUI to the FridgeServer, and connects to an address and a port that the server is running on. 
It plots the target temperature and current temperature of the water, and this data can be saved. 

The FridgeCLI program can set the target temperature of the server, and can also read its current state and outputs to the terminal. 

To get more specific help with each program, the -h flag can be used when running to print all available options. 
##To do
1. ~~Don't block server while waiting for connections~~
2. Web page to access the daemon
