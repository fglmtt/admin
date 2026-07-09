# first and last name: mattia fogli
# student id: 123456
#
# path: ~/permission-auditor/app.py

import argparse
from datetime import datetime
import os
import stat
import sys


def walk(target_dir, mode, log_path):
    for filename in os.listdir(target_dir):
        path = os.path.join(target_dir, filename)
        if os.path.isfile(path):
            perms = stat.S_IMODE(os.stat(path).st_mode)
            if perms != mode:
                with open(log_path, "a") as log_file:
                    log_file.write(f"{datetime.now()} {oct(perms)} {path}\n")
        elif os.path.isdir(path):
            walk(path, mode, log_path)


def main():
    parser = argparse.ArgumentParser(description="permission auditor")
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="absolute path of the directory to scan",
    )
    parser.add_argument(
        "--mode",
        type=str,
        required=True,
        help="expected permissions in octal notation",
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
    try:
        mode = int(args.mode, 8)
    except ValueError:
        print(f"error: {args.mode} is not an octal number", file=sys.stderr)
        sys.exit(1)
    if not os.path.isabs(args.log):
        print(f"error: {args.log} is not an absolute path", file=sys.stderr)
        sys.exit(1)

    os.makedirs(os.path.dirname(args.log), exist_ok=True)
    walk(args.path, mode, args.log)


if __name__ == "__main__":
    main()
