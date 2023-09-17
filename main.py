import logging
from biMInterface import BiMInterface
from bigraph import Bigraph

def main():
    # example graph
    g = Bigraph(
        "chapter-ex",
        [0,1,2,3,4],
        [5,6,7,8,9,10],
        {
            0:[6],
            1:[5,7],
            2:[5,6],
            3:[6,8,9,10],
            4:[6,8]
        }
    )

    logging.basicConfig(encoding='utf-8', level=logging.DEBUG, format="%(message)s")
    interface = BiMInterface(g)


if __name__ == "__main__":
    main()