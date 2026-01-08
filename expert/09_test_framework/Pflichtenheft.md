# Pflichtenheft: Test Framework

## Expected Functionality
A simple test framework implementation similar to unittest/pytest. Supports test discovery, assertions, setup/teardown, test execution, and result reporting with pass/fail/error status.

## Input
- **Test cases**: Classes inheriting from TestCase
- **Test methods**: Methods starting with `test_`
- **Assertions**: Various assert methods

## Expected Output
```
Test Framework Demo

Running MathTests:
  MathTests.test_addition ... PASS
  MathTests.test_subtraction ... PASS
  MathTests.test_multiplication ... PASS

Running StringTests:
  StringTests.test_upper ... PASS
  StringTests.test_lower ... PASS
  StringTests.test_contains ... PASS

======================================================================
Ran 6 tests
Passed: 6
Failed: 0
Errors: 0
======================================================================
SUCCESS
```

## Tests

### Test 1: Assert Equal - Pass
**Input:** `Assert.equal(2 + 2, 4)`  
**Expected Output:** No exception raised

### Test 2: Assert Equal - Fail
**Input:** `Assert.equal(2 + 2, 5)`  
**Expected Output:** Raises `AssertionError`

### Test 3: Assert True
**Input:** `Assert.true(True)`  
**Expected Output:** No exception raised

### Test 4: Assert Raises
**Input:** `Assert.raises(ValueError, int, "not a number")`  
**Expected Output:** No exception (ValueError was raised as expected)

### Test 5: Setup/Teardown
**Input:** Test case with setup() and teardown() methods  
**Expected Output:** setup() called before test, teardown() after

### Test 6: Test Discovery
**Input:** TestCase with multiple `test_*` methods  
**Expected Output:** All test methods discovered and executed

## Dependencies
- Standard library only (sys, traceback, typing, functools)

## Usage
```bash
python script.py
```

## Notes
Demonstrates testing framework concepts: test discovery, assertions, fixtures (setup/teardown), result collection, and reporting. Shows how testing frameworks work internally.
