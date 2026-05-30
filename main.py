#!/usr/bin/env python3
"""
File Integrity Checker
======================
Entry point. Parses CLI arguments and delegates to the right command.

Usage:
  python main.py baseline <path> [--algo sha256]
  python main.py verify   <path>
  python main.py report   <path>
  python main.py watch    <path> [--interval 60]
"""

import argparse
from commands.baseline import run_baseline
from commands.verify   import run_verify
from commands.report   import run_report
from commands.watch    import run_watch


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="fic",
        description="File Integrity Checker — detect unauthorized file changes",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "command",
        choices=["baseline", "verify", "report", "watch"],
        help=(
            "baseline  Scan path and create a trusted hash database\n"
            "verify    Compare current files against the baseline (summary only)\n"
            "report    Verify and save a full incident report to disk\n"
            "watch     Continuously monitor on a schedule"
        ),
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="File or folder to scan (default: current directory)",
    )
    parser.add_argument(
        "--algo",
        default="sha256",
        choices=["md5", "sha1", "sha256", "sha512"],
        help="Hash algorithm to use (default: sha256)",
    )
    parser.add_argument(
        "--baseline-file",
        default="integrity_baseline.json",
        help="Path to the baseline JSON file (default: integrity_baseline.json)",
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=60,
        help="Seconds between checks in watch mode (default: 60)",
    )
    return parser


def main():
    parser = build_parser()
    args   = parser.parse_args()

    if args.command == "baseline":
        run_baseline(args.path, args.algo, args.baseline_file)

    elif args.command == "verify":
        run_verify(args.baseline_file)

    elif args.command == "report":
        run_report(args.baseline_file)

    elif args.command == "watch":
        run_watch(args.baseline_file, args.interval)


if __name__ == "__main__":
    main()
