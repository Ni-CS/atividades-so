class MemoryPartition:
    def __init__(self, size):
            self.size = size
            self.process = None  #none quer dizer que ela tá livre

    def is_free(self):
        return self.process is None