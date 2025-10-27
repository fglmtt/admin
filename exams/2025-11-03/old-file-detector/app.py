# nome e cognome: mattia fogli
# matricola: 123456
#
# path: $HOME/old-file-detector/app.py

import argparse
import os
import sys
import time


def walk(basepath, threshold, log_file_path):
    for filename in os.listdir(basepath):
        path = os.path.join(basepath, filename)
        if os.path.isfile(path):
            last_modified = os.path.getmtime(path)
            if last_modified < threshold:
                print(f"{path} (last modified: {time.ctime(last_modified)})")
                with open(log_file_path, "a") as f:
                    f.write(f"{path}\n")
                os.remove(path)
        elif os.path.isdir(path):
            walk(path, threshold, log_file_path)


def main():
    parser = argparse.ArgumentParser(description="old file detector")
    parser.add_argument(
        "--target", type=str, required=True, help="directory to scan for old files."
    )
    parser.add_argument(
        "--days", type=int, required=True, help="number of days to consider a file old."
    )
    parser.add_argument(
        "--interval",
        type=int,
        required=True,
        help="interval in seconds between checks.",
    )
    parser.add_argument(
        "--log",
        type=str,
        required=True,
        help="directory to save the log file.",
    )
    args = parser.parse_args()

    if not os.path.isabs(args.target):
        print("error: --target must be an absolute path.", file=sys.stderr)
        sys.exit(1)
    if not os.path.exists(args.target):
        print("error: --target path does not exist.", file=sys.stderr)
        sys.exit(1)
    if not os.path.isdir(args.target):
        print("error: --target path is not a directory.", file=sys.stderr)
        sys.exit(1)

    if args.days <= 0:
        print("error: --days must be a positive integer.", file=sys.stderr)
        sys.exit(1)

    if args.interval <= 0:
        print("error: --interval must be a positive integer.", file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(args.log):
        print("error: --log path does not exist.", file=sys.stderr)
        sys.exit(1)
    if not os.path.isdir(args.log):
        print("error: --log path is not a directory.", file=sys.stderr)
        sys.exit(1)

    log_file_path = os.path.join(args.log, "old-file-detector.log")
    while True:
        threshold = time.time() - (args.days * 86400)
        walk(args.target, threshold, log_file_path)
        time.sleep(args.interval)


if __name__ == "__main__":
    main()
