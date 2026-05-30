# File Integrity Checker

Detect unauthorized modifications, deletions, or new files by comparing
cryptographic hashes against a trusted baseline database.

---

## Folder Structure

```
file_integrity_checker/
│
├── main.py              ← Entry point — run this
├── config.py            ← All settings in one place
│
├── core/
│   ├── hasher.py        ← compute_hash(), get_file_metadata()
│   ├── scanner.py       ← collect_files() — walks a path respecting skip rules
│   ├── baseline.py      ← create / save / load the JSON baseline
│   └── verifier.py      ← compares current files against the baseline
│
├── commands/
│   ├── baseline.py      ← `baseline` command handler
│   ├── verify.py        ← `verify` command handler
│   ├── report.py        ← `report` command handler
│   └── watch.py         ← `watch` command handler
│
└── utils/
    └── reporter.py      ← formats and writes the incident report
```

---

## Requirements

- Python 3.7 or newer
- No external libraries needed — uses only the standard library

---

## How to Run

All commands are run from **inside** the `file_integrity_checker/` folder:

```bash
cd file_integrity_checker
```

### 1. Create a baseline

Scan a folder (or single file) and save SHA-256 hashes to `integrity_baseline.json`.

```bash
python main.py baseline /path/to/folder
```

Optional flags:
```bash
python main.py baseline /path/to/folder --algo sha512
python main.py baseline /path/to/folder --baseline-file my_baseline.json
```

---

### 2. Verify (quick check)

Re-hash all files and print a summary. Does **not** write a report file.

```bash
python main.py verify
```

---

### 3. Report (full check + save)

Same as verify, but also writes a detailed `integrity_report.txt`.

```bash
python main.py report
```

---

### 4. Watch (continuous monitoring)

Check every 60 seconds (or any interval you choose). Saves a report whenever
tampering is detected. Press `Ctrl+C` to stop.

```bash
python main.py watch
python main.py watch --interval 30
```

---

## Output Files

| File | Created by | Contents |
|---|---|---|
| `integrity_baseline.json` | `baseline` | Trusted hashes + metadata |
| `integrity_report.txt` | `report` / `watch` | Timestamped incident report |

---

## Configuration

Edit `config.py` to change defaults without touching any other file:

```python
DEFAULT_HASH_ALGO = "sha256"     # md5 / sha1 / sha256 / sha512
SKIP_EXTENSIONS   = {".log", ".tmp", ...}
SKIP_DIRS         = {".git", "__pycache__", ...}
```

---

## Example Output

```
=================================================================
  FILE INTEGRITY CHECKER — VERIFICATION REPORT
=================================================================
  Timestamp     : 2026-05-29T10:08:44
  Target        : /home/user/myproject
  Algorithm     : SHA256
  Files Checked : 3
-----------------------------------------------------------------
  ✅  Unchanged  : 1
  ⚠️   Modified   : 1
  🔴  Missing    : 1
  ℹ️   New Files  : 1
-----------------------------------------------------------------

  [MODIFIED FILES — POSSIBLE TAMPERING DETECTED]
  ⚠️  /home/user/myproject/config.cfg
      Expected : 719c5303...
      Actual   : 4468a49f...
      Size Δ   : 14 → 31 bytes

  [MISSING FILES — POSSIBLE DELETION / MOVE]
  🔴  /home/user/myproject/script.sh

  [NEW / UNREGISTERED FILES]
  ℹ️   /home/user/myproject/malware.sh
-----------------------------------------------------------------
  Overall Status : COMPROMISED 🔴
=================================================================
```
