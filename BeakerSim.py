#!/usr/bin/env python3
import daemon
import sys
import socket
import struct
import argparse
import select
from time import time

BEAKER_PORT=10001
MESSAGE_SIZE=16
usage_string="Usage:\nstart - start/restart the daemon\n(halt/quit/close) - halt the daemon"

def send_message(message):
    sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address=('localhost', BEAKER_PORT)
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

class BeakerSim:
    def __init__(self):
        self.running=False
        self.current_temp=20
        self.target_temp=10
        self.mass=1
        self.heat_cap=10
        self.efficiency=0.2
        self.power=1

    def get_message(self, connection):
        try:
            data=connection.recv(MESSAGE_SIZE)
            return data
        except:
            return "err"

    def quit(self):
        self.running=False

    def run(self):
        self.running=True
        sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_address=('localhost', BEAKER_PORT)
        try:
            sock.bind(server_address)
            sock.listen(4)
            read_list=[sock]
            

            while self.running:

                time_start=time()
                ######## Do socket reading
                readable, writable, errored = select.select(read_list, [], [],0.1)
                for s in readable:
                    if s is sock:
                        message=""
                        connection, client_address=sock.accept()
                        read_list.append(connection)
                    else:
                        try:
                            data=self.get_message(s)
                            try:
                                message=data.decode('UTF-8')
                            except (UnicodeDecodeError, AttributeError) as e:
                                message="temp"
                            if message=='stop':
                                self.quit()
                            elif message=='gct':
                                s.sendall(struct.pack('f', self.current_temp))
                            elif message=='gtt':
                                s.sendall(struct.pack('f', self.target_temp))
                            else:
                                new_temp=struct.unpack('f', data)[0]
                                self.target_temp=new_temp
                        finally:
                            s.close()
                            read_list.remove(s)

                time_taken=time()-time_start
                self.current_temp+=(self.target_temp-self.current_temp)*time_taken/self.heat_cap
        finally:
            sock.close()

    def daemonise():
        with daemon.DaemonContext():
            a=BeakerSim()
            a.run()

if __name__=='__main__':
    parser=argparse.ArgumentParser(description='Daemon to Simulate Beaker being Controlled')
    parser.add_argument('option', choices=['start', 'stop'], help='Option to give the daemon. Can be start or stop')
    parser.add_argument('--no-daemon', '-nd', action='store_true', help='Flag given when starting to keep the process in the terminal. No forking')
    args=parser.parse_args()
    if args.option=="start":
        if not args.no_daemon:
            BeakerSim.daemonise()
        else:
            a=BeakerSim()
            a.run()
    elif args.option=="stop":
        send_message("stop")
