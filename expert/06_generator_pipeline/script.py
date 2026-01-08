#!/usr/bin/env python3
"""
Generator Pipeline Script
Data processing pipeline using generators for memory efficiency.
"""

from typing import Iterator, Callable, Any
import time


def read_data(source: list) -> Iterator[dict]:
    """
    Generate data items from source.
    
    Args:
        source: Data source
    
    Yields:
        dict: Data items
    """
    for item in source:
        yield item


def filter_pipeline(data: Iterator, predicate: Callable) -> Iterator:
    """
    Filter data using predicate function.
    
    Args:
        data: Input data iterator
        predicate: Filter function
    
    Yields:
        Items that pass the filter
    """
    for item in data:
        if predicate(item):
            yield item


def transform_pipeline(data: Iterator, transformer: Callable) -> Iterator:
    """
    Transform data items.
    
    Args:
        data: Input data iterator
        transformer: Transformation function
    
    Yields:
        Transformed items
    """
    for item in data:
        yield transformer(item)


def batch_pipeline(data: Iterator, batch_size: int) -> Iterator[list]:
    """
    Batch data items into groups.
    
    Args:
        data: Input data iterator
        batch_size: Size of each batch
    
    Yields:
        list: Batches of items
    """
    batch = []
    for item in data:
        batch.append(item)
        if len(batch) >= batch_size:
            yield batch
            batch = []
    
    if batch:  # Yield remaining items
        yield batch


def enumerate_pipeline(data: Iterator) -> Iterator[tuple]:
    """
    Add index to items.
    
    Args:
        data: Input data iterator
    
    Yields:
        tuple: (index, item) pairs
    """
    for i, item in enumerate(data):
        yield (i, item)


def tee_pipeline(data: Iterator, n: int = 2) -> list:
    """
    Split iterator into n independent iterators.
    
    Args:
        data: Input data iterator
        n: Number of independent iterators
    
    Returns:
        list: List of independent iterators
    """
    from itertools import tee
    return list(tee(data, n))


class Pipeline:
    """Chainable pipeline for data processing."""
    
    def __init__(self, source: Iterator):
        """
        Initialize pipeline.
        
        Args:
            source: Data source iterator
        """
        self.source = source
    
    def filter(self, predicate: Callable) -> 'Pipeline':
        """
        Add filter stage.
        
        Args:
            predicate: Filter function
        
        Returns:
            Pipeline: Chainable pipeline
        """
        self.source = filter_pipeline(self.source, predicate)
        return self
    
    def map(self, transformer: Callable) -> 'Pipeline':
        """
        Add transformation stage.
        
        Args:
            transformer: Transformation function
        
        Returns:
            Pipeline: Chainable pipeline
        """
        self.source = transform_pipeline(self.source, transformer)
        return self
    
    def batch(self, size: int) -> 'Pipeline':
        """
        Add batching stage.
        
        Args:
            size: Batch size
        
        Returns:
            Pipeline: Chainable pipeline
        """
        self.source = batch_pipeline(self.source, size)
        return self
    
    def enumerate(self) -> 'Pipeline':
        """
        Add enumeration stage.
        
        Returns:
            Pipeline: Chainable pipeline
        """
        self.source = enumerate_pipeline(self.source)
        return self
    
    def execute(self) -> list:
        """
        Execute pipeline and return results.
        
        Returns:
            list: Processed data
        """
        return list(self.source)


def fibonacci_generator(n: int) -> Iterator[int]:
    """
    Generate Fibonacci numbers.
    
    Args:
        n: Number of Fibonacci numbers to generate
    
    Yields:
        int: Fibonacci numbers
    """
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b


def sliding_window(data: Iterator, window_size: int) -> Iterator[list]:
    """
    Generate sliding windows over data.
    
    Args:
        data: Input data iterator
        window_size: Size of sliding window
    
    Yields:
        list: Windows of data
    """
    window = []
    for item in data:
        window.append(item)
        if len(window) > window_size:
            window.pop(0)
        if len(window) == window_size:
            yield window.copy()


def main():
    """Main function to demonstrate generator pipelines."""
    print("Generator Pipeline Demo")
    
    # Sample data
    data = [
        {'id': 1, 'value': 10, 'type': 'A'},
        {'id': 2, 'value': 25, 'type': 'B'},
        {'id': 3, 'value': 15, 'type': 'A'},
        {'id': 4, 'value': 30, 'type': 'B'},
        {'id': 5, 'value': 20, 'type': 'A'},
    ]
    
    # Pipeline example
    print("\n1. Chainable Pipeline:")
    result = (Pipeline(read_data(data))
              .filter(lambda x: x['type'] == 'A')
              .map(lambda x: x['value'])
              .execute())
    print(f"  Filtered type A values: {result}")
    
    # Batching
    print("\n2. Batching Pipeline:")
    numbers = range(10)
    batches = list(batch_pipeline(iter(numbers), 3))
    print(f"  Batches: {batches}")
    
    # Fibonacci generator
    print("\n3. Fibonacci Generator:")
    fibs = list(fibonacci_generator(10))
    print(f"  First 10 Fibonacci: {fibs}")
    
    # Sliding window
    print("\n4. Sliding Window:")
    windows = list(sliding_window(iter(range(5)), 3))
    print(f"  Windows: {windows}")
    
    # Complex pipeline
    print("\n5. Complex Pipeline:")
    result = (Pipeline(read_data(data))
              .filter(lambda x: x['value'] > 15)
              .map(lambda x: {'id': x['id'], 'doubled': x['value'] * 2})
              .batch(2)
              .execute())
    print(f"  Result: {result}")
    
    # Memory efficiency demonstration
    print("\n6. Memory Efficiency:")
    
    def large_dataset():
        """Generate large dataset."""
        for i in range(1000000):
            yield i
    
    start = time.time()
    # Process only first 5 items (generator doesn't generate all)
    result = []
    for i, item in enumerate(large_dataset()):
        if i >= 5:
            break
        result.append(item * 2)
    elapsed = time.time() - start
    
    print(f"  Processed 5 items from 1M in {elapsed:.6f}s")
    print(f"  Result: {result}")


if __name__ == "__main__":
    main()
