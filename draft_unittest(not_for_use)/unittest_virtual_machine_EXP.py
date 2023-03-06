import unittest
import os
import time
import threading
import queue
from datetime import datetime
from unittest.mock import MagicMock

from logical_clocks import virtual_machine, server, client

class TestVirtualMachine(unittest.TestCase):
    def test_virtual_machine(self):
        from_id = 0
        experiment_start_time = time.time()
        clock_rate = 1.0

        logical_clock = 0

        # Create mock log file
        mock_log_file = MagicMock()

        # Create message queue to test messaging
        message_queue = queue.Queue()

        # Create mock sockets dictionary
        sockets_dict = {}

        # Start the server thread
        server_thread = threading.Thread(
            target=server,
            args=(8000, message_queue, from_id, sockets_dict),
        )
        server_thread.start()

        # Give the server enough time to start up
        time.sleep(2)

        # Start the client threads
        client1_thread = threading.Thread(
            target=client, args=((from_id + 1) % 3, message_queue, from_id, sockets_dict)
        )
        client1_thread.start()

        # Wait for the virtual machines to all connect properly
        time.sleep(3)

        # Run the virtual machine
        virtual_machine(from_id, experiment_start_time, clock_rate)

        # Check that the logical clock was incremented at least once
        self.assertGreater(logical_clock, 0)

        # Check that the log file was written to at least once
        self.assertGreater(mock_log_file.write.call_count, 0)
