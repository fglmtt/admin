import argparse
import psutil
import time


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--interval", type=int, default=1, help="Interval between logs in seconds"
    )
    args = parser.parse_args()

    while True:
        print(f"{time.time()} - {psutil.cpu_percent()}")
        time.sleep(args.interval)


if __name__ == "__main__":
    main()
