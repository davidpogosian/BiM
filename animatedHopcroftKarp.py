from bigraph import Bigraph # for typing
from bigraphGenerator import BigraphGenerator # for debugging
import time
import logging

class AnimatedHopcroftKarp:
    def __init__(self, pauseDuration=0):
        self.pauseDuration = pauseDuration
    
    def setCanvas(self, canvas):
        self.canvas = canvas

    def changePauseDuration(self, newDuration):
        self.pauseDuration = float(newDuration)
        logging.debug(f'pauseDuraton: {self.pauseDuration}')
    
    def symmetricDifference(self, g: Bigraph, augmentingPaths: list[list[int]]):
        for ap in augmentingPaths:
            if g.matching[ap[0]][ap[1] - len(g.edges)] == 0:
                g.matching[ap[0]][ap[1] - len(g.edges)] = 1
            else:
                g.matching[ap[0]][ap[1] - len(g.edges)] = 0

	# procedure BFS(G, root) is
    # 	let Q be a queue
    #   label root as explored
    #   Q.enqueue(root)
    #   while Q is not empty do
    #       v := Q.dequeue()
    #       if v is the goal then
    #           return v
    #       for all edges from v to w in G.adjacentEdges(v) do
    #           if w is not labeled as explored then
    #               label w as explored
    #               w.parent := v
    #               Q.enqueue(w)

    def BFSM(self, g: Bigraph) -> dict[int, list[int]]:
        logging.debug(f'BFSM:')
        Q = []
        parent = {}
        explored = [0] * (len(g.edges) + len(g.edges[0]))
        isVertexMatched = g.getVertexMatchLookupTable()
        for leftVertex in range(len(g.edges)):
            if not isVertexMatched[leftVertex]:
                explored[leftVertex] = 1
                Q.append(leftVertex)
        found = False
        while len(Q) != 0:
            v = Q.pop(0)
            logging.debug(f"v: {v}")
            # self.canvas.after(1000, self.canvas.itemconfig(g.vertexToTag[v], fill="green"))
            # time.sleep(self.pauseDuration)
            if v < len(g.edges):
                for column in range(len(g.edges[0])):
                    if g.edges[v][column] == 1 and g.matching[v][column] == 0:
                        neighbor = column + len(g.edges)
                        logging.debug(f'\tneighbor: {neighbor}')
                        if not isVertexMatched[neighbor] and not found:
                            found = True
                            logging.debug(f"\t\tfound free vertex in right partition; stopping")
                        if not explored[neighbor]:
                            explored[neighbor] = 1
                            if not found:
                                Q.append(neighbor)
                                logging.debug(f'\t\tadded {neighbor} to Q')
                            parent[neighbor] = [v]
                        else:
                            parent[neighbor].append(v)
            else:
                for row in range(len(g.edges)):
                    logging.debug(f'consider: {row} left <- right cond1 = {g.edges[row][v - len(g.edges)] == 1} cond2 = {g.matching[row][v - len(g.edges)] == 1}')
                    if g.edges[row][v - len(g.edges)] == 1 and g.matching[row][v - len(g.edges)] == 1:
                        neighbor = row
                        logging.debug(f'\tneighbor: {neighbor}')
                        if not explored[neighbor]:
                            explored[neighbor] = 1
                            if not found:
                                Q.append(neighbor)
                                logging.debug(f'\t\tadded {neighbor} to Q')
                            parent[neighbor] = [v]
                        else:
                            parent[neighbor].append(v)
        return parent

	# procedure DFS(G, root) is
    # 	let S be a stack
    #   label root as explored
    #   S.push(root)
    #   while S is not empty do
    #       v := S.pop()
    #       if v is the goal then
    #           return v
    #       for all edges from v to w in G.adjacentEdges(v) do
    #           if w is not labeled as explored then
    #               label w as explored
    #               w.parent := v
    #               S.push(w)

    def DFSM(self, g: Bigraph, BFSMForest: dict[int, list[int]]) -> list[list[int]]:
        logging.debug(f'DFSM:')
        augmentingPaths = []
        unmatchedRightVertices = []
        isVertexMatched = g.getVertexMatchLookupTable()
        for rightVertex in range(len(g.edges), len(g.edges) + len(g.edges[0])):
            if not isVertexMatched[rightVertex]:
                unmatchedRightVertices.append(rightVertex)
        for rightVertex in unmatchedRightVertices:
            logging.debug(f'looking for an ap from {rightVertex}')
            S = [rightVertex]
            parent = {}
            explored = [0] * (len(g.edges) + len(g.edges[0]))
            explored[rightVertex] = 1 # doubt this is necessary
            found = False
            while len(S) != 0:
                v = S.pop()
                logging.debug(f'v: {v}')
                if v in parent:
                    BFSMForest[parent[v]].remove(v)
                    logging.debug(f'removed {parent[v]} -> {v}')
                if v < len(g.edges) and not isVertexMatched[v]:
                    found = True
                    isVertexMatched[v] = 1
                    while v in parent:
                        logging.debug(f'{v} => {parent[v]}')
                        ap = [v, parent[v]] if parent[v] > v  else [parent[v], v]
                        augmentingPaths.append(ap)
                        v = parent[v]
                    break
                if v in BFSMForest:
                    for w in BFSMForest[v]:
                        if not explored[w]:
                            explored[w] = 1
                            parent[w] = v
                            S.append(w)
        return augmentingPaths

    def findAugPaths(self, g: Bigraph):
        BFSMForest = self.BFSM(g)
        logging.debug(f'BFSMForest: {BFSMForest}')
        augmentingPaths = self.DFSM(g, BFSMForest)
        logging.debug(f'augmentingPaths: {augmentingPaths}')
        return augmentingPaths

    def hopcroftKarp(self, g: Bigraph):
        augmentingPaths = self.findAugPaths(g)
        while len(augmentingPaths) != 0:
            logging.debug('running symmetric difference!')
            self.symmetricDifference(g, augmentingPaths)
            augmentingPaths = self.findAugPaths(g)
        logging.debug(f'maximum matching:')
        for row in range(len(g.matching)):
            for column in range(len(g.matching[0])):
                if g.matching[row][column]:
                    logging.debug(f'{row} => {column + len(g.edges)}')
    

if __name__ == "__main__":
    #logging.basicConfig(encoding='utf-8', level=logging.DEBUG, format="%(message)s")
    AnimatedHopcroftKarp().hopcroftKarp(BigraphGenerator().generateBigraph())