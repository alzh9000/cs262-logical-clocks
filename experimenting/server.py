import socket
import time

# create a socket object
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
host = socket.gethostname()

port = 9999

# bind the socket to a public host, and a port
serversocket.bind((host, port))

# become a server socket
serversocket.listen(1)

while True:
    # establish a connection
    clientsocket, addr = serversocket.accept()

    print("Got a connection from %s" % str(addr))

    while True:
        # get the current time
        current_time = time.ctime(time.time())

        # send the time to the client
        clientsocket.send(current_time.encode("ascii"))

        # wait for 2 seconds
        time.sleep(2)

        # receive the response from the client
        data = clientsocket.recv(1024)

        # print the response from the client
        print("Server Received message: %s" % data.decode("ascii"))

    # close the client socket
    clientsocket.close()
