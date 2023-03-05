import unittest
from unittest.mock import MagicMock
from logical_clocks import send_message

class TestSendMessage(unittest.TestCase):

    def test_send_message_updates_logical_clock_and_logs_correctly_short_message(self):
        # create a mock socket object
        sock = MagicMock()
        # create a mock log file object
        log_file = MagicMock()
        # initialize logical clock and message
        logical_clock = 0
        msg = "hello"

        # call the send_message function
        new_logical_clock = send_message(sock, msg, logical_clock, log_file)

        # assert that the socket's send method was called with the encoded message
        sock.send.assert_called_once_with(msg.encode())

        # assert that the logical clock was incremented by 1
        self.assertEqual(new_logical_clock, logical_clock + 1)
        # assert that the log file was written to with the correct message
        # global_time_string = datetime.utcnow().strftime("%m-%d_%H-%M-%S.%f")
        actual_message = log_file.write.mock_calls[0][1][0]
        global_time_string = actual_message.split("system) ")[1].split(" with logical clock time 1")[0]
        print("actual_message is", global_time_string)
        expected_log_message = f"Sent message {msg} at global UTC time (gotten from the system) {global_time_string} with logical clock time {new_logical_clock}.\n"
        log_file.write.assert_called_once_with(expected_log_message)

    def test_send_message_updates_logical_clock_and_logs_correctly_long_message(self):
        # create a mock socket object
        sock = MagicMock()
        # create a mock log file object
        log_file = MagicMock()
        # initialize logical clock and message
        logical_clock = 0
        msg = "hello"

        # call the send_message function
        new_logical_clock = send_message(sock, msg, logical_clock, log_file)

        # assert that the socket's send method was called with the encoded message
        sock.send.assert_called_once_with(msg.encode())

        # assert that the logical clock was incremented by 1
        self.assertEqual(new_logical_clock, logical_clock + 1)

        # assert that the log file was written to with the correct message
        actual_message = log_file.write.mock_calls[0][1][0]
        global_time_string = actual_message.split("system) ")[1].split(" with logical clock time 1")[0]
        print("actual_message is", global_time_string)
        expected_log_message = f"Sent message {msg} at global UTC time (gotten from the system) {global_time_string} with logical clock time {new_logical_clock}.\n"
        log_file.write.assert_called_once_with(expected_log_message)

    def test_send_message_updates_logical_clock_and_logs_correctly_clock_value(self):
        # create a mock socket object
        sock = MagicMock()
        # create a mock log file object
        log_file = MagicMock()
        # initialize logical clock and message
        logical_clock = 12312346578970
        msg = "hello"
        # call the send_message function
        new_logical_clock = send_message(sock, msg, logical_clock, log_file)

        # assert that the socket's send method was called with the encoded message
        sock.send.assert_called_once_with(msg.encode())

        # assert that the logical clock was incremented by 1
        self.assertEqual(new_logical_clock, logical_clock + 1)

        # assert that the log file was written to with the correct message
        actual_message = log_file.write.mock_calls[0][1][0]
        global_time_string = actual_message.split("system) ")[1].split(" with logical clock time 1")[0]
        print("actual_message is", global_time_string)
        expected_log_message = f"Sent message {msg} at global UTC time (gotten from the system) {global_time_string} with logical clock time {new_logical_clock}.\n"
        log_file.write.assert_called_once_with(expected_log_message)

