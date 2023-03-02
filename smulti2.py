import queue
import socket
import threading
import time
import random
import os
import multiprocessing

# Define the IP address and port numbers to use for the virtual machines
IP_ADDRESS = "localhost"
PORTS = [50000, 50001, 50002]


# Define the server function to listen on the specified port
def server(port, q):
    # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a port
    host = "localhost"
    port = port
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

        # Add the message to the queue
        q.put(data)

        # Send a response to the client
        message = f"Hello, client! from {port}"
        conn.send(message.encode())

        # Close the connection
        conn.close()


# Define the client function to connect to the specified port
def client(port, q):
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
            message = f"Hello, peer! from {port}"
            s.send(message.encode())

            # Receive a message from the peer
            data = s.recv(1024).decode()
            print("Received from peer:", data)

            # Add the message to the queue
            q.put(data)

            # Close the connection
            s.close()

            # Wait for 1 second before trying again
            time.sleep(5)
        except ConnectionRefusedError:
            print("Connection refused on port", port)

            # Wait for 1 second before trying again
            time.sleep(5)


# Define a function to simulate a virtual machine
def virtual_machine(socks, id):
    # Initialize the logical clock value to 0
    logical_clock = 0

    # Try to create a log file for this virtual machine's events
    try:
        # Create a subdirectory for this virtual machine's logs if it doesn't exist already
        os.makedirs(f"svm{id}_logs", exist_ok=True)
        # Create a log file for this virtual machine in its corresponding subdirectory
        log_file = open(f"svm{id}_logs/vm{id}_log.txt", "w")
    # If there was an error creating the log file, print an error message and return
    except FileNotFoundError as e:
        print(f"File Error: {e}")
        return

    # Create a message queue to store messages from clients
    message_queue = queue.Queue()

    # Start the server thread
    server_thread = threading.Thread(
        target=server,
        args=(
            PORTS[(id) % 3],
            message_queue,
        ),
    )
    server_thread.start()

    # Start the client threads
    client1_thread = threading.Thread(
        target=client, args=(PORTS[(id + 1) % 3], message_queue)
    )
    client1_thread.start()

    client2_thread = threading.Thread(
        target=client, args=(PORTS[(id + 2) % 3], message_queue)
    )
    client2_thread.start()

    # s = socks[id % 3]
    # s.bind((IP_ADDRESS, PORTS[id % 3]))
    # print(f"VM of id {id} Listening on port", port)

    # # Listen for incoming connections
    # s.listen()

    # # Accept incoming connections and handle them
    # while True:
    #     conn, addr = s.accept()
    #     print("Accepted connection from", addr)

    #     # Receive data from the client
    #     data = conn.recv(1024).decode()
    #     print("Received from client:", data)

    #     # Add the message to the queue
    #     q.put(data)

    #     # Send a response to the client
    #     message = f"Hello, client! from {port}"
    #     conn.send(message.encode())

    #     # Close the connection
    #     conn.close()

    # # Try to connect to the other virtual machines
    # try:
    #     # Connect to the next virtual machine in the ring
    #     next_sock = socks[(id + 1) % 3]
    #     print((IP_ADDRESS, PORTS[(id + 1) % 3]))
    #     next_sock.connect((IP_ADDRESS, PORTS[(id + 1) % 3]))
    #     print(f"VM of id {id} connected to {IP_ADDRESS}:{PORTS[(id + 1) % 3]}")
    #     # Connect to the previous virtual machine in the ring
    #     prev_sock = socks[(id + 2) % 3]
    #     prev_sock.connect((IP_ADDRESS, PORTS[(id + 2) % 3]))
    #     print(f"VM of id {id} connected to {IP_ADDRESS}:{PORTS[(id + 2) % 3]}")
    #     # Send an initialization message to the next machine in the ring
    #     logical_clock = send_message(
    #         next_sock, "Initialization message", logical_clock, log_file
    #     )
    #     # Send an initialization message to the previous machine in the ring
    #     logical_clock = send_message(
    #         prev_sock, "Initialization message", logical_clock, log_file
    #     )
    # # If there was an error connecting to the other virtual machines, print an error message and return
    # except socket.error as e:
    #     print(f"Socket Error: {e}")
    #     return

    # # Main loop for the virtual machine
    # while True:
    #     # Receive messages from the next and previous virtual machines in the ring, updating the logical clock value accordingly
    #     logical_clock = receive_message(next_sock, logical_clock, log_file)
    #     logical_clock = receive_message(prev_sock, logical_clock, log_file)
    #     # Generate events and update the logical clock value based on the outcome of the events
    #     logical_clock = process_events(socks, logical_clock, log_file, id)
    #     # Wait for one second before checking for messages and generating events again
    #     time.sleep(1)


# Define a function to send a message to another virtual machine
def send_message(sock, msg, logical_clock, log_file):
    # Encode the message and send it to the other virtual machine
    sock.send(msg.encode())
    # Increment the logical clock value and write a log entry for the sent message
    logical_clock += 1
    log_file.write(
        f"Sent message {msg} at {time.time()} with logical clock {logical_clock}\n"
    )
    # Return the updated logical clock value
    return logical_clock


# Define a function to receive a message from another virtual machine
def receive_message(sock, logical_clock, log_file):
    # Try to receive a message from the other virtual machine
    try:
        # Receive the message and decode it
        msg = sock.recv(1024).decode()
        # Update the local logical clock value to be the maximum between its current value and the sender's logical clock value
        sender_clock = int(msg.split()[1])
        logical_clock = max(logical_clock, sender_clock) + 1
        # Write a log entry for the received message
        log_file.write(
            f"Received message {msg} at {time.time()} with logical clock {logical_clock}\n"
        )
    # If there was an error receiving the message, just increment the local logical clock value and write a log entry for no message being received
    except socket.error:
        logical_clock += 1
        log_file.write(
            f"No message received at {time.time()} with logical clock {logical_clock}\n"
        )
    # Return the updated logical clock value
    return logical_clock


# Define a function to generate events and update the logical clock accordingly
def process_events(socks, logical_clock, log_file, id):
    # Generate a random integer between 1 and 10 to decide what event to perform
    event = random.randint(1, 10)
    # If the event is 1, send a message to another machine with the current logical clock value
    if event == 1:
        sock = socks[(id + 1) % 3]
        logical_clock = send_message(
            sock, f"{id} {logical_clock}", logical_clock, log_file
        )
    # If the event is 2, send a message to the next machine in the ring with the current logical clock value
    elif event == 2:
        sock = socks[(id + 1) % 3]
        logical_clock = send_message(
            sock, f"{id} {logical_clock}", logical_clock, log_file
        )
    # If the event is 3, send a message to both other machines in the ring with the current logical clock value
    elif event == 3:
        sock1 = socks[(id + 1) % 3]
        sock2 = socks[(id + 2) % 3]
        logical_clock = send_message(
            sock1, f"{id} {logical_clock}", logical_clock, log_file
        )
        logical_clock = send_message(
            sock2, f"{id} {logical_clock}", logical_clock, log_file
        )
    # If the event is any other number between 4 and 10, just increment the local logical clock value and write a log entry for an internal event
    else:
        logical_clock += 1
        log_file.write(
            f"Internal event occurred at {time.time()} with logical clock {logical_clock}\n"
        )
    # Return the updated logical clock value
    return logical_clock


if __name__ == "__main__":
    # Create a list to hold the sockets for each virtual machine
    socks = []

    # # Create a socket for each virtual machine and add it to the list
    # for port in PORTS:
    #     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     # sock.bind((IP_ADDRESS, port))
    #     # sock.listen()
    #     socks.append(sock)

    # Create a process for each virtual machine
    processes = []
    for id in range(3):
        processes.append(
            multiprocessing.Process(target=virtual_machine, args=(socks, id))
        )

    # Start each process
    for process in processes:
        process.start()

    # Wait for each process to finish
    for process in processes:
        process.join()
