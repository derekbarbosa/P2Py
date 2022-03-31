import socket
import multithreading


def port_setup():
    port_to_send = input("Port to send to: ")
    ip_to_send = input("Ip address to send to: ")
    port_to_listen = input("Port to receive on: ")
    conn_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    conn_sock.setblocking(0)
    send_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    send_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    send_sock.setblocking(0)
    conn_sock.bind('', int(port_to_listen))
    conn_sock.listen(1)
    send_sock.connect(ip_to_send, int(port_to_send))
    return conn_sock, send_sock

def receive_messages(self, sock):
    #send messages
    while True:
        message_received = sock.recv(1024)
        if message_received == ' ':
            pass
        else:
            print(message_received.decode())


def send_messages(self, sock):
    #receive messages
    while True:
        message_to_send = input("Enter message: ").replace('b', '').encode('utf-8')
        if message_to_send == ' ':
            pass
        else:
            sock.sendall(message_to_send)
            print("Message sent!")
            q_code = str(input("Do you wish to continue (Y/N)?"))
            if q_code == "Y":
                return
            else:
                continue


if __name__ == "__main__":
    recv_sock, send_sock = port_setup()
    # set up message receiving in the background on a different thread
    receive_thread = multithreading.Thread(target=receive_messages, args=([recv_sock]))
    receive_thread.start()
    send_messages()   
    receive_thread.join()
