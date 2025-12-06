#!/usr/bin/env python3
"""
File Organization Bot - Standalone Version

This is a single-file version of the File Organization Bot that can be run
without installation. Simply download this file and run it with Python 3.8+.

Usage:
    python file_organizer_standalone.py watch
    python file_organizer_standalone.py organize
    python file_organizer_standalone.py watch --path /custom/path
    python file_organizer_standalone.py organize --log-file organizer.log

Requirements:
    pip install watchdog
"""

import os
import sys
import time
import shutil
import logging
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, Set, Optional
from threading import Timer

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
except ImportError:
    print("Error: watchdog library not found. Install it with: pip install watchdog")
    sys.exit(1)


# ============================================================================
# FileCategorizer
# ============================================================================

class FileCategorizer:
    """Categorizes files based on their extension."""
    
    CATEGORIES: Dict[str, Set[str]] = {
        "Pictures": {"jpg", "jpeg", "png", "gif", "bmp", "svg", "webp"},
        "Documents": {"pdf", "doc", "docx", "txt", "rtf", "odt", "xls", "xlsx", "ppt", "pptx"},
        "Videos": {"mp4", "avi", "mkv", "mov", "wmv", "flv", "webm"},
        "Audio": {"mp3", "wav", "flac", "aac", "ogg", "m4a"},
        "Archives": {"zip", "rar", "tar", "gz", "7z", "bz2"},
    }
    
    def __init__(self):
        self._extension_to_category: Dict[str, str] = {}
        for category, extensions in self.CATEGORIES.items():
            for ext in extensions:
                self._extension_to_category[ext.lower()] = category
    
    def get_category(self, file_path: Path) -> str:
        extension = file_path.suffix.lstrip('.').lower()
        if not extension:
            return "Others"
        return self._extension_to_category.get(extension, "Others")


# ============================================================================
# FileMover
# ============================================================================

class FileMover:
    """Handles file movement operations with duplicate detection."""
    
    def __init__(self, logger: logging.Logger):
        self.logger = logger
    
    def create_destination_path(self, base_dir: Path, category: str, file_date: datetime) -> Path:
        year = file_date.strftime("%Y")
        month = file_date.strftime("%b")
        destination_dir = base_dir / category / year / month
        destination_dir.mkdir(parents=True, exist_ok=True)
        return destination_dir
    
    def handle_duplicate(self, destination: Path) -> Path:
        if not destination.exists():
            return destination
        
        stem = destination.stem
        suffix = destination.suffix
        parent = destination.parent
        
        counter = 1
        while True:
            new_name = f"{stem}({counter}){suffix}"
            new_path = parent / new_name
            if not new_path.exists():
                return new_path
            counter += 1
    
    def move_file(self, source: Path, destination_dir: Path, category: str, file_date: datetime) -> Path:
        dest_folder = self.create_destination_path(destination_dir, category, file_date)
        intended_destination = dest_folder / source.name
        final_destination = self.handle_duplicate(intended_destination)
        
        if final_destination != intended_destination:
            self.logger.info(f"Duplicate detected: '{source.name}' renamed to '{final_destination.name}'")
        
        shutil.move(str(source), str(final_destination))
        self.logger.info(f"Moved: '{source}' -> '{final_destination}'")
        
        return final_destination


# ============================================================================
# FileOrganizer
# ============================================================================

class FileOrganizer:
    """Coordinates file categorization and movement operations."""
    
    def __init__(self, base_path: Path, categorizer: FileCategorizer, 
                 file_mover: FileMover, logger: logging.Logger):
        self.base_path = Path(base_path)
        self.categorizer = categorizer
        self.file_mover = file_mover
        self.logger = logger
        
        if not self.base_path.exists():
            raise ValueError(f"Base path does not exist: {self.base_path}")
        if not self.base_path.is_dir():
            raise ValueError(f"Base path is not a directory: {self.base_path}")
    
    def _get_file_date(self, file_path: Path) -> datetime:
        timestamp = os.path.getmtime(file_path)
        return datetime.fromtimestamp(timestamp)
    
    def _should_process_file(self, file_path: Path) -> bool:
        if not file_path.is_file():
            return False
        if file_path.name.startswith('.'):
            return False
        if file_path.is_symlink():
            self.logger.debug(f"Skipping symlink: {file_path}")
            return False
        if file_path.name.endswith('.tmp') or file_path.name.endswith('.temp'):
            return False
        return True
    
    def organize_file(self, file_path: Path, max_retries: int = 3) -> bool:
        try:
            if not self._should_process_file(file_path):
                return False
            
            if not file_path.exists():
                self.logger.warning(f"File no longer exists: {file_path}")
                return False
            
            category = self.categorizer.get_category(file_path)
            self.logger.info(f"Detected file: '{file_path.name}' -> Category: {category}")
            
            file_date = self._get_file_date(file_path)
            
            for attempt in range(max_retries):
                try:
                    self.file_mover.move_file(file_path, self.base_path, category, file_date)
                    return True
                except PermissionError as e:
                    if attempt < max_retries - 1:
                        wait_time = 2 ** attempt
                        self.logger.warning(
                            f"File locked, retrying in {wait_time}s (attempt {attempt + 1}/{max_retries}): {file_path}"
                        )
                        time.sleep(wait_time)
                    else:
                        self.logger.error(f"Permission denied after {max_retries} attempts for '{file_path}': {e}")
                        return False
                except OSError as e:
                    self.logger.error(f"Failed to move '{file_path}': {e}")
                    return False
                    
        except Exception as e:
            self.logger.error(f"Unexpected error organizing '{file_path}': {e}")
            return False
    
    def organize_all(self) -> int:
        self.logger.info(f"Starting organization of: {self.base_path}")
        
        count = 0
        files = [f for f in self.base_path.iterdir() if f.is_file()]
        
        self.logger.info(f"Found {len(files)} files to process")
        
        for file_path in files:
            if self.organize_file(file_path):
                count += 1
        
        self.logger.info(f"Organization complete. Processed {count} files.")
        return count


# ============================================================================
# FileWatcher
# ============================================================================

class FileEventHandler(FileSystemEventHandler):
    """Handles file system events."""
    
    def __init__(self, organizer: FileOrganizer, logger: logging.Logger, debounce_seconds: float = 1.0):
        super().__init__()
        self.organizer = organizer
        self.logger = logger
        self.debounce_seconds = debounce_seconds
        self._pending_timers = {}
    
    def on_created(self, event):
        if event.is_directory:
            return
        
        file_path = Path(event.src_path)
        
        if file_path in self._pending_timers:
            self._pending_timers[file_path].cancel()
        
        timer = Timer(self.debounce_seconds, self._process_file, args=[file_path])
        self._pending_timers[file_path] = timer
        timer.start()
    
    def _process_file(self, file_path: Path):
        try:
            self.organizer.organize_file(file_path)
        finally:
            if file_path in self._pending_timers:
                del self._pending_timers[file_path]


class FileWatcher:
    """Monitors a directory for new files."""
    
    def __init__(self, watch_path: Path, organizer: FileOrganizer, 
                 logger: logging.Logger, debounce_seconds: float = 1.0):
        self.watch_path = Path(watch_path)
        self.organizer = organizer
        self.logger = logger
        self.debounce_seconds = debounce_seconds
        
        if not self.watch_path.exists():
            raise ValueError(f"Watch path does not exist: {self.watch_path}")
        if not self.watch_path.is_dir():
            raise ValueError(f"Watch path is not a directory: {self.watch_path}")
        
        self.event_handler = FileEventHandler(organizer, self.logger, debounce_seconds)
        self.observer = Observer()
    
    def start(self) -> None:
        self.logger.info(f"Starting file watcher on: {self.watch_path}")
        self.logger.info("Press Ctrl+C to stop watching...")
        
        self.observer.schedule(self.event_handler, str(self.watch_path), recursive=False)
        self.observer.start()
        
        try:
            while self.observer.is_alive():
                self.observer.join(timeout=1)
        except KeyboardInterrupt:
            self.logger.info("Received stop signal")
            self.stop()
    
    def stop(self) -> None:
        self.logger.info("Stopping file watcher...")
        self.observer.stop()
        self.observer.join()
        self.logger.info("File watcher stopped")


# ============================================================================
# Logger Setup
# ============================================================================

def setup_logger(name: str = "file_organizer", log_file: Optional[Path] = None) -> logging.Logger:
    """Configure and return a logger instance."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    
    formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    if log_file:
        try:
            log_file.parent.mkdir(parents=True, exist_ok=True)
            file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
            file_handler.setLevel(logging.INFO)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
            logger.info(f"File logging enabled: {log_file}")
        except Exception as e:
            logger.error(f"Failed to enable file logging: {e}")
    
    return logger


# ============================================================================
# CLI
# ============================================================================

def get_default_downloads_path() -> Path:
    """Get the default Downloads folder path."""
    downloads_path = Path.home() / "Downloads"
    if not downloads_path.exists():
        raise FileNotFoundError(
            f"Default Downloads folder not found: {downloads_path}\n"
            "Please specify a custom path using --path"
        )
    return downloads_path


def run_watch_mode(args: argparse.Namespace) -> int:
    """Run the bot in watch mode."""
    try:
        log_file = Path(args.log_file) if args.log_file else None
        logger = setup_logger(log_file=log_file)
        
        watch_path = Path(args.path) if args.path else get_default_downloads_path()
        
        if not watch_path.exists():
            print(f"Error: Path does not exist: {watch_path}", file=sys.stderr)
            return 1
        
        logger.info("=" * 60)
        logger.info("File Organization Bot - Watch Mode")
        logger.info("=" * 60)
        logger.info(f"Monitoring: {watch_path}")
        
        categorizer = FileCategorizer()
        file_mover = FileMover(logger)
        organizer = FileOrganizer(watch_path, categorizer, file_mover, logger)
        watcher = FileWatcher(watch_path, organizer, logger)
        
        watcher.start()
        return 0
        
    except KeyboardInterrupt:
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def run_organize_mode(args: argparse.Namespace) -> int:
    """Run the bot in organize mode."""
    try:
        log_file = Path(args.log_file) if args.log_file else None
        logger = setup_logger(log_file=log_file)
        
        organize_path = Path(args.path) if args.path else get_default_downloads_path()
        
        if not organize_path.exists():
            print(f"Error: Path does not exist: {organize_path}", file=sys.stderr)
            return 1
        
        logger.info("=" * 60)
        logger.info("File Organization Bot - Organize Mode")
        logger.info("=" * 60)
        logger.info(f"Organizing: {organize_path}")
        
        categorizer = FileCategorizer()
        file_mover = FileMover(logger)
        organizer = FileOrganizer(organize_path, categorizer, file_mover, logger)
        
        count = organizer.organize_all()
        
        logger.info("=" * 60)
        logger.info(f"Successfully organized {count} files")
        logger.info("=" * 60)
        
        return 0
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        prog="file-organizer",
        description="Automatically organize files by type and date",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python file_organizer_standalone.py watch
  python file_organizer_standalone.py organize
  python file_organizer_standalone.py watch --path /path/to/folder
  python file_organizer_standalone.py organize --log-file organizer.log
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    watch_parser = subparsers.add_parser('watch', help='Monitor directory in real-time')
    watch_parser.add_argument('--path', type=str, help='Directory to monitor (default: ~/Downloads)')
    watch_parser.add_argument('--log-file', type=str, help='Enable file logging')
    
    organize_parser = subparsers.add_parser('organize', help='Organize all existing files')
    organize_parser.add_argument('--path', type=str, help='Directory to organize (default: ~/Downloads)')
    organize_parser.add_argument('--log-file', type=str, help='Enable file logging')
    
    args = parser.parse_args()
    
    if args.command == 'watch':
        sys.exit(run_watch_mode(args))
    elif args.command == 'organize':
        sys.exit(run_organize_mode(args))
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
