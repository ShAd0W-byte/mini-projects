"""
            MULTITHREADED NETWORK SCANNER
Target IP: 192.168.1.10

Ports/ranges: 1-1000,8080,8443

Protocol:
1. TCP
2. UDP
Select: 1

Worker threads: 20

Save results? [y/n]: y

Output filename: scan.txt
"""


import ipaddress
import socket
import threading
import queue

#checking target
def chechtarget(TargetIp):
    try:
        ipaddress.ip_address(TargetIp)
    except ValueError:
        print("invalid ip address")
        raise SystemExit()

#making port list
def checkandmakeport(PortRange):
    dummystr=list(PortRange)
    if '-' in dummystr and ',' in dummystr:
        print("invalid port range")
        raise SystemExit()
    elif '-' in dummystr:
        PortRange=PortRange.split('-')
        if len(PortRange) == 2:
            try:
                start_port=int(PortRange[0])
                end_port=int(PortRange[1])
                if start_port < end_port and start_port > 0 and end_port <= 65535:
                    for i in range(start_port,end_port+1):
                        Portlist.append(i)
                else:
                    print("invalid port range")
                    raise SystemExit()
            except ValueError:
                print("invalid port range")
                raise SystemExit()
        else:
            print("invalid port range")
            raise SystemExit()
    elif ',' in dummystr:
        PortRange=PortRange.split(',')
        for i in PortRange:
            try:
                port=int(i)
                if 0 < port <= 65535:
                    Portlist.append(port)
                else:
                    print("invalid port range")
                    raise SystemExit()
            except ValueError:
                print("invalid port range")
                raise SystemExit()
    else:
        try:
            port=int(PortRange)
            if 0 < port <= 65535:
                Portlist.append(port)
            else:
                print("invalid port range")
                raise SystemExit()
        except ValueError:
            print("invalid port range")
            raise SystemExit()

#tcp scanning
def scan_tcp_port(target_ip,port):
    try:
        with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as c:
            c.settimeout(1.5)
            c.connect((target_ip,port))
            return "open"
    except ConnectionRefusedError:
        return "closed"
    except socket.timeout:
        return "filtered/timeout"
    except OSError:
        return "filtered/timeout"

#udp scanning
def scan_udp_port(target_ip,port):
    try:
        with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as c:
            c.settimeout(1.5)
            c.sendto(b"x",(target_ip,port))
            data,address=c.recvfrom(1024)
            return "open"
    except socket.timeout:
        return "open/filtered"
    except ConnectionRefusedError:
        return "closed"
    except OSError:
        return "open/filtered"

#tcp worker function
def tcpWorkerFunction():
    while True:
        port=PortQueue.get()
        if port is None:
            PortQueue.task_done()
            break
        result=scan_tcp_port(TargetIp,port)
        with result_lock:
            scannedPort[port]=result
        PortQueue.task_done()

#udp worker function
def udpWorkerFunction():
    while True:
        port=PortQueue.get()
        if port is None:
            PortQueue.task_done()
            break
        result=scan_udp_port(TargetIp,port)
        with result_lock:
            scannedPort[port]=result
        PortQueue.task_done()

Portlist=[]
scannedPort={}
threads=[]
result_lock=threading.Lock()

TargetIp=input("Target IP (example: 192.168.1.2): ")
PortRange=input("Ports/ranges (example: 1-1000 or 22,25): ")
Protocol=input("Enter the protocol 'T' for TCP and 'U' for UDP: ").lower()

try:
    WorkerThreads=int(input("enter number of threads under 40: "))
except ValueError:
    print("invalid number of threads")
    raise SystemExit()

SaveOutput=input("Save results [y/n]: ").lower()

chechtarget(TargetIp)

if WorkerThreads < 1 or WorkerThreads > 40:
    print("number of threads must be between 1 and 40")
    raise SystemExit()

if Protocol == "t":
    fd=tcpWorkerFunction
elif Protocol == "u":
    fd=udpWorkerFunction
else:
    print("wrong protocol input")
    raise SystemExit()

if SaveOutput not in ("y","n"):
    print("wrong save option")
    raise SystemExit()

checkandmakeport(PortRange)

if not Portlist:
    print("no ports were provided")
    raise SystemExit()

#creating queue and putting ports into it
PortQueue=queue.Queue()
for i in Portlist:
    PortQueue.put(i)

#putting None for every worker to stop the workers
for i in range(WorkerThreads):
    PortQueue.put(None)

#creating threads
for i in range(WorkerThreads):
    t=threading.Thread(target=fd)
    threads.append(t)
    t.start()

#waiting for all queue tasks to finish
PortQueue.join()

#waiting for all threads to finish
for i in threads:
    i.join()

if SaveOutput == 'n':
    for i,j in sorted(scannedPort.items()):
        if j == 'open':
            print(f"{i} : {j}")
else:
    with open("scanned_ports.txt","w") as f:
        for i,j in sorted(scannedPort.items()):
            if j == 'open':
                f.write(f"{i} : {j}\n")
    print("results saved to scanned_ports.txt")