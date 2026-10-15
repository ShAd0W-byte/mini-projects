from scapy.all import *
import sys
import ipaddress
from mac_vendor_lookup import MacLookup
from rich.console import Console
from rich.table import Table

class hostDiscovery():
    def __init__(self,addresslist,interface,table):
        self.addresslist=addresslist
        self.interface=interface
        self.table=table
        self.answeredhostsMapping={}
        for i in addresslist:
            self.constructARPPacket(i)
            self.sendARPPacket()
        self.findVendorAndPrint()

    def constructARPPacket(self,ipaddress):
        self.datapacket=Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ipaddress)

    def sendARPPacket(self):
        answered,unanswered=srp(self.datapacket,iface=self.interface,timeout=1,verbose=False)
        if answered:
            for sent,recived in answered:
                self.answeredhostsMapping[recived[ARP].psrc]=recived[ARP].hwsrc

    def findVendorAndPrint(self):
        for ip,mac in self.answeredhostsMapping.items():
            try:
                vendor=MacLookup().lookup(mac)
                self.table.add_row(ip,mac,vendor)
            except:
                self.table.add_row(ip,mac,"Unknown")

addresslist=[]
console=Console()
table=Table()
table.add_column("IP Address")
table.add_column("MAC Address")
table.add_column("Vendor")

inputipaddr = input("Enter the IP addresses or CIDR ranges separated by spaces (e.g., 192.168.3.0/24 192.168.3.21): ").split()
interface = input("Enter the network interface name (e.g., wlan0 or eth0): ")
print("Finding Hosts........")
for ip in inputipaddr:
    if "/" not in ip:
        try:
            address=ipaddress.ip_address(ip)
            addresslist.append(str(ip))
        except:
            print(f"invalid address: {ip}") 
            sys.exit()
    elif "/" in ip:
        try:
            ips=ipaddress.ip_network(ip,strict=False)
            for ipadd in ips.hosts():
                addresslist.append(str(ipadd))
        except:
            print(f"invalid range: {ip}")
            sys.exit()
    else:
        print("invalid input")
        sys.exit()

addresslist=list(dict.fromkeys(addresslist))
calldiscovery=hostDiscovery(addresslist,interface,table)
console.print(table)
