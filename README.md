# lazy-automation.kiro
A simple script to automate boring digital tasks as part of Kiro Week 2 Challenge.

# Kiro Week 2 — Lazy Automation metadata

Author: Subhrajit Kar  
Challenge: Kiro Week 2 - Lazy Automation  
Project: lazy-automation-kiro

Description:
A Python tool to automatically organize a target folder (Downloads recommended) into categorized subfolders (PDFs, Images, Videos, Docs, Archives, Audio, Others). Includes dry-run, duplicate detection (by SHA-1), and safe-renaming to avoid overwrites.

Features:
- Dry-run mode to review proposed changes
- Duplicate detection using file SHA-1 (removes duplicates safely)
- Safe renaming to avoid overwriting files
- Cross-platform (Linux, macOS, Windows)

## Usage

1. Clone the repo
2. Inspect the code
3. Dry run (recommended):
```bash
python organize_files.py --path "~/Downloads" --dry-run
