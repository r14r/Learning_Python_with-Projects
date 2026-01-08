#!/usr/bin/env python3
"""
Cache System Script
LRU (Least Recently Used) cache implementation.
"""

from typing import Any, Optional
from collections import OrderedDict
import time
import functools


class LRUCache:
    """Least Recently Used (LRU) cache implementation."""
    
    def __init__(self, capacity: int = 100):
        """
        Initialize LRU cache.
        
        Args:
            capacity: Maximum number of items in cache
        """
        self.capacity = capacity
        self.cache = OrderedDict()
        self.hits = 0
        self.misses = 0
    
    def get(self, key: Any) -> Optional[Any]:
        """
        Get value from cache.
        
        Args:
            key: Cache key
        
        Returns:
            Cached value or None if not found
        """
        if key in self.cache:
            self.hits += 1
            # Move to end (most recently used)
            self.cache.move_to_end(key)
            return self.cache[key]
        else:
            self.misses += 1
            return None
    
    def put(self, key: Any, value: Any):
        """
        Put value in cache.
        
        Args:
            key: Cache key
            value: Value to cache
        """
        if key in self.cache:
            # Update existing key
            self.cache.move_to_end(key)
        else:
            # Add new key
            if len(self.cache) >= self.capacity:
                # Remove least recently used (first item)
                self.cache.popitem(last=False)
        
        self.cache[key] = value
    
    def clear(self):
        """Clear the cache."""
        self.cache.clear()
        self.hits = 0
        self.misses = 0
    
    def stats(self) -> dict:
        """
        Get cache statistics.
        
        Returns:
            dict: Statistics including hits, misses, and hit rate
        """
        total = self.hits + self.misses
        hit_rate = self.hits / total if total > 0 else 0
        
        return {
            'capacity': self.capacity,
            'size': len(self.cache),
            'hits': self.hits,
            'misses': self.misses,
            'hit_rate': hit_rate
        }


class TTLCache:
    """Cache with Time-To-Live (TTL) expiration."""
    
    def __init__(self, ttl: float = 60.0):
        """
        Initialize TTL cache.
        
        Args:
            ttl: Time-to-live in seconds
        """
        self.ttl = ttl
        self.cache = {}
    
    def get(self, key: Any) -> Optional[Any]:
        """
        Get value from cache if not expired.
        
        Args:
            key: Cache key
        
        Returns:
            Cached value or None if not found/expired
        """
        if key in self.cache:
            value, expiry = self.cache[key]
            if time.time() < expiry:
                return value
            else:
                # Expired, remove from cache
                del self.cache[key]
        return None
    
    def put(self, key: Any, value: Any):
        """
        Put value in cache with expiry time.
        
        Args:
            key: Cache key
            value: Value to cache
        """
        expiry = time.time() + self.ttl
        self.cache[key] = (value, expiry)
    
    def cleanup(self):
        """Remove expired entries."""
        current_time = time.time()
        expired_keys = [
            key for key, (_, expiry) in self.cache.items()
            if current_time >= expiry
        ]
        for key in expired_keys:
            del self.cache[key]


def cached(cache: LRUCache):
    """
    Decorator to cache function results.
    
    Args:
        cache: Cache instance to use
    
    Returns:
        Decorator function
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache key
            key = (func.__name__, args, tuple(sorted(kwargs.items())))
            
            # Try to get from cache
            result = cache.get(key)
            if result is not None:
                return result
            
            # Compute and cache result
            result = func(*args, **kwargs)
            cache.put(key, result)
            return result
        
        return wrapper
    return decorator


# Example usage
cache = LRUCache(capacity=3)


@cached(cache)
def expensive_computation(n: int) -> int:
    """Simulate expensive computation."""
    print(f"Computing for {n}...")
    time.sleep(0.1)  # Simulate delay
    return n * n


def main():
    """Main function to demonstrate cache system."""
    print("Cache System Demo")
    
    # LRU Cache
    print("\n1. LRU Cache:")
    lru = LRUCache(capacity=3)
    
    # Add items
    lru.put('a', 1)
    lru.put('b', 2)
    lru.put('c', 3)
    print(f"  Cache after adding a, b, c: {list(lru.cache.keys())}")
    
    # Access 'a' (moves to end)
    lru.get('a')
    print(f"  After accessing 'a': {list(lru.cache.keys())}")
    
    # Add 'd' (evicts 'b', least recently used)
    lru.put('d', 4)
    print(f"  After adding 'd': {list(lru.cache.keys())}")
    
    # Statistics
    stats = lru.stats()
    print(f"  Stats: {stats}")
    
    # TTL Cache
    print("\n2. TTL Cache:")
    ttl = TTLCache(ttl=1.0)
    
    ttl.put('key1', 'value1')
    print(f"  Immediately after put: {ttl.get('key1')}")
    
    time.sleep(1.1)
    print(f"  After TTL expired: {ttl.get('key1')}")
    
    # Cached function
    print("\n3. Cached Function:")
    cache.clear()
    
    print("  First call (computes):")
    start = time.time()
    result1 = expensive_computation(5)
    time1 = time.time() - start
    print(f"  Result: {result1}, Time: {time1:.4f}s")
    
    print("  Second call (cached):")
    start = time.time()
    result2 = expensive_computation(5)
    time2 = time.time() - start
    print(f"  Result: {result2}, Time: {time2:.6f}s")
    
    print(f"  Speedup: {time1/time2:.1f}x")
    print(f"  Cache stats: {cache.stats()}")
    
    # LRU eviction
    print("\n4. LRU Eviction:")
    small_cache = LRUCache(capacity=2)
    
    for i in range(4):
        result = cached(small_cache)(expensive_computation)(i)
    
    print(f"  Cache size: {small_cache.stats()['size']}")
    print(f"  Cache keys: {[k[1][0] for k in small_cache.cache.keys()]}")


if __name__ == "__main__":
    main()
