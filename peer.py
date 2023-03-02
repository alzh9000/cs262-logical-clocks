import argparse
import socket
import threading
import time
import queue

# Define the server function to listen on the specified port
def server(q):
    # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Set the SO_REUSEADDR option
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

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
        while True:
            data = conn.recv(1024)
            if not data:
                print("breaking connection")
                break
            print(f"Received: {data.decode()}")

            # Send a response to the client
            message = f"Hello, client! from {port}"
            conn.send(message.encode())
        # # Receive data from the client
        # data = conn.recv(1024).decode()
        # print("Received from client:", data)

        # # Add the message to the queue
        # q.put(data)

        # Send a response to the client
        message = f"Hello, client! from {port}"
        conn.send(message.encode())

        # Close the connection
        print("CLOSING CONNECTION")
        conn.close()


# Define the client function to connect to the specified port
def client(port, q):
    connected = False
    while not connected:
        # Create a socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Set the SO_REUSEADDR option
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Define the IP address to connect to
        host = "localhost"

        # Connect to the peer
        try:
            s.connect((host, port))
            connected = True
            print("Connected to", host, "on port", port)

            # Send a message to the peer
            message = f"Hello, peer! from {args.server_port}"
            s.send(message.encode())

            # Receive a message from the peer
            data = s.recv(1024).decode()
            print("Received from peer:", data)

            # Add the message to the queue
            q.put(data)

            # # Close the connection
            # s.close()

            # Wait for 1 second before trying again
            time.sleep(1)
            # s.connect((host, port))
            connected = True
            print("Connected to", host, "on port", port)

            # Send a message to the peer
            message = f"LIT LIT Hello, peer! from {args.server_port}"
            s.send(message.encode())

            # Receive a message from the peer
            data = s.recv(1024).decode()
            print("Received from peer:", data)

            # Add the message to the queue
            q.put(data)

            # Close the connection
            while True:
                message = f"LITTY Hello, peer! from {args.server_port}"
                s.send(message.encode())
                time.sleep(1)
            s.send(message.encode())
            # s.close()

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
        required=True,
    )
    parser.add_argument(
        "-p1",
        "--peer1-port",
        type=int,
        help="the port number to connect to for the first peer",
        required=True,
    )
    parser.add_argument(
        "-p2",
        "--peer2-port",
        type=int,
        help="the port number to connect to for the second peer",
        required=True,
    )
    args = parser.parse_args()

    # Create a message queue to store messages from clients
    message_queue = queue.Queue()

    # Start the server thread
    server_thread = threading.Thread(target=server, args=(message_queue,))
    server_thread.start()

    # Start the client threads
    client1_thread = threading.Thread(
        target=client, args=(args.peer1_port, message_queue)
    )
    client1_thread.start()

    client2_thread = threading.Thread(
        target=client, args=(args.peer2_port, message_queue)
    )
    client2_thread.start()
