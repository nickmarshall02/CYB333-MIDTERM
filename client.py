import socket  # provides access to the BSD socket interface for network communication

# Must match the server's host and port exactly
HOST = '127.0.0.1'
PORT = 65432

def main():
    # Create a TCP/IPv4 socket; 'with' ensures it closes automatically
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            # Set a 5-second timeout so the program doesn't hang forever
            # if the server doesn't respond (raises socket.timeout if exceeded)
            client_socket.settimeout(5)

            # Attempt to connect to the server at HOST:PORT
            # Raises ConnectionRefusedError if nothing is listening there
            client_socket.connect((HOST, PORT))
            print(f"[*] Connected to server at {HOST}:{PORT}")

            # Loop so the user can send multiple messages
            while True:
                # Prompt the user for input from the keyboard
                message = input("Enter message (or 'quit' to exit): ")

                # Encode the string to bytes and send it to the server
                client_socket.sendall(message.encode('utf-8'))

                # If user wants to quit, notify and break out without waiting for a reply
                if message.lower() == "quit":
                    print("[*] Closing connection")
                    break

                # Wait for and receive the server's response (up to 1024 bytes)
                data = client_socket.recv(1024)

                # Decode bytes back into a readable string and display it
                print(f"[*] Server response: {data.decode('utf-8')}")

        # Raised when the target port has no server listening (server not running)
        except ConnectionRefusedError:
            print("[!] Connection failed: Is the server running?")

        # Raised if connect() or recv() takes longer than the timeout
        except socket.timeout:
            print("[!] Connection timed out")

        # Catches any other socket-related errors (e.g., invalid address)
        except OSError as e:
            print(f"[!] Socket error: {e}")

# Entry point guard - only run main() if this script is run directly
if __name__ == "__main__":
    main()