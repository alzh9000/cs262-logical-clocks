import random
import time
import sys
import socket

class LogicalClock:
    def __init__(self):
        self.time = 0
        
    def update(self, time):
        self.time = max(self.time, time) + 1
        
    def get_time(self):
        return self.time
        
class VirtualMachine:
    def __init__(self, id, rate, hosts):
        self.id = id
        self.rate = rate
        self.hosts = hosts
        self.clock = LogicalClock()
        self.queue = []
        self.log_file = open(f"vm{self.id}_log.txt", "w")
        self.sockets = [socket.socket(socket.AF_INET, socket.SOCK_STREAM) for _ in range(len(hosts))]
        self.init_sockets()
        
    def init_sockets(self):
        for i, host in enumerate(self.hosts):
            self.sockets[i].connect(host)
            
    def send(self, message):
        for socket in self.sockets:
            socket.send(message)
        
    def receive(self, message):
        timestamp = int(message.decode())
        self.clock.update(timestamp)
        self.log(f"Received message {message} at time {self.clock.get_time()}")
        
    def log(self, message):
        global_time = time.time()
        queue_length = len(self.queue)
        clock_time = self.clock.get_time()
        self.log_file.write(f"{message}, Global Time: {global_time}, Queue Length: {queue_length}, Clock Time: {clock_time}\n")
        
    def start(self):
        while True:
            if self.queue:
                message = self.queue.pop(0)
                self.receive(message)
            else:
                event = random.randint(1, 10)
                if event == 1:
                    # Send message to one of the other machines
                    message = str(self.clock.get_time()).encode()
                    receiver = random.choice([self.id+1, self.id+2])
                    self.send(message, receiver)
                    self.clock.update(self.clock.get_time())
                    self.log(f"Sent message {message} to {receiver} at time {self.clock.get_time()}")
                elif event == 2:
                    # Send message to other machine
                    message = str(self.clock.get_time()).encode()
                    receiver = self.id+2 if self.id==0 else self.id+1
                    self.send(message, receiver)
                    self.clock.update(self.clock.get_time())
                    self.log(f"Sent message {message} to {receiver} at time {self.clock.get_time()}")
                elif event == 3:
                    # Send message to both other machines
                    message = str(self.clock.get_time()).encode()
                    receivers = [self.id+1, self.id+2]
                    receivers.remove(self.id)
                    self.send(message, receivers)
                    self.clock.update(self.clock.get_time())
                    self.log(f"Sent message {message} to {receivers} at time {self.clock.get_time()}")
                else:
                    # Internal event
                    self.clock.update(self.clock.get_time())
                    self.log(f"Internal event at time {self.clock.get_time()}")
            
            time.sleep(1/self.rate)
            
    def send(self, message, receivers):
        if isinstance(receivers, int):
            receivers = [receivers]
        for receiver in receivers:
            self.sockets[receiver-self.id-1].send(message)
            
if __name__ == "__main__":
    # Initialize virtual machines
    # vm1 = VirtualMachine(0, random.randint(1, 6), [("localhost", 8001), ("localhost", 8002)])
    # vm2 = VirtualMachine(1, random.randint(1, 6), [("localhost", 8000), ("localhost", 8002)])
    # vm3 = VirtualMachine(2, random.randint(1, 6), [("localhost", 8000), ("localhost", 8001)])
    
    # take in a command line flag for the port number
    port = int(sys.argv[1])
    
    # Create a socket object
    s = socket.socket()
    
    # Bind to the port
    s.bind(('', port))
    
    # queue up to 5 requests
    s.listen(5)
    
    while True:
        # Establish connection with client.
        c, addr = s.accept()
    
        # Receive message from client
        message = c.recv(1024)
    
        # Close the connection with the client
        c.close()
        
        # Add message to queue
        vm1.queue.append(message)
    
    # Start virtual machines
    vm1.start()
    vm2.start()
    vm3.start()