import daemon
import socket

class FridgeServer:
    def __init__(self):
        self.running=False

    def get_message(self, connection):
        data_str=""
        try:
            while True:
                data=connection.recv(4)
                data_str+=data.decode('UTF-8')
                if not data or data_str.find("$end$")!=-1:
                    break
        finally: connection.close()
        return data_str.strip("$end$")

    def quit(self):
        self.running=False

    def run(self):
        self.running=True
        sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address=('localhost', 10000)
        sock.bind(server_address)
        
        sock.listen(1)

        while self.running:
            connection, client_address=sock.accept()
            message=self.get_message(connection)
            if message=='halt' or message=='quit' or message=='close':
                self.quit()

with daemon.DaemonContext():
    a=FridgeServer()
    a.run()
