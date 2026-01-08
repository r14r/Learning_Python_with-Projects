#!/usr/bin/env python3
"""
Context Manager Script
Custom context manager implementations using both class-based and decorator approaches.
"""

import time
from contextlib import contextmanager
from typing import Any, Optional
import os


class Timer:
    """Context manager to measure execution time."""
    
    def __init__(self, name: str = "Operation"):
        """
        Initialize timer.
        
        Args:
            name: Name of operation being timed
        """
        self.name = name
        self.start_time = None
        self.elapsed = None
    
    def __enter__(self):
        """Start timing."""
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Stop timing and report.
        
        Args:
            exc_type: Exception type if raised
            exc_val: Exception value if raised
            exc_tb: Exception traceback if raised
        
        Returns:
            False to propagate exceptions
        """
        self.elapsed = time.time() - self.start_time
        print(f"{self.name} took {self.elapsed:.4f} seconds")
        return False  # Don't suppress exceptions


class FileManager:
    """Context manager for safe file operations."""
    
    def __init__(self, filename: str, mode: str = 'r'):
        """
        Initialize file manager.
        
        Args:
            filename: Path to file
            mode: File open mode
        """
        self.filename = filename
        self.mode = mode
        self.file = None
    
    def __enter__(self):
        """Open file."""
        print(f"Opening {self.filename}")
        self.file = open(self.filename, self.mode)
        return self.file
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close file."""
        if self.file:
            print(f"Closing {self.filename}")
            self.file.close()
        return False


class DatabaseConnection:
    """Context manager simulating database connection."""
    
    def __init__(self, db_name: str):
        """
        Initialize connection.
        
        Args:
            db_name: Database name
        """
        self.db_name = db_name
        self.connected = False
    
    def __enter__(self):
        """Establish connection."""
        print(f"Connecting to {self.db_name}...")
        self.connected = True
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close connection and handle transactions."""
        if exc_type is None:
            print(f"Committing transaction to {self.db_name}")
        else:
            print(f"Rolling back transaction to {self.db_name}")
        
        print(f"Closing connection to {self.db_name}")
        self.connected = False
        return False
    
    def execute(self, query: str):
        """Execute a query."""
        if not self.connected:
            raise RuntimeError("Not connected to database")
        print(f"Executing: {query}")
        return f"Result for: {query}"


@contextmanager
def temporary_directory(path: str):
    """
    Context manager to create and cleanup temporary directory.
    
    Args:
        path: Directory path
    
    Yields:
        Directory path
    """
    print(f"Creating directory: {path}")
    os.makedirs(path, exist_ok=True)
    
    try:
        yield path
    finally:
        print(f"Removing directory: {path}")
        if os.path.exists(path):
            os.rmdir(path)


@contextmanager
def suppress_output():
    """Context manager to suppress stdout."""
    import sys
    from io import StringIO
    
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    
    try:
        yield
    finally:
        sys.stdout = old_stdout


class ResourcePool:
    """Context manager for resource pool with cleanup."""
    
    def __init__(self, resources: list):
        """
        Initialize resource pool.
        
        Args:
            resources: List of resources to manage
        """
        self.resources = resources
        self.acquired = []
    
    def __enter__(self):
        """Acquire all resources."""
        print(f"Acquiring {len(self.resources)} resources...")
        self.acquired = self.resources.copy()
        return self.acquired
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Release all resources."""
        print(f"Releasing {len(self.acquired)} resources...")
        self.acquired.clear()
        return False


def main():
    """Main function to demonstrate context managers."""
    print("Context Manager Demo")
    
    # Timer context manager
    print("\n1. Timer Context Manager:")
    with Timer("Sleep operation"):
        time.sleep(0.1)
    
    # File manager
    print("\n2. File Manager Context Manager:")
    test_file = "/tmp/test_context.txt"
    with open(test_file, 'w') as f:
        f.write("test content")
    
    with FileManager(test_file, 'r') as f:
        content = f.read()
        print(f"  Read: {content}")
    
    # Database connection (simulated)
    print("\n3. Database Connection Context Manager:")
    with DatabaseConnection("test_db") as db:
        db.execute("SELECT * FROM users")
    
    # Temporary directory
    print("\n4. Temporary Directory Context Manager:")
    with temporary_directory("/tmp/temp_test_dir") as temp_dir:
        print(f"  Working in: {temp_dir}")
    
    # Resource pool
    print("\n5. Resource Pool Context Manager:")
    with ResourcePool(["resource1", "resource2", "resource3"]) as resources:
        print(f"  Using resources: {resources}")
    
    print("\n6. Error Handling:")
    try:
        with DatabaseConnection("test_db") as db:
            db.execute("INSERT INTO users VALUES (1, 'Alice')")
            raise ValueError("Simulated error")
    except ValueError:
        print("  Error was caught outside context manager")


if __name__ == "__main__":
    main()
