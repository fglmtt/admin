# first and last name: mattia fogli
# student id: 123456
#
# path: $HOME/owner-detector/app.py

import argparse
from datetime import datetime
import os
import sys
import time


def walk(target_dir, uids, log_file):
    for filename in os.listdir(target_dir):
        path = os.path.join(target_dir, filename)
        if os.path.isfile(path):
            uid = os.stat(path).st_uid
            if uid in uids:
                line = f"{datetime.now()} {path} {uid}"
                log_file.write(line + "\n")
                print(line)
        elif os.path.isdir(path):
            walk(path, uids, log_file)


def main():
    parser = argparse.ArgumentParser(description="owner detector")
    parser.add_argument(
        "--target",
        type=str,
        required=True,
        help="absolute path to the directory to scan",
    )
    parser.add_argument(
        "--users",
        type=str,
        required=True,
        help="comma-separated list of the uids to detect",
    )
    parser.add_argument(
        "--interval",
        type=int,
        required=True,
        help="interval in seconds between checks",
    )
    parser.add_argument(
        "--log",
        type=str,
        required=True,
        help="absolute path to the log file",
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

    uids = []
    for item in args.users.split(","):
        try:
            uid = int(item)
        except ValueError:
            print(f"error: {item} is not an integer", file=sys.stderr)
            sys.exit(1)
        if uid < 0:
            print(f"error: {uid} is a negative uid", file=sys.stderr)
            sys.exit(1)
        uids.append(uid)

    if args.interval <= 0:
        print("error: --interval must be a positive integer", file=sys.stderr)
        sys.exit(1)

    if not os.path.isabs(args.log):
        print(f"error: {args.log} is not an absolute path", file=sys.stderr)
        sys.exit(1)
    log_dir = os.path.dirname(args.log)
    if not os.path.exists(log_dir):
        print(f"error: {log_dir} does not exist", file=sys.stderr)
        sys.exit(1)
    if not os.path.isdir(log_dir):
        print(f"error: {log_dir} is not a directory", file=sys.stderr)
        sys.exit(1)

    while True:
        with open(args.log, "w") as log_file:
            walk(args.target, uids, log_file)
        time.sleep(args.interval)


if __name__ == "__main__":
    main()
