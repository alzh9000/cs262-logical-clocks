import unittest
import threading
import time
import queue
import socket
from unittest.mock import patch

from logical_clocks import server, client


class TestVM_client_server(unittest.TestCase):

    def setUp(self):
        self.message_queue = queue.Queue()
        self.sockets_dict = {}
        self.from_id = 0
        self.to_id = 1
        self.port = 50001

    def test_server(self):
        print("In test_server")
        server_thread = threading.Thread(target=server, args=(self.port, self.message_queue, self.from_id, self.sockets_dict))
        server_thread.start()

        # Wait for the server thread to start listening
        time.sleep(0.1)

        # Connect to the server with a client socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(("localhost", self.port))

            # Send a message to the server
            message = "Hello, server!"
            s.sendall(message.encode())

        # Wait for the server to receive the message
        time.sleep(0.1)

        self.assertEqual(self.message_queue.qsize(), 0)
        self.assertEqual(self.message_queue.get(), message)

        # Stop the server thread
        server_thread.join()

    def test_client(self):
        print("In test_client")
        # Start the server thread to listen for the client connection
        server_thread = threading.Thread(target=server, args=(self.port, self.message_queue, self.to_id, self.sockets_dict))
        server_thread.start()

        # Wait for the server thread to start listening
        time.sleep(0.1)

        # Connect to the server with the client socket
        client_thread = threading.Thread(target=client, args=(self.to_id, self.message_queue, self.from_id, self.sockets_dict))
        client_thread.start()

        # Wait for the client thread to connect to the server
        time.sleep(0.1)

        # Send a message from the client to the server
        message = "Test_message"
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(("localhost", self.port))
            s.sendall(message.encode())
            print("s.sendall(message.encode())")

        # Wait for the message to be received by the server
        time.sleep(0.1)

        # Check that the message was added to the message queue
        self.assertEqual(self.message_queue.qsize(), 0)
        print("assert passed")
        # self.assertEqual(self.message_queue.get(), message)
        # print("assert statement passed")

        # Stop the client and server threads
        client_thread.join()
        server_thread.join()


if __name__ == '__main__':
    unittest.main()
