from bigraph import Bigraph

class BigraphGenerator:
    def __init__(self):
        pass

    def generateBigraph(self) -> Bigraph:
        # implement random bigraph generation

        # TEMP
        return Bigraph(
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