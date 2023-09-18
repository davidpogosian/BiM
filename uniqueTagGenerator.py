


class UniqueTagGenerator:
    def __init__(self):
        self.val = 0

    def generate(self) -> int:
        self.val += 1
        return self.val