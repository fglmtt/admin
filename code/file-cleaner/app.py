# first and last name: mattia fogli
# serial number: 123456
#
# path: $HOME/file-cleaner/app.py

import argparse
import os
import sys


def walk(basepath, extension):
    for filename in os.listdir(basepath):
        path = os.path.join(basepath, filename)

        if os.path.isfile(path) and path.endswith(extension):
            print(f"removing {path}")
            os.remove(path)
        elif os.path.isdir(path):
            walk(path, extension)


def main():
    parser = argparse.ArgumentParser(description="file cleaner")
    parser.add_argument("--path", type=str, required=True, help="directory to clean")
    parser.add_argument(
        "--extension", type=str, required=True, help="file extension to remove"
    )
    args = parser.parse_args()

    if not os.path.isabs(args.path):
        print(f"error: {args.path} must be absolute", file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(args.path):
        print(f"error: {args.path} does not exist", file=sys.stderr)
        sys.exit(1)

    if not os.path.isdir(args.path):
        print(f"error: {args.path} is not a directory", file=sys.stderr)
        sys.exit(1)

    if not args.extension.startswith("."):
        print(f"error: {args.extension} must start with a dot", file=sys.stderr)
        sys.exit(1)

    walk(args.path, args.extension)


if __name__ == "__main__":
    main()
