#!/usr/bin/env python3
import socket
import time
import struct

from FridgeServer import *

def set_temp(temp):
    try:
        sock=socket.create_connection(('localhost', FRIDGE_PORT))
        sock.sendall(struct.pack('f', temp))
        sock.close()
        returnval=0
    except ConnectionRefusedError:
        returnval=-1
    finally:
        return returnval

def get_current_temp():
    return get_command('gct')

def get_target_temp():
    return get_command('gtt')

def get_command(cmd):
    cmd=cmd.encode()
    data=None
    try:
        sock=socket.create_connection(('localhost', FRIDGE_PORT))
        sock.sendall(cmd)
        data=struct.unpack('f', sock.recv(MESSAGE_SIZE))[0]
        sock.close()
        returnval=0
    except ConnectionRefusedError:
        returnval=-1
    finally:
        return data, returnval

