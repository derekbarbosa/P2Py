from concurrent.futures import thread
import socket
import threading
import datetime

def receive_messages(chat_fd, remoteUserName):
    # send messages
    port = input("Port to bind to: ")
    recv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    recv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    recv_sock.bind(('', int(port)))
    recv_sock.listen(1)
    conn, addr = recv_sock.accept()
    while True:
        message_received = conn.recv(1024)
        if len(message_received.decode()) > 1:
            if message_received.decode() == "discon_ACK":
                return
            else:
                print("\n" + message_received.decode())
                chat_fd.write("MESSAGE RECEIVED \n" + " Username: " + message_received.decode() + " at " + str(datetime.datetime.now()) + "\n")


def send_messages(chat_fd, localUserName, remoteUserName, remote_ip):
    # send messages
    s_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    peer_port = input("Enter port of " + remoteUserName + " peer to send to: ")
    s_sock.connect((remote_ip, int(peer_port)))
    while True:
        message_to_send = input("Enter message: ").replace(
            'b', '').encode('utf-8')
        if message_to_send == ' ':
            pass
        else:
            s_sock.sendall("\n MESSAGE RECEIVED: ".encode('utf-8'))
            s_sock.sendall(bytes(localUserName + ":  ", encoding='utf8') + message_to_send)
            chat_fd.write("MESSAGE SENT: \n" + "Username: " + localUserName + message_to_send.decode() + " at " + str(datetime.datetime.now()) + "\n")
            q_code = str(input("Do you wish to continue (Y/N)?"))
            if q_code == "n" or q_code == "N" or q_code == "no" or q_code == "quit" or q_code == "exit" or q_code == "stop":
                s_sock.sendall(bytes("discon_ACK", encoding='utf8'))
                return 9999
            elif q_code == "y" or q_code == "Y" or q_code == "yes":
                continue
            else:
                print("\nplease choose a valid option, dingus\n")
                continue


def chatConnection(chatfd, localUserName, remoteUserName, remote_IP):
    receiveThread = threading.Thread(target=receive_messages,
                              args=[chatfd, remoteUserName])

    sendThread = threading.Thread(target=send_messages, args=[chatfd, localUserName, remoteUserName, remote_IP])

    receiveThread.start()
    sendThread.start()
    if sendThread.join() == 9999:
        print("Chat Disconnected! Goodbye :) ")
        receiveThread.join()
