import socket
import multithreading
import datetime

def port_setup():
    port_to_send = 9124
    sending_hostname = input("Hostname of person to send to: ")
    ip_to_send = socket.gethostbyname(sending_hostname)
    port_to_listen = 9124
    recv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    recv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    recv_sock.setblocking(0)
    send_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    send_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    send_sock.setblocking(0)
    recv_sock.bind('', int(port_to_listen))
    recv_sock.listen(1)
    send_sock.connect(ip_to_send, int(port_to_send))
    return recv_sock, send_sock, sending_hostname, ip_to_send

def receive_messages(self, sock, chat_fd,remoteUserName):
    #send messages
    conn, addr = sock.accept()
    while True:
        message_received = conn.recv(1024)
        if message_received == ' ':
            pass
        else:
            print(remoteUserName + message_received.decode())
            chat_fd.write("MESSAGE RECEIVED: " + message_received.decode() + " " + str(datetime.datetime.now()) + "\n")


def send_messages(self, sock, chat_fd, localUserName):
    #receive messages
    while True:
        message_to_send = input("Enter message: ").replace('b', '').encode('utf-8')
        if message_to_send == ' ':
            pass
        else:
            sock.sendall(message_to_send + localUserName)
            print("Message sent!")
            chat_fd.write("MESSAGE SENT: " + message_to_send.decode() + " " + str(datetime.datetime.now()) + "\n")
            q_code = str(input("Do you wish to continue (Y/N)?"))
            if q_code == "Y":
                return
            else:
                continue

