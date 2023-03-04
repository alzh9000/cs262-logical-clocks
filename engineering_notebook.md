# Engineering Notebook
# Day 1: 2-27
- Preface: We wrote our last project in C++, which was good for writing our own code but wasn't good for linking gRPC and running it, since we had to deal with cmake and incomplete/non-existent documentation.
- Although we aren't using any libraries this time, we decided to write the project in Python since Albert and Dean aren't as familiar with C++ and this is a shorter term project (much smaller code size as well)
- This day, we just got familiar with sockets in Python and sketched out exactly what it was we needed to do for the project (since some of the details weren't so clear).
- We decided to have three peers connect to each other using sockets (using a pre-defined ordering and ports), with threads designated to reading from the sockets on each VM, otherwise nothing too special. All the other details were essentially decided by the project spec, so there's not much to note there.

# Day 2: 3-1
- We reviewed the content from class about logical clocks. 
- We basically finished the server code this day. There were some issues getting the ordering to work correctly, involving a while True loop that would repeatedly attempt to connect the servers to each other if a connection failed (if, for example, one of the forked processes ran in the wrong order, this would lead to a failed connection).
- Otherwise, everything went smoothly. Compared to the first project, the details here are more well-defined, so there's less need for any rewrites. It's also all of our own code, so no need to dive into documentation beyond the pages on Python sockets and threads.

# Day 3: 3-2
- Project is officially finished, besides unit testing. For unit testing, we are mostly concerned with making sure the logical clocks work correctly and sync up.

# Design
- There are only two interesting parts of the design, involving the ordering of the VMs connections and the message queue.
- By the nature of sockets, one end needs to be listening *before* a connection is initiated, while the other side needs to connect *after* the other end has started listening.
- Because of this, we needed to give an ordering for the VMs to connect to each other. It's very simple.
- VM B listens on port X, VM A connects on X. VM C listens on port Y, VM B connects on port Y. Finally, VM A listens on port Z, and VM C connects on port Z.
- In order to get around any race conditions from one VM connecting in the wrong order (e.g., if B tries to connect to C before C starts listening), we sleep if the connection fails and try again after 100ms.

- The message queue is handled by two separate threads in each VM process, one for each open socket. 
- Since the message queue runs independently of the VM clock/logical clock, messages are read from the sockets and emplaced on the queue as soon as possible. This gives us an easy separation of concerns.
- It doesn't matter which side connnected or listened, since once a connection is established, reading/writing to a socket can be done by either side.
- The main thread in every VM handles the rest of the logic (i.e., the logical clock, clock ticks, etc.). 
- Consequently, the main thread also writes to both sockets randomly (which is fine, since sockets have two buffers internally for reading/writing respectively. Reading from a socket can be done while writing).
