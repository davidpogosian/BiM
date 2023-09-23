from bigraph import Bigraph # for typing
from bigraphGenerator import BigraphGenerator # for debugging
import logging

class AnimatedHopcroftKarp:
    def __init__(self, pauseLength=0):
        self.pauseLength = pauseLength
    
    def symmetricDifference(self, g: Bigraph, augmentingPaths: list[list[int]]):
        pass

    def BFSM(self, g: Bigraph) -> dict[int, list[int]]:
        stop = False
        treeDictionary = {}
        spotted = [0] * (len(g.edges) + len(g.edges[0]))
        isVertexMatched = g.getVertexMatchLookupTable()
        Q = []
        for leftVertexIndex in range(len(g.edges)):
            if isVertexMatched[leftVertexIndex] == 0:
                Q.append(leftVertexIndex)
        logging.debug(f'initial queue: {Q}')
        while len(Q) != 0:
            currentVertex = Q.pop(0)
            logging.debug(f'current vertex: {currentVertex}')
            if currentVertex < len(g.edges):
                for column in range(len(g.edges[0])):
                    if g.edges[currentVertex][column] == 1:
                        neighbor = column + len(g.edges)
                        logging.debug(f'\tneighbor: {neighbor}')
                        if isVertexMatched[neighbor] == 0:
                            stop = True
                            logging.debug(f"\t\tfound free vertex in right partition; stopping")
                        if spotted[neighbor] == 0:
                            logging.debug(f'\t\tnot spotted')
                            spotted[neighbor] = 1
                            if not stop:
                                Q.append(neighbor)
                                logging.debug(f'\t\tadded {neighbor} to Q')
                            treeDictionary[neighbor] = [currentVertex]
                        else:
                            treeDictionary[neighbor].append(currentVertex)
                            logging.debug(f'\t\talready spotted')
            else:
                for row in range(len(g.edges)):
                    if g.edges[row][currentVertex - len(g.edges)] == 1 and g.matching[row][currentVertex - len(g.edges) == 1]:
                        neighbor = row
                        logging.debug(f'\tneighbor: {neighbor}')
                        if spotted[neighbor] == 0:
                            logging.debug(f'\t\tnot spotted')
                            spotted[neighbor] = 1
                            if not stop:
                                Q.append(neighbor)
                                logging.debug(f'\t\tadded {neighbor} to Q')
                            treeDictionary[neighbor] = [currentVertex]
                        else:
                            treeDictionary[neighbor].append(currentVertex)
                            logging.debug(f'\t\talready spotted')
        return treeDictionary

    def DFSM(self, g: Bigraph, BFSMForest: dict[int, list[int]]) -> list[list[int]]:
        isVertexMatched = g.getVertexMatchLookupTable()
        freeRightVertices = []
        for vertex in range(len(g.edges), len(g.edges) + len(g.edges[0])):
            if isVertexMatched[vertex] == 0:
                freeRightVertices.append(vertex)
        for freeRightVertex in freeRightVertices:
            spotted = [0] * (len(g.edges) + len(g.edges[0]))
            S = [freeRightVertex]
            path = []
            parentof = {}
            while len(S) != 0:
                currentVertex = S.pop()
                if currentVertex < len(g.edges) and isVertexMatched[currentVertex] == 0:
                    logging.debug('found path!')
                    break
                if not currentVertex in BFSMForest:
                    continue
                for neighbor in BFSMForest[currentVertex]:
                    if spotted[neighbor] == 0:
                        spotted[neighbor] = 1
                        S.append(neighbor)
                    parentof[neighbor] = currentVertex


    def findAugPaths(self, g: Bigraph):
        BFSMForest = self.BFSM(g)
        print(BFSMForest)
        self.DFSM(g, BFSMForest)

    def hopcroftKarp(self, g: Bigraph):
        self.findAugPaths(g)
    

if __name__ == "__main__":
    logging.basicConfig(encoding='utf-8', level=logging.DEBUG, format="%(message)s")
    print(AnimatedHopcroftKarp().hopcroftKarp(BigraphGenerator().generateBigraph()))



