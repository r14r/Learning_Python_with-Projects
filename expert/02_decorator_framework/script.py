#!/usr/bin/env python3
"""
Decorator Framework Script
Custom decorator system with various patterns and use cases.
"""

import functools
import time
from typing import Callable, Any


def timer(func: Callable) -> Callable:
    """
    Decorator to measure function execution time.
    
    Args:
        func: Function to decorate
    
    Returns:
        Wrapped function
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"{func.__name__} took {elapsed:.4f} seconds")
        return result
    return wrapper


def retry(max_attempts: int = 3, delay: float = 1.0):
    """
    Decorator to retry function on failure.
    
    Args:
        max_attempts: Maximum number of retry attempts
        delay: Delay between retries in seconds
    
    Returns:
        Decorator function
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts >= max_attempts:
                        raise
                    print(f"Attempt {attempts} failed: {e}. Retrying in {delay}s...")
                    time.sleep(delay)
        return wrapper
    return decorator


def memoize(func: Callable) -> Callable:
    """
    Decorator to cache function results.
    
    Args:
        func: Function to decorate
    
    Returns:
        Wrapped function with caching
    """
    cache = {}
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Create cache key from arguments
        key = str(args) + str(kwargs)
        
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        else:
            print(f"Cache hit for {func.__name__}")
        
        return cache[key]
    
    wrapper.cache = cache
    wrapper.clear_cache = lambda: cache.clear()
    return wrapper


def validate_types(**type_kwargs):
    """
    Decorator to validate function argument types.
    
    Args:
        **type_kwargs: Argument names and their expected types
    
    Returns:
        Decorator function
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Get function signature
            import inspect
            sig = inspect.signature(func)
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()
            
            # Validate types
            for arg_name, expected_type in type_kwargs.items():
                if arg_name in bound_args.arguments:
                    value = bound_args.arguments[arg_name]
                    if not isinstance(value, expected_type):
                        raise TypeError(
                            f"Argument '{arg_name}' must be {expected_type.__name__}, "
                            f"got {type(value).__name__}"
                        )
            
            return func(*args, **kwargs)
        return wrapper
    return decorator


def log_calls(func: Callable) -> Callable:
    """
    Decorator to log function calls with arguments.
    
    Args:
        func: Function to decorate
    
    Returns:
        Wrapped function
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        print(f"Calling {func.__name__}({signature})")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned {result!r}")
        return result
    return wrapper


# Example usage functions

@timer
@memoize
def fibonacci(n: int) -> int:
    """Calculate Fibonacci number (with timer and memoization)."""
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


@validate_types(x=int, y=int)
def add_numbers(x: int, y: int) -> int:
    """Add two numbers (with type validation)."""
    return x + y


@log_calls
def greet(name: str, greeting: str = "Hello") -> str:
    """Greet a person (with call logging)."""
    return f"{greeting}, {name}!"


def main():
    """Main function to demonstrate decorators."""
    print("Decorator Framework Demo")
    
    # Timer and memoize
    print("\n1. Timer + Memoize Decorator:")
    result = fibonacci(10)
    print(f"Result: {result}")
    print("Calling again (should be cached):")
    result = fibonacci(10)
    
    # Type validation
    print("\n2. Type Validation Decorator:")
    print(f"add_numbers(5, 3) = {add_numbers(5, 3)}")
    try:
        add_numbers("5", 3)  # Should raise TypeError
    except TypeError as e:
        print(f"Error caught: {e}")
    
    # Log calls
    print("\n3. Log Calls Decorator:")
    greet("Alice")
    greet("Bob", greeting="Hi")


if __name__ == "__main__":
    main()
