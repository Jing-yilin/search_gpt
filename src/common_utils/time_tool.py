"""This is time_tool.py."""

import time


def tic() -> float:
    """Starts a timer."""
    global _start_time
    _start_time = time.time()
    return _start_time


def toc() -> float:
    """Stops the timer and prints the elapsed time."""
    if "_start_time" in globals():
        print("Time cost: {:.2f} seconds.".format(time.time() - _start_time))
        return time.time() - _start_time
    else:
        print("Toc: start time not set")
