import tkinter as tk
import logging
from interface import BiMInterface

# I will model graphs as dictionaries because it's easy and I'm lazy

def main():
    logging.basicConfig(encoding='utf-8', level=logging.DEBUG, format="%(message)s")
    interface = BiMInterface()


if __name__ == "__main__":
    main()