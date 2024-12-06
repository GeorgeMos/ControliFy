import socket
import select
from enum import Enum

class STATES(Enum):
    UNCONECTED = 1
    CONNECTED = 2


class udpCom:
    def __init__(self, port):
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) 
        self.UDP_IP = ""
        self.UDP_PORT = port
        self.state = STATES.UNCONECTED

    
    def setIp(self, ip):
        self.UDP_IP = ip


    def send(self, data):

        self.sock.sendto(str(data).encode(), (self.UDP_IP, self.UDP_PORT))

    def sendRaw(self, data):
        self.sock.sendto(data, (self.UDP_IP, self.UDP_PORT))

    def setTimeout(self, sec):
        self.sock.settimeout(sec)

    def recv(self):
        data = self.sock.recv(self.UDP_PORT)
        data = data.decode()
        return data
    
    def recvRaw(self):
        data = self.sock.recv(self.UDP_PORT)
        return data
    
    def close(self):
        self.sock.close()

    
