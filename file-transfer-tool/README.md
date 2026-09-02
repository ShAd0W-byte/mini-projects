# File Transfer Tool

A lightweight command-line file transfer tool for local networks, built with raw Python sockets. One machine acts as the **receiver** (server) and the other as the **sender** (client); files are streamed directly over a TCP connection — no external server or internet access required.

## Features

- Send one or multiple files in a single session
- Simple request/response handshake to confirm filename and file size before each transfer
- Chunked streaming (1 MB reads) to handle large files without loading them fully into memory
- Interactive network-interface picker on the receiving side, using `netifaces` to list available interfaces and IPs
- Minimal, dependency-light implementation

## Requirements

- Python 3.x
- [`netifaces`](https://pypi.org/project/netifaces/) (used by the receiver to list network interfaces)

Install the dependency with:

```bash
pip install netifaces
```

## Project structure

```
file-transfer-tool/
├── main.py       # Entry point — interactive menu (send / receive / quit)
├── sender.py     # Client-side logic for sending files
└── receiver.py   # Server-side logic for receiving files
```

## Usage

Both the sender and receiver machines must be on the same network.

Run the tool on both machines:

```bash
python main.py
```

You'll be shown a menu:

```
you need to be in the same network to send the files are recive
enter `S` if you want to send files or to recive enter `R` or to quit `Q`:
```

### Receiving files

1. Choose `R`.
2. Enter how many files you're expecting to receive.
3. Pick the network interface to listen on from the list shown.
4. The tool prints its IP address and listens on port `4444` — share this IP with the sender.
5. Incoming files are saved in the current directory, prefixed with `received_` (e.g. `received_photo.jpg`).

### Sending files

1. Choose `S`.
2. Enter the receiver's IP address and port (`4444` by default, as shown on the receiver's side).
3. Enter the absolute path(s) of the file(s) to send, separated by spaces for multiple files.
4. Each file is sent in turn, with a confirmation printed once the transfer completes.

### Example

**Receiver:**
```
enter `S` if you want to send files or to recive enter `R` or to quit `Q`: r
enter number of files you are reciving, like 1 or 2 or 3 ... file: 1
Available network interfaces:
lo
eth0
Enter the interface you are using: eth0
Ask sender to connect to IP: '192.168.1.10' and port '4444'
```

**Sender:**
```
enter `S` if you want to send files or to recive enter `R` or to quit `Q`: s
enter the receiver ipaddress: 192.168.1.10
enter the port number of receiver port: 4444
enter the absolute file path of the file you want to send, ...: /home/user/notes.txt
file notes.txt sent
```

## How it works

1. The receiver binds to `0.0.0.0:4444` on the chosen interface and waits for a connection.
2. For each file, the sender transmits the filename, waits for an `ok` acknowledgment, then sends the file size, waits for another `ok`, and finally streams the file contents in 1 MB chunks.
3. The receiver reads exactly `filesize` bytes, writes them to disk, and acknowledges completion before the next file (if any) begins.

## Limitations

- No encryption — traffic is sent in plaintext, so this is intended for trusted local networks only.
- No authentication between sender and receiver.
- No resume support if a transfer is interrupted.
- Only tested for one sender connecting to one receiver at a time.

## License

Add a license of your choice (e.g. MIT) before publishing.
