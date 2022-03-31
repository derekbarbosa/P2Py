from http.client import CONTINUE
import os
import string
import time
import datetime
import pyjokes
import logging
import socket
from . import messaging

class UserData:
    def __init__(self, userName, hostIP, filedescriptor):
        self.name = userName
        self.ip = hostIP
        self.fd = filedescriptor


def tell_joke():
    logging.debug("Telling a joke")
    print(pyjokes.get_joke(language="en", category="all"))


def quit_program():
    logging.debug("Quitting program")
    print("Goodbye!")
    time.sleep(1)
    exit(1)


def chat_setup(f):
    os.system('clear')
    print("Initalizing user settings...")
    time.sleep(1)
    hostname = socket.gethostname()
    hostIP = socket.gethostbyname(hostname)

    userName = input("Before we get started, please enter a username: ").strip()
    logging.debug("Entering Infinite While Loop!")
    while not userName:
        try:
            userName = str(userName)
        except ValueError:
            logging.error("Exceuption occured. Variable %s was not a valid entry", userName)
            continue
        if userName:
            print("You entered: " + str(userName))
            break;
        else:
            print("Error, username not valid. Please enter valid username")

    user = UserData(userName=userName,hostIP=hostIP,filedescriptor=f)

    f.write("FILE CREATED: " + str(datetime.datetime.now()) + "\n")
    f.write("USER-ENTERED 'USERNAME': " + userName + "\n")
    f.write("USER HOST IP: " + hostIP + "\n")
    return user

#messaging() in message.py
def chat(user1):
    user2 = UserData()
    recv_sock, send_sock, user2.name, user2.ip= messaging.port_setup()
    user1.fd.write("REMOTE HOSTNAME: " +  user2.name + "\n")
    user1.fd.write("REMOTE IP: " + user2.ip + "\n")
    user1.fd.write("**** BEGIN CHAT LOGS **** ")

    # set up message receiving in the background on a different thread
    receive_thread = multithreading.Thread(target=messaging.receive_messages, args=([recv_sock, user2.name]))
    receive_thread.start()
    messaging.send_messages(send_sock, user1.name)   
    receive_thread.join()

def main_menu():
    os.system('clear')

    f = open("chatdata" + str(datetime.datetime.now()) + ".txt", "w+")

    print("WELCOME TO OUR CHAT ROOM")
    print("PLEASE ENJOY YOUR STAY!!")

    while True:
        print("************************")
        print("*|        MENU        |*")
        print("*|                    |*")
        print("*| 1: Connect & Chat! |*")
        print("*| 2: Save & Quit!    |*")
        print("*| 3: Tell a Joke!    |*")
        print("*|                    |*")
        print("************************")

        print("All invalid options will be ignored")
        ui = input("Please select options 1-3 using your keyboard  \n").strip()
        print("\n\n")
        try:
            ui = int(ui)
            print("You entered: " + str(ui))
        except ValueError:
            logging.error("Exceuption occured. Variable %s was not a valid entry", ui)
            continue
        if ui == 1:
            logging.debug("Succesfully broke from while loop")
            user1 = chat_setup(f)
            user2 = chat(user1)
            ##connect chat (pass fd and user obj)
            continue
        if ui == 2:
            f.close()
            quit_program()
            break
        if ui == 3:
            print("\n\n")
            tell_joke()
            print("\n\n")
            continue
        
