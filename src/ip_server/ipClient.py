import socket

server_address = '0.0.0.0'
server_port = 8000

def login(username:str):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setblocking(0)
    sock.connect(str(server_address), int(server_port))
    sock.sendall(username)
    sock.close()
    print("Logged in: " + username)

def logout(username:str):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setblocking(0)
    sock.connect(str(server_address), int(server_port))
    message = "quit"
    sock.sendall(message)
    sock.close()
    print("Logged out: " + username)

def getActiveUsers():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setblocking(0)
    sock.connect(str(server_address), int(server_port))
    message = "Get"
    sock.sendall(message)
    sock.close()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setblocking(0)
    sock.bind(('', 8000))
    sock.listen(1)
    conn, addr = sock.accept()
    active_users = conn.recv(1024)
    sock.close()
    active_users = active_users.decode()
    userlist = active_users.split(' ')
    return userlist




