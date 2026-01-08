# Pflichtenheft: Generator Pipeline

## Expected Functionality
Data processing pipeline using Python generators for memory-efficient streaming operations. Demonstrates lazy evaluation, chaining operations, batching, and sliding windows without loading all data into memory.

## Input
- **Pipeline stages**:
  - `source` (Iterator): Data source
  - `predicate` (Callable): Filter function
  - `transformer` (Callable): Transform function
  - `batch_size` (int): Batch size
  - `window_size` (int): Sliding window size

## Expected Output
```
Generator Pipeline Demo

1. Chainable Pipeline:
  Filtered type A values: [10, 15, 20]

2. Batching Pipeline:
  Batches: [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]

3. Fibonacci Generator:
  First 10 Fibonacci: [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

4. Sliding Window:
  Windows: [[0, 1, 2], [1, 2, 3], [2, 3, 4]]

5. Complex Pipeline:
  Result: [[{'id': 2, 'doubled': 50}, {'id': 4, 'doubled': 60}], [{'id': 5, 'doubled': 40}]]

6. Memory Efficiency:
  Processed 5 items from 1M in 0.000015s
  Result: [0, 2, 4, 6, 8]
```

## Tests

### Test 1: Filter Pipeline
**Input:** `list(filter_pipeline(iter([1,2,3,4]), lambda x: x > 2))`  
**Expected Output:** `[3, 4]`

### Test 2: Transform Pipeline
**Input:** `list(transform_pipeline(iter([1,2,3]), lambda x: x * 2))`  
**Expected Output:** `[2, 4, 6]`

### Test 3: Batch Pipeline
**Input:** `list(batch_pipeline(iter(range(7)), 3))`  
**Expected Output:** `[[0,1,2], [3,4,5], [6]]`

### Test 4: Chainable Pipeline
**Input:** `Pipeline(data).filter(...).map(...).execute()`  
**Expected Output:** Processed data through all stages

### Test 5: Sliding Window
**Input:** `list(sliding_window(iter([1,2,3,4]), 2))`  
**Expected Output:** `[[1,2], [2,3], [3,4]]`

### Test 6: Memory Efficiency
**Input:** Process first 10 items from infinite generator  
**Expected Output:** Fast execution, only 10 items generated

## Dependencies
- Standard library only (typing, time, itertools)

## Usage
```bash
python script.py
```

## Notes
Demonstrates lazy evaluation, generator expressions, yield keyword, itertools usage, and memory-efficient data processing patterns. Shows how generators enable processing of datasets larger than memory.
