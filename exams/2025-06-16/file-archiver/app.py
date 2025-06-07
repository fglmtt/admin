# first and last name: mattia fogli
# serial number: 123456
#
# path: $HOME/file-cleaner/app.py

import argparse
import os
import sys
import time
import shutil


def walk(basepath, seconds, archive_path):
    for filename in os.listdir(basepath):
        path = os.path.join(basepath, filename)
        if os.path.isfile(path):
            file_age_seconds = time.time() - os.path.getmtime(path)
            if file_age_seconds >= seconds:
                shutil.move(path, archive_path)
                print(f"moved {path} to {archive_path}")
        elif os.path.isdir(path):
            walk(path, seconds, archive_path)


def main():
    parser = argparse.ArgumentParser(description="file archiver")
    parser.add_argument(
        "--path", type=str, required=True, help="path to the directory to check"
    )
    parser.add_argument(
        "--seconds",
        type=int,
        required=True,
        help="maximum age of files in seconds to archive",
    )
    args = parser.parse_args()

    if not os.path.isabs(args.path):
        print(f"error: {args.path} is not an absolute path.", file=sys.stderr)
        sys.exit(1)
    if not os.path.exists(args.path):
        print(f"error: {args.path} does not exist.", file=sys.stderr)
        sys.exit(1)
    if not os.path.isdir(args.path):
        print(f"error: {args.path} is not a directory.", file=sys.stderr)
        sys.exit(1)
    if args.seconds <= 0:
        print(f"error: --seconds must be a positive integer.", file=sys.stderr)
        sys.exit(1)

    archive_path = os.path.expanduser("~/archive")
    os.makedirs(archive_path, exist_ok=True)
    walk(args.path, args.seconds, archive_path)


if __name__ == "__main__":
    main()
