
(You may keep screenshots local until ready — or include them if you want.)

---

## e) `run_demo.sh` (optional helper)
Make a small helper for Linux/macOS to run dry-run and real run:

```bash
#!/usr/bin/env bash
# run_demo.sh - demo: dry run then run
if [ -z "$1" ]; then
  echo "Usage: ./run_demo.sh /path/to/Downloads"
  exit 1
fi
TARGET="$1"
echo "DRY RUN:"
python3 organize_files.py --path "$TARGET" --dry-run
echo "If DRY RUN looks good, run the actual move? (y/N)"
read ans
if [[ "$ans" == "y" || "$ans" == "Y" ]]; then
  python3 organize_files.py --path "$TARGET"
fi


# replace email/name if necessary
git init
git add .
git commit -m "KIRO Week2: lazy automation - organize Downloads (add script, README, .kiro)"
git branch -M main
git remote add origin https://github.com/SUBHRAJITKAR1379/lazy-automation-kiro.git
git push -u origin main

git add .
git commit -m "Add automation script and KIRO metadata"
git push

