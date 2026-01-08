#!/usr/bin/env python3
"""
Test Framework Script
Simple test framework implementation similar to unittest/pytest.
"""

import sys
import traceback
from typing import Callable, List, Any
from functools import wraps


class TestResult:
    """Store test execution results."""
    
    def __init__(self):
        """Initialize test result."""
        self.passed = 0
        self.failed = 0
        self.errors = 0
        self.failures = []
        self.error_details = []
    
    def add_success(self):
        """Record a successful test."""
        self.passed += 1
    
    def add_failure(self, test_name: str, message: str):
        """Record a test failure."""
        self.failed += 1
        self.failures.append((test_name, message))
    
    def add_error(self, test_name: str, error: Exception):
        """Record a test error."""
        self.errors += 1
        self.error_details.append((test_name, error, traceback.format_exc()))
    
    def total(self) -> int:
        """Get total number of tests."""
        return self.passed + self.failed + self.errors
    
    def is_success(self) -> bool:
        """Check if all tests passed."""
        return self.failed == 0 and self.errors == 0


class AssertionError(Exception):
    """Custom assertion error."""
    pass


class Assert:
    """Assertion helper class."""
    
    @staticmethod
    def equal(actual, expected, message: str = ""):
        """Assert that two values are equal."""
        if actual != expected:
            msg = message or f"Expected {expected}, got {actual}"
            raise AssertionError(msg)
    
    @staticmethod
    def not_equal(actual, expected, message: str = ""):
        """Assert that two values are not equal."""
        if actual == expected:
            msg = message or f"Expected values to be different, both are {actual}"
            raise AssertionError(msg)
    
    @staticmethod
    def true(value, message: str = ""):
        """Assert that value is True."""
        if value is not True:
            msg = message or f"Expected True, got {value}"
            raise AssertionError(msg)
    
    @staticmethod
    def false(value, message: str = ""):
        """Assert that value is False."""
        if value is not False:
            msg = message or f"Expected False, got {value}"
            raise AssertionError(msg)
    
    @staticmethod
    def raises(exception_type: type, func: Callable, *args, **kwargs):
        """Assert that function raises specific exception."""
        try:
            func(*args, **kwargs)
            raise AssertionError(f"Expected {exception_type.__name__} to be raised")
        except exception_type:
            pass  # Expected exception raised
        except Exception as e:
            raise AssertionError(f"Expected {exception_type.__name__}, got {type(e).__name__}")
    
    @staticmethod
    def contains(item, collection, message: str = ""):
        """Assert that item is in collection."""
        if item not in collection:
            msg = message or f"Expected {item} to be in {collection}"
            raise AssertionError(msg)


class TestCase:
    """Base class for test cases."""
    
    def setup(self):
        """Setup before each test."""
        pass
    
    def teardown(self):
        """Cleanup after each test."""
        pass
    
    def assert_equal(self, actual, expected, message: str = ""):
        """Assert equal."""
        Assert.equal(actual, expected, message)
    
    def assert_true(self, value, message: str = ""):
        """Assert true."""
        Assert.true(value, message)
    
    def assert_false(self, value, message: str = ""):
        """Assert false."""
        Assert.false(value, message)


class TestRunner:
    """Test runner to discover and execute tests."""
    
    def __init__(self):
        """Initialize test runner."""
        self.result = TestResult()
    
    def run_test_case(self, test_case: TestCase):
        """
        Run all test methods in a test case.
        
        Args:
            test_case: TestCase instance
        """
        # Find all test methods
        test_methods = [
            method for method in dir(test_case)
            if method.startswith('test_') and callable(getattr(test_case, method))
        ]
        
        for method_name in test_methods:
            self.run_test(test_case, method_name)
    
    def run_test(self, test_case: TestCase, method_name: str):
        """
        Run a single test method.
        
        Args:
            test_case: TestCase instance
            method_name: Name of test method
        """
        test_name = f"{test_case.__class__.__name__}.{method_name}"
        print(f"  {test_name} ... ", end="")
        
        try:
            # Setup
            test_case.setup()
            
            # Run test
            method = getattr(test_case, method_name)
            method()
            
            # Teardown
            test_case.teardown()
            
            print("PASS")
            self.result.add_success()
            
        except AssertionError as e:
            print("FAIL")
            self.result.add_failure(test_name, str(e))
            
        except Exception as e:
            print("ERROR")
            self.result.add_error(test_name, e)
    
    def print_summary(self):
        """Print test results summary."""
        print("\n" + "=" * 70)
        print(f"Ran {self.result.total()} tests")
        print(f"Passed: {self.result.passed}")
        print(f"Failed: {self.result.failed}")
        print(f"Errors: {self.result.errors}")
        
        if self.result.failures:
            print("\nFAILURES:")
            for test_name, message in self.result.failures:
                print(f"  {test_name}: {message}")
        
        if self.result.error_details:
            print("\nERRORS:")
            for test_name, error, tb in self.result.error_details:
                print(f"  {test_name}: {error}")
                print(f"  {tb}")
        
        print("=" * 70)
        
        if self.result.is_success():
            print("SUCCESS")
        else:
            print("FAILED")


# Example test cases

class MathTests(TestCase):
    """Example math tests."""
    
    def test_addition(self):
        """Test addition."""
        self.assert_equal(2 + 2, 4)
    
    def test_subtraction(self):
        """Test subtraction."""
        self.assert_equal(5 - 3, 2)
    
    def test_multiplication(self):
        """Test multiplication."""
        self.assert_equal(3 * 4, 12)


class StringTests(TestCase):
    """Example string tests."""
    
    def setup(self):
        """Setup test data."""
        self.test_string = "Hello, World!"
    
    def test_upper(self):
        """Test string upper()."""
        self.assert_equal(self.test_string.upper(), "HELLO, WORLD!")
    
    def test_lower(self):
        """Test string lower()."""
        self.assert_equal(self.test_string.lower(), "hello, world!")
    
    def test_contains(self):
        """Test string contains."""
        self.assert_true("World" in self.test_string)


def main():
    """Main function to demonstrate test framework."""
    print("Test Framework Demo\n")
    
    runner = TestRunner()
    
    # Run test cases
    print("Running MathTests:")
    runner.run_test_case(MathTests())
    
    print("\nRunning StringTests:")
    runner.run_test_case(StringTests())
    
    # Print summary
    runner.print_summary()
    
    # Exit with appropriate code
    sys.exit(0 if runner.result.is_success() else 1)


if __name__ == "__main__":
    main()
