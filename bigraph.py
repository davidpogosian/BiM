

class Bigraph:
    def __init__(self, name: str, edges: list[list[int]], matching: list[list[int]]) -> None:
        self.name   = name
        self.edges  = edges
        self.matching = matching

        self.nameTag = None

        # dict[vertexId, tag]
        self.vertexToTag: dict[int, float] = {}

        # dict[(vertex1, vertex2), tag]
        self.edgeToTag: dict[(int, int), float] = {}

    def getVertexMatchLookupTable(self) -> list[int]:
        lookupTable = [0] * (len(self.edges) + len(self.edges[0]))
        for vertex in range(len(lookupTable)):
            if vertex < len(self.edges):
                # left
                for entry in self.matching[vertex]:
                    if entry == 1:
                        lookupTable[vertex] = 1
            else:
                # right
                for row in self.matching:
                    if row[vertex - len(self.edges)] == 1:
                        lookupTable[vertex] = 1
        return lookupTable
    
    def matchingCardinality(self):
        cardinality = 0
        for row in self.matching:
            rowContainsEdge = False
            for entry in row:
                if entry == 1:
                    if rowContainsEdge:
                        print(f'INVALID MATCHING!!!')
                    cardinality += 1
                    rowContainsEdge = True
        return cardinality
