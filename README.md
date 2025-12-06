# File Organization Bot 🤖📁

Automatically organize your Downloads folder by file type and date. Never manually sort files again!

## 🎯 Problem

Downloads folders get messy fast. Images, PDFs, videos, and archives pile up, making it hard to find what you need. Manual organization is tedious and time-consuming.

## ✨ Solution

File Organization Bot automatically categorizes and organizes files into a clean directory structure:

```
Downloads/
├── Pictures/
│   └── 2025/
│       └── Dec/
│           ├── photo1.jpg
│           └── screenshot.png
├── Documents/
│   └── 2025/
│       └── Dec/
│           ├── report.pdf
│           └── notes.txt
├── Videos/
│   └── 2025/
│       └── Dec/
│           └── tutorial.mp4
└── Archives/
    └── 2025/
        └── Dec/
            └── backup.zip
```

## 🚀 Features

- **Real-time Monitoring**: Watch mode automatically organizes new files as they appear
- **Batch Processing**: Organize mode cleans up existing files in one go
- **Smart Categorization**: Recognizes 30+ file types across 6 categories
- **Date-based Organization**: Files organized by year and month
- **Duplicate Handling**: Safely renames duplicates (file.pdf → file(1).pdf)
- **Cross-platform**: Works on Windows, macOS, and Linux
- **Comprehensive Logging**: Track all operations with console and optional file logging
- **Safe Operations**: Never overwrites files, handles errors gracefully

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Install from Source

```bash
# Clone the repository
git clone https://github.com/yourusername/file-organizer-bot.git
cd file-organizer-bot

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

## 🎮 Usage

### Watch Mode (Real-time)

Monitor your Downloads folder and automatically organize new files:

```bash
file-organizer watch
```

Watch a custom directory:

```bash
file-organizer watch --path /path/to/folder
```

Enable file logging:

```bash
file-organizer watch --log-file organizer.log
```

### Organize Mode (One-time)

Organize all existing files in your Downloads folder:

```bash
file-organizer organize
```

Organize a custom directory:

```bash
file-organizer organize --path /path/to/folder
```

### Stop Watching

Press `Ctrl+C` to stop watch mode gracefully.

## 📂 File Categories

| Category   | Extensions |
|------------|------------|
| Pictures   | jpg, jpeg, png, gif, bmp, svg, webp |
| Documents  | pdf, doc, docx, txt, rtf, odt, xls, xlsx, ppt, pptx |
| Videos     | mp4, avi, mkv, mov, wmv, flv, webm |
| Audio      | mp3, wav, flac, aac, ogg, m4a |
| Archives   | zip, rar, tar, gz, 7z, bz2 |
| Others     | All unrecognized file types |

## 🛡️ Safety Features

- **No Overwrites**: Duplicate files are renamed with numeric suffixes
- **Error Handling**: Gracefully handles permission errors, locked files, and disk space issues
- **Retry Logic**: Automatically retries locked files with exponential backoff
- **Symlink Protection**: Skips symlinks to avoid infinite loops
- **Hidden File Handling**: Ignores hidden files (starting with .)
- **Validation**: Checks paths and prevents circular references

## 📊 Example Output

```
2025-12-04 10:30:15 - file_organizer - INFO - Starting file watcher on: /Users/you/Downloads
2025-12-04 10:30:15 - file_organizer - INFO - Press Ctrl+C to stop watching...
2025-12-04 10:30:22 - file_organizer - INFO - Detected file: 'report.pdf' -> Category: Documents
2025-12-04 10:30:22 - file_organizer - INFO - Moved: '/Users/you/Downloads/report.pdf' -> '/Users/you/Downloads/Documents/2025/Dec/report.pdf'
2025-12-04 10:30:35 - file_organizer - INFO - Detected file: 'photo.jpg' -> Category: Pictures
2025-12-04 10:30:35 - file_organizer - INFO - Duplicate detected: 'photo.jpg' renamed to 'photo(1).jpg'
2025-12-04 10:30:35 - file_organizer - INFO - Moved: '/Users/you/Downloads/photo.jpg' -> '/Users/you/Downloads/Pictures/2025/Dec/photo(1).jpg'
```

## 🧪 Development

### Running Tests

```bash
# Install development dependencies
pip install -r requirements.txt

# Run all tests
pytest

# Run with coverage
pytest --cov=src/file_organizer --cov-report=html

# Run property-based tests
pytest tests/test_properties.py -v
```

### Project Structure

```
file-organizer-bot/
├── src/
│   └── file_organizer/
│       ├── __init__.py
│       ├── categorizer.py      # File type categorization
│       ├── file_mover.py        # File movement operations
│       ├── organizer.py         # Core organization logic
│       ├── watcher.py           # Real-time file monitoring
│       ├── logger.py            # Logging configuration
│       └── cli.py               # Command-line interface
├── tests/
│   ├── test_categorizer.py
│   ├── test_file_mover.py
│   ├── test_organizer.py
│   ├── test_properties.py       # Property-based tests
│   └── conftest.py
├── requirements.txt
├── setup.py
└── README.md
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with [Kiro.dev](https://kiro.dev) - AI-powered development assistant
- Uses [watchdog](https://github.com/gorakhargosh/watchdog) for file system monitoring
- Property-based testing with [Hypothesis](https://hypothesis.readthedocs.io/)

## 📧 Contact

Your Name - [@yourtwitter](https://twitter.com/yourtwitter)

Project Link: [https://github.com/yourusername/file-organizer-bot](https://github.com/yourusername/file-organizer-bot)

---

**Made with ❤️ and Kiro.dev**
