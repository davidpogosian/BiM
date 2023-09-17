

class Bigraph:
    def __init__(self, name: str, left: list[int], right: list[int], edges: dict[int, list[int]]) -> None:
        self.name   = name
        self.left   = left
        self.right  = right
        self.edges  = edges