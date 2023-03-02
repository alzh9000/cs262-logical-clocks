import socket
import time

# create a socket object
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
host = socket.gethostname()

port = 9999

# connection to hostname on the port.
clientsocket.connect((host, port))

while True:
    # receive the current time from the server
    data = clientsocket.recv(1024)

    # print the current time
    print("Client Received time: %s" % data.decode("ascii"))

    # get the current time
    current_time = time.ctime(time.time())

    # send the current time to the server
    clientsocket.send(current_time.encode("ascii"))

    # wait for 2 seconds
    time.sleep(2)

# close the socket
clientsocket.close()
