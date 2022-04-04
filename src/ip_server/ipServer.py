## Remote server to store usernames, IPs, and ports of online users
## Does not act as a centralized server for communication, only as an online users list
## Acts as the known "Bootstrap" server that every node will connect to on login
## Always use port 8000

import socket
import threading

## dictionary of format 'hostname':'ip_addr'
IP_dict = {}
## dictionary of format 'hostname': port
port_dict = {}

# listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# listener.setblocking(0)
# listener.bind('', 8000)
# listener.listen(1)

def dicts_new_entry(username:str, ip_address:str, port:int):
    if username not in IP_dict:
        IP_dict[username] = ip_address
    else:
        if IP_dict[username] != ip_address:
            IP_dict[username] = ip_address
    
    if username not in port_dict:
        port_dict[username] = port
    else:
        if port_dict[username] != port:
            port_dict[username] = port

def dicts_remove_entry(ip_address:str, port:int):
    for key,value in IP_dict.items():
        if value == ip_address:
            del IP_dict[key]

    for key,value in port_dict.items():
        if value == port:
            del port_dict[key]


## program to run in own thread to listen for new signins and signouts
def listen(listener):
    while True:
        conn, address = listener.accept()
        if address[0] and address[1]:
            username = listener.recv(1024)
            if username.decode() == "quit":
                dicts_remove_entry(address[0], address[1])
            elif username.decode() == "Get":
                send_users(address[0], address[1])
            else:
                dicts_new_entry(username.decode(), address[0], address[1])

## send string containing usernameIpPort strings separated by a space to users who request it
def send_users(ip_address:str, port:int):
    active_users = []
    for key,value in IP_dict:
        active_users.append(key+value)
    i = 0
    for key,value in port_dict:
        active_users[i] = active_users[i]+value
    
    message = ""
    for item in active_users:
        message = message+item+" "

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setblocking(0)
    sock.connect(ip_address, port)
    sock.sendall(message)
    sock.close()    

## run server containing IP + port data for active users
def run_server():
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.setblocking(0)
    listener.bind(('', 8000))
    listener.listen(1)
    
    listen_thread = threading.Thread(target=listen, args=([listener]))
    listen_thread.start()







