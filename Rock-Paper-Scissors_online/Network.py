import os
import socket
import pickle

class Network:
    ''' Handles the connection between the client and the server '''
    
    def __init__(self):
        """Initialize the Network class with default configurations """
        self.session = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = os.getenv('RPS_SERVER', '127.0.0.1')
        self.port = 5555
        self.addr = (self.server, self.port)
        self.playerID = -1

    def get_playerID(self):
        """Receive and return the playerID from the server."""
        self.playerID = self.session.recv(2048).decode()
        return self.playerID  # receive playerID (1 or 2)

    def connect(self):
        """ Make connection """
        try:
            self.session.connect(self.addr)
            print('conected to', self.addr)
        except:
            print('not connected')

    def exchange_instructions(self, text):
        """ Send instructions to the server."""
        try:
            self.session.send(str.encode(text))
        except socket.error as e:
            print(e)

    def exchange_objs(self, obj):
        """ Exchange information with the server """
        try:
            self.session.send(str.encode(obj))
            return pickle.loads(self.session.recv(2048*4))
        except socket.error as e:
            print(e)

    def receive_stats(self):
        """Receive and return stats from the server."""
        return pickle.loads(self.session.recv(2048))