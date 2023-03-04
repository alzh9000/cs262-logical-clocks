# Engineering Notebook
# Day 1: 2-27
- Preface: We wrote our last project in C++, which was good for writing our own code but wasn't good for linking gRPC and running it, since we had to deal with cmake and incomplete/non-existent documentation.
- Although we aren't using any libraries this time, we decided to write the project in Python since Albert and Dean aren't as familiar with C++ and this is a shorter term project (much smaller code size as well)
- This day, we just got familiar with sockets and sketched out exactly what it was we needed to do for the project (since some of the details weren't so clear).
- We decided to have three peers connect to each other using sockets (using a pre-defined ordering and ports), with threads designated to reading from the sockets on each VM, otherwise nothing too special. All the other details were essentially decided by the project spec, so there's not much to note there.

# Day 2: 3-1
- We basically finished the server code this day. There were some issues getting the ordering to work correctly, involving a while True loop that would repeatedly attempt to connect the servers to each other if a connection failed (if, for example, one of the forked processes ran in the wrong order, this would lead to a failed connection).
- Otherwise, everything went smoothly. Compared to the first project, the details here are more well-defined, so there's less need for any rewrites. It's also all of our own code, so no need to dive into documentation beyond the pages on Python sockets.

# Day 3: 3-2
- Project is officially finished, besides unit testing. Added comments for clarity; otherwise, everything is done.


