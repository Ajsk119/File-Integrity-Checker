# config.py
# ──────────────────────────────────────────────────────────────────────────────
# Central configuration for File Integrity Checker.
# Edit these values to customise behaviour without touching any other file.
# ──────────────────────────────────────────────────────────────────────────────

# Default cryptographic algorithm used when none is specified via --algo
DEFAULT_HASH_ALGO = "sha256"

# Default output filenames (written to the current working directory)
BASELINE_FILE = "integrity_baseline.json"
REPORT_FILE   = "integrity_report.txt"

# File extensions that will be skipped during scanning
SKIP_EXTENSIONS = {}

# Directory names that will be skipped entirely during recursive scans
SKIP_DIRS = {"__pycache__", ".git", ".svn", ".hg", "node_modules", ".DS_Store"}

# Width of the progress bar drawn in the terminal (number of block characters)
PROGRESS_BAR_WIDTH = 30
