#!/usr/bin/env python3
import daemon
import sys
import socket
import struct
import argparse

FRIDGE_PORT=10000
MESSAGE_SIZE=16
INITIAL_TARGET_TEMP=10
usage_string="Usage:\nstart - start/restart the daemon\n(halt/quit/close) - halt the daemon"

def send_message(message):
    sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address=('localhost', FRIDGE_PORT)
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
        self.target_temp=INITIAL_TARGET_TEMP

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
        server_address=('localhost', FRIDGE_PORT)
        try:
            sock.bind(server_address)
            
            sock.listen(4)

            while self.running:
                message=""
                connection, client_address=sock.accept()
                try:
                    data=self.get_message(connection)
                    try:
                        message=data.decode('UTF-8')
                    except (UnicodeDecodeError, AttributeError) as e:
                        message="temp"
                    if message=='stop':
                        self.quit()
                    elif message=='gct':
                        connection.sendall(struct.pack('f', self.current_temp))
                    elif message=='gtt':
                        connection.sendall(struct.pack('f', self.target_temp))
                    else:
                        self.target_temp=struct.unpack('f', data)[0]
                finally:
                    connection.close()
        finally:
            sock.close()

    def daemonise():
        with daemon.DaemonContext():
            a=FridgeServer()
            a.run()

if __name__=='__main__':
    parser=argparse.ArgumentParser(description='Daemon to control Refrigerator')
    parser.add_argument('option', choices=['start', 'stop'], help='Option to give the daemon. Can be start or stop')
    parser.add_argument('--no-daemon', '-nd', action='store_true', help='Flag given when starting to keep the process in the terminal. No forking')
    args=parser.parse_args()
    if args.option=="start":
        if not args.no_daemon:
            FridgeServer.daemonise()
        else:
            a=FridgeServer()
            a.run()
    elif args.option=="stop":
        send_message("stop")
