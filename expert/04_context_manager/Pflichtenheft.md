# Pflichtenheft: Context Manager

## Expected Functionality
Comprehensive demonstration of context manager implementations using both class-based (`__enter__`/`__exit__`) and decorator-based (`@contextmanager`) approaches. Shows resource management, error handling, and cleanup patterns.

## Input
- **Context manager parameters**:
  - `name` (str): Operation name for Timer
  - `filename` (str): File path for FileManager
  - `db_name` (str): Database name
  - `path` (str): Directory path
  - `resources` (list): Resources to manage

## Expected Output
```
Context Manager Demo

1. Timer Context Manager:
Sleep operation took 0.1001 seconds

2. File Manager Context Manager:
Opening /tmp/test_context.txt
  Read: test content
Closing /tmp/test_context.txt

3. Database Connection Context Manager:
Connecting to test_db...
Executing: SELECT * FROM users
Committing transaction to test_db
Closing connection to test_db

4. Temporary Directory Context Manager:
Creating directory: /tmp/temp_test_dir
  Working in: /tmp/temp_test_dir
Removing directory: /tmp/temp_test_dir

5. Resource Pool Context Manager:
Acquiring 3 resources...
  Using resources: ['resource1', 'resource2', 'resource3']
Releasing 3 resources...

6. Error Handling:
Connecting to test_db...
Executing: INSERT INTO users VALUES (1, 'Alice')
Rolling back transaction to test_db
Closing connection to test_db
  Error was caught outside context manager
```

## Tests

### Test 1: Timer Context Manager
**Input:** `with Timer("Test"): time.sleep(0.1)`  
**Expected Output:** Prints timing information (~0.1 seconds)

### Test 2: File Manager - Open and Close
**Input:** `with FileManager("test.txt", "r") as f: ...`  
**Expected Output:** File opened, used, and properly closed

### Test 3: Database - Successful Transaction
**Input:** `with DatabaseConnection("db") as db: db.execute("query")`  
**Expected Output:** Transaction committed, connection closed

### Test 4: Database - Failed Transaction
**Input:** `with DatabaseConnection("db") as db: raise Exception()`  
**Expected Output:** Transaction rolled back, connection closed

### Test 5: Temporary Directory Cleanup
**Input:** `with temporary_directory("/tmp/test"): ...`  
**Expected Output:** Directory created and removed after use

### Test 6: Resource Pool
**Input:** `with ResourcePool([1, 2, 3]) as r: ...`  
**Expected Output:** Resources acquired and released

## Dependencies
- Standard library only (time, contextlib, typing, os, sys, io)

## Usage
```bash
python script.py
```

## Notes
Demonstrates the context manager protocol, RAII pattern, proper exception handling in `__exit__`, and both class-based and generator-based (@contextmanager) implementations.
