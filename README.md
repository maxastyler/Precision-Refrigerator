# Precision-Refrigerator
Code for controlling a Peltier thermoelectric device with two temperature sensors. A server is set up which interacts with a thermometer and peltier device to read and control the current temperature a beaker of water. This server then connects to clients, and transfers information using sockets. Two example clients are written, one for command line and one with a multi-threaded GUI. This GUI graphs the data coming in, and can save the saved data into a numpy formatted plain text file.

A little beaker simulator (BeakerSim.py) allows testing of the daemon interface.

Written by Bonar Robb and Max Tyler for the DAH course project

# How To Use!
The FridgeServer.py class needs to be run on the computer that is connected to the peltier element and thermometer. This takes the readings and responds to the clients. 

Once the FridgeServer.py is running, you can connect from an interface. There are two written, using the functions defined in the FridgeClient class to communicate with the server: FridgeCLI and FridgeTK.
FridgeTK is the GUI to the FridgeServer, and connects to an address and a port that the server is running on. 
It plots the target temperature and current temperature of the water, and this data can be saved. 

The FridgeCLI program can set the target temperature of the server, and can also read its current state and outputs to the terminal. 

To get more specific help with each program, the -h flag can be used when running to print all available options. 

## Quick Usage Example
Run the FridgeServer.py class as a daemon
```
./FridgeServer.py
```
Now run FridgeTK to connect to this running daemon.
```
./FridgeTK
```
Once you're done with FridgeTK, shutdown the daemon.
```
./FridgeServer.py stop
```
# Requirements
This project runs with python3

Here are the requirements for each class:
- FridgeServer.py
  - python-daemon
  - RPi.GPIO
  - w1thermsensor
- BeakerSim.py
  - python-daemon
- FridgeTK
  - tk
  - matplotlib
  - numpy
  
These dependencies can be installed using python-pip, with the exception of tk which is installed through the package manager/compiled for your system (eg. pacman -S tk)
