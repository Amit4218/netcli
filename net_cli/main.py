import sys
from src.cli import app
from src.cli import search


def main():

    if len(sys.argv) > 1:
        app()
    else:
        search(movie=None)


if __name__ == "__main__":
    main()
