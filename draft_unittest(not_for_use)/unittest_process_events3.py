import unittest
from queue import Queue
from unittest.mock import patch, Mock
from datetime import datetime

# import the function you want to test
from logical_clocks import process_events

class TestProcessEvents(unittest.TestCase):
    def setUp(self):
        self.experiment_start_time = datetime.now().timestamp()
        self.clock_rate = 1.0

    def test_process_events(self):
        # create a message queue to store messages from other virtual machines
        message_queue = Queue()
        
        # create mock sockets dictionary
        # BUT THIS IS NOT POPULATED YET, SO CAREFUL WITH USES
        sockets_dict = {}

        # create a list of mock threads
        threads = []
        for i in range(3):
            # create a mock thread for each virtual machine
            mock_thread = Mock()
            mock_thread.start.return_value = None
            mock_thread.join.return_value = None
            threads.append(mock_thread)

        # patch the `threading.Thread` function to return the mock threads instead of starting new threads
        with patch('threading.Thread', side_effect=threads):
            process_events(sockets_dict, logical_clock = self.experiment_start_time, log_file, from_id, clock_rate = self.clock_rate, message_queue=message_queue)

        # assert that the message queue is not empty
        self.assertFalse(message_queue.empty())

        # assert that the sockets dictionary has been populated
        self.assertDictEqual(sockets_dict, {
            (0, 2): threads[0].sockets_dict.get.call_args[0][0],
            (0, 1): threads[0].sockets_dict.get.call_args[0][1],
            (1, 0): threads[1].sockets_dict.get.call_args[0][0],
            (1, 2): threads[1].sockets_dict.get.call_args[0][1],
            (2, 1): threads[2].sockets_dict.get.call_args[0][0],
            (2, 0): threads[2].sockets_dict.get.call_args[0][1],
        })

if __name__ == '__main__':
    unittest.main()
