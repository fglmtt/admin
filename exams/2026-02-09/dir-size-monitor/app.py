# first and last name: mattia fogli
# student id: 123456
#
# path: $HOME/dir-size-monitor/app.py

import argparse
from datetime import datetime
import os
import sys
import time


def get_total_size(target_dir):
    total_size = 0
    for filename in os.listdir(target_dir):
        path = os.path.join(target_dir, filename)
        if os.path.isfile(path):
            total_size += os.path.getsize(path)
        elif os.path.isdir(path):
            total_size += get_total_size(path)
    return total_size


def main():
    parser = argparse.ArgumentParser(description="dir size monitor")
    parser.add_argument(
        "--target",
        type=str,
        required=True,
        help="absolute path to the directory to monitor",
    )
    parser.add_argument(
        "--threshold", type=int, required=True, help="size threshold in bytes"
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
    if args.threshold <= 0:
        print(f"error: --threshold must be a positive integer", file=sys.stderr)
        sys.exit(1)
    if args.interval <= 0:
        print(f"error: --interval must be a positive integer", file=sys.stderr)
        sys.exit(1)
    if not os.path.isabs(args.log):
        print(f"error: {args.log} is not an absolute path", file=sys.stderr)
        sys.exit(1)
    if not os.path.exists(args.log):
        print(f"error: {args.log} does not exist", file=sys.stderr)
        sys.exit(1)
    if not os.path.isdir(args.log):
        print(f"error: {args.log} is not a directory", file=sys.stderr)
        sys.exit(1)

    log_path = os.path.join(args.log, "dir-size-monitor.log")

    while True:
        total_size = get_total_size(args.target)
        if total_size > args.threshold:
            with open(log_path, "a") as log_file:
                log_file.write(f"{datetime.now()} {total_size}\n")
            print(f"total size {total_size} bytes exceeds threshold {args.threshold}")
        time.sleep(args.interval)


if __name__ == "__main__":
    main()
