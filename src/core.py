from http.client import CONTINUE
import os
import time
import datetime
import pyjokes
import logging
import socket
import signal
from . import messaging


class UserData:
    def __init__(self, userName, hostIP, filedescriptor):
        self.name = userName
        self.ip = hostIP
        self.fd = filedescriptor


def tell_joke():
    logging.debug("Telling a joke")
    print(pyjokes.get_joke(language="en", category="all"))
    return


def quit_program():
    logging.debug("Quitting program")
    print("Goodbye!")
    return


def chat_setup(f):
    os.system('clear')
    print("Initalizing user settings...")
    time.sleep(1)
    hostname = socket.gethostname()
    hostIP = socket.gethostbyname(hostname)

    userName = input(
        "Before we get started, please enter a username: ").strip()
    logging.debug("Entering Infinite While Loop!")
    while not userName:
        try:
            userName = str(userName)
        except ValueError:
            logging.error(
                "Exceuption occured. Variable %s was not a valid entry", userName)
            continue
        if userName:
            print("You entered: " + str(userName))
            break
        else:
            print("Error, username not valid. Please enter valid username")

    user = UserData(userName=userName, hostIP=hostIP, filedescriptor=f)

    f.write("FILE CREATED: " + str(datetime.datetime.now()) + "\n")
    f.write("USER-ENTERED 'USERNAME': " + userName + "\n")
    f.write("USER HOST IP: " + hostIP + "\n")
    return user

# messaging() in message.py


def chat(user1):
    dudfd = 0
    tempname = input("Who are you messaging (what is their hostname)? ")
    tempIP = input("What is their IP address? ")
    user2 = UserData(tempname, tempIP, dudfd)
    user1.fd.write("REMOTE HOSTNAME: " + user2.name + "\n")
    user1.fd.write("REMOTE IP: " + user2.ip + "\n")
    user1.fd.write("**** BEGIN CHAT LOGS **** ")
    messaging.chatConnection(user1.fd, user1.name, user2.name, user2.ip)
    return user2


def main_menu():
    os.system('clear')

    f = open("chatdata" + str(datetime.datetime.now()) + ".txt", "w+")

    print("WELCOME TO OUR CHAT ROOM")
    print("SEND YOUR MESSAGES AND HAVE FUN!!")

    while True:
        print("************************")
        print("*|        MENU        |*")
        print("*|                    |*")
        print("*| 1: Connect & Chat! |*")
        print("*| 2: Save & Quit!    |*")
        print("*| 3: Tell a Joke!    |*")
        print("*|                    |*")
        print("************************")

        print("All invalid options will be ignored you donut")
        ui = input("Please select options 1-3 using your keyboard  \n").strip()
        print("\n\n")
        try:
            ui = int(ui)
            print("You entered: " + str(ui))
        except ValueError:
            logging.error(
                "Exceuption occured. Variable %s was not a valid entry", ui)
            continue
        if ui == 1:
            logging.debug("Succesfully broke from while loop")
            user1 = chat_setup(f)
            user2 = chat(user1)
            continue
        if ui == 2:
            f.close()
            quit_program()
            return
        if ui == 3:
            print("\n\n")
            tell_joke()
            print("\n\n")
            continue
    return
