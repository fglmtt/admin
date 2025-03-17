import os
import sys
import time


def main():
    pid = os.fork()

    if pid < 0:
        print("fork failed", file=sys.stderr)
        sys.exit(1)

    if pid == 0:
        print(f"child: pid {os.getpid()}, ppid {os.getppid()}")
        time.sleep(10)
        print(f"child: pid {os.getpid()}, ppid {os.getppid()}")

    if pid > 0:
        time.sleep(5)
        print(f"parent: pid {os.getpid()}, child's pid {pid}")


if __name__ == "__main__":
    main()
