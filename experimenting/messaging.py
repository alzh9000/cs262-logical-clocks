import socket
import threading
import time

# Define the IP address and port number for the server
SERVER_IP = "127.0.0.1"
SERVER_PORT = 5000

# Create a socket object for the client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the client to the server
client_socket.connect((SERVER_IP, SERVER_PORT))

# Define a function for sending messages to the server
def send_message():
    while True:
        message = input("Enter your message: ")
        client_socket.send(message.encode())
        time.sleep(4)


# Define a function for receiving messages from the server
def receive_message():
    while True:
        message = client_socket.recv(1024).decode()
        print(message)


# Create two threads for sending and receiving messages
send_thread = threading.Thread(target=send_message)
receive_thread = threading.Thread(target=receive_message)

# Start both threads
send_thread.start()
receive_thread.start()
