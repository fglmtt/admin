# first and last name: mattia fogli
# student id: 123456
#
# path: ~/extension-sorter/app.py

import argparse
from datetime import datetime
import os
import shutil
import sys


def walk(target_dir, dest_dir, extensions, log_path):
    for filename in os.listdir(target_dir):
        path = os.path.join(target_dir, filename)
        if os.path.isfile(path):
            for extension in extensions:
                if filename.endswith(f".{extension}"):
                    target_subdir = os.path.join(dest_dir, extension)
                    shutil.move(path, target_subdir)
                    with open(log_path, "a") as log_file:
                        log_file.write(f"{datetime.now()} {path} {target_subdir}\n")
        elif os.path.isdir(path):
            walk(path, dest_dir, extensions, log_path)


def main():
    parser = argparse.ArgumentParser(description="extension sorter")
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="absolute path of the directory to scan",
    )
    parser.add_argument(
        "--dest",
        type=str,
        required=True,
        help="absolute path of the destination directory",
    )
    parser.add_argument(
        "--extensions",
        type=str,
        required=True,
        help="comma-separated extensions to monitor",
    )
    parser.add_argument(
        "--log",
        type=str,
        required=True,
        help="absolute path of the log file",
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
    if not os.path.isabs(args.dest):
        print(f"error: {args.dest} is not an absolute path", file=sys.stderr)
        sys.exit(1)
    if not os.path.exists(args.dest):
        print(f"error: {args.dest} does not exist", file=sys.stderr)
        sys.exit(1)
    if not os.path.isdir(args.dest):
        print(f"error: {args.dest} is not a directory", file=sys.stderr)
        sys.exit(1)
    extensions = args.extensions.split(",")
    for extension in extensions:
        if not extension:
            print("error: empty extension", file=sys.stderr)
            sys.exit(1)
    if not os.path.isabs(args.log):
        print(f"error: {args.log} is not an absolute path", file=sys.stderr)
        sys.exit(1)

    os.makedirs(os.path.dirname(args.log), exist_ok=True)
    for extension in extensions:
        os.makedirs(os.path.join(args.dest, extension), exist_ok=True)
    walk(args.path, args.dest, extensions, args.log)


if __name__ == "__main__":
    main()
