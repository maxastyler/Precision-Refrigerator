#!/usr/bin/env python3
import daemon
import sys
import socket
import struct
import argparse
import select
import configparser
from time import time, sleep
from helpers import *

config=configparser.SafeConfigParser()
config.read('fridge.config')

settings=ConfigSectionMap("FridgeServer", config)

FRIDGE_PORT=int(settings['port'])
MESSAGE_SIZE=int(settings['message_size'])
INITIAL_TARGET_TEMP=float(settings['initial_target_temp'])
DAEMON_DELAY=float(settings['daemon_delay']) #Time that the daemon waits for new connections to the socket
usage_string="Usage:\nstart - start/restart the daemon\n(halt/quit/close) - halt the daemon"
SIM_DELAY=0.5 #A simulated delay in reading the peltier

def send_message(message, port=FRIDGE_PORT):
    sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address=('', port)
    try:
        sock.connect(server_address)
    except:
        sock.close()
        return -1
    try:
        sock.sendall('{}'.format(message).encode())
    finally:
        sock.close()
        return 0

class FridgeServer:
    def __init__(self):
        self.running=False
        self.current_temp=0
        self.target_temp=args.target_temp

    def get_message(self, connection):
        try:
            data=connection.recv(MESSAGE_SIZE)
            if args.verbose: print("Reading data from {}".format(connection))
            return data
        except:
            return "err"

    def quit(self):
        self.running=False

    def run(self):
        self.running=True
        sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_address=('', FRIDGE_PORT)
        try:
            sock.bind(server_address)
            
            sock.listen(4)
            if args.verbose: print("Socket listening on {}".format(FRIDGE_PORT))
            read_list=[sock]

            while self.running:
                readable, writable, errored = select.select(read_list, [], [],DAEMON_DELAY)
                for s in readable:
                    if s is sock:
                        message=""
                        connection, client_address=sock.accept()
                        if args.verbose: print("Connection from {}".format(client_address))
                        read_list.append(connection)
                    else:
                        try:
                            data=self.get_message(s)
                            try:
                                message=data.decode('UTF-8')
                            except (UnicodeDecodeError, AttributeError) as e:
                                message="temp"
                            if message=='stop':
                                if args.verbose: print("Shutting down server")
                                self.quit()
                            elif message=='gct':
                                s.sendall(struct.pack('f', self.current_temp))
                            elif message=='gtt':
                                s.sendall(struct.pack('f', self.target_temp))
                            else:
                                try:
                                    new_temp=struct.unpack('f', data)[0]
                                except struct.error:
                                    if args.verbose: print("Struct error. Setting the new temperature to 0")
                                    new_temp=0
                                if args.verbose: print("Setting new temperature {}".format(new_temp))
                                self.target_temp=new_temp
                        finally:
                            s.close()
                            read_list.remove(s)
                self.update_peltier()
        except OSError as e:
            if args.verbose: print("Error: {}\nTry restarting the daemon".format(e))    
        finally:
            if args.verbose: print("Closing socket")
            sock.close()

    def update_peltier(self):
        cur_tar_temp=self.target_temp
        try:
            sock=socket.create_connection(('localhost', 10001))
            sock.sendall("gct".encode())
            self.current_temp=struct.unpack('f', sock.recv(MESSAGE_SIZE))[0]
        except:
            pass
        finally:
            try:
                sock.close()
            except: 
                pass
        try:
            sock=socket.create_connection(('localhost', 10001))
            sock.sendall("gtt".encode())
            cur_tar_temp=struct.unpack('f', sock.recv(MESSAGE_SIZE))[0]
        except:
            pass
        finally:
            try:
                sock.close()
            except:
                pass
        if self.target_temp!=cur_tar_temp:
            try:
                sock2=socket.create_connection(('localhost', 10001))
                sock2.sendall(struct.pack('f', self.target_temp))
            except:
                pass
            finally:
                try:
                    sock2.close()
                except:
                    pass    
        sleep(SIM_DELAY)

    def daemonise():
        if args.verbose: print("Daemonising")
        with daemon.DaemonContext():
            a=FridgeServer()
            a.run()


if __name__=='__main__':
    parser=argparse.ArgumentParser(description='Daemon to control Refrigerator')
    parser.add_argument('option', choices=['start', 'restart', 'stop'], help='Option to give the daemon')
    parser.add_argument('--no-daemon', '-nd', action='store_true', help='Flag given when starting to keep the process in the terminal. No forking')
    parser.add_argument('--verbose', '-v', action='store_true', help='Option to make the daemon print out what it\'s doing')
    parser.add_argument('--target-temp', '-t', type=float, default=INITIAL_TARGET_TEMP, help='Set the initial target temp for the daemon')
    parser.add_argument('--port', '-p', type=int, default=FRIDGE_PORT, help='Set the port for the server to run on')
    args=parser.parse_args()
    FRIDGE_PORT=args.port
    if args.option=="start":
        if not args.no_daemon:
            FridgeServer.daemonise()
        else:
            a=FridgeServer()
            a.run()
    elif args.option=="stop":
        send_message("stop", FRIDGE_PORT)
    elif args.option=="restart":
        send_message("stop", FRIDGE_PORT)
        sleep(2)
        if not args.no_daemon:
            FridgeServer.daemonise()
        else:
            a=FridgeServer()
            a.run()
