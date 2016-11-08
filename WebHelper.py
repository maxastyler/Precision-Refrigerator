#!/usr/bin/env python3
from FridgeClient import *
import argparse
import sys

if __name__=='__main__':
    parser=argparse.ArgumentParser(description='Script to help with controlling FridgeServer from a webpage')
    parser.add_argument('option', choices=['get_current', 'get_target', 'set_temp'], help='Options to run this script with. get_current gets the current measured temperature. get_target gets the temperature that the pi wants the cooler to be. set_temp sets the target temp')
    parser.add_argument('--temperature', '-t', type=float, help='When the set_temp option is called, this is the temperature that it is set to')
    args=parser.parse_args()
    if args.option=='get_current':
        returned=get_current_temp()
        if returned[1]!=0:
            print("Error receiving current temperature! Maybe daemon isn't running?")
        elif returned[1]==0:
            print("{}".format(returned[0]))
        else:
            print("Unknown Error")
    elif args.option=='get_target':
        returned=get_target_temp()
        if returned[1]!=0:
            print("Error receiving current temperature! Maybe daemon isn't running?")
        elif returned[1]==0:
            print("{}".format(returned[0]))
        else:
            print("Unknown Error")
    elif args.option=='set_temp':
        if args.temperature is not None:
            try:
                set_temp(args.temperature)
            except:
                pass
