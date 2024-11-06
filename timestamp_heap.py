""" TimestampHeap """

import heapq
from typing import Any

class TimestampHeap:
    """ TimestampHeap is a structure that keeps (key, value) pairs and allows efficient:
    - retrieval of the pair with minimum value
    - update or addition of (key, value) pairs

    Example:
    - It will be used to manage the clocks' expiry time
    """
    def __init__(self):
        self.heap = []  # Min-heap to store (timestamp, key) pairs
        self.timestamps = {}  # Dictionary to store current timestamp for each key

    def add_or_update(self, key: Any, timestamp: float):
        """ Adds or updates the (key, timestamp) entry """
        # Update the dictionary with the new timestamp
        self.timestamps[key] = timestamp
        # Push the new value onto the heap
        heapq.heappush(self.heap, (timestamp, key))

    def remove_key(self, key):
        """ Removes an entry """
        # Remove the key by deleting it from the dictionary
        if key in self.timestamps:
            del self.timestamps[key]

    def pop_min(self) -> tuple[Any, float] | None:
        """ Pops and returns the minimum entry """
        # Remove and return the key with the minimum timestamp
        while self.heap:
            timestamp, key = heapq.heappop(self.heap)
            # Check if this entry is still valid (not removed/updated)
            if key in self.timestamps and self.timestamps[key] == timestamp:
                del self.timestamps[key]
                return key, timestamp
        return None  # If the heap is empty or all entries are stale

if __name__ == "__main__":
    # Example usage:
    ts_heap = TimestampHeap()
    ts_heap.add_or_update(1, 100)
    ts_heap.add_or_update(2, 50)
    ts_heap.add_or_update(3, 75)

    print(ts_heap.pop_min())  # Should return (2, 50)
    print(ts_heap.pop_min())  # Should return (3, 75)

    # Update key 1 and remove it later
    ts_heap.add_or_update(1, 30)
    print(ts_heap.pop_min())  # Should return (1, 30)
    print(ts_heap.pop_min())  # Should return (1, 30)
