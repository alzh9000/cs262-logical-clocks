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
- Because of this, we needed to give a simple ordering for the VMs to connect to each other:
    - VM B listens on port X, VM A connects on X. VM C listens on port Y, VM B connects on port Y. Finally, VM A listens on port Z, and VM C connects on port Z.
- In order to get around any race conditions from one VM connecting in the wrong order (e.g., if B tries to connect to C before C starts listening), we sleep if the connection fails and try again after 100ms.

- The message queue is handled by two separate threads in each VM process, one for each open socket. 
- Since the message queue runs independently of the VM clock/logical clock, messages are read from the sockets and emplaced on the queue as soon as possible. This gives us an easy separation of concerns.
- It doesn't matter which side connnected or listened, since once a connection is established, reading/writing to a socket can be done by either side.
- The main thread in every VM handles the rest of the logic (i.e., the logical clock, clock ticks, etc.). 
- Consequently, the main thread also writes to both sockets randomly (which is fine, since sockets have two buffers internally for reading/writing respectively. Reading from a socket can be done while writing).

# Observations
- Under normal circumstances, the amount of jump in clock rate depends on whether the VM is slower than the fastest VM. Generally, we observed that the logical clock rate would change an amount equal to some power of the difference (though typically it was equal to the difference between its clock rate and the VM's). For example, the clock rate might jump by 4 if VM A has clock rate 2 and VM B has clock rate 4, though typically only by 1-2 cycles.
- Setting all machines to have the same clock rate results in very few jumps in logical clocks between machines. The highest jump observed over 5 trials was +2 logical clock cycles between messages, which makes sense (in a perfect system, we would expect that they are perfectly synced, but since the OS has o schedule each thread and has some latency in communication, some drift is expected).
- We also observe this under normal circumstances (i.e., if two machines with the same clock rate have the highest clock rate, they will not experience many jumps in logical clock time, if any, during the entire minute).
- In general, these observations held up to different clock speeds, even when the clock speeds weren't uniform (e.g. clock speeds of 3, 4, 6). Basically, the more aperiodicity in clock rates, the more variance there was in how big each gap was, but the one constant was that the larger clock speeds would experience little or no gaps, while the smallest clock speed would experience one often, especially if the gap between it and the highest clock speed was large.
- The message queue was also affected by the clock speed. As expected, the lowest clock speed was most likely to have two or more messages in its queue, with this probability increasing as the gap between it and the other VMs increased. Since the clock speed determines how often each machine sends out messages, this clearly makes sense since the lowest clock speed will process messages at a fraction of the speed that the highest clock speed machine will send them out.
- Reducing the chance of an internal event from 60% to 25% heavily increased the amount of backlogged queue messages for the slowest machine (e.g., a difference of 2 cycles of speed from the slowest to fastest VM led to five messages backlogged in the queue every cycle on average, versus 0-1 on average before).
- The slowest machine in our experiments was constantly backlogged, and appeared to be constantly behind the "true" logical clock time set by the fastest machine. Sending too many messages seems to have a negative effect on how up-to-date the slowest machine is, since it can only process one message at a time. With the maximum gap of 5 (1-6), the machine never sent out a message except at the very start, and its queue size filled up to over 300 messages.
- However, if the machine could process every message in one cycle, more messages would give it up-to-date information. Whether this models well to a real world scenario depends on whether each machine is able to process each message quickly enough (i.e. it has enough throughput). We imagine that in a fully-connected distributed system, however, it is not practical to receive that many messages (O(n^2) messages).
- A better design for a distributed system that wishes to keep up-to-date might be to have one machine keep track of time and sends the messages out to each machine, instead of every machine figuring out the logical clock time through a stream of messages. Machines can keep a separate queue for such messages and update as they see fit, instead of having to keep O(n^2) connections alive.
