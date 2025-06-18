# first and last name: mattia fogli
# serial number: 123456
#
# path: $HOME/large-file-detector/app.py

import argparse
import os
import sys
import time


def walk(basepath, size, log_path):
    for filename in os.listdir(basepath):
        path = os.path.join(basepath, filename)
        if os.path.isfile(path):
            file_size = os.path.getsize(path)
            if file_size >= size:
                print(f"found large file: {path} ({file_size} bytes)")
                with open(log_path, "a") as log_file:
                    log_file.write(f"{path}\n")
        elif os.path.isdir(path):
            walk(path, size, log_path)


def main():
    parser = argparse.ArgumentParser(description="large file detector")
    parser.add_argument(
        "--target",
        type=str,
        required=True,
        help="absolute path to the directory to check",
    )
    parser.add_argument(
        "--size",
        type=int,
        required=True,
        help="minimum size of files to report in bytes",
    )
    parser.add_argument(
        "--interval", type=int, required=True, help="interval in seconds between checks"
    )
    parser.add_argument("--log", type=str, required=True, help="directory for log file")
    args = parser.parse_args()

    if not os.path.isabs(args.target):
        print(f"error: {args.target} is not an absolute path.", file=sys.stderr)
        sys.exit(1)
    if not os.path.exists(args.target):
        print(f"error: {args.target} does not exist.", file=sys.stderr)
        sys.exit(1)
    if not os.path.isdir(args.target):
        print(f"error: {args.target} is not a directory.", file=sys.stderr)
        sys.exit(1)
    if args.size <= 0:
        print(f"error: --size must be a positive integer.", file=sys.stderr)
        sys.exit(1)
    if args.interval <= 0:
        print(f"error: --interval must be a positive integer.", file=sys.stderr)
        sys.exit(1)
    if not os.path.exists(args.log):
        print(f"error: the path for --log does not exist.", file=sys.stderr)
        sys.exit(1)
    if not os.path.isdir(args.log):
        print(f"error: the path for --log is not a directory.", file=sys.stderr)
        sys.exit(1)

    log_path = os.path.join(args.log, "large-file-detector.log")
    while True:
        walk(args.target, args.size, log_path)
        try:
            time.sleep(args.interval)
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    main()
