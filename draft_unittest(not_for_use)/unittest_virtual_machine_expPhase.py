import unittest
from unittest import mock
from io import StringIO
from datetime import datetime
from logical_clocks import virtual_machine

class TestVirtualMachine(unittest.TestCase):
    @mock.patch('logical_clocks.os.makedirs')
    @mock.patch('builtins.open')
    # @mock.patch('logical_clocks.server_threading.Thread.start')
    # @mock.patch('logical_clocks.client_threading.Thread.start')
    def test_virtual_machine(self, mock_client_start, mock_server_start, mock_open, mock_makedirs):
        from_id = 0
        experiment_start_time = datetime.now().timestamp()
        clock_rate = 2
        expected_log_file_path = f"virtual_machine_{from_id}_logs/vm{from_id}_{experiment_start_time.strftime('%m-%d_%H-%M-%S')}_clock_rate_{clock_rate}_log.txt"
        
        # Mock os.makedirs to return None (i.e. no exception) when called
        mock_makedirs.return_value = None
        
        # Mock open() to return a StringIO object (in-memory file) instead of a real file object
        mock_log_file = StringIO()
        mock_open.return_value = mock_log_file
        
        # Call virtual_machine with the mock objects
        virtual_machine(from_id, experiment_start_time, clock_rate)
        # Check that os.makedirs was called with the expected path
        mock_makedirs.assert_called_once_with(f"virtual_machine_{from_id}_logs", exist_ok=True)
        
        # Check that open() was called with the expected path and mode
        mock_open.assert_called_once_with(expected_log_file_path, "w")
        
        # Check that server_threading.Thread.start() was called with the expected arguments
        mock_server_start.assert_called_once_with(
            target=mock.ANY,
            args=(mock.ANY, mock.ANY, from_id, mock.ANY),
        )
        
        # Check that client_threading.Thread.start() was called with the expected arguments
        mock_client_start.assert_called_once_with(
            target=mock.ANY,
            args=((from_id + 1) % 3, mock.ANY, from_id, mock.ANY)
        )
        mock_log_file.seek(0)
        log_content = mock_log_file.read()
        self.assertIn("Starting virtual machine", log_content)
        self.assertIn("Connected to server", log_content)
        self.assertIn("Received message", log_content)
        self.assertIn("Sending message", log_content)
