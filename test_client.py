import socket
import time

sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address=('localhost', 10000)
sock.connect(server_address)

try:
    sock.sendall(b'quit$end$')
finally:
    sock.close()
