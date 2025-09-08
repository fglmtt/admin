# first and last name: mattia fogli
# student id: 123456
#
# path: $HOME/log-extractor/app.py

import argparse
import os
import sys


def find(filename, pattern):
    with open(filename, "r") as f:
        lines = f.readlines()
    return [line for line in lines if pattern in line]


def dump(filename, lines):
    with open(filename, "w") as f:
        f.writelines(lines)


def walk(log_dir, backup_dir, pattern):
    for filename in os.listdir(log_dir):
        path = os.path.join(log_dir, filename)
        if os.path.isfile(path) and filename.endswith(".log"):
            lines = find(path, pattern)
            if lines:
                print(f"found {len(lines)} lines in {path}")
                backup_filename = os.path.join(backup_dir, filename)
                dump(backup_filename, lines)
                print(f"wrote {len(lines)} lines to {backup_filename}")
        elif os.path.isdir(path):
            walk(path, backup_dir, pattern)


def main():
    parser = argparse.ArgumentParser(description="log extractor")
    parser.add_argument(
        "--path", type=str, required=True, help="path to the directory to analyze"
    )
    parser.add_argument(
        "--pattern", type=str, required=True, help="pattern to search for in log files"
    )
    args = parser.parse_args()

    if not os.path.isabs(args.path):
        print(f"error: {args.path} is not an absolute path", file=sys.stderr)
        sys.exit(1)
    if not os.path.exists(args.path):
        print(f"error: {args.path} does not exist", file=sys.stderr)
        sys.exit(1)
    if not os.path.isdir(args.path):
        print(f"error: {args.path} is not a directory", file=sys.stderr)
        sys.exit(1)
    if not args.pattern:
        print(f"error: --pattern must be a non-empty string", file=sys.stderr)
        sys.exit(1)

    backup_path = os.path.expanduser("~/backup")
    os.makedirs(backup_path, exist_ok=True)
    walk(args.path, backup_path, args.pattern)


if __name__ == "__main__":
    main()
