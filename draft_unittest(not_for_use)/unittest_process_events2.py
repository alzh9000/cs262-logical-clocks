import queue
from datetime import datetime
from logical_clocks import process_events
import unittest
import time
import os

class test_process_events(unittest.TestCase):
    def test_process_events(self):
        # Initialize variables
        experiment_start_time = datetime.now().timestamp()
        clock_rate = 1
        event_queue = queue.Queue()
        message_queue = queue.Queue()
        from_id = 1
        try:
            # Create a subdirectory for this virtual machine's logs if it doesn't exist already
            os.makedirs(f"virtual_machine_{from_id}_logs", exist_ok=True)
            # Create a log file for this virtual machine in its corresponding subdirectory with useful information in the file name
            experiment_start_time_string = time.strftime(
                "%m-%d_%H-%M-%S", time.localtime(experiment_start_time)
            )
            log_file = open(
                f"virtual_machine_{from_id}_logs/vm{from_id}_{experiment_start_time_string}_clock_rate_{clock_rate}_log.txt",
                "w",
            )
        except Exception as e:
            pass

        # Add some events to the event queue
        event_queue.put((0, "event 1"))
        event_queue.put((1, "event 2"))
        event_queue.put((2, "event 3"))

        # Call the function to be tested
        process_events(sockets_dict, logical_clock, log_file, from_id, clock_rate, message_queue)
        # Check that the events have been processed and the messages have been added to the message queue
        assert message_queue.get() == "event 1"
        assert message_queue.get() == "event 2"
        assert message_queue.get() == "event 3"
