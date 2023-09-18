


class UniqueTagGenerator:
    def __init__(self):
        self.val = 0.5 # 0.5 instead of 0, to not look like id

    def generate(self) -> float:
        self.val += 1
        return self.val