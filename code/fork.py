import os
import sys


def main():
    pid = os.fork()

    if pid < 0:
        print("fork failed", file=sys.stderr)
        sys.exit(1)

    if pid == 0:
        try:
            os.execl("/bin/ls", "ls", "-l")
        except Exception as e:
            print(f"exec failed: {e}", file=sys.stderr)
            os._exit(1)

    if pid > 0:
        os.wait()
        print("child done")


if __name__ == "__main__":
    main()
