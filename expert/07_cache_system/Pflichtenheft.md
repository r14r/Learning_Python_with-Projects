# Pflichtenheft: Cache System

## Expected Functionality
Implementation of LRU (Least Recently Used) and TTL (Time-To-Live) cache systems. Includes cache decorator for function memoization, statistics tracking, and automatic eviction policies.

## Input
- **Cache parameters**:
  - `capacity` (int): Maximum cache size
  - `ttl` (float): Time-to-live in seconds
  - `key` (Any): Cache key
  - `value` (Any): Value to cache

## Expected Output
```
Cache System Demo

1. LRU Cache:
  Cache after adding a, b, c: ['a', 'b', 'c']
  After accessing 'a': ['b', 'c', 'a']
  After adding 'd': ['c', 'a', 'd']
  Stats: {'capacity': 3, 'size': 3, 'hits': 1, 'misses': 0, 'hit_rate': 1.0}

2. TTL Cache:
  Immediately after put: value1
  After TTL expired: None

3. Cached Function:
  First call (computes):
  Computing for 5...
  Result: 25, Time: 0.1002s
  Second call (cached):
  Result: 25, Time: 0.000012s
  Speedup: 8350.0x
  Cache stats: {'capacity': 3, 'size': 1, 'hits': 1, 'misses': 1, 'hit_rate': 0.5}

4. LRU Eviction:
  Computing for 0...
  Computing for 1...
  Computing for 2...
  Computing for 3...
  Cache size: 2
  Cache keys: [2, 3]
```

## Tests

### Test 1: LRU Cache - Basic Operations
**Input:** `put('a', 1)`, then `get('a')`  
**Expected Output:** Returns `1`

### Test 2: LRU Cache - Eviction
**Input:** Cache capacity=2, add 3 items  
**Expected Output:** First item evicted

### Test 3: LRU Cache - Access Order
**Input:** Add [a, b, c], access 'a', add 'd'  
**Expected Output:** 'b' evicted (least recently used)

### Test 4: TTL Cache - Valid
**Input:** `put('key', 'value')`, immediate `get('key')`  
**Expected Output:** Returns `'value'`

### Test 5: TTL Cache - Expired
**Input:** `put('key', 'value')`, wait > TTL, `get('key')`  
**Expected Output:** Returns `None`

### Test 6: Cache Statistics
**Input:** Multiple get/put operations  
**Expected Output:** Correct hits, misses, and hit rate

## Dependencies
- Standard library only (typing, collections, time, functools)

## Usage
```bash
python script.py
```

## Notes
Demonstrates OrderedDict usage for LRU, time-based expiration, decorator patterns for transparent caching, and performance optimization techniques.
