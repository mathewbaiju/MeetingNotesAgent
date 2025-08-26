#!/usr/bin/env python3
"""
Temp File Manager for MeetingNotesAgent
Handles temporary file operations with Mac-optimized temp directory management
"""

import os
import tempfile
import shutil
from pathlib import Path
from datetime import datetime
import time


class TempFileManager:
    def __init__(self, temp_dir=None, cleanup_after_hours=24):
        """
        Initialize the temp file manager.
        
        Args:
            temp_dir (str, optional): Custom temp directory. If None, uses system temp
            cleanup_after_hours (int): Hours after which temp files are considered stale
        """
        if temp_dir is None:
            # Use Mac system temp directory
            self.temp_dir = Path(tempfile.gettempdir()) / "MeetingNotesAgent"
        else:
            self.temp_dir = Path(temp_dir)
        
        self.cleanup_after_hours = cleanup_after_hours
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories for different file types
        self.transcripts_dir = self.temp_dir / "transcripts"
        self.notes_dir = self.temp_dir / "notes"
        self.attachments_dir = self.temp_dir / "attachments"
        
        for directory in [self.transcripts_dir, self.notes_dir, self.attachments_dir]:
            directory.mkdir(exist_ok=True)
    
    def get_temp_path(self, filename, file_type="general"):
        """
        Get a temporary file path.
        
        Args:
            filename (str): Original filename
            file_type (str): Type of file (transcripts, notes, attachments, general)
            
        Returns:
            Path: Full path to the temporary file
        """
        # Add timestamp to avoid conflicts
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        name, ext = os.path.splitext(filename)
        temp_filename = f"{name}_{timestamp}{ext}"
        
        if file_type == "transcripts":
            return self.transcripts_dir / temp_filename
        elif file_type == "notes":
            return self.notes_dir / temp_filename
        elif file_type == "attachments":
            return self.attachments_dir / temp_filename
        else:
            return self.temp_dir / temp_filename
    
    def cleanup_old_files(self, dry_run=False):
        """
        Clean up old temporary files.
        
        Args:
            dry_run (bool): If True, only show what would be deleted
            
        Returns:
            list: List of files that were/would be deleted
        """
        cutoff_time = time.time() - (self.cleanup_after_hours * 3600)
        files_to_delete = []
        
        for file_path in self.temp_dir.rglob('*'):
            if file_path.is_file():
                if file_path.stat().st_mtime < cutoff_time:
                    files_to_delete.append(file_path)
        
        if not dry_run:
            for file_path in files_to_delete:
                try:
                    file_path.unlink()
                    print(f"🗑️  Deleted: {file_path}")
                except Exception as e:
                    print(f"❌ Failed to delete {file_path}: {e}")
        else:
            print(f"📋 Would delete {len(files_to_delete)} old files:")
            for file_path in files_to_delete:
                print(f"   {file_path}")
        
        return files_to_delete
    
    def list_temp_files(self, file_type=None):
        """
        List temporary files.
        
        Args:
            file_type (str, optional): Filter by file type
            
        Returns:
            list: List of file paths
        """
        if file_type == "transcripts":
            search_dir = self.transcripts_dir
        elif file_type == "notes":
            search_dir = self.notes_dir
        elif file_type == "attachments":
            search_dir = self.attachments_dir
        else:
            search_dir = self.temp_dir
        
        files = list(search_dir.rglob('*'))
        files = [f for f in files if f.is_file()]
        
        if not files:
            print(f"📁 No files found in {search_dir}")
            return []
        
        print(f"\n📁 Files in {search_dir}:")
        for i, file_path in enumerate(files, 1):
            size = file_path.stat().st_size
            size_mb = size / (1024 * 1024)
            mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
            print(f"{i:2d}. {file_path.name} ({size_mb:.1f} MB) - {mtime.strftime('%Y-%m-%d %H:%M:%S')}")
        
        return files
    
    def get_temp_dir_info(self):
        """Get information about the temp directory."""
        total_size = sum(f.stat().st_size for f in self.temp_dir.rglob('*') if f.is_file())
        total_size_mb = total_size / (1024 * 1024)
        file_count = len([f for f in self.temp_dir.rglob('*') if f.is_file()])
        
        print(f"\n📊 Temp Directory Info:")
        print(f"   Location: {self.temp_dir}")
        print(f"   Total Size: {total_size_mb:.1f} MB")
        print(f"   File Count: {file_count}")
        print(f"   Cleanup After: {self.cleanup_after_hours} hours")
        
        return {
            'location': str(self.temp_dir),
            'total_size_mb': total_size_mb,
            'file_count': file_count,
            'cleanup_after_hours': self.cleanup_after_hours
        }


def main():
    """Main function for testing the temp file manager."""
    print("=== Temp File Manager Test ===")
    
    # Initialize temp file manager
    temp_manager = TempFileManager()
    
    # Show temp directory info
    temp_manager.get_temp_dir_info()
    
    # List any existing files
    temp_manager.list_temp_files()
    
    # Test cleanup (dry run)
    print("\n=== Testing Cleanup (Dry Run) ===")
    temp_manager.cleanup_old_files(dry_run=True)


if __name__ == "__main__":
    main()
