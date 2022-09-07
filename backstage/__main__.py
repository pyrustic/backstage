import os
import os.path
import sys
from backstage.cli import Cli


__all__ = []


def main():
    directory = os.getcwd()
    command = sys.argv[1:]
    cli = Cli(directory)
    if command:
        cli.run(command)
        return
    cli.loop()


if __name__ == "__main__":
    main()
