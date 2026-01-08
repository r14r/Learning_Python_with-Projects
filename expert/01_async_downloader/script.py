#!/usr/bin/env python3
"""
Async Downloader Script
Asynchronous file downloader using asyncio and aiohttp.
"""

import asyncio
import aiohttp
from pathlib import Path
from typing import List, Dict
import time


async def download_file(session: aiohttp.ClientSession, url: str, destination: str) -> Dict:
    """
    Download a single file asynchronously.
    
    Args:
        session: aiohttp session
        url: URL to download
        destination: Local file path
    
    Returns:
        dict: Download result with status and info
    """
    start_time = time.time()
    
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=30)) as response:
            if response.status == 200:
                content = await response.read()
                
                # Write to file
                Path(destination).parent.mkdir(parents=True, exist_ok=True)
                with open(destination, 'wb') as f:
                    f.write(content)
                
                elapsed = time.time() - start_time
                return {
                    'url': url,
                    'destination': destination,
                    'status': 'success',
                    'size': len(content),
                    'time': elapsed
                }
            else:
                return {
                    'url': url,
                    'status': 'error',
                    'error': f'HTTP {response.status}'
                }
    except Exception as e:
        return {
            'url': url,
            'status': 'error',
            'error': str(e)
        }


async def download_multiple(urls: List[str], output_dir: str = '/tmp/downloads') -> List[Dict]:
    """
    Download multiple files concurrently.
    
    Args:
        urls: List of URLs to download
        output_dir: Directory to save files
    
    Returns:
        List[Dict]: Results for each download
    """
    async with aiohttp.ClientSession() as session:
        tasks = []
        
        for i, url in enumerate(urls):
            filename = f"file_{i}_{Path(url).name}"
            destination = f"{output_dir}/{filename}"
            tasks.append(download_file(session, url, destination))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return results


async def download_with_progress(urls: List[str], output_dir: str = '/tmp/downloads'):
    """
    Download files with progress updates.
    
    Args:
        urls: List of URLs to download
        output_dir: Directory to save files
    """
    total = len(urls)
    completed = 0
    
    print(f"Starting download of {total} files...")
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        
        for i, url in enumerate(urls):
            filename = f"file_{i}_{Path(url).name}"
            destination = f"{output_dir}/{filename}"
            tasks.append(download_file(session, url, destination))
        
        for coro in asyncio.as_completed(tasks):
            result = await coro
            completed += 1
            status = "✓" if result['status'] == 'success' else "✗"
            print(f"{status} [{completed}/{total}] {result.get('url', 'Unknown')[:50]}...")


def main():
    """Main function to demonstrate async downloading."""
    print("Async Downloader Demo")
    
    # Example URLs (using httpbin for testing)
    test_urls = [
        "https://httpbin.org/delay/1",
        "https://httpbin.org/delay/2",
        "https://httpbin.org/delay/1"
    ]
    
    print(f"\nDownloading {len(test_urls)} files concurrently...")
    
    start_time = time.time()
    
    # Run async downloads
    results = asyncio.run(download_multiple(test_urls, '/tmp/async_downloads'))
    
    total_time = time.time() - start_time
    
    # Print results
    print(f"\nCompleted in {total_time:.2f} seconds")
    
    successful = sum(1 for r in results if isinstance(r, dict) and r.get('status') == 'success')
    print(f"Successful: {successful}/{len(results)}")
    
    for result in results:
        if isinstance(result, dict):
            if result['status'] == 'success':
                print(f"  ✓ Downloaded {result.get('size', 0)} bytes to {result['destination']}")
            else:
                print(f"  ✗ Failed: {result.get('error', 'Unknown error')}")


if __name__ == "__main__":
    main()
