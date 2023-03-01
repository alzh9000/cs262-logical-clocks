import multiprocessing
import time
import random


def send_message(queue, msg, sender_id, logical_clock, log_file):
    queue.put((msg, sender_id, logical_clock))
    logical_clock += 1
    log_file.write(
        f"Sent message {msg} from {sender_id} at {time.time()} with logical clock {logical_clock}\n"
    )
    return logical_clock


def receive_message(queue, logical_clock, log_file):
    if not queue.empty():
        msg, sender_id, sender_clock = queue.get()
        logical_clock = max(logical_clock, sender_clock) + 1
        log_file.write(
            f"Received message {msg} from {sender_id} at {time.time()} with logical clock {logical_clock}\n"
        )
    else:
        logical_clock += 1
        log_file.write(
            f"No message received at {time.time()} with logical clock {logical_clock}\n"
        )
    return logical_clock


def process_events(queue, logical_clock, log_file, id):
    event = random.randint(1, 10)
    if event == 1:
        logical_clock = send_message(queue, logical_clock, id, logical_clock, log_file)
    elif event == 2:
        logical_clock = send_message(
            queue, logical_clock, (id + 1) % 3, logical_clock, log_file
        )
    elif event == 3:
        logical_clock = send_message(
            queue, logical_clock, (id + 1) % 3, logical_clock, log_file
        )
        logical_clock = send_message(
            queue, logical_clock, (id + 2) % 3, logical_clock, log_file
        )
    else:
        logical_clock += 1
        log_file.write(
            f"Internal event occurred at {time.time()} with logical clock {logical_clock}\n"
        )
    return logical_clock


def virtual_machine(queue1, queue2, queue3, id):
    logical_clock = 0
    # Initialization phase
    try:
        log_file = open(f"vm{id}_log.txt", "w")
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return

    # Initialization phase
    if id == 0:
        send_message(queue2, "Initialization message", id, logical_clock, log_file)
        send_message(queue3, "Initialization message", id, logical_clock, log_file)
    elif id == 1:
        send_message(queue1, "Initialization message", id, logical_clock, log_file)
        send_message(queue3, "Initialization message", id, logical_clock, log_file)
    else:
        send_message(queue1, "Initialization message", id, logical_clock, log_file)
        send_message(queue2, "Initialization message", id, logical_clock, log_file)

    # Main loop
    while True:
        logical_clock = receive_message(queue1, logical_clock, log_file)
        logical_clock = receive_message(queue2, logical_clock, log_file)
        logical_clock = receive_message(queue3, logical_clock, log_file)
        logical_clock = process_events(queue1, logical_clock, log_file, id)
        time.sleep(1)


if __name__ == "__main__":
    queue1 = multiprocessing.Queue()
    queue2 = multiprocessing.Queue()
    queue3 = multiprocessing.Queue()
    p0 = multiprocessing.Process(
        target=virtual_machine, args=(queue1, queue2, queue3, 0)
    )
    p1 = multiprocessing.Process(
        target=virtual_machine, args=(queue1, queue2, queue3, 1)
    )
    p2 = multiprocessing.Process(
        target=virtual_machine, args=(queue1, queue2, queue3, 2)
    )

    p0.start()
    p1.start()
    p2.start()

    p0.join()
    p1.join()
    p2.join()
