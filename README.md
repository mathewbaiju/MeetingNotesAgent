# MeetingNotesAgent

Automatically fetch meeting transcripts from URLs and generate meeting notes based on templates. Built with Mac optimization and comprehensive file management.

## 🚀 Features

### Core Functionality
- **URL-based transcript fetching** with automatic download and organization
- **Temp file management** with Mac-optimized directory structure
- **Progress tracking** with visual progress bars and ETA
- **Meeting metadata tracking** for organized transcript management
- **Automatic cleanup** of old temporary files
- **Multiple file format support** (txt, pdf, doc, docx, rtf, html, json)

### File Management
- **Organized temp directories** for transcripts, notes, and attachments
- **Timestamp-based naming** to avoid file conflicts
- **Metadata storage** alongside downloaded files
- **Export functionality** for transcript lists and reports

## 📁 Project Structure

```
MeetingNotesAgent/
├── file_downloader.py           # Main file downloader with temp support
├── temp_file_manager.py         # Mac-optimized temp file management
├── meeting_transcript_fetcher.py # Specialized transcript fetching
├── example_usage.py             # Comprehensive usage examples
├── requirements.txt             # Python dependencies
├── README.md                    # This documentation
└── Temp Files/                  # Local temp files directory
```

## 🛠️ Installation

### Prerequisites
- Python 3.6+
- macOS (optimized for Mac development)
- Git

### Setup
1. **Clone the repository:**
   ```bash
   git clone https://github.com/mathewbaiju/MeetingNotesAgent.git
   cd MeetingNotesAgent
   ```

2. **Install dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```

## 📖 Usage

### Command Line Interface

#### Basic File Download
```bash
# Download to Downloads folder
python3 file_downloader.py https://example.com/transcript.txt

# Download with custom filename
python3 file_downloader.py https://example.com/transcript.txt "meeting_notes.txt"
```

#### Temp File Downloads
```bash
# Download to temp directory (transcripts)
python3 file_downloader.py https://example.com/transcript.txt --temp --type transcripts

# Download to temp directory (notes)
python3 file_downloader.py https://example.com/notes.pdf --temp --type notes

# Download to temp directory (attachments)
python3 file_downloader.py https://example.com/attachment.docx --temp --type attachments
```

### Programmatic Usage

#### File Downloader
```python
from file_downloader import FileDownloader

# Initialize downloader
downloader = FileDownloader()

# Download to regular Downloads folder
result = downloader.download_file("https://example.com/transcript.pdf")

# Download to temp directory
temp_result = downloader.download_to_temp("https://example.com/transcript.txt", file_type="transcripts")

# Fetch and download (main method for transcripts)
transcript = downloader.fetch_and_download("https://example.com/transcript.txt", file_type="transcripts")
```

#### Temp File Manager
```python
from temp_file_manager import TempFileManager

# Initialize temp manager
temp_manager = TempFileManager()

# Get temp file path
temp_path = temp_manager.get_temp_path("transcript.txt", file_type="transcripts")

# List temp files
transcripts = temp_manager.list_temp_files("transcripts")

# Clean up old files
temp_manager.cleanup_old_files(dry_run=True)  # Show what would be deleted
temp_manager.cleanup_old_files(dry_run=False)  # Actually delete old files
```

#### Meeting Transcript Fetcher
```python
from meeting_transcript_fetcher import MeetingTranscriptFetcher

# Initialize fetcher
fetcher = MeetingTranscriptFetcher()

# Fetch single transcript
result = fetcher.fetch_transcript(
    "https://example.com/transcript.txt",
    meeting_id="MEETING_001",
    metadata={"type": "weekly_standup", "participants": 5}
)

# Fetch multiple transcripts
urls = [
    "https://example.com/transcript1.txt",
    "https://example.com/transcript2.txt"
]
meeting_ids = ["MEETING_001", "MEETING_002"]
results = fetcher.fetch_multiple_transcripts(urls, meeting_ids)

# List all transcripts with metadata
transcripts = fetcher.list_transcripts(include_metadata=True)

# Export transcript list
export_path = fetcher.export_transcript_list()
```

## 🔧 Configuration

### Temp Directory Structure
The system automatically creates organized temp directories:
```
/var/folders/.../MeetingNotesAgent/
├── transcripts/          # Meeting transcripts
├── notes/               # Generated notes
├── attachments/         # Meeting attachments
└── general/             # Other files
```

### File Type Categories
- **transcripts**: Meeting transcript files
- **notes**: Generated meeting notes
- **attachments**: Meeting-related attachments
- **general**: Other downloaded files

### Cleanup Settings
- **Default cleanup**: 24 hours
- **Transcript cleanup**: 7 days (configurable)
- **Automatic cleanup**: Configurable via TempFileManager

## 📊 Examples

### Complete Workflow Example
```python
from meeting_transcript_fetcher import MeetingTranscriptFetcher

# 1. Initialize the fetcher
fetcher = MeetingTranscriptFetcher()

# 2. Fetch a meeting transcript
transcript = fetcher.fetch_transcript(
    "https://meeting-service.com/transcript/12345",
    meeting_id="WEEKLY_2024_001",
    metadata={
        "type": "weekly_standup",
        "date": "2024-01-15",
        "participants": ["Alice", "Bob", "Charlie"],
        "duration": "45 minutes"
    }
)

# 3. List all available transcripts
all_transcripts = fetcher.list_transcripts()

# 4. Get detailed info about a specific transcript
transcript_info = fetcher.get_transcript_info(transcript['file_path'])

# 5. Export transcript list for reporting
export_path = fetcher.export_transcript_list("weekly_report.json")

# 6. Clean up old files (dry run first)
fetcher.cleanup_old_transcripts(days_old=30, dry_run=True)
```

### Running Examples
```bash
# Test temp file manager
python3 temp_file_manager.py

# Test file downloader
python3 file_downloader.py https://httpbin.org/robots.txt --temp --type transcripts

# Test meeting transcript fetcher
python3 meeting_transcript_fetcher.py

# Run comprehensive examples
python3 example_usage.py
```

## 🧪 Testing

### Test URLs
The examples use `httpbin.org` for testing:
- `https://httpbin.org/robots.txt` - Simple text file
- `https://httpbin.org/json` - JSON data
- `https://httpbin.org/xml` - XML data
- `https://httpbin.org/html` - HTML content
- `https://httpbin.org/bytes/1024` - Binary data

### Verification Commands
```bash
# Check temp directory info
python3 -c "from temp_file_manager import TempFileManager; TempFileManager().get_temp_dir_info()"

# List downloaded files
python3 -c "from file_downloader import FileDownloader; FileDownloader(use_temp=True).list_downloaded_files()"

# Test download functionality
python3 file_downloader.py https://httpbin.org/robots.txt --temp --type transcripts
```

## 🔍 Troubleshooting

### Common Issues

#### Import Errors
```bash
# Ensure dependencies are installed
pip3 install -r requirements.txt

# Check Python version
python3 --version  # Should be 3.6+
```

#### Permission Issues
```bash
# Check temp directory permissions
ls -la /var/folders/*/MeetingNotesAgent/

# Create temp directory manually if needed
mkdir -p /tmp/MeetingNotesAgent
```

#### Network Issues
```bash
# Test network connectivity
curl -I https://httpbin.org/robots.txt

# Check proxy settings if behind corporate firewall
export HTTP_PROXY=http://proxy.company.com:8080
export HTTPS_PROXY=http://proxy.company.com:8080
```

### Debug Mode
```python
# Enable verbose logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Test individual components
from temp_file_manager import TempFileManager
temp_manager = TempFileManager()
temp_manager.get_temp_dir_info()
```

## 🤝 Contributing

### Development Workflow
1. **Create feature branch:**
   ```bash
   git checkout -b feature-name
   ```

2. **Make changes and test:**
   ```bash
   python3 -m pytest  # If tests exist
   python3 example_usage.py
   ```

3. **Commit changes:**
   ```bash
   git add .
   git commit -m 'Add feature description'
   ```

4. **Push and create PR:**
   ```bash
   git push origin feature-name
   # Create Pull Request on GitHub
   ```

### Code Style
- Follow PEP 8 Python style guidelines
- Use descriptive variable and function names
- Include docstrings for all public methods
- Add type hints where appropriate

## 📝 License

This project is open source and available under the MIT License.

## 🆘 Support

### Getting Help
- **Issues**: Create an issue on GitHub for bugs or feature requests
- **Documentation**: Check this README and inline code comments
- **Examples**: Run `python3 example_usage.py` for working examples

### System Requirements
- **OS**: macOS (optimized), Linux/Windows (compatible)
- **Python**: 3.6+ (3.8+ recommended)
- **Memory**: 100MB+ available RAM
- **Storage**: 1GB+ available disk space for temp files

### Performance Notes
- **Download speed**: Depends on network and file size
- **Temp storage**: Automatically managed with cleanup
- **Memory usage**: Minimal for most operations
- **File handling**: Optimized for Mac file system

---

**Built with ❤️ for Technical Program Managers who need efficient meeting transcript management**
