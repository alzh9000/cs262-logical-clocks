# Usage
python peer.py -s 11111 -p1 22222 -p2 33333
python peer.py -s 22222 -p1 33333 -p2 11111
python peer.py -s 33333 -p1 22222 -p2 11111

# Spec
Scale Models and Logical Clocks
Due Sunday by 11:59pm Points 20 Submitting a website url or a file upload Available after Feb 27 at 2pm
In this assignment, you and your partner will build a model of a small, asynchronous distributed system. It will run on a single machine, but you will model multiple machines running at different speeds. 
Multiple processes connecting using sockets



And you will build a logical clock for each of the model machines.

Each model machine will run at a clock rate determined during initialization. You will pick a random number between 1 and 6, and that will be the number of clock ticks per (real world) second for that machine. This means that only that many instructions can be performed by the machine during that time. Each machine will also have a network queue (which is not constrained to the n operations per second) in which it will hold incoming messages. The (virtual) machine should listen on one or more sockets for such messages.

Each of your virtual machines should connect to each of the other virtual machines so that messages can be passed between them. Doing this is part of initialization, and not constrained to happen at the speed of the internal model clocks. 
- sockets
- 3 machines


Each virtual machine should also open a file as a log. 

Finally, each machine should have a logical clock, which should be updated using the rules for logical clocks.

Once initialization is complete, each virtual machine should work according to the following specification:

On each clock cycle, if there is a message in the message queue for the machine (remember, the queue is not running at the same cycle speed) the virtual machine should take one message off the queue, update the local logical clock, and write in the log that it received a message, the global time (gotten from the system), the length of the message queue, and the logical clock time.

If there is no message in the queue, the virtual machine should generate a random number in the range of 1-10, and

Let machines be A, B, C
From A's perspective:
1, 2, 3 are same except 1: A sends to B, 2: A sends to C, 3: A sends to B and C

if the value is 1, send to one of the other machines a message that is the local logical clock time, update it’s own logical clock, and update the log with the send, the system time, and the logical clock time
if the value is 2, send to the other virtual machine a message that is the local logical clock time, update it’s own logical clock, and update the log with the send, the system time, and the logical clock time.
if the value is 3, send to both of the other virtual machines a message that is the logical clock time, update it’s own logical clock, and update the log with the send, the system time, and the logical clock time.
if the value is other than 1-3, treat the cycle as an internal event; update the local logical clock, and log the internal event, the system time, and the logical clock value.

While working on this, keep a lab notebook in which you note the design decisions you have made. Then, run the scale model at least 5 times for at least one minute each time. Examine the logs, and discuss (in the lab book) the size of the jumps in the values for the logical clocks, drift in the values of the local logical clocks in the different machines (you can get a god’s eye view because of the system time), and the impact different timings on such things as gaps in the logical clock values and length of the message queue. Observations and reflections about the model and the results of running the model are more than welcome.

Once you have run this on three virtual machines that can vary their internal times by an order of magnitude, try running it with a smaller variation in the clock cycles and a smaller probability of the event being internal. What differences do those variations make? Add these observations to your lab notebook. Play around, and see if you can find something interesting.

You may use whatever packages or support code for the construction of the model machines and for the communication between the processes. 

You will turn in both the code (or a pointer to your repo containing the code) and the lab notebook. You will also demo this, presenting your code and choices, during demo day 2.

# Plan
Initialize the virtual machines:

Pick a random number between 1 and 6 to determine the clock rate for each machine.
Open a file as a log for each machine.
Connect each machine to every other machine.
Implement the logical clock:

Each machine should have a logical clock.
Update the logical clock using the rules for logical clocks.
When a machine sends or receives a message, update the logical clock accordingly.
Implement the main loop for each machine:

On each clock cycle:
If there is a message in the queue for the machine, take one message off the queue, update the local logical clock, and write in the log that it received a message, the global time (gotten from the system), the length of the message queue, and the logical clock time.
If there is no message in the queue:
Generate a random number in the range of 1-10.
If the value is 1, send a message to one of the other machines that is the local logical clock time, update its own logical clock, and update the log with the send, the system time, and the logical clock time.
If the value is 2, send a message to the other virtual machine that is the local logical clock time, update its own logical clock, and update the log with the send, the system time, and the logical clock time.
If the value is 3, send a message to both of the other virtual machines that is the logical clock time, update its own logical clock, and update the log with the send, the system time, and the logical clock time.
If the value is other than 1-3, treat the cycle as an internal event, update the local logical clock, and log the internal event, the system time, and the logical clock value.
Run the scale model:

Run the model at least 5 times for at least one minute each time.
Examine the logs and record observations in the lab notebook.
Analyze the size of the jumps in the values for the logical clocks, drift in the values of the local logical clocks in the different machines, and the impact of different timings on gaps in the logical clock values and the length of the message queue.
Experiment with different variations:

Try running the model with a smaller variation in the clock cycles and a smaller probability of the event being internal.
Record observations in the lab notebook and analyze the differences between the variations.


Regenerate response


# About 
We developed a simple client/server chat application with the following functions:
1.    Create an account. You must supply a unique user name.
2.    List accounts (or a subset of the accounts, by text wildcard)
3.    Send a message to a recipient. If the recipient is logged in, deliver immediately; otherwise queue the message and deliver on demand. If the message is sent to someone who isn't a user, return an error message. 
4.    Deliver undelivered messages to a particular user. 
5.    Delete an account. You can only delete your own account.

More details about the specifics of each function can be found in our Engineering Notebook's Functionality section [`engineering_notebook.md#functionality`](engineering_notebook.md#functionality). 

There are two versions of our chat app: one that uses a custom wire protocol, and one that uses gRPC. The custom wire protocol app is in the root directory of this repository, and the gRPC version is in the `grpc` directory.


# Setup and Run
## Custom wire protocol
1. Edit `client.cpp` to have the IP address of the server, specifically where it says `// Please change this to the IP address of the server` near the top of the file. You need to use the IPv4 address in your server computer's settings, not the public IP address provided by https://www.whatismyip.com/ or other websites. 
   1. For MacOS, the IPv4 address is in Settings > Network > Advanced > TCP/IP. 
   2. For Windows, open Settings -> Network & Internet -> Your Wi-Fi Network. Under Properties, look for "IPv4 address" to find your local IP address. Both the client and server must be on the same network.
2. For the server computer, run `make`, then run `./server` from the root directory of this repository. 
3. For the client computer, run `make`, then run `./client` from the root directory of this repository. 
4. To disconnect the client from the server (which is how you log out of that account), press `Ctrl+C` in the client terminal. To shut down the server, press `Ctrl+C` in the server terminal.
## gRPC
1. Edit `grpc/client.cc` to have the IP address of the server, specifically where it says `// Please change this to include the IP address of the server`. You need to use the IPv4 address in your server computer's settings, not the public IP address provided by https://www.whatismyip.com/ or other websites. 
   1. For MacOS, the IPv4 address is in Settings > Network > Advanced > TCP/IP. 
   2. For Windows, open Settings -> Network & Internet -> Your Wi-Fi Network. Under Properties, look for "IPv4 address" to find your local IP address. Both the client and server must be on the same network.
2. On both the client and server computers, you need to install gRPC. Follow the instructions in the [gRPC Quick Start Guide](https://grpc.io/docs/languages/cpp/quickstart/) to install gRPC. 
3. Then, do `cd grpc` to go to the grpc directory in our project folder, then run `make` to compile the gRPC code.
4. Then, do `cd cmake/build` from the grpc directory to go to the build directory, then run `cmake ../..`.
5. Then, run `make` again in that directory (the `grpc/cmake/build` directory)
6. For the server computer, run `./server` from the `grpc/cmake/build` directory of this repository. 
7. For the client computer, run `./client` from the `grpc/cmake/build` directory of this repository. When prompted, type `n` to user the client normally rather than run the tests.
8. To disconnect the client from the server (which is how you log out of that account), press `Ctrl+C` in the client terminal. To shut down the server, press `Ctrl+C` in the server terminal.

# Documentation

Please refer to our [`engineering_notebook.md`](engineering_notebook.md) to see our explanations and documentation on high-level design, decisions we made, why we made them, and our discussion of using gRPC vs our own custom wire protocol. For example, the specifications and design discussion of our wire protocol can be found in [`engineering_notebook.md#wire-protocol-design`](engineering_notebook.md#wire-protocol-design). Our code and testing files are also well documented, with comments in each of the files. 

# Testing
We wrote a collection of unit tests that test the functionality of every operation in the Design Specification on Canvas for our server and client, for both gRPC and our custom wire protocol. We decided to write unit tests for each operation because that way we can individually test the functionality of each single operation (without different operations interfering with each other), and it is also a good way to test the functionality of the server and client as a whole.

* For our custom wire protocol: Our testing is all done in `test.cpp`. To run our tests, simply run `make test` in the root directory of the project. This will compile the tests and run them. If the tests all succeed, it will output `Tests succeeded`, otherwise the output will stop at the last test that succeeded (and error out at the first test that failed). You may see a line that looks something like `/bin/sh: line 1:  7896 Terminated: 15          ./server` - this is because the server is killed after the tests are run, and this is expected behavior. 

* For gRPC: Our testing is all done in `grpc/client.cc` (primarily at the bottom of the file, in `run_tests()`). To run our tests, simply follow the instructions in the Setup and Run section earlier, and when prompted, type 'y' to and run the tests. If the tests all succeed, it will output `All tests under client 2 succeeded` and `All tests under client 1 succeeded`, otherwise the output will stop at the first test that failed for each client.

We also personally tested our server and client by running them on two different machines on the same network, for both gRPC and our custom wire protocol. We were able to create accounts, send messages, deliver undelivered messages, list accounts, and delete accounts, all as expected. We also verified that the server and client were able to handle multiple clients at once, and that the server and client were able to handle disconnections (if the server or clients are unexpectedly killed).

<!-- 
# TODO:
You should handle one or the other side of the socket disconnecting without warning...
* ask for IP to use for server and client? or just have the reviewer edit the code. ask client for the IP address of the server -->
<!-- 
TF said we're being graded primarily on the quality of our wire protocol and how well we handle failures, illegal operations, edge cases, etc. for the wire protocol, as far as "completeness" or "correctness" of the code goes. We can assume client is not malicious, but they might do something weird (idrk what this means? we should be fine though, we have checks). We're not being graded on the UI, so that's why doesn't rlly matter if UI is ugly (messaging cuts off input). Our code should be well documented though, cuz code review grading. 

TF said for demo day, we can instruct the testers to change the IP address in the code. They don't need to input IP address at runtime. 

For Design Journal, waldo said do in chronological order, kinda like a more well explained commit history. Can be bullet points, not complete sentences or formal. Instructions for how to run/documentation is more formal and about the final version. Design journal is less formal and about the process, what u tried. 

Grading:
FYI https://canvas.harvard.edu/courses/116261/assignments/679690
Perform a (written) code review on the chat servers you were given to run. The review should examine code clarity and correctness, completeness of the documentation (both code documentation and deployment documentation), and the coverage of the unit tests. Grade on a 20 point scale, with 8 points for code correctness and clarity; 8 points for documentation correctness and clarity, and 4 points for test suite coverage.


# cs262-wire-protocols
10.250.19.239

Let’s try working backwards like Waldo said - start by building out chat app using Protobufs/gRPC, which should be easier, then build it using a wire protocol we create. 

Have a mechanism to throw an exception back to the caller? waldo said 3:06pm on 2/6

Length = total # bytes in the message 
Size = total # bytes in the data of the message

## Design
### Account 
- username
- 

## Requirements

Part 1:

For the first design exercise, you will develop a simple chat application. This will be a client/server application, with the following functions:

    Create an account. You must supply a unique user name.
    List accounts (or a subset of the accounts, by text wildcard)
    Send a message to a recipient. If the recipient is logged in, deliver immediately; otherwise queue the message and deliver on demand. If the message is sent to someone who isn't a user, return an error message
    Deliver undelivered messages to a particular user
    Delete an account. You will need to specify the semantics of what happens if you attempt to delete an account that contains undelivered message.

The purpose of this assignment is to get you to design a wire protocol. So the solution is not to go looking for a library that will do this work for you. You should use sockets and transfer buffers (of your definition) between the machines.

You will need to write a specification of the wire protocol used in the system, and then build a client and server that use that protocol. It should be possible for multiple clients to connect to the server at the same time; you can assume a single instance of the server is all that is needed at this point.  -->
<!-- 
Build this in a repo on github that you make publicly available. The repo should include a README file that gives a set of instructions on setting up the client and server so that the system can be run. Part of your grade will depend on how well the code that you provide is documented. You may write you client and server in any of (or any combination of) python, C, C++, Java, or C#. Any other language requires the explicit permission of the instructor, which you won't get. Keep a notebook for what decisions you made, and why you made them the way you did, and any interesting observations that come up along the way.

You may turn in either a link to your repository (which should then be a public repo; "public" in this case just means open to the Harvard community) or as a tar or zip archive of the final result.

Please do not include your name in the files; we will be making use of anonymous peer reviewing for this (and other) assignments. Your code will be reviewed by the students in another group; part of that review will be following your instructions to set up and test the system that you built. This review will be part of the grade that your group gets for this assignment.

Part 2:

Re-implement (or alter) the application you built in Part 1 using gRPC. Add to your notebook comparisons over the complexity of the code, any performance differences, and the size of the buffers being sent back and forth between the client and the server.  -->
