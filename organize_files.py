#!/usr/bin/env python3
"""
lazy-automation-kiro
Organize a target folder (Downloads recommended) into type-based subfolders.

Usage:
    python organize_files.py --path "/home/yourname/Downloads" --dry-run
"""

from pathlib import Path
import shutil
import argparse
import time
import hashlib
import sys

# Configure categories here
CATEGORY_MAP = {
    "PDFs": [".pdf"],
    "Images": [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff", ".webp", ".svg"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov", ".webm"],
    "Docs": [".doc", ".docx", ".ppt", ".pptx", ".xls", ".xlsx", ".txt", ".md", ".csv"],
    "Archives": [".zip", ".tar", ".gz", ".rar", ".7z"],
    "Audio": [".mp3", ".wav", ".flac", ".m4a", ".aac"],
}

def compute_hash(path: Path, blocksize: int = 65536) -> str:
    h = hashlib.sha1()
    with path.open("rb") as f:
        while True:
            chunk = f.read(blocksize)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()

def categorize_file(path: Path) -> str:
    ext = path.suffix.lower()
    for cat, exts in CATEGORY_MAP.items():
        if ext in exts:
            return cat
    return "Others"

def safe_name(dest_dir: Path, name: str) -> Path:
    dest = dest_dir / name
    if not dest.exists():
        return dest
    base = dest.stem
    ext = dest.suffix
    timestamp = int(time.time())
    new_name = f"{base}_{timestamp}{ext}"
    return dest_dir / new_name

def organize(folder: Path, dry_run: bool = True, copy_only: bool = False, verbose: bool = True):
    if not folder.exists() or not folder.is_dir():
        raise ValueError(f"{folder} is not a valid directory")

    summary = {"moved": 0, "copied": 0, "skipped": 0, "removed_duplicates": 0, "errors": 0}
    created_dirs = set()

    for p in list(folder.iterdir()):
        try:
            # skip directories created by this tool (so we don't recurse)
            if p.is_dir():
                if p.name in list(CATEGORY_MAP.keys()) + ["Others"]:
                    if verbose:
                        print(f"Skipping folder: {p.name}")
                    summary["skipped"] += 1
                    continue
                else:
                    # don't enter nested folders
                    if verbose:
                        print(f"Skipping nested folder: {p.name}")
                    summary["skipped"] += 1
                    continue

            cat = categorize_file(p)
            target_dir = folder / cat

            if dry_run:
                print(f"[DRY-RUN] {p.name} -> {cat}/")
                summary["skipped"] += 1
                continue

            if target_dir.name not in created_dirs:
                target_dir.mkdir(exist_ok=True)
                created_dirs.add(target_dir.name)

            dest = target_dir / p.name
            if dest.exists():
                # if identical then remove source to deduplicate
                if compute_hash(dest) == compute_hash(p):
                    print(f"Duplicate detected. Removing source: {p.name}")
                    p.unlink()
                    summary["removed_duplicates"] += 1
                    continue
                # else choose a safe name
                dest = safe_name(target_dir, p.name)

            if copy_only:
                shutil.copy2(str(p), str(dest))
                summary["copied"] += 1
                if verbose:
                    print(f"Copied: {p.name} -> {dest.relative_to(folder)}")
            else:
                shutil.move(str(p), str(dest))
                summary["moved"] += 1
                if verbose:
                    print(f"Moved: {p.name} -> {dest.relative_to(folder)}")

        except Exception as e:
            print(f"Error handling {p}: {e}", file=sys.stderr)
            summary["errors"] += 1

    return summary

def parse_args():
    parser = argparse.ArgumentParser(description="Organize a folder by file types safely.")
    parser.add_argument("--path", "-p", required=True, help="Target folder to organize (e.g., ~/Downloads)")
    parser.add_argument("--dry-run", action="store_true", help="Show what would happen without moving files")
    parser.add_argument("--copy-only", action="store_true", help="Copy files instead of moving")
    parser.add_argument("--no-verbose", action="store_true", help="Minimize output")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    folder = Path(args.path).expanduser().resolve()
    if args.no_verbose:
        verbose = False
    else:
        verbose = True

    print(f"Organizing folder: {folder}")
    result = organize(folder, dry_run=args.dry_run, copy_only=args.copy_only, verbose=verbose)
    print("Result:", result)
