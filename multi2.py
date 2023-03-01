import multiprocessing
import time
import random
import os

# Define a function to send a message to a queue
def send_message(queue, msg, sender_id, logical_clock, log_file):
    # Put the message into the queue along with its sender ID and logical clock value
    queue.put((msg, sender_id, logical_clock))
    # Increment the logical clock value and write a log entry for the sent message
    logical_clock += 1
    log_file.write(
        f"Sent message {msg} from {sender_id} at {time.time()} with logical clock {logical_clock}\n"
    )
    # Return the updated logical clock value
    return logical_clock


# Define a function to receive a message from a queue
def receive_message(queue, logical_clock, log_file):
    # If the queue is not empty, get the next message from it and its sender ID and logical clock value
    if not queue.empty():
        msg, sender_id, sender_clock = queue.get()
        # Update the local logical clock to be the maximum value between its current value and the sender's logical clock value
        logical_clock = max(logical_clock, sender_clock) + 1
        # Write a log entry for the received message
        log_file.write(
            f"Received message {msg} from {sender_id} at {time.time()} with logical clock {logical_clock}\n"
        )
    # If the queue is empty, just increment the local logical clock value and write a log entry for no message being received
    else:
        logical_clock += 1
        log_file.write(
            f"No message received at {time.time()} with logical clock {logical_clock}\n"
        )
    # Return the updated logical clock value
    return logical_clock


# Define a function to generate events and update the logical clock accordingly
def process_events(queue, logical_clock, log_file, id):
    # Generate a random integer between 1 and 10 to decide what event to perform
    event = random.randint(1, 10)
    # If the event is 1, send a message to another machine with the current logical clock value
    if event == 1:
        logical_clock = send_message(queue, logical_clock, id, logical_clock, log_file)
    # If the event is 2, send a message to the next machine in the ring with the current logical clock value
    elif event == 2:
        logical_clock = send_message(
            queue, logical_clock, (id + 1) % 3, logical_clock, log_file
        )
    # If the event is 3, send a message to both other machines in the ring with the current logical clock value
    elif event == 3:
        logical_clock = send_message(
            queue, logical_clock, (id + 1) % 3, logical_clock, log_file
        )
        logical_clock = send_message(
            queue, logical_clock, (id + 2) % 3, logical_clock, log_file
        )
    # If the event is any other number between 4 and 10, just increment the local logical clock value and write a log entry for an internal event
    else:
        logical_clock += 1
        log_file.write(
            f"Internal event occurred at {time.time()} with logical clock {logical_clock}\n"
        )
    # Return the updated logical clock value
    return logical_clock


# Define a function to simulate a virtual machine
def virtual_machine(queue1, queue2, queue3, id):
    # Initialize the logical clock value to 0
    logical_clock = 0

    # Try to create a log file for this virtual machine's events
    try:
        # Create a subdirectory for this virtual machine's logs if it doesn't exist already
        os.makedirs(f"vm{id}_logs", exist_ok=True)
        # Create a log file for this virtual machine in its corresponding subdirectory
        log_file = open(f"vm{id}_logs/vm{id}_log.txt", "w")
    # If there was an error creating the log file, print an error message and return
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return

    # If this is the first machine in the ring, send initialization messages to the other two machines
    if id == 0:
        send_message(queue2, "Initialization message", id, logical_clock, log_file)
        send_message(queue3, "Initialization message", id, logical_clock, log_file)
    # If this is the second machine in the ring, send initialization messages to the first and third machines
    elif id == 1:
        send_message(queue1, "Initialization message", id, logical_clock, log_file)
        send_message(queue3, "Initialization message", id, logical_clock, log_file)
    # If this is the third machine in the ring, send initialization messages to the first and second machines
    else:
        send_message(queue1, "Initialization message", id, logical_clock, log_file)
        send_message(queue2, "Initialization message", id, logical_clock, log_file)

    # Main loop for the virtual machine
    while True:
        # Receive messages from all three queues, updating the logical clock value accordingly
        logical_clock = receive_message(queue1, logical_clock, log_file)
        logical_clock = receive_message(queue2, logical_clock, log_file)
        logical_clock = receive_message(queue3, logical_clock, log_file)
        # Generate events and update the logical clock value accordingly
        logical_clock = process_events(queue1, logical_clock, log_file, id)
        # Wait for one second before checking for messages and generating events again
        time.sleep(1)


if __name__ == "__main__":
    # Create three message queues for the three virtual machines
    queue1 = multiprocessing.Queue()
    queue2 = multiprocessing.Queue()
    queue3 = multiprocessing.Queue()

    # Create three processes to simulate the three virtual machines
    p0 = multiprocessing.Process(
        target=virtual_machine, args=(queue1, queue2, queue3, 0)
    )
    p1 = multiprocessing.Process(
        target=virtual_machine, args=(queue1, queue2, queue3, 1)
    )
    p2 = multiprocessing.Process(
        target=virtual_machine, args=(queue1, queue2, queue3, 2)
    )

    # Start the three processes
    p0.start()
    p1.start()
    p2.start()

    # Wait for all three processes to finish
    p0.join()
    p1.join()
    p2.join()

# TODO: make each process wait the correct fraction of a second based on randomization. check if we can use pipes or multiprocessing.
