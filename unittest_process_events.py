# To run: python3 -m unittest unittest_process_events.py

import io
import queue
import unittest
import unittest.mock as mock
import time
from logical_clocks import process_events
class test_process(unittest.TestCase):
    def test_process_events_1(self):
        sockets_dict = {
            (0, 1): mock.MagicMock(),
            (1, 2): mock.MagicMock(),
            (2, 0): mock.MagicMock(),
        }
        logical_clock = 4
        log_file = io.StringIO()
        from_id = 0
        clock_rate = 1
        message_queue = queue.Queue()


        ### TEST 1
        msg = "1 3"
        message_queue.put(msg)
        
        with mock.patch("time.time", side_effect=[0, 1]):
            result = process_events(
                sockets_dict, logical_clock, log_file, from_id, clock_rate, message_queue
            )
        
        # Check the output
        expected_result = logical_clock + 1
        global_time_string = log_file.getvalue().split("(gotten from the system) ")[1].split(" with logical clock time")[0]
        expected_log_output = (
            f"Received message {msg} at global UTC time (gotten from the system) {global_time_string} with logical clock time {logical_clock + 1}. The length of the message queue remaining is 0\n"
        )
        assert result == expected_result
        print("log_file.getvalue() is", log_file.getvalue())
        print("expected_log_output is", expected_log_output)
        assert log_file.getvalue().strip("\n").strip(" ") == expected_log_output.strip("\n").strip(" ")

    def test_process_events_2(self):
        sockets_dict = {
            (0, 1): mock.MagicMock(),
            (1, 2): mock.MagicMock(),
            (2, 0): mock.MagicMock(),
        }
        logical_clock = 5
        log_file = io.StringIO()
        from_id = 0
        clock_rate = 1
        message_queue = queue.Queue()
        msg = "2 3"
        message_queue.put(msg)
        
        with mock.patch("time.time", side_effect=[0, 1]):
            result = process_events(
                sockets_dict, logical_clock, log_file, from_id, clock_rate, message_queue
            )
        
        # Check the output
        expected_result = logical_clock + 1
        global_time_string = log_file.getvalue().split("(gotten from the system) ")[1].split(" with logical clock time")[0]
        expected_log_output = (
            f"Received message {msg} at global UTC time (gotten from the system) {global_time_string} with logical clock time {logical_clock + 1}. The length of the message queue remaining is 0\n"
        )
        assert result == expected_result
        print("log_file.getvalue() is", log_file.getvalue())
        print("expected_log_output is", expected_log_output)
        assert log_file.getvalue() == expected_log_output

    def test_process_events_3(self):
        sockets_dict = {
            (0, 1): mock.MagicMock(),
            (1, 2): mock.MagicMock(),
            (2, 0): mock.MagicMock(),
        }
        logical_clock = 7
        log_file = io.StringIO()
        from_id = 1
        clock_rate = 1
        message_queue = queue.Queue()
        msg = "2 3"
        message_queue.put(msg)
        
        with mock.patch("time.time", side_effect=[0, 1]):
            result = process_events(
                sockets_dict, logical_clock, log_file, from_id, clock_rate, message_queue
            )
        
        # Check the output
        expected_result = logical_clock + 1
        global_time_string = log_file.getvalue().split("(gotten from the system) ")[1].split(" with logical clock time")[0]
        expected_log_output = (
            f"Received message {msg} at global UTC time (gotten from the system) {global_time_string} with logical clock time {logical_clock + 1}. The length of the message queue remaining is 0\n"
        )
        assert result == expected_result
        print("log_file.getvalue() is", log_file.getvalue())
        print("expected_log_output is", expected_log_output)
        assert log_file.getvalue() == expected_log_output

