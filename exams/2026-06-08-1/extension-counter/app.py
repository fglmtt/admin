# first and last name: mattia fogli
# student id: 123456
#
# path: $HOME/extension-counter/app.py

import argparse
from datetime import datetime
import os
import sys
import time


def walk(target_dir, ext):
    count = 0
    for filename in os.listdir(target_dir):
        path = os.path.join(target_dir, filename)
        if os.path.isfile(path):
            if os.path.splitext(path)[1] == ext:
                count += 1
        elif os.path.isdir(path):
            count += walk(path, ext)
    return count


def main():
    parser = argparse.ArgumentParser(description="extension counter")
    parser.add_argument(
        "--target",
        type=str,
        required=True,
        help="absolute path to the directory to monitor",
    )
    parser.add_argument(
        "--ext", type=str, required=True, help="file extension to count (e.g. .log)"
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
    if not args.ext:
        print("error: --ext must be non-empty", file=sys.stderr)
        sys.exit(1)
    if not args.ext.startswith("."):
        print(f"error: {args.ext} must start with a dot", file=sys.stderr)
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

    log_path = os.path.join(args.log, "extension-counter.log")

    while True:
        count = walk(args.target, args.ext)
        with open(log_path, "a") as log_file:
            log_file.write(f"{datetime.now()} {args.ext} {count}\n")
        print(f"{datetime.now()} {args.ext} {count}")
        time.sleep(args.interval)


if __name__ == "__main__":
    main()
