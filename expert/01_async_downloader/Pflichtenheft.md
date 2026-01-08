# Pflichtenheft: Async Downloader

## Expected Functionality
An asynchronous file downloader using `asyncio` and `aiohttp` for concurrent downloads. Demonstrates non-blocking I/O, concurrent task execution, and progress tracking for multiple simultaneous downloads.

## Input
- **Function parameters**:
  - `urls` (List[str]): List of URLs to download
  - `output_dir` (str): Directory to save downloaded files
  - `session` (aiohttp.ClientSession): HTTP session for downloads

## Expected Output
```
Async Downloader Demo

Downloading 3 files concurrently...

Completed in 2.15 seconds
Successful: 3/3
  ✓ Downloaded 450 bytes to /tmp/async_downloads/file_0_delay
  ✓ Downloaded 450 bytes to /tmp/async_downloads/file_1_delay
  ✓ Downloaded 450 bytes to /tmp/async_downloads/file_2_delay
```

## Tests

### Test 1: Single File Download
**Input:** `download_file(session, "https://httpbin.org/get", "/tmp/test.json")`  
**Expected Output:** Dictionary with status='success' and file information

### Test 2: Multiple Concurrent Downloads
**Input:** `download_multiple(["url1", "url2", "url3"])`  
**Expected Output:** List of 3 result dictionaries

### Test 3: Download Speed
**Input:** Download 3 files with 1-second delay each  
**Expected Output:** Total time ~2 seconds (concurrent) vs ~3 seconds (sequential)

### Test 4: Error Handling - Invalid URL
**Input:** `download_file(session, "https://invalid.url", "/tmp/test")`  
**Expected Output:** Dictionary with status='error'

### Test 5: Progress Tracking
**Input:** `download_with_progress(urls)`  
**Expected Output:** Progress updates printed during download

## Dependencies
```
aiohttp
asyncio (standard library)
```

## Usage
```bash
pip install aiohttp
python script.py
```

## Notes
This script demonstrates advanced async/await patterns, concurrent execution with asyncio.gather(), and proper error handling in asynchronous code.
