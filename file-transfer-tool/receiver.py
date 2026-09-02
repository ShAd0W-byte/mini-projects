import socket
import netifaces
import time


def revcFile(nooffiles):
    print("Available network interfaces:")
    interfaces = netifaces.interfaces()
    for interface in interfaces:
        print(interface)
    interface = input("\nEnter the interface you are using: ")
    # Get IPv4 address
    try:
        ip = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]["addr"]
    except (KeyError, IndexError):
        print("No IPv4 address found for this interface.")
        return
    print(f"\nAsk sender to connect to IP: '{ip}' and port '4444'")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("0.0.0.0", 4444))
    s.listen()
    x, c_addr = s.accept()
    print(f"Sender connected from {c_addr}")
    time.sleep(2)

    for i in range(nooffiles):
        filename = "received_" + x.recv(1024).decode()
        x.send("ok".encode())
        filesize = int(x.recv(1024).decode())
        x.send("ok".encode())
        with open(filename, "wb") as f:
            while filesize != 0:
                filedata = x.recv(1024)
                length = len(filedata)
                filesize -= length
                f.write(filedata)
        print(f"file {filename} received")
        x.send("ok".encode())
    x.close()
    s.close()