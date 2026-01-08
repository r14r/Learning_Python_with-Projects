# Pflichtenheft: Thread Pool

## Expected Functionality
Multi-threaded task executor demonstrating thread pool patterns including custom implementation, ThreadPoolExecutor usage, task queuing, and thread-safe operations with locks.

## Input
- **ThreadPool parameters**:
  - `num_threads` (int): Number of worker threads
  - `max_workers` (int): Maximum concurrent workers
- **Task parameters**:
  - `task` (Callable): Function to execute
  - `items` (List): Items to process
  - `delay` (float): Processing delay

## Expected Output
```
Thread Pool Demo

1. Simple Thread Pool:
[Thread-1] Processing 0
[Thread-2] Processing 1
[Thread-3] Processing 2
[Thread-1] Processing 3
[Thread-2] Processing 4
[Thread-3] Processing 5
  Completed 6 tasks

2. ThreadPoolExecutor (Ordered):
[ThreadPoolExecutor-0_0] Processing 0
[ThreadPoolExecutor-0_1] Processing 1
[ThreadPoolExecutor-0_2] Processing 2
[ThreadPoolExecutor-0_0] Processing 3
[ThreadPoolExecutor-0_1] Processing 4
  Processed 5 items in 0.42s

3. ThreadPoolExecutor (As Completed):
[ThreadPoolExecutor-1_0] Processing 1
[ThreadPoolExecutor-1_1] Processing 2
[ThreadPoolExecutor-1_2] Processing 3
[ThreadPoolExecutor-1_0] Processing 4
[ThreadPoolExecutor-1_1] Processing 5
  Completed 5 tasks

4. Thread-Safe Counter:
  Final counter value: 5000 (expected: 5000)
```

## Tests

### Test 1: Simple Thread Pool - Task Execution
**Input:** Submit 10 tasks to pool with 3 threads  
**Expected Output:** All tasks complete, results collected

### Test 2: Parallel Map - Speed Improvement
**Input:** Process 10 items with delay=0.1s using 5 threads  
**Expected Output:** Total time ~0.2s (parallel) vs 1.0s (sequential)

### Test 3: Thread-Safe Counter
**Input:** 5 threads each increment counter 1000 times  
**Expected Output:** Final value = 5000 (no race conditions)

### Test 4: Task Queue
**Input:** Submit tasks faster than they can be processed  
**Expected Output:** Tasks queued and processed in order

### Test 5: Exception Handling
**Input:** Submit task that raises exception  
**Expected Output:** Exception caught, other tasks continue

### Test 6: As Completed Order
**Input:** Process items with varying delays  
**Expected Output:** Results returned in completion order

## Dependencies
- Standard library only (threading, queue, time, concurrent.futures)

## Usage
```bash
python script.py
```

## Notes
Demonstrates thread synchronization, locks, queues, the GIL implications, and proper thread pool shutdown. Shows both custom and standard library implementations.
