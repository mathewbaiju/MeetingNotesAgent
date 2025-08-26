#!/usr/bin/env python3
"""
File Downloader for MeetingNotesAgent
Downloads files from URLs with progress tracking and error handling
"""

import os
import sys
import requests
from urllib.parse import urlparse, unquote
from pathlib import Path
import time
from temp_file_manager import TempFileManager


class FileDownloader:
    def __init__(self, download_dir=None, use_temp=False):
        """
        Initialize the downloader with optional download directory.
        
        Args:
            download_dir (str): Custom download directory. If None, uses default
            use_temp (bool): If True, downloads to temp directory instead
        """
        self.use_temp = use_temp
        
        if use_temp:
            self.temp_manager = TempFileManager()
            self.download_dir = None
        else:
            if download_dir is None:
                # Default to Downloads folder on Mac
                self.download_dir = Path.home() / "Downloads" / "MeetingNotesAgent"
            else:
                self.download_dir = Path(download_dir)
            
            # Create download directory if it doesn't exist
            self.download_dir.mkdir(parents=True, exist_ok=True)
    
    def download_file(self, url, filename=None, show_progress=True, file_type="general"):
        """
        Download a file from the given URL.
        
        Args:
            url (str): The URL to download from
            filename (str, optional): Custom filename. If None, extracts from URL
            show_progress (bool): Whether to show download progress
            file_type (str): Type of file for temp storage (transcripts, notes, attachments, general)
            
        Returns:
            Path: Path to the downloaded file
        """
        try:
            # Parse URL and get filename if not provided
            if filename is None:
                filename = self._extract_filename(url)
            
            # Determine filepath based on mode
            if self.use_temp:
                filepath = self.temp_manager.get_temp_path(filename, file_type)
            else:
                filepath = self.download_dir / filename
            
            # Start the download
            print(f"Downloading: {url}")
            print(f"Destination: {filepath}")
            
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            # Get file size for progress tracking
            total_size = int(response.headers.get('content-length', 0))
            
            # Download with progress tracking
            downloaded_size = 0
            start_time = time.time()
            
            with open(filepath, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
                        downloaded_size += len(chunk)
                        
                        if show_progress and total_size > 0:
                            self._show_progress(downloaded_size, total_size, start_time)
            
            # Final progress update
            if show_progress:
                self._show_progress(downloaded_size, total_size, start_time, final=True)
            
            print(f"\n✅ Download completed: {filepath}")
            return filepath
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Download failed: {e}")
            return None
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return None
    
    def download_to_temp(self, url, filename=None, show_progress=True, file_type="general"):
        """
        Download a file directly to the temp directory.
        
        Args:
            url (str): The URL to download from
            filename (str, optional): Custom filename. If None, extracts from URL
            show_progress (bool): Whether to show download progress
            file_type (str): Type of file (transcripts, notes, attachments, general)
            
        Returns:
            Path: Path to the downloaded temp file
        """
        # Create a temporary instance for this download
        temp_downloader = FileDownloader(use_temp=True)
        return temp_downloader.download_file(url, filename, show_progress, file_type)
    
    def fetch_and_download(self, url, filename=None, show_progress=True, file_type="general"):
        """
        Fetch URL content and download to temp directory.
        This is the main method for meeting transcript fetching.
        
        Args:
            url (str): The URL to fetch and download
            filename (str, optional): Custom filename
            show_progress (bool): Whether to show download progress
            file_type (str): Type of file (transcripts, notes, attachments, general)
            
        Returns:
            Path: Path to the downloaded file
        """
        print(f"🔄 Fetching and downloading: {url}")
        return self.download_to_temp(url, filename, show_progress, file_type)
    
    def _extract_filename(self, url):
        """Extract filename from URL, handling URL encoding."""
        parsed_url = urlparse(url)
        filename = unquote(parsed_url.path.split('/')[-1])
        
        # If no filename in URL, generate one
        if not filename or '.' not in filename:
            filename = f"downloaded_file_{int(time.time())}.txt"
        
        return filename
    
    def _show_progress(self, downloaded, total, start_time, final=False):
        """Show download progress bar."""
        if total > 0:
            percentage = (downloaded / total) * 100
            bar_length = 50
            filled_length = int(bar_length * downloaded // total)
            bar = '█' * filled_length + '-' * (bar_length - filled_length)
            
            # Calculate speed and ETA
            elapsed_time = time.time() - start_time
            if elapsed_time > 0:
                speed = downloaded / elapsed_time
                if downloaded < total:
                    eta = (total - downloaded) / speed
                    eta_str = f"ETA: {eta:.1f}s"
                else:
                    eta_str = "Complete!"
                
                # Format file sizes
                downloaded_mb = downloaded / (1024 * 1024)
                total_mb = total / (1024 * 1024)
                speed_mb = speed / (1024 * 1024)
                
                print(f"\r[{bar}] {percentage:5.1f}% | "
                      f"{downloaded_mb:.1f}MB/{total_mb:.1f}MB | "
                      f"{speed_mb:.1f}MB/s | {eta_str}", end='', flush=True)
                
                if final:
                    print()  # New line when complete
    
    def list_downloaded_files(self):
        """List all downloaded files."""
        if self.use_temp:
            return self.temp_manager.list_temp_files()
        
        files = list(self.download_dir.glob('*'))
        if not files:
            print("No files downloaded yet.")
            return []
        
        print(f"\n📁 Downloaded files in {self.download_dir}:")
        for i, file in enumerate(files, 1):
            size = file.stat().st_size
            size_mb = size / (1024 * 1024)
            print(f"{i:2d}. {file.name} ({size_mb:.1f} MB)")
        
        return files
    
    def get_temp_info(self):
        """Get information about temp files if using temp mode."""
        if self.use_temp:
            return self.temp_manager.get_temp_dir_info()
        else:
            print("Not using temp mode. Use download_to_temp() or set use_temp=True")
            return None


def main():
    """Main function for command-line usage."""
    if len(sys.argv) < 2:
        print("Usage: python file_downloader.py <URL> [filename] [--temp] [--type <file_type>]")
        print("Example: python file_downloader.py https://example.com/file.pdf")
        print("Example: python file_downloader.py https://example.com/transcript.txt --temp --type transcripts")
        print("\nOptions:")
        print("  --temp          Download to temp directory")
        print("  --type <type>   File type: transcripts, notes, attachments, general")
        return
    
    url = sys.argv[1]
    filename = None
    use_temp = False
    file_type = "general"
    
    # Parse command line arguments
    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == "--temp":
            use_temp = True
        elif sys.argv[i] == "--type" and i + 1 < len(sys.argv):
            file_type = sys.argv[i + 1]
            i += 1
        elif not filename and not sys.argv[i].startswith("--"):
            filename = sys.argv[i]
        i += 1
    
    if use_temp:
        print(f"📁 Downloading to temp directory (type: {file_type})")
        downloader = FileDownloader(use_temp=True)
        result = downloader.download_file(url, filename, file_type=file_type)
    else:
        downloader = FileDownloader()
        result = downloader.download_file(url, filename)
    
    if result:
        print(f"\n🎉 File successfully downloaded to: {result}")
        downloader.list_downloaded_files()
    else:
        print("\n💥 Download failed. Please check the URL and try again.")


if __name__ == "__main__":
    main()
