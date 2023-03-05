import unittest
from queue import Queue
from datetime import datetime
from logical_clocks import process_events

class TestProcessEvents(unittest.TestCase):

    def test_process_events_with_message(self):
        sockets_dict = {}
        logical_clock = 0
        log_file = open("test_log.txt", "w")
        from_id = 0
        clock_rate = 1
        message_queue = Queue()
        message_queue.put("1 10") # Add a message to the queue

        new_logical_clock = process_events(sockets_dict, logical_clock, log_file, from_id, clock_rate, message_queue)

        # Assert that the logical clock has been updated to the max value of the message's sender logical clock plus one
        self.assertEqual(new_logical_clock, 11)

        # Assert that the log file has been updated correctly
        expected_log = f"Received message 1 10 at global UTC time (gotten from the system) {datetime.utcnow().strftime('%m-%d_%H-%M-%S.%f')} with logical clock time 11. The length of the message queue remaining is 0\n"
        with open("test_log.txt", "r") as f:
            actual_log = f.read()
        self.assertEqual(actual_log, expected_log)

    def test_process_events_without_message(self):
        sockets_dict = {}
        logical_clock = 0
        log_file = open("test_log.txt", "w")
        from_id = 0
        clock_rate = 1
        message_queue = Queue()

        new_logical_clock = process_events(sockets_dict, logical_clock, log_file, from_id, clock_rate, message_queue)

        # Assert that the logical clock has been incremented by 1
        self.assertEqual(new_logical_clock, 1)

        # Assert that the log file has been updated correctly
        expected_log = f"Internal event occurred at global UTC time (gotten from the system) {datetime.utcnow().strftime('%m-%d_%H-%M-%S.%f')} with logical clock time 1.\n"
        with open("test_log.txt", "r") as f:
            actual_log = f.read()
        self.assertEqual(actual_log, expected_log)
