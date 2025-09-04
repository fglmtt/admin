# first and last name: mattia fogli
# student id: 123456
#
# path: ~/disk-usage-monitor/app.py

import argparse
import shutil
import sys
import os
from datetime import datetime


def main():
    parser = argparse.ArgumentParser(description="disk usage monitor")
    parser.add_argument(
        "--partition",
        type=str,
        required=True,
        help="absolute path of the partition to monitor",
    )
    parser.add_argument(
        "--threshold",
        type=int,
        required=True,
        help="usage threshold in percent (0–100)",
    )
    args = parser.parse_args()

    if not os.path.isabs(args.partition):
        print(f"error: {args.partition} is not an absolute path", file=sys.stderr)
        sys.exit(1)
    if not os.path.exists(args.partition):
        print(f"error: {args.partition} does not exist", file=sys.stderr)
        sys.exit(1)
    if args.threshold < 0 or args.threshold > 100:
        print(f"error: {args.threshold} must be between 0 and 100", file=sys.stderr)
        sys.exit(1)

    total, used, _ = shutil.disk_usage(args.partition)
    percent_used = used / total * 100
    print(f"disk usage for {args.partition}: {percent_used:.2f}%")

    if percent_used >= args.threshold:
        log_dir = os.path.expanduser("~/disk-usage-monitor")
        os.makedirs(log_dir, exist_ok=True)

        log_path = os.path.join(log_dir, "disk-usage-monitor.log")
        with open(log_path, "a") as log_file:
            now = datetime.now()
            log_file.write(f"{now} {percent_used:.2f}%\n")


if __name__ == "__main__":
    main()
