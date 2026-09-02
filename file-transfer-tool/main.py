import os
import sender
import receiver

def sendfilecall():
    ipOfSender=input("enter the receiver ipaddress: ")
    senderPort=int(input("enter the port number of receiver port: "))
    filenames=input("enter the absolute file path of the file you want to send, to send multiple files enter the paths one after another with the space in between:").split()
    for i in filenames:
        if os.path.exists(i):
            continue
        else:
            print(f"path file {i} does not exist")
            return
    sender.sendFile(ipOfSender,senderPort,filenames)

def recvfilecall():
    nooffiles=int(input("enter number of files you are reciving, like 1 or 2 or 3 ... file: "))
    receiver.revcFile(nooffiles)

while True:
    print("you need to be in the same network to send the files are recive")
    SendOrRecv=input("enter `S` if you want to send files or to recive enter `R` or to quit `Q`: ").lower()
    if SendOrRecv == "s":
        sendfilecall()
    elif SendOrRecv == "r":
        recvfilecall()
    elif SendOrRecv == "q":
        break
    else:
        print("enter the correct input")
