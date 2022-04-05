from concurrent.futures import thread
import socket
import threading
import datetime


# def port_setup():
#     port_to_send = 9125
#     ip_to_send = input("IP of person to send to: ")
#     port_to_listen = 9124
#     recv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     recv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#     #recv_sock.setblocking(0)
#     send_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     send_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#     #send_sock.setblocking(0)
#     recv_sock.bind(('', int(port_to_listen)))
#     recv_sock.listen(1)
#     send_sock.connect((ip_to_send, int(port_to_send)))
#     return recv_sock, send_sock, ip_to_send


def receive_messages(self, chat_fd, remoteUserName):
    # send messages
    port = input("Port to bind to: ")
    recv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    recv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    recv_sock.bind(('', int(port)))
    recv_sock.listen(1)
    conn, addr = recv_sock.accept()
    print("Received connection from " + addr[0])
    while True:
        # conn, addr = recv_sock.accept()
        # print("Received connection from " + addr[0])
        message_received = conn.recv(1024)
        if message_received == ' ':
            pass
        else:
            print(addr[0] + message_received.decode())
            chat_fd.write("MESSAGE RECEIVED: " + message_received.decode() +
                          " " + str(datetime.datetime.now()) + "\n")


def send_messages(self, chat_fd, localUserName):
    # send messages
    s_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    while True:
        peer_ip = input("Enter IP of peer to send to: ")
        peer_port = input("Enter port of peer to send to: ")
        message_to_send = input("Enter message: ").replace(
            'b', '').encode('utf-8')
        if message_to_send == ' ':
            pass
        else:
            s_sock.connect((peer_ip, peer_port))
            s_sock.sendall(message_to_send + localUserName)
            print("Message sent!")
            s_sock.shutdown()
            chat_fd.write("MESSAGE SENT: " + message_to_send.decode() +
                          " " + str(datetime.datetime.now()) + "\n")
            q_code = str(input("Do you wish to continue (Y/N)?"))
            if q_code == "Y":
                return
            else:
                continue


def main():

    chatfd = open('sample.txt', 'w+')
    username = input('wats ur username')
    remoteuser = input('who u talkin 2')

    dumvar = threading.Thread(target=receive_messages,
                     args=[chatfd, remoteuser])

    dumvar2 = threading.Thread(target=send_messages, args=[chatfd, username])


    dumvar.start()
    dumvar2.start()
    


if __name__ == '__main__':
    main()
