import socket               # for creating sockets and resolving hostnames
import sys                  # for exiting the program with an error code
import time                 # for adding delays between scan attempts
from datetime import datetime  # for timestamping scan output

# Dictionary mapping well-known port numbers to their typical service names
COMMON_PORTS = {21: "FTP", 22: "SSH", 80: "HTTP", 443: "HTTPS"}

def scan_port(target, port, timeout=1):
    """Attempt to connect to a single port. Return True if open, False if closed."""
    try:
        # Create a new TCP socket for this single connection attempt
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Set how long to wait before giving up on this port
            s.settimeout(timeout)

            # connect_ex() returns an error code instead of raising an exception,
            # which makes it efficient for scanning many ports in a loop.
            # 0 means the connection succeeded (port is open).
            result = s.connect_ex((target, port))
            return result == 0

    # Raised if the hostname itself can't be resolved - let caller handle this
    except socket.gaierror:
        raise

    # Catches other socket errors (e.g., network unreachable) and treats port as closed
    except OSError:
        return False

def scan_range(target, start_port, end_port, delay=0.1):
    # Print a header with the start time for documentation/screenshot purposes
    print(f"\n[*] Scan started at {datetime.now()}")
    print(f"[*] Target: {target}  Ports: {start_port}-{end_port}\n")

    # Validate the hostname can be resolved before scanning begins.
    # This avoids repeating the same DNS error for every single port.
    try:
        socket.gethostbyname(target)
    except socket.gaierror:
        print(f"[!] Error: Cannot resolve host '{target}'. Check the address.")
        return  # exit the function early since scanning is pointless here

    open_ports = []  # collect open ports to summarize at the end

    # Loop through every port in the requested range (inclusive of end_port)
    for port in range(start_port, end_port + 1):
        if scan_port(target, port):
            # Look up a friendly service name, or "unknown" if not in our dict
            service = COMMON_PORTS.get(port, "unknown")
            print(f"[+] Port {port} OPEN  ({service})")
            open_ports.append(port)
        else:
            print(f"[-] Port {port} closed")

        # Brief pause between each port check to avoid hammering the target
        # (important for being respectful to scanme.nmap.org)
        time.sleep(delay)

    # Print a footer with the end time and summary of findings
    print(f"\n[*] Scan finished at {datetime.now()}")
    print(f"[*] Open ports: {open_ports if open_ports else 'None found'}")

def main():
    print("=== Simple Port Scanner ===")

    # Get target host from the user and strip any accidental whitespace
    target = input("Enter target host (127.0.0.1 or scanme.nmap.org): ").strip()

    try:
        # Convert user input to integers; raises ValueError if not numeric
        start_port = int(input("Enter start port: "))
        end_port = int(input("Enter end port: "))

        # Validate port numbers are within the valid TCP port range (1-65535)
        if not (0 < start_port <= 65535) or not (0 < end_port <= 65535):
            raise ValueError("Ports must be between 1 and 65535")

        # Ensure the range makes logical sense
        if start_port > end_port:
            raise ValueError("Start port must be <= end port")

    # Catches non-numeric input AND the custom validation errors raised above
    except ValueError as e:
        print(f"[!] Invalid input: {e}")
        sys.exit(1)  # exit with non-zero status to indicate an error occurred

    # All validation passed - run the actual scan
    scan_range(target, start_port, end_port)

# Entry point guard - only run main() if this script is run directly
if __name__ == "__main__":
    main()