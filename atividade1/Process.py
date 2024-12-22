import threading
import time

class Process:
    def __init__(self, name, pid, size):
            self.name = name
            self.pid = pid
            self.size = size
            self.running = True
            self.thread = threading.Thread(target=self.run)
            self.thread.daemon = True  #garantia de que a thread termine quando o programa encerrar
            self.thread.start()

    def run(self):
        while self.running:
            time.sleep(1)

    def stop(self):
        self.running = False