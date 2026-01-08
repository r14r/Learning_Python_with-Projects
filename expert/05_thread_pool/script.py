#!/usr/bin/env python3
"""
Thread Pool Script
Multi-threaded task executor with thread pool management.
"""

import threading
import queue
import time
from typing import Callable, Any, List
from concurrent.futures import ThreadPoolExecutor, as_completed


class SimpleThreadPool:
    """Simple thread pool implementation."""
    
    def __init__(self, num_threads: int = 4):
        """
        Initialize thread pool.
        
        Args:
            num_threads: Number of worker threads
        """
        self.num_threads = num_threads
        self.task_queue = queue.Queue()
        self.results = []
        self.threads = []
        self.stop_event = threading.Event()
    
    def worker(self):
        """Worker thread function."""
        while not self.stop_event.is_set():
            try:
                task, args, kwargs = self.task_queue.get(timeout=0.1)
                result = task(*args, **kwargs)
                self.results.append(result)
                self.task_queue.task_done()
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Error in worker: {e}")
                self.task_queue.task_done()
    
    def start(self):
        """Start worker threads."""
        for _ in range(self.num_threads):
            thread = threading.Thread(target=self.worker, daemon=True)
            thread.start()
            self.threads.append(thread)
    
    def submit(self, task: Callable, *args, **kwargs):
        """
        Submit a task to the pool.
        
        Args:
            task: Function to execute
            *args: Positional arguments
            **kwargs: Keyword arguments
        """
        self.task_queue.put((task, args, kwargs))
    
    def wait_completion(self):
        """Wait for all tasks to complete."""
        self.task_queue.join()
    
    def shutdown(self):
        """Shutdown the thread pool."""
        self.stop_event.set()
        for thread in self.threads:
            thread.join()


def process_item(item: Any, delay: float = 0.1) -> dict:
    """
    Process an item (simulated work).
    
    Args:
        item: Item to process
        delay: Processing delay
    
    Returns:
        dict: Processing result
    """
    thread_id = threading.current_thread().name
    print(f"[{thread_id}] Processing {item}")
    time.sleep(delay)
    return {
        'item': item,
        'thread': thread_id,
        'result': item * 2
    }


def parallel_map(func: Callable, items: List, max_workers: int = 4) -> List:
    """
    Apply function to items in parallel using thread pool.
    
    Args:
        func: Function to apply
        items: List of items to process
        max_workers: Maximum number of worker threads
    
    Returns:
        List: Results in order
    """
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(func, item) for item in items]
        results = [future.result() for future in futures]
    return results


def parallel_map_unordered(func: Callable, items: List, max_workers: int = 4) -> List:
    """
    Apply function to items in parallel, returning results as completed.
    
    Args:
        func: Function to apply
        items: List of items to process
        max_workers: Maximum number of worker threads
    
    Returns:
        List: Results in completion order
    """
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(func, item): item for item in items}
        
        for future in as_completed(futures):
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                print(f"Task raised exception: {e}")
    
    return results


class ThreadSafeCounter:
    """Thread-safe counter using locks."""
    
    def __init__(self):
        """Initialize counter."""
        self.value = 0
        self.lock = threading.Lock()
    
    def increment(self):
        """Increment counter safely."""
        with self.lock:
            self.value += 1
    
    def get_value(self):
        """Get current value."""
        with self.lock:
            return self.value


def main():
    """Main function to demonstrate thread pool."""
    print("Thread Pool Demo")
    
    # Simple thread pool
    print("\n1. Simple Thread Pool:")
    pool = SimpleThreadPool(num_threads=3)
    pool.start()
    
    for i in range(6):
        pool.submit(process_item, i, 0.1)
    
    pool.wait_completion()
    print(f"  Completed {len(pool.results)} tasks")
    pool.shutdown()
    
    # Using ThreadPoolExecutor with ordered results
    print("\n2. ThreadPoolExecutor (Ordered):")
    items = list(range(5))
    start = time.time()
    results = parallel_map(lambda x: process_item(x, 0.2), items, max_workers=3)
    elapsed = time.time() - start
    print(f"  Processed {len(results)} items in {elapsed:.2f}s")
    
    # Using ThreadPoolExecutor with unordered results
    print("\n3. ThreadPoolExecutor (As Completed):")
    items = [1, 2, 3, 4, 5]
    results = parallel_map_unordered(lambda x: process_item(x, 0.1), items, max_workers=3)
    print(f"  Completed {len(results)} tasks")
    
    # Thread-safe counter
    print("\n4. Thread-Safe Counter:")
    counter = ThreadSafeCounter()
    
    def increment_many(n):
        for _ in range(n):
            counter.increment()
    
    threads = []
    for _ in range(5):
        thread = threading.Thread(target=increment_many, args=(1000,))
        thread.start()
        threads.append(thread)
    
    for thread in threads:
        thread.join()
    
    print(f"  Final counter value: {counter.get_value()} (expected: 5000)")


if __name__ == "__main__":
    main()
