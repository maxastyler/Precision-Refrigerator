# Precision-Refrigerator
Code for controlling a Peltier thermoelectric device with two temperature sensors.

Requirements are python-daemon

Run the daemon, FridgeServer.py and connect with some program using the methods in FridgeClient to fetch, set data. 

A little beaker simulator (BeakerSim.py) allows testing of the daemon interfaces

Written by Bonar Robb and Max Tyler for the DAH course project

##To do
1. ~~Don't block server while waiting for connections~~
2. Web page to access the daemon
