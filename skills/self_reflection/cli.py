"""CLI for Self-Reflection & Habit Tracker."""
import argparse
import sys

from . import extractor, habit_tracker, code_cleaner

def cmd_scan():
    analysis = extractor.analyze()
    habit_tracker.ingest_analysis(analysis)
    print("Scan complete. Extracted lessons:", len(analysis["lessons"]))
    for l in analysis["lessons"]:
        print(f"  - [{l['kind']}] {l['text']}")
    print("Habits:", analysis["habits"])
    return analysis

def cmd_report():
    from .habit_tracker import get_suggestions
    suggestions = get_suggestions()
    if suggestions:
        print("Suggestions:")
        for s in suggestions:
            print(" -", s)
    else:
        print("No suggestions at this time.")

def cmd_clean(target: str, dry_run: bool):
    root = "."
    if target in ("mem", "memory", "all"):
        # clean MEMORY.md
        from pathlib import Path
        m = Path("MEMORY.md")
        if m.exists():
            r = code_cleaner.clean_code_file(m, dry_run=dry_run)
            print(f"MEMORY.md: changed={r['changed']}")
    if target in ("code", "all"):
        res = code_cleaner.clean_directory(".", dry_run=dry_run)
        print(f"Cleaned {len(res)} files.")
        for r in res:
            if r["changed"]:
                print(f"  changed: {r['path']}")

def main():
    parser = argparse.ArgumentParser(description="Self-Reflection & Habit Tracker")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("scan", help="Scan sources and update habit tracker")
    sub.add_parser("report", help="Show suggestions")
    cl = sub.add_parser("clean", help="Clean code/output files")
    cl.add_argument("--target", default="all", choices=["mem", "code", "all"])
    cl.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if args.cmd == "scan":
        cmd_scan()
    elif args.cmd == "report":
        cmd_report()
    elif args.cmd == "clean":
        cmd_clean(args.target, args.dry_run)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()