# Usage
`python logical_clocks.py` or `python3 logical_clocks.py`

You don't need to use pip to install any packages. This was originally wrote for and run on Python 3.9.13. 

After two minutes have elapsed, the simulation will stop running automatically (no more output will be printed to the terminal or logged). Press Ctrl+C to shut it down.


# About 
We fully implemented the specification on Canvas. We created a simulation of a small distributed system containing three machines with varying clock speeds, which can be set by a random seed. Each machine connects to each other in a pre-specified order and begins sending out messages randomly to both of its neighboring machines in the network randomly. 

Each clock cycle, a machine reads its pending messages from its queue (if any) and updates its logical clock based on the logical clock number it has received from  neighboring machines. If there are none pending, it randomly may either send a message to one of the machines or both or update its own logical clock internally.

See `engineering_notebook.md` for more details on the decision-making process simulation design and its results.


# Testing
[TODO: Dean, please fill this out with details on how the testing works]
