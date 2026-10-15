# Network Host Discovery Tool

A Python-based network host discovery tool that uses Scapy and ARP requests to identify active IPv4 hosts on a local network. It displays discovered IP addresses, MAC addresses, and their associated vendors in a formatted terminal table.

## Features

- Accepts individual IPv4 addresses and CIDR ranges as input.
- Expands CIDR ranges into individual host IP addresses.
- Removes duplicate target IP addresses.
- Uses ARP requests to discover responding hosts on a local network.
- Extracts IP and MAC addresses from ARP responses.
- Identifies MAC address vendors using `mac-vendor-lookup`.
- Displays results in a formatted terminal table using Rich.

## Technologies Used

- Python 3
- Scapy
- `ipaddress` — Python standard library
- `mac-vendor-lookup`
- Rich

## Requirements

- Python 3
- Linux environment with an active network interface
- Root privileges or appropriate permissions to send and receive raw network packets
- A local IPv4 network accessible through the selected interface

## Installation

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd network-host-discovery-tool
```

Replace the placeholder with your repository URL.

### 2. Create and activate a virtual environment

```bash
python3 -m venv myvenv
source myvenv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Usage

Run the tool using the Python interpreter from your virtual environment:

```bash
sudo ./myvenv/bin/python3 main.py
```

### Example input

```text
Enter the IP addresses or CIDR ranges separated by spaces (e.g., 192.168.3.0/24 192.168.3.21): 192.168.1.0/24 192.168.1.5
Enter the network interface name (e.g., wlan0 or eth0): wlan0
```

### Example output

The tool displays responding hosts in a table containing their IP address, MAC address, and vendor.

| IP Address | MAC Address | Vendor |
|---|---|---|
| 192.168.1.1 | AA:BB:CC:DD:EE:01 | Example Vendor |
| 192.168.1.5 | AA:BB:CC:DD:EE:02 | Unknown |

The displayed addresses and vendors above are illustrative examples.

## How It Works

1. Accepts individual IP addresses and CIDR ranges from the user.
2. Validates the input and expands CIDR ranges into individual IPv4 host addresses.
3. Constructs Ethernet broadcast frames containing ARP requests.
4. Sends ARP requests through the selected network interface.
5. Collects matching ARP responses and extracts the responding hosts' IP and MAC addresses.
6. Looks up the MAC address vendor and displays the results in a formatted table.
