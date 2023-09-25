from bigraph import Bigraph # for typing
import random

class BigraphGenerator:
    def __init__(self):
        pass

    def generateBigraph(self) -> Bigraph:
        # implement random bigraph generation
        matrix = []
        emptyMatrix = []
        n = random.randint(3, 10)
        p = 0.3

        for i in range(n):
            row = [0] * n
            for j in range(n):
                if random.random() < p:
                    row[j] = 1
            matrix.append(row)
            emptyMatrix.append([0] * n)

        return Bigraph(
            'Default Name',
            matrix,
            emptyMatrix

        )



        # TEMP
        # return Bigraph(
        #     "chapter-ex",
        #     [   #5, 6, 7, 8, 9, 10
        #         [0, 1, 0, 0, 0, 0], #0
        #         [1, 0, 1, 0, 0, 0], #1
        #         [1, 1, 0, 0, 0, 0], #2
        #         [0, 1, 0, 1, 1, 1], #3
        #         [0, 1, 0, 1, 0, 0], #4
        #     ],
        #     [   #5, 6, 7, 8, 9, 10
        #         [0, 0, 0, 0, 0, 0], #0
        #         [0, 0, 0, 0, 0, 0], #1
        #         [0, 0, 0, 0, 0, 0], #2
        #         [0, 0, 0, 0, 0, 0], #3
        #         [0, 0, 0, 0, 0, 0], #4
        #     ]

        # )

# import random
    # def generateGraph(n):
        # cap = n
        # randomU = []
        # randomW = []
        # randomEdges = []
        # lengthU = random.randint(1, cap)
        # lengthW = random.randint(1, cap)
        # for u in range(0, lengthU):
        #     randomU.append(u)
        # for w in range(cap, cap + lengthW):
        #     randomW.append(w)
        # for i in range(random.randint(lengthU * lengthW // 2, lengthU * lengthW)):
        #     while True:
        #     edge = [random.choice(randomU), random.choice(randomW)]
        #     if not edge in randomEdges:
        #         randomEdges.append(edge)
        #         break
        # return (randomU, randomW, randomEdges)