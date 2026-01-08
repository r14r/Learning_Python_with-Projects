# Pflichtenheft: Profiler Decorator

## Expected Functionality
A performance profiling tool using decorators and context managers. Tracks function execution times, provides statistical analysis (mean, median, min, max, stdev), and generates comprehensive profiling reports.

## Input
- **Decorator usage**: `@profile` on functions
- **Context manager**: `with ProfileContext("name"): ...`
- **Configuration**: Optional custom name for profiled functions

## Expected Output
```
Profiler Decorator Demo

1. Profiling simple functions:

2. Verbose profiling:
[PROFILE] Starting verbose_function
[PROFILE] verbose_function completed in 0.050234s
[PROFILE] Starting verbose_function
[PROFILE] verbose_function completed in 0.050198s

3. Context manager profiling:

4. Profiling recursive function:
  fibonacci(5) = 5
  fibonacci(8) = 21
  fibonacci(10) = 55

5. Overhead comparison:
  Profiled (1000 calls): 0.002156s
  Unprofiled (1000 calls): 0.000234s
  Overhead: 1.922µs per call

================================================================================
PROFILING REPORT
================================================================================

Function: custom_slow_function
  Calls:   3
  Total:   0.371234s
  Average: 0.123745s
  Median:  0.120045s
  Min:     0.100123s
  Max:     0.150234s
  StdDev:  0.021234s

Function: fibonacci
  Calls:   15
  Total:   0.000456s
  Average: 0.000030s
  Median:  0.000028s
  Min:     0.000012s
  Max:     0.000089s
  StdDev:  0.000018s

================================================================================
```

## Tests

### Test 1: Profile Decorator - Basic
**Input:** `@profile` on function, then call it  
**Expected Output:** Execution time recorded in profiler

### Test 2: Multiple Calls Statistics
**Input:** Call profiled function 10 times  
**Expected Output:** Stats show count=10, average calculated correctly

### Test 3: Profile Context Manager
**Input:** `with ProfileContext("test"): ...`  
**Expected Output:** Block execution time recorded

### Test 4: Custom Name
**Input:** `@profile(name="custom")`  
**Expected Output:** Stats use "custom" as function name

### Test 5: Statistical Analysis
**Input:** Multiple calls with varying durations  
**Expected Output:** Correct min, max, mean, median, stdev

### Test 6: Profiling Report
**Input:** `profiler.print_report()`  
**Expected Output:** Formatted report with all profiled functions

## Dependencies
- Standard library only (time, functools, typing, statistics)

## Usage
```bash
python script.py
```

## Notes
Demonstrates performance analysis, decorator patterns, context managers, statistical analysis, and how profiling tools work. Shows the overhead of profiling itself.
