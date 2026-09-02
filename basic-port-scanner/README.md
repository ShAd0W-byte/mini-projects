# Basic Port Scanner

A simple multithreaded TCP/UDP port scanner written in Python. It scans a target IP across a given set of ports or port ranges using a configurable number of worker threads, and optionally saves the results to a file.

> ⚠️ **Disclaimer:** Only scan hosts and networks you own or have explicit permission to test. Unauthorized port scanning may be illegal in your jurisdiction.

## Features

- TCP and UDP scanning modes
- Multithreaded scanning with a configurable thread pool (1–40 threads)
- Flexible port input: a single port, a range (`1-1000`), or a comma-separated list (`22,25,80`)
- Basic input validation for IP address, port range, protocol, and thread count
- Optional export of open ports to a text file

## Requirements

- Python 3.x
- No third-party dependencies (uses only the standard library: `socket`, `threading`, `queue`, `ipaddress`)

## Usage

Run the script and follow the interactive prompts:

```bash
python main.py
```

You will be asked for:

| Prompt | Example | Notes |
|---|---|---|
| Target IP | `192.168.1.10` | Must be a valid IPv4/IPv6 address |
| Ports/ranges | `1-1000` or `22,25,80` | A single port, a range, or a comma-separated list |
| Protocol | `T` or `U` | `T` for TCP, `U` for UDP |
| Worker threads | `20` | Must be between 1 and 40 |
| Save results? | `y` or `n` | Saves open ports to a file if `y` |
| Output filename | (only if saving) | File the results are written to |

### Example session

```
Target IP (example: 192.168.1.2): 192.168.1.10
Ports/ranges (example: 1-1000 or 22,25): 1-1000
Enter the protocol 'T' for TCP and 'U' for UDP: t
enter number of threads under 40: 20
Save results [y/n]: y
results saved to scanned_ports.txt
```

## How it works

1. The target IP and port list are validated.
2. Ports are pushed onto a thread-safe queue.
3. A pool of worker threads pulls ports from the queue and scans each one:
   - **TCP** — attempts a full connection; classifies the port as `open`, `closed`, or `filtered/timeout`.
   - **UDP** — sends a probe packet and classifies the port as `open`, `closed`, or `open/filtered` based on the response (or lack thereof).
4. Results are collected in a shared dictionary protected by a lock.
5. Open ports are printed to the console or written to the output file.

## Limitations

- UDP scanning results can be unreliable, since the absence of a response doesn't always mean a port is closed.
- No support for scanning multiple hosts in a single run.
- Command-line arguments aren't supported yet — all input is interactive.

## License

Add a license of your choice (e.g. MIT) before publishing.
