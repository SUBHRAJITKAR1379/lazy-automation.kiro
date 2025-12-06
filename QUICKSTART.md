# Quick Start Guide

Get your File Organization Bot running in 2 minutes!

## Option 1: Full Installation (Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/file-organizer-bot.git
cd file-organizer-bot

# 2. Install dependencies
pip install -r requirements.txt

# 3. Install the package
pip install -e .

# 4. Run it!
file-organizer organize  # Organize existing files once
# OR
file-organizer watch     # Monitor in real-time
```

## Option 2: Standalone Script (No Installation)

```bash
# 1. Download the standalone script
# (Just download file_organizer_standalone.py)

# 2. Install watchdog
pip install watchdog

# 3. Run it!
python file_organizer_standalone.py organize
# OR
python file_organizer_standalone.py watch
```

## Usage Examples

### Organize Your Downloads Folder
```bash
file-organizer organize
```

### Watch Your Downloads Folder
```bash
file-organizer watch
```
Press `Ctrl+C` to stop.

### Organize a Custom Directory
```bash
file-organizer organize --path /path/to/folder
```

### Enable File Logging
```bash
file-organizer watch --log-file organizer.log
```

## What It Does

Before:
```
Downloads/
├── report.pdf
├── photo.jpg
├── video.mp4
├── song.mp3
└── archive.zip
```

After:
```
Downloads/
├── Documents/2025/Dec/report.pdf
├── Pictures/2025/Dec/photo.jpg
├── Videos/2025/Dec/video.mp4
├── Audio/2025/Dec/song.mp3
└── Archives/2025/Dec/archive.zip
```

## File Categories

| Category   | Extensions |
|------------|------------|
| Pictures   | jpg, jpeg, png, gif, bmp, svg, webp |
| Documents  | pdf, doc, docx, txt, rtf, odt, xls, xlsx, ppt, pptx |
| Videos     | mp4, avi, mkv, mov, wmv, flv, webm |
| Audio      | mp3, wav, flac, aac, ogg, m4a |
| Archives   | zip, rar, tar, gz, 7z, bz2 |
| Others     | Everything else |

## Safety Features

✅ Never overwrites files (adds numeric suffixes)  
✅ Handles locked files (retries automatically)  
✅ Skips hidden files and symlinks  
✅ Validates paths before operating  
✅ Logs all operations  

## Need Help?

```bash
file-organizer --help
file-organizer watch --help
file-organizer organize --help
```

## Troubleshooting

**"Downloads folder not found"**
- Use `--path` to specify a custom directory

**"Permission denied"**
- Run with appropriate permissions
- Check file isn't locked by another program

**"Module not found"**
- Make sure you installed dependencies: `pip install -r requirements.txt`

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check out [examples/](examples/) for programmatic usage
- See [docs/blog-post-draft.md](docs/blog-post-draft.md) for the full story

---

**Happy organizing! 🎉**
