import queue
import socket
import threading
import time
import random
import os
import multiprocessing
from datetime import datetime

# Define terminal color codes
COLORS = {
    0: "\033[0;31m",  # Red
    1: "\033[0;32m",  # Green
    2: "\033[0;34m",  # Blue
}
RESET = "\033[0m"

# Define the IP address and port numbers to use for the virtual machines
IP_ADDRESS = "localhost"
PORTS = [50000, 50001, 50002]


# Define the server function to listen on the specified port
def server(port, message_queue, from_id, sockets_dict):
    # Create a socket object, our socket code is based on online documentation
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Set the SO_REUSEADDR option. It can help to avoid errors and make our code more robust, especially in situations where sockets are frequently opened and closed.
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind the socket to a port
    s.bind((IP_ADDRESS, port))
    print(COLORS[from_id] + "Listening on port", port, "" + RESET)

    # Listen for incoming connections
    s.listen()

    # Accept incoming connections and handle them
    while True:
        conn, addr = s.accept()
        print(COLORS[from_id] + "Accepted connection from", addr, "" + RESET)
        # Store the socket in the sockets dictionary with label for which virtual machines are connected so we can use it in the main thread
        sockets_dict[(from_id, (from_id - 1) % 3)] = conn

        # Receive data from the other virtual machine that connected to this virtual machine
        while True:
            data = conn.recv(1024).decode()
            if not data:
                print("breaking connection")
                break

            # Used for debugging and testing purposes. TODO: can remove later
            print(COLORS[from_id] + "Received from client:", data, "" + RESET)

            # Add the message to the message queue
            message_queue.put(data)

        # Close the connection
        conn.close()


# Connects virtual machine with from_id to the specified port for virtual machine with to_id
def client(to_id, message_queue, from_id, sockets_dict):
    port = PORTS[to_id]
    connected = False
    # Create a socket object, our socket code is based on online documentation
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Set the SO_REUSEADDR option. It can help to avoid errors and make our code more robust, especially in situations where sockets are frequently opened and closed.
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    while not connected:
        # Connect to the other virtual machine
        try:
            s.connect((IP_ADDRESS, port))
            connected = True
            # Store the socket in the sockets dictionary with label for which virtual machines are connected so we can use it in the main thread
            sockets_dict[(from_id, to_id)] = s

            # Wait before trying again
            time.sleep(0.2)

        except ConnectionRefusedError:
            print(COLORS[from_id] + "Connection refused on port", port, "" + RESET)

            # Wait before trying again
            time.sleep(0.2)

    # Receive data from the virtual machine we're connected to
    while True:
        data = s.recv(1024).decode()
        if not data:
            print("breaking connection")
            break

        # Used for debugging and testing purposes. TODO: can remove later
        print(COLORS[from_id] + "Received from client:", data, "" + RESET)

        # Add the message to the message queue
        message_queue.put(data)

    while True:
        # keep socket open
        pass


# Define a function to simulate a virtual machine
def virtual_machine(id, experiment_start_time, clock_rate):
    # Initialize the logical clock value to 0
    logical_clock = 0

    from_id = id

    # Try to create a log file for this virtual machine's events
    try:
        # Create a subdirectory for this virtual machine's logs if it doesn't exist already
        os.makedirs(f"svm{id}_logs", exist_ok=True)
        # Create a log file for this virtual machine in its corresponding subdirectory
        experiment_start_time_string = time.strftime(
            "%m-%d_%H-%M-%S", time.localtime(experiment_start_time)
        )
        log_file = open(
            f"svm{id}_logs/vm{id}_{experiment_start_time_string}_clock_rate_{clock_rate}_log.txt",
            "w",
        )
    # If there was an error creating the log file, print an error message and return
    except FileNotFoundError as e:
        print(COLORS[from_id] + f"File Error: {e}", "" + RESET)
        return

    # Create a message queue to store messages from clients
    message_queue = queue.Queue()

    # TODO: @gianni do we need to add mutexes or locks for when we're adding sockets to the dictionary in our threads? since client1 and client2 threads can both access at same time
    sockets_dict = {}

    # Start the server thread
    server_thread = threading.Thread(
        target=server,
        args=(PORTS[(id) % 3], message_queue, from_id, sockets_dict),
    )
    server_thread.start()

    # Give the servers enough time to start up
    time.sleep(2)
    # Start the client threads
    client1_thread = threading.Thread(
        target=client, args=((id + 1) % 3, message_queue, from_id, sockets_dict)
    )
    client1_thread.start()

    time.sleep(3)
    print(sockets_dict)
    s = sockets_dict[(from_id, (from_id - 1) % 3)]
    message = f"HEYY Hello, {(from_id - 1) % 3}! from {from_id}"
    print(message)
    s.send(message.encode())
    time.sleep(0.1)
    s = sockets_dict[(from_id, (from_id + 1) % 3)]
    message = f"BROOO Hello, {(from_id + 1) % 3}! from {from_id}"
    print(message)
    s.send(message.encode())

    time.sleep(2)
    print(COLORS[from_id] + str(message_queue), "" + RESET)
    # print and remove the contents of the queue
    while not message_queue.empty():
        print(COLORS[from_id] + "", message_queue.get(), "" + RESET)

    # Connect to the next virtual machine in the ring
    next_sock = sockets_dict[(from_id, (from_id + 1) % 3)]
    # Connect to the previous virtual machine in the ring
    prev_sock = sockets_dict[(from_id, (from_id - 1) % 3)]
    # Send an initialization message to the next machine in the ring
    logical_clock = send_message(
        next_sock, "Initialization message", logical_clock, log_file
    )
    # Send an initialization message to the previous machine in the ring
    logical_clock = send_message(
        prev_sock, "Initialization message", logical_clock, log_file
    )

    time.sleep(0.2)
    # print and remove the contents of the queue
    while not message_queue.empty():
        print(COLORS[from_id] + "", message_queue.get(), "" + RESET)

    # print(f"Logical clock value: {logical_clock}")

    time.sleep(0.4)
    # Main loop for the virtual machine
    # Run for 120 seconds. TODO: we could change this if we want, we're doing 120 seconds to be safe because Canvas says "run the scale model at least 5 times for at least one minute each time. "
    time_so_far = time.time() - experiment_start_time
    while time_so_far < 120:
        # On each clock cycle, perform functionality and update logical clock.
        logical_clock = process_events(
            sockets_dict, logical_clock, log_file, from_id, clock_rate, message_queue
        )

        time_so_far = time.time() - experiment_start_time
        # Used for debugging and testing purposes. TODO: can remove later
        # print(
        #     COLORS[from_id] + "",
        #     f"It has been {time_so_far} seconds so far",
        #     "" + RESET,
        # )


# Define a function to send a message to another virtual machine
def send_message(sock, msg, logical_clock, log_file):
    # Encode the message and send it to the other virtual machine
    sock.send(msg.encode())
    # update it’s own logical clock
    logical_clock += 1
    # update the log with the send, the system time, and the logical clock time
    global_time_string = datetime.utcnow().strftime("%m-%d_%H-%M-%S.%f")
    log_file.write(
        f"Sent message {msg} at global UTC time (gotten from the system) {global_time_string} with logical clock time {logical_clock}.\n"
    )
    # Return the updated logical clock value
    return logical_clock


# Define a function to generate events and update the logical clock accordingly
def process_events(
    sockets_dict, logical_clock, log_file, from_id, clock_rate, message_queue
):
    # Track how long this function takes to run so we know how long to wait before running it again to maintain the desired clock rate better
    start_time = time.time()

    # On each clock cycle, if there is a message in the message queue for the machine
    if not message_queue.empty():
        # The virtual machine should take one message off the queue
        msg = message_queue.get()
        # Update the local logical clock value to be the maximum between its current value and the sender's logical clock value
        sender_clock = int(msg.split()[1])
        logical_clock = max(logical_clock, sender_clock) + 1
        # TODO: @gianni @angelloghernan for ur analysis, it might be easier to log to a CSV or parse this text output. it's not required by spec but might be easier for you
        # Write in the log that it received a message, the global time (gotten from the system), the length of the message queue, and the logical clock time.
        global_time_string = datetime.utcnow().strftime("%m-%d_%H-%M-%S.%f")
        log_file.write(
            f"Received message {msg} at global UTC time (gotten from the system) {global_time_string} with logical clock time {logical_clock}. The length of the message queue remaining is {message_queue.qsize()}\n"
        )
    else:
        # If there is no message in the queue, the virtual machine should generate a random number in the range of 1-10
        event = random.randint(1, 10)
        # if the value is 1, send to one of the other machines a message that is the local logical clock time, update it’s own logical clock, and update the log with the send, the system time, and the logical clock time
        if event == 1:
            # Send the desired message to next machine in the loop of machines
            sock = sockets_dict[(from_id, (from_id + 1) % 3)]
            logical_clock = send_message(
                sock, f"{from_id} {logical_clock}", logical_clock, log_file
            )
        # if the value is 2, send to the other virtual machine a message that is the local logical clock time, update it’s own logical clock, and update the log with the send, the system time, and the logical clock time.
        elif event == 2:
            # Send the desired message to previous machine in the loop of machines
            sock = sockets_dict[(from_id, (from_id - 1) % 3)]
            logical_clock = send_message(
                sock, f"{from_id} {logical_clock}", logical_clock, log_file
            )
        # if the value is 3, send to both of the other virtual machines a message that is the logical clock time, update it’s own logical clock, and update the log with the send, the system time, and the logical clock time.
        elif event == 3:
            sock1 = sockets_dict[(from_id, (from_id + 1) % 3)]
            sock2 = sockets_dict[(from_id, (from_id - 1) % 3)]
            logical_clock = send_message(
                sock1, f"{from_id} {logical_clock}", logical_clock, log_file
            )
            logical_clock = send_message(
                sock2, f"{from_id} {logical_clock}", logical_clock, log_file
            )
        # if the value is other than 1-3, treat the cycle as an internal event; update the local logical clock, and log the internal event, the system time, and the logical clock value.
        else:
            logical_clock += 1
            global_time_string = datetime.utcnow().strftime("%m-%d_%H-%M-%S.%f")
            log_file.write(
                f"Internal event occurred at global UTC time (gotten from the system) {global_time_string} with logical clock time {logical_clock}.\n"
            )

    # TODO: check this works
    end_time = time.time()
    elapsed_time = end_time - start_time
    time.sleep((1 / clock_rate) - elapsed_time)

    # Return the updated logical clock value
    return logical_clock


if __name__ == "__main__":
    # Used to name the log files for this run that is consistent between the 3 processes (virtual machines)
    experiment_start_time = time.time()

    # TODO: can remove this later if want to. Keep right now for consistency when testing. Should change this when we do "run the scale model at least 5 times for at least one minute each time. " to get different results we can talk about in the report.
    random.seed(262)

    # Create a process for each virtual machine
    processes = []
    for id in range(3):
        processes.append(
            multiprocessing.Process(
                target=virtual_machine,
                args=(id, experiment_start_time, random.randint(1, 6)),
            )
        )

    # Start each process
    for process in processes:
        process.start()

    # Wait for each process to finish
    for process in processes:
        process.join()
