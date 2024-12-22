class Process:
    def __init__(self, name, pid, size):
        self.name = name
        self.pid = pid
        self.size = size
        self.pages = []