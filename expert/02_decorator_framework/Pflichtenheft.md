# Pflichtenheft: Decorator Framework

## Expected Functionality
A comprehensive decorator framework demonstrating various decorator patterns including timing, retry logic, memoization, type validation, and call logging. Shows both simple and parameterized decorators.

## Input
- **Decorator parameters**:
  - `max_attempts` (int): Retry attempts
  - `delay` (float): Retry delay
  - `**type_kwargs`: Type validation specifications
- **Decorated function arguments**: Varies by function

## Expected Output
```
Decorator Framework Demo

1. Timer + Memoize Decorator:
fibonacci took 0.0001 seconds
Result: 55
Calling again (should be cached):
Cache hit for fibonacci
fibonacci took 0.0000 seconds

2. Type Validation Decorator:
add_numbers(5, 3) = 8
Error caught: Argument 'x' must be int, got str

3. Log Calls Decorator:
Calling greet('Alice')
greet returned 'Hello, Alice!'
Calling greet('Bob', greeting='Hi')
greet returned 'Hi, Bob!'
```

## Tests

### Test 1: Timer Decorator
**Input:** Call decorated function  
**Expected Output:** Execution time printed to console

### Test 2: Memoize Decorator
**Input:** Call fibonacci(10) twice  
**Expected Output:** Second call uses cache (faster)

### Test 3: Retry Decorator
**Input:** Function that fails 2 times then succeeds  
**Expected Output:** Function retries and eventually succeeds

### Test 4: Type Validation - Valid
**Input:** `add_numbers(5, 3)`  
**Expected Output:** `8`

### Test 5: Type Validation - Invalid
**Input:** `add_numbers("5", 3)`  
**Expected Output:** Raises `TypeError`

### Test 6: Log Calls
**Input:** `greet("Alice")`  
**Expected Output:** Logs function call with arguments and return value

## Dependencies
- Standard library only (functools, time, typing, inspect)

## Usage
```bash
python script.py
```

## Notes
Demonstrates advanced Python concepts: closures, higher-order functions, function introspection, and proper use of functools.wraps to preserve function metadata.
