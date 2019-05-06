import socket, json

class server:
    def __init__(self, server_address):
        self.server_address = (server_address, 8284)
    
    def liveconnection(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(self.server_address)
            s.close()
            return True
        except:
            return False
    
    class server_info:
        def __init__(self, j_str):
            self.name = j_str['param']['name']
            self.description = j_str['param']['desc']
    
    def info(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        request = {'type': 'request.server.basicinfo'}

        s.connect(self.server_address)
        s.send(bytes(str(request), 'utf-8'))

        data = json.loads(s.recv(2048).decode('utf-8'))
        return server.server_info(data)
    
    def member_count(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        request = {'type': 'request.server.onlinecount'}

        s.connect(self.server_address)
        s.send(bytes(str(request), 'utf-8'))
        
        data = json.loads(s.recv(2048).decode('utf-8'))
        return data['param']