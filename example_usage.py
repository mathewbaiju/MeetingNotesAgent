#!/usr/bin/env python3
"""
Example usage of the FileDownloader class with temp file management
"""

from file_downloader import FileDownloader
from temp_file_manager import TempFileManager


def main():
    """Example of how to use the FileDownloader class with temp files."""
    
    print("=== MeetingNotesAgent File Downloader Examples ===\n")
    
    # Example 1: Download to regular Downloads folder
    print("=== Example 1: Download to Downloads folder ===")
    downloader = FileDownloader()
    url1 = "https://httpbin.org/robots.txt"
    result1 = downloader.download_file(url1)
    
    # Example 2: Download to temp directory
    print("\n=== Example 2: Download to temp directory ===")
    temp_downloader = FileDownloader(use_temp=True)
    url2 = "https://httpbin.org/json"
    result2 = temp_downloader.download_file(url2, file_type="transcripts")
    
    # Example 3: Use the fetch_and_download method (main method for transcripts)
    print("\n=== Example 3: Fetch and download to temp (for transcripts) ===")
    url3 = "https://httpbin.org/xml"
    result3 = downloader.fetch_and_download(url3, file_type="transcripts")
    
    # Example 4: Download different file types to temp
    print("\n=== Example 4: Download different file types to temp ===")
    url4 = "https://httpbin.org/html"
    result4 = downloader.download_to_temp(url4, file_type="notes")
    
    url5 = "https://httpbin.org/bytes/1024"
    result5 = downloader.download_to_temp(url5, file_type="attachments")
    
    # Example 5: Show temp directory information
    print("\n=== Example 5: Temp directory information ===")
    temp_manager = TempFileManager()
    temp_manager.get_temp_dir_info()
    
    # Example 6: List files by type
    print("\n=== Example 6: List files by type ===")
    temp_manager.list_temp_files("transcripts")
    temp_manager.list_temp_files("notes")
    temp_manager.list_temp_files("attachments")
    
    # Example 7: Test cleanup (dry run)
    print("\n=== Example 7: Test cleanup (dry run) ===")
    temp_manager.cleanup_old_files(dry_run=True)
    
    # Example 8: List all downloaded files
    print("\n=== Example 8: All downloaded files ===")
    downloader.list_downloaded_files()
    
    print("\n=== Temp files ===")
    temp_downloader.list_downloaded_files()


if __name__ == "__main__":
    main()
