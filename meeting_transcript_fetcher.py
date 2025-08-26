#!/usr/bin/env python3
"""
Meeting Transcript Fetcher for MeetingNotesAgent
Specialized module for fetching and managing meeting transcripts
"""

from file_downloader import FileDownloader
from temp_file_manager import TempFileManager
from pathlib import Path
import json
from datetime import datetime
import time


class MeetingTranscriptFetcher:
    def __init__(self):
        """Initialize the meeting transcript fetcher."""
        self.downloader = FileDownloader(use_temp=True)
        self.temp_manager = TempFileManager()
        
        # Supported transcript formats
        self.supported_formats = ['.txt', '.pdf', '.doc', '.docx', '.rtf', '.html', '.json']
    
    def fetch_transcript(self, url, meeting_id=None, metadata=None):
        """
        Fetch a meeting transcript from a URL and store it in temp.
        
        Args:
            url (str): URL to the meeting transcript
            meeting_id (str, optional): Unique meeting identifier
            metadata (dict, optional): Additional meeting metadata
            
        Returns:
            dict: Result information including file path and metadata
        """
        try:
            print(f"🎯 Fetching meeting transcript from: {url}")
            
            # Generate filename with meeting ID if provided
            if meeting_id:
                filename = f"meeting_{meeting_id}_transcript"
            else:
                filename = f"meeting_transcript_{int(time.time())}"
            
            # Download to temp directory
            result = self.downloader.download_file(
                url, 
                filename=filename, 
                file_type="transcripts"
            )
            
            if result:
                # Prepare result metadata
                file_info = {
                    'file_path': str(result),
                    'file_size': result.stat().st_size,
                    'download_time': datetime.now().isoformat(),
                    'url': url,
                    'meeting_id': meeting_id,
                    'metadata': metadata or {},
                    'status': 'success'
                }
                
                # Save metadata alongside the file
                metadata_file = result.with_suffix('.json')
                with open(metadata_file, 'w') as f:
                    json.dump(file_info, f, indent=2)
                
                print(f"✅ Transcript fetched successfully: {result}")
                return file_info
            else:
                return {
                    'status': 'failed',
                    'error': 'Download failed',
                    'url': url,
                    'meeting_id': meeting_id
                }
                
        except Exception as e:
            error_info = {
                'status': 'error',
                'error': str(e),
                'url': url,
                'meeting_id': meeting_id,
                'timestamp': datetime.now().isoformat()
            }
            print(f"❌ Error fetching transcript: {e}")
            return error_info
    
    def fetch_multiple_transcripts(self, urls, meeting_ids=None):
        """
        Fetch multiple meeting transcripts.
        
        Args:
            urls (list): List of URLs to fetch
            meeting_ids (list, optional): List of meeting IDs corresponding to URLs
            
        Returns:
            list: List of result dictionaries
        """
        if meeting_ids is None:
            meeting_ids = [None] * len(urls)
        
        results = []
        for i, (url, meeting_id) in enumerate(zip(urls, meeting_ids)):
            print(f"\n📥 Fetching transcript {i+1}/{len(urls)}")
            result = self.fetch_transcript(url, meeting_id)
            results.append(result)
            
            # Small delay between downloads
            if i < len(urls) - 1:
                time.sleep(1)
        
        return results
    
    def list_transcripts(self, include_metadata=True):
        """
        List all available transcripts.
        
        Args:
            include_metadata (bool): Whether to include metadata information
            
        Returns:
            list: List of transcript files with optional metadata
        """
        transcript_files = self.temp_manager.list_temp_files("transcripts")
        
        if include_metadata:
            enhanced_list = []
            for file_path in transcript_files:
                file_info = {
                    'file_path': str(file_path),
                    'file_name': file_path.name,
                    'file_size': file_path.stat().st_size,
                    'modified_time': datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
                    'metadata': None
                }
                
                # Try to load metadata if available
                metadata_file = file_path.with_suffix('.json')
                if metadata_file.exists():
                    try:
                        with open(metadata_file, 'r') as f:
                            file_info['metadata'] = json.load(f)
                    except:
                        pass
                
                enhanced_list.append(file_info)
            
            return enhanced_list
        
        return transcript_files
    
    def get_transcript_info(self, file_path):
        """
        Get detailed information about a specific transcript.
        
        Args:
            file_path (str or Path): Path to the transcript file
            
        Returns:
            dict: Detailed file information
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            return {'error': 'File not found'}
        
        # Basic file info
        file_info = {
            'file_path': str(file_path),
            'file_name': file_path.name,
            'file_size': file_path.stat().st_size,
            'file_size_mb': file_path.stat().st_size / (1024 * 1024),
            'created_time': datetime.fromtimestamp(file_path.stat().st_ctime).isoformat(),
            'modified_time': datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
            'metadata': None
        }
        
        # Try to load metadata
        metadata_file = file_path.with_suffix('.json')
        if metadata_file.exists():
            try:
                with open(metadata_file, 'r') as f:
                    file_info['metadata'] = json.load(f)
            except Exception as e:
                file_info['metadata_error'] = str(e)
        
        return file_info
    
    def cleanup_old_transcripts(self, days_old=7, dry_run=True):
        """
        Clean up old transcript files.
        
        Args:
            days_old (int): Age in days after which files are considered old
            dry_run (bool): If True, only show what would be deleted
            
        Returns:
            list: List of files that were/would be deleted
        """
        # Override the default cleanup time for transcripts
        temp_manager = TempFileManager(cleanup_after_hours=days_old * 24)
        return temp_manager.cleanup_old_files(dry_run=dry_run)
    
    def export_transcript_list(self, output_file=None):
        """
        Export a list of all transcripts to a file.
        
        Args:
            output_file (str, optional): Output file path. If None, uses default
            
        Returns:
            str: Path to the exported file
        """
        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"transcript_list_{timestamp}.json"
        
        transcripts = self.list_transcripts(include_metadata=True)
        
        export_data = {
            'export_time': datetime.now().isoformat(),
            'total_transcripts': len(transcripts),
            'transcripts': transcripts
        }
        
        output_path = Path(output_file)
        with open(output_path, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        print(f"📋 Transcript list exported to: {output_path}")
        return str(output_path)


def main():
    """Main function for testing the meeting transcript fetcher."""
    print("=== Meeting Transcript Fetcher Test ===\n")
    
    fetcher = MeetingTranscriptFetcher()
    
    # Test fetching a transcript
    print("=== Testing Transcript Fetch ===")
    test_url = "https://httpbin.org/robots.txt"
    result = fetcher.fetch_transcript(test_url, meeting_id="TEST_001", metadata={"type": "test"})
    
    print(f"\nResult: {json.dumps(result, indent=2)}")
    
    # List all transcripts
    print("\n=== Listing Transcripts ===")
    transcripts = fetcher.list_transcripts()
    print(f"Found {len(transcripts)} transcript(s)")
    
    # Show temp directory info
    print("\n=== Temp Directory Info ===")
    fetcher.temp_manager.get_temp_dir_info()
    
    # Test cleanup (dry run)
    print("\n=== Testing Cleanup (Dry Run) ===")
    fetcher.cleanup_old_transcripts(days_old=1, dry_run=True)


if __name__ == "__main__":
    main()
