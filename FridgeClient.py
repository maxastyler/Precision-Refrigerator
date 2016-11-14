#!/usr/bin/env python3
import socket
import time
import struct

from FridgeServer import *

def set_temp(temp, host, port):
    returnval=None
    try:
        sock=socket.create_connection((host, port))
        sock.sendall(struct.pack('f', temp))
        sock.close()
        returnval=0
    except ConnectionRefusedError:
        returnval=-1
    finally:
        return returnval

def get_current_temp(host, port):
    return get_command('gct', host, port)

def get_target_temp(host, port):
    return get_command('gtt', host, port)

def get_command(cmd, host, port):
    cmd=cmd.encode()
    data=None
    returnval=None
    try:
        sock=socket.create_connection((host, port))
        sock.sendall(cmd)
        data=struct.unpack('f', sock.recv(MESSAGE_SIZE))[0]
        sock.close()
        returnval=0
    except ConnectionRefusedError:
        returnval=-1
    finally:
        return data, returnval

