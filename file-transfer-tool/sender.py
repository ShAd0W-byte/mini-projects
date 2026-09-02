#sender is acting as the client
import socket
import os

def sendFile(ipOfSender,senderPort,filenames):
    c=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    c.connect((ipOfSender,senderPort))
    print("connection to reciver sending data")
    for i in range(len(filenames)):
        filename=((filenames[i]).split("/"))[-1]
        filesize=os.path.getsize(filenames[i])
        c.sendall((filename).encode())
        if c.recv(1024).decode()=="ok":
            c.sendall(str(filesize).encode())
            if c.recv(1024).decode()=="ok":
                with open(filenames[i],"rb") as f:
                    while True:
                        filedata=f.read(1024*1024)
                        if not filedata:
                            break
                        c.sendall(filedata)
                if c.recv(1024).decode()=="ok":
                    pass
        print(f"file {filename} sent")
    c.close()
