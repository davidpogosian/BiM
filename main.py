import logging
from biMInterface import BiMInterface

def main():
    logging.basicConfig(encoding='utf-8', level=logging.DEBUG, format="%(message)s")
    interface = BiMInterface()


if __name__ == "__main__":
    main()