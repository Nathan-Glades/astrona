import socket, json, string, random

server_settings = {
    "auth": {
        "req-auth": False,
        "auth-pwd": ""
    }
}

server_info = {
    "name": "Astrona Server",
    "desc": "Test server"
}

member_session = {}

server = ('', 8284)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(server)

def build(sock, response_code, response):
    response_data = {'state': response_code, 'param': response}
    send = str(response_data).replace("'", '"')
    sock.send(bytes(send, 'utf-8'))

def session_key():
    out = ''
    for i in range(32):
        out += random.choice(string.ascii_lowercase + string.ascii_uppercase)
    return out

while True:
    s.listen()
    conn, addr = s.accept()

    print('New connection from {}!'.format(addr[0]))
    data = conn.recv(2048).decode('utf-8')

    print(addr[0] + ": 2048 bytes recv")

    data = json.loads(data.replace("'", '"'))

    data_type = data['type'].split('.')

    if data_type[0] == 'request':
        # Request type
        if data_type[1] == 'server':
            # Request server
            if data_type[2] == 'basicinfo':
                # Request server basic info
                status_code = 200
                response = server_info

                build(conn, status_code, response)
                conn.close()
                print(addr[0] + ": {}, data processed. {} reponse code. Connection closed.".format(data['type'], status_code))
            if data_type[2] == 'onlinecount':
                # Members online request
                status_code = 200
                response = len(member_session)
                
                build(conn, status_code, response)
                conn.close()
                print(addr[0] + ": {}, data processed. {} reponse code. Connection closed.".format(data['type'], status_code))
        
        if data_type[1] == 'auth':
            # Authentication
            if data_type[2] == 'login':
                # Login auth
                # Check if the authentication req
                if server_settings['auth']['req-auth']: # Authentication / password is requiared
                    # Verifying username and password
                    uid = ''
                    pwd = ''
                    if 'uid' in data['param']:
                        uid = data['param']['uid']
                    if 'pwd' in data['param']:
                        pwd = data['param']['pwd']
                    
                    s_key = ''
                    status_code = 0
                    
                    if uid != '' and pwd != '': # Username and password entered
                        if pwd == server_settings['auth']['auth-pwd']: # Username correct
                            status_code = 200
                            s_key = session_key()

                            member_session[s_key] = uid
                        else:
                            status_code = 403
                    else:
                        status_code = 403
                    
                    response = {'s_key': s_key}
                    build(conn, status_code, response)
                    conn.close()
                else:
                    status_code = 200
                    s_key = session_key()
                    uid = ''
                    if 'uid' in data['param']:
                        uid = data['param']['uid']
                    
                    member_session[s_key] = uid
                    response = {'s_key': s_key}
                    build(conn, status_code, response)
                print(addr[0] + ": {}, data processed. {} reponse code. Connection closed.".format(data['type'], status_code))


    
    if data_type[0] == 'info':
        # Info type
        pass