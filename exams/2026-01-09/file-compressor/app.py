# first and last name: mattia fogli
# student id: 123456
#
# path: $HOME/file-compressor/app.py

import argparse
import os
import sys
import zipfile
import time


def walk(target_dir, archive_path, threshold):
    for filename in os.listdir(target_dir):
        path = os.path.join(target_dir, filename)
        if os.path.isfile(path):
            file_size = os.path.getsize(path)
            if file_size >= threshold:
                with zipfile.ZipFile(archive_path, "a") as zipf:
                    zipf.write(path, arcname=filename)
                os.remove(path)
                print(f"compressed {path} ({file_size} bytes) into {archive_path}")
        elif os.path.isdir(path):
            walk(path, archive_path, threshold)


def main():
    parser = argparse.ArgumentParser(description="file compressor")
    parser.add_argument(
        "--path", type=str, required=True, help="absolute path to the directory to scan"
    )
    parser.add_argument(
        "--size", type=int, required=True, help="size threshold in bytes"
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
    if args.size <= 0:
        print(f"error: --size must be a positive integer", file=sys.stderr)
        sys.exit(1)

    archives_dir = os.path.expanduser("~/archives")
    os.makedirs(archives_dir, exist_ok=True)
    archive_path = os.path.join(archives_dir, f"{int(time.time())}.zip")
    walk(args.path, archive_path, args.size)


if __name__ == "__main__":
    main()
