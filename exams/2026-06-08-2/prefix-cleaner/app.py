# first and last name: mattia fogli
# student id: 123456
#
# path: $HOME/prefix-cleaner/app.py

import argparse
from datetime import datetime
import os
import sys
import time


def walk(target_dir, prefix, log_path):
    for filename in os.listdir(target_dir):
        path = os.path.join(target_dir, filename)
        if os.path.isfile(path):
            if filename.startswith(prefix):
                with open(log_path, "a") as log_file:
                    log_file.write(f"{datetime.now()} {path}\n")
                os.remove(path)
                print(f"{datetime.now()} {path}")
        elif os.path.isdir(path):
            walk(path, prefix, log_path)


def main():
    parser = argparse.ArgumentParser(description="prefix cleaner")
    parser.add_argument(
        "--target",
        type=str,
        required=True,
        help="absolute path to the directory to clean",
    )
    parser.add_argument(
        "--prefix", type=str, required=True, help="prefix of the file names to remove"
    )
    parser.add_argument(
        "--interval", type=int, required=True, help="interval in seconds between checks"
    )
    parser.add_argument(
        "--log", type=str, required=True, help="directory where to save the log file"
    )
    args = parser.parse_args()

    if not os.path.isabs(args.target):
        print(f"error: {args.target} is not an absolute path", file=sys.stderr)
        sys.exit(1)
    if not os.path.exists(args.target):
        print(f"error: {args.target} does not exist", file=sys.stderr)
        sys.exit(1)
    if not os.path.isdir(args.target):
        print(f"error: {args.target} is not a directory", file=sys.stderr)
        sys.exit(1)
    if not args.prefix:
        print(f"error: --prefix must be non-empty", file=sys.stderr)
        sys.exit(1)
    if args.interval <= 0:
        print(f"error: --interval must be a positive integer", file=sys.stderr)
        sys.exit(1)
    if not os.path.exists(args.log):
        print(f"error: {args.log} does not exist", file=sys.stderr)
        sys.exit(1)
    if not os.path.isdir(args.log):
        print(f"error: {args.log} is not a directory", file=sys.stderr)
        sys.exit(1)

    log_path = os.path.join(args.log, "prefix-cleaner.log")

    while True:
        walk(args.target, args.prefix, log_path)
        time.sleep(args.interval)


if __name__ == "__main__":
    main()
