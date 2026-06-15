import socket  # provides access to the BSD socket interface for network communication

# Define the host and port the server will bind to
HOST = '127.0.0.1'  # localhost - only accessible from this machine
PORT = 65432        # port number above 1023 to avoid needing admin/root privileges

def main():
    # socket.AF_INET = use IPv4 addressing
    # socket.SOCK_STREAM = use TCP (connection-oriented, reliable)
    # 'with' ensures the socket is automatically closed when done
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        try:
            # SO_REUSEADDR lets us restart the server quickly without
            # getting "Address already in use" errors from a lingering socket
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            # Bind the socket to the host and port so it can receive connections there
            server_socket.bind((HOST, PORT))

            # Put the socket into listening mode; '1' = max queued connections
            server_socket.listen(1)
            print(f"[*] Server listening on {HOST}:{PORT}")

            # Block here until a client connects.
            # 'conn' is a new socket object for talking to that client.
            # 'addr' is the client's (ip, port) tuple.
            conn, addr = server_socket.accept()

            # 'with' on conn ensures it closes automatically when this block ends
            with conn:
                print(f"[*] Connected by {addr}")

                # Loop continuously to handle multiple messages from the client
                while True:
                    # Receive up to 1024 bytes from the client; blocks until data arrives
                    data = conn.recv(1024)

                    # An empty bytes object means the client closed the connection
                    if not data:
                        print("[*] Client disconnected")
                        break

                    # Convert received bytes into a readable string
                    message = data.decode('utf-8')
                    print(f"[*] Received: {message}")

                    # Allow the client to request a clean shutdown
                    if message.lower() == "quit":
                        print("[*] Client requested shutdown")
                        break

                    # Build a response string and send it back to the client
                    response = f"Echo: {message}"
                    conn.sendall(response.encode('utf-8'))  # encode string to bytes before sending
                    print(f"[*] Sent: {response}")

        # Catches errors like "address already in use" or invalid bind addresses
        except OSError as e:
            print(f"[!] Socket error: {e}")

        # Allows the server to be stopped cleanly with Ctrl+C
        except KeyboardInterrupt:
            print("\n[*] Server shutting down")

# Standard Python entry point check:
# ensures main() only runs when this file is executed directly, not when imported
if __name__ == "__main__":
    main()


