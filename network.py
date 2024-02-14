import socket


# client side of the network
class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = '127.0.0.1'
        self.port = 5555
        self.addr = (self.server, self.port)
        self.init_client_pos = [num for num in map(int, self.connect().split(','))]

    def get_init_client_pos(self):
        return self.init_client_pos

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            pass

    def send(self, data: bytes):
        try:
            self.client.send(data)
            return self.client.recv(4096)
        except socket.error as e:
            print(e)
