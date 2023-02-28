import argparse
import socket
import threading
import time

# Define the server function to listen on the specified port
def server():
    # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a port
    host = "localhost"
    port = args.server_port
    s.bind((host, port))
    print("Listening on port", port)

    # Listen for incoming connections
    s.listen()

    # Accept incoming connections and handle them
    while True:
        conn, addr = s.accept()
        print("Accepted connection from", addr)

        # Receive data from the client
        data = conn.recv(1024).decode()
        print("Received from client:", data)

        # Send a response to the client
        message = f"Hello, client! from {port}"
        conn.send(message.encode())

        # Close the connection
        conn.close()


# Define the client function to connect to the specified port
def client(port):
    connected = False
    while not connected:
        # Create a socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Define the IP address to connect to
        host = "localhost"

        # Connect to the peer
        try:
            s.connect((host, port))
            connected = True
            print("Connected to", host, "on port", port)

            # Send a message to the peer
            message = "Hello, peer!"
            s.send(message.encode())

            # Receive a message from the peer
            data = s.recv(1024).decode()
            print("Received from peer:", data)

            # Close the connection
            s.close()

            # Wait for 1 second before trying again
            time.sleep(5)
        except ConnectionRefusedError:
            print("Connection refused on port", port)

            # Wait for 1 second before trying again
            time.sleep(5)


if __name__ == "__main__":
    # Parse the command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s",
        "--server-port",
        type=int,
        help="the port number to listen on for incoming connections",
    )
    parser.add_argument(
        "-p1",
        "--peer1-port",
        type=int,
        help="the port number to connect to for the first peer",
    )
    parser.add_argument(
        "-p2",
        "--peer2-port",
        type=int,
        help="the port number to connect to for the second peer",
    )
    args = parser.parse_args()

    # Start the server thread if server port is specified
    if args.server_port:
        server_thread = threading.Thread(target=server)
        server_thread.start()

    # Start the client threads if peer ports are specified
    if args.peer1_port:
        client1_thread = threading.Thread(target=client, args=(args.peer1_port,))
        client1_thread.start()

    if args.peer2_port:
        client2_thread = threading.Thread(target=client, args=(args.peer2_port,))
        client2_thread.start()
