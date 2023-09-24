from bigraphGenerator import BigraphGenerator
from bigraph import Bigraph

class Intersection:
    def __init__(self, center=None):
        self.center: int = center
        self.edges: list[tuple(int, int)] = []
        self.weights: dict[tuple(int, int), int] = {}
    
    def __str__(self) -> str:
        return str(self.edges)

class Path:
    def __init__(self):
        pass

class SubgraphIntersection:
    def __init__(self):
        pass

    def computeMaximumMatching(self, g: Bigraph):
        intersections = []
        degreeOfVertices = [0] * (len(g.edges) + len(g.edges[0]))
        for row in range(len(g.edges)):
            for column in range(len(g.edges[0])):
                if g.edges[row][column] == 1:
                    degreeOfVertices[row] += 1
                    degreeOfVertices[column + len(g.edges)] += 1

        for vertex in range(len(degreeOfVertices)):
            if degreeOfVertices[vertex] > 2:
                newIntersection = Intersection(vertex)
                if vertex < len(g.edges):
                    for column in range(len(g.edges[0])):
                        if g.edges[vertex][column] == 1:
                            newIntersection.edges.append((vertex, column + len(g.edges)))
                else:
                    for row in range(len(g.edges)):
                        if g.edges[row][vertex - len(g.edges)] == 1:
                            newIntersection.edges.append((row, vertex))
                intersections.append(newIntersection)

        for intersection in intersections:
            print(intersection)
            for edge in intersection.edges:
                endpoint = edge[0] if edge[0] != intersection.center else edge[1]
                print(endpoint)
                probe = endpoint
                pathLength = 0
                firstIterationFlag = True
                while True: # infinite loop :)
                    print('cycle')
                    if degreeOfVertices[probe] > 2:
                        intersection.weights[edge] = 0 if pathLength % 2 == 0 else -1
                        break
                    if degreeOfVertices[probe] == 1:
                        intersection.weights[edge] = 0 if pathLength % 2 == 0 else -1
                        break
                    if degreeOfVertices[probe] == 2:
                        if probe < len(g.edges):
                            for column in range(len(g.edges[0])):
                                if g.edges[probe][column] == 1:
                                    probe = column + len(g.edges)
                                    break
                        else:
                            for row in range(len(g.edges)):
                                if g.edges[row][probe - len(g.edges)] == 1:
                                    probe = row
                                    break
                    if firstIterationFlag:
                        firstIterationFlag = False
                    else:
                        pathLength += 1

        
        # identify subgraphs
        # apply weights to edges in intersections
        # pick out edges from intersections
        # produce matching
































if __name__ == "__main__":
    SubgraphIntersection().computeMaximumMatching(BigraphGenerator().generateBigraph())