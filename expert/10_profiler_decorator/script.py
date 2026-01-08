#!/usr/bin/env python3
"""
Profiler Decorator Script
Performance profiling tool using decorators.
"""

import time
import functools
from typing import Callable, Dict, List
import statistics


class ProfilerStats:
    """Store profiling statistics."""
    
    def __init__(self):
        """Initialize profiler stats."""
        self.calls: Dict[str, List[float]] = {}
        self.memory_usage: Dict[str, List[int]] = {}
    
    def add_call(self, func_name: str, duration: float):
        """
        Record function call duration.
        
        Args:
            func_name: Function name
            duration: Execution time in seconds
        """
        if func_name not in self.calls:
            self.calls[func_name] = []
        self.calls[func_name].append(duration)
    
    def get_stats(self, func_name: str) -> Dict:
        """
        Get statistics for a function.
        
        Args:
            func_name: Function name
        
        Returns:
            dict: Statistics including count, total, average, min, max
        """
        if func_name not in self.calls:
            return {}
        
        durations = self.calls[func_name]
        
        return {
            'count': len(durations),
            'total': sum(durations),
            'average': statistics.mean(durations),
            'median': statistics.median(durations),
            'min': min(durations),
            'max': max(durations),
            'stdev': statistics.stdev(durations) if len(durations) > 1 else 0
        }
    
    def print_report(self):
        """Print profiling report."""
        print("\n" + "=" * 80)
        print("PROFILING REPORT")
        print("=" * 80)
        
        for func_name in sorted(self.calls.keys()):
            stats = self.get_stats(func_name)
            print(f"\nFunction: {func_name}")
            print(f"  Calls:   {stats['count']}")
            print(f"  Total:   {stats['total']:.6f}s")
            print(f"  Average: {stats['average']:.6f}s")
            print(f"  Median:  {stats['median']:.6f}s")
            print(f"  Min:     {stats['min']:.6f}s")
            print(f"  Max:     {stats['max']:.6f}s")
            if stats['stdev'] > 0:
                print(f"  StdDev:  {stats['stdev']:.6f}s")
        
        print("\n" + "=" * 80)


# Global profiler instance
profiler = ProfilerStats()


def profile(func: Callable = None, *, name: str = None):
    """
    Decorator to profile function execution.
    
    Args:
        func: Function to profile
        name: Optional custom name for the function
    
    Returns:
        Decorated function
    """
    def decorator(f: Callable) -> Callable:
        func_name = name or f.__name__
        
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            
            try:
                result = f(*args, **kwargs)
                return result
            finally:
                duration = time.time() - start_time
                profiler.add_call(func_name, duration)
        
        return wrapper
    
    # Allow use as @profile or @profile()
    if func is None:
        return decorator
    else:
        return decorator(func)


def profile_verbose(func: Callable) -> Callable:
    """
    Decorator to profile and print each call.
    
    Args:
        func: Function to profile
    
    Returns:
        Decorated function
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        print(f"[PROFILE] Starting {func.__name__}")
        
        result = func(*args, **kwargs)
        
        duration = time.time() - start_time
        print(f"[PROFILE] {func.__name__} completed in {duration:.6f}s")
        
        profiler.add_call(func.__name__, duration)
        return result
    
    return wrapper


class ProfileContext:
    """Context manager for profiling code blocks."""
    
    def __init__(self, name: str):
        """
        Initialize profile context.
        
        Args:
            name: Name for this profile section
        """
        self.name = name
        self.start_time = None
    
    def __enter__(self):
        """Start profiling."""
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Stop profiling and record time."""
        duration = time.time() - self.start_time
        profiler.add_call(self.name, duration)
        return False


# Example functions to profile

@profile
def fibonacci(n: int) -> int:
    """Calculate Fibonacci number (recursive)."""
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


@profile(name="custom_slow_function")
def slow_function(delay: float = 0.1):
    """Function with custom profile name."""
    time.sleep(delay)
    return "done"


@profile_verbose
def verbose_function(x: int) -> int:
    """Function with verbose profiling."""
    time.sleep(0.05)
    return x * 2


def fast_function(x: int) -> int:
    """Fast function for comparison."""
    return x * 2


def main():
    """Main function to demonstrate profiler."""
    print("Profiler Decorator Demo")
    
    # Profile simple functions
    print("\n1. Profiling simple functions:")
    slow_function(0.1)
    slow_function(0.15)
    slow_function(0.12)
    
    # Profile with verbose output
    print("\n2. Verbose profiling:")
    verbose_function(5)
    verbose_function(10)
    
    # Profile using context manager
    print("\n3. Context manager profiling:")
    with ProfileContext("manual_block"):
        time.sleep(0.05)
        result = sum(range(1000))
    
    # Profile recursive function
    print("\n4. Profiling recursive function:")
    for i in [5, 8, 10]:
        result = fibonacci(i)
        print(f"  fibonacci({i}) = {result}")
    
    # Compare profiled vs unprofiled
    print("\n5. Overhead comparison:")
    
    @profile
    def profiled_fast(x):
        return x * 2
    
    # Time profiled version
    start = time.time()
    for _ in range(1000):
        profiled_fast(5)
    profiled_time = time.time() - start
    
    # Time unprofiled version
    start = time.time()
    for _ in range(1000):
        fast_function(5)
    unprofiled_time = time.time() - start
    
    print(f"  Profiled (1000 calls): {profiled_time:.6f}s")
    print(f"  Unprofiled (1000 calls): {unprofiled_time:.6f}s")
    print(f"  Overhead: {(profiled_time - unprofiled_time) * 1000:.3f}µs per call")
    
    # Print profiling report
    profiler.print_report()


if __name__ == "__main__":
    main()
