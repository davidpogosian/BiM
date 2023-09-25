from bigraph import Bigraph
from bigraphGenerator import BigraphGenerator
import logging


class SinglePath:
    def __init__(self):
        pass

    def computeMatching(self, g: Bigraph):
        isVertexMatched = [0] * (len(g.edges) + len(g.edges[0]))
        alternator = True
        for row in range(len(g.edges)):
            for col in range(len(g.edges[0])):
                if isVertexMatched[row] or isVertexMatched[col + len(g.edges)]:
                    continue
                if g.edges[row][col] == 1:
                    isVertexMatched[row] = 1
                    isVertexMatched[col + len(g.edges)] = 1
                    tail = row
                    head = col + len(g.edges)
                    path = [tail, head]
                    iterations = 0
                    while True:
                        headNext = None
                        tailNext = None
                        logging.debug(f'tail-head: {tail}-{head}')
                        if head < len(g.edges):
                            for c in range(len(g.edges[0])):
                                if g.edges[head][c] == 1:
                                    if not isVertexMatched[c + len(g.edges)]:
                                        headNext = c + len(g.edges)
                                        logging.debug(f'headNext: {headNext}')
                                        break
                        else:
                            for r in range(len(g.edges)):
                                if g.edges[r][head - len(g.edges)] == 1:
                                    if not isVertexMatched[r]:
                                        headNext = r
                                        logging.debug(f'headNext: {headNext}')
                                        break
                        if tail < len(g.edges):
                            for c in range(len(g.edges[0])):
                                if g.edges[tail][c] == 1:
                                    if not isVertexMatched[c + len(g.edges)]:
                                        tailNext = c + len(g.edges)
                                        logging.debug(f'tailNext: {tailNext}')
                                        break
                        else:
                            for r in range(len(g.edges)):
                                if g.edges[r][tail - len(g.edges)] == 1:
                                    if not isVertexMatched[r]:
                                        tailNext = r
                                        logging.debug(f'headNext: {tailNext}')
                                        break
                        logging.debug(f'path: {path}')
                        if headNext == None and tailNext == None:
                            logging.debug(f'both ends dead')
                            if alternator:
                                alternator = not alternator
                                logging.debug(f'rolling back tail')
                                if path[0] > path[1]:
                                    g.matching[path[1]][path[0] - len(g.edges)] = 1
                                else:
                                    g.matching[path[0]][path[1] - len(g.edges)] = 1
                                if len(path) >= 3:
                                    tail = path[2]
                                    path = path[2:]
                                    logging.debug(f'tail rolls back; new tail: {tail}; new path: {path}')
                                else:
                                    logging.debug(f'tail got nowhere to go')
                                    break
                            else:
                                logging.debug(f'rolling back head')
                                if path[-1] > path[-2]:
                                    g.matching[path[-2]][path[-1] - len(g.edges)] = 1
                                else:
                                    g.matching[path[-1]][path[-2] - len(g.edges)] = 1
                                if len(path) >= 3:
                                    head = path[len(path)-3]
                                    path = path[:len(path)-2]
                                    logging.debug(f'head rolls back; new head: {head}; new path: {path}')
                                else:
                                    logging.debug(f'head got nowhere to go')
                                    break
                            continue
                        elif headNext == None:
                            if path[-1] > path[-2]:
                                g.matching[path[-2]][path[-1] - len(g.edges)] = 1
                            else:
                                g.matching[path[-1]][path[-2] - len(g.edges)] = 1
                            if len(path) >= 3:
                                head = path[len(path)-3]
                                path = path[:len(path)-2]
                                logging.debug(f'head rolls back; new head: {head}; new path: {path}')
                            else:
                                logging.debug(f'head got nowhere to go')
                                break
                        elif tailNext == None:
                            if path[0] > path[1]:
                                g.matching[path[1]][path[0] - len(g.edges)] = 1
                            else:
                                g.matching[path[0]][path[1] - len(g.edges)] = 1
                            if len(path) >= 3:
                                tail = path[2]
                                path = path[2:]
                                logging.debug(f'tail rolls back; new tail: {tail}; new path: {path}')
                            else:
                                logging.debug(f'tail got nowhere to go')
                                break
                        else:
                            path.insert(0, tailNext)
                            path.append(headNext)
                            isVertexMatched[headNext] = 1
                            isVertexMatched[tailNext] = 1
                            head = headNext
                            tail = tailNext
                            logging.debug(f'longer ap found! {path}')
                        iterations += 1
                    for x in g.matching:
                        logging.debug(x)




        



































if __name__ == "__main__":
    logging.basicConfig(encoding='utf-8', level=logging.DEBUG, format="%(message)s")
    g = Bigraph(
        'name',
        [
            [0, 0, 1, 0, 0, 1, 0, 0],
            [1, 0, 1, 0, 0, 1, 0, 0],
            [1, 0, 0, 0, 1, 1, 0, 1],
            [0, 1, 0, 0, 0, 0, 1, 0],
            [1, 0, 0, 0, 1, 0, 0, 0],
            [0, 1, 0, 0, 1, 0, 1, 0],
            [1, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 0, 0, 1, 1]
        ],
        [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ]
    )
# should be 4
    SinglePath().computeMatching(g)