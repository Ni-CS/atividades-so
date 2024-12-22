import threading
import time
import random

class MemoryPartition:
    def __init__(self, size):
        self.size = size
        self.process = None  # None means the partition is free

    def is_free(self):
        return self.process is None

class Process:
    def __init__(self, name, pid, size):
        self.name = name
        self.pid = pid
        self.size = size
        self.running = True
        self.thread = threading.Thread(target=self.run)
        self.thread.daemon = True  # Ensure the thread ends when the main program exits
        self.thread.start()

    def run(self):
        while self.running:
            time.sleep(1)

    def stop(self):
        self.running = False

class MemoryManager:
    def __init__(self, total_memory, partition_sizes, allocation_algorithm="first-fit"):
        self.total_memory = total_memory
        self.partitions = [MemoryPartition(size) for size in partition_sizes]
        self.swapped_out_processes = []  # List to store processes in secondary memory
        self.allocation_algorithm = allocation_algorithm

    def allocate_process(self, process):
        allocation_methods = {
            "first-fit": self.first_fit_allocation,
            "best-fit": self.best_fit_allocation,
            "worst-fit": self.worst_fit_allocation
        }
        if self.allocation_algorithm in allocation_methods:
            while True:
                allocated = allocation_methods[self.allocation_algorithm](process)
                if allocated:
                    return True
                print(f"Failed to allocate process {process.name} (PID: {process.pid}). No suitable partition found. Swapping out...")
                if not self.swap_out_process():
                    print(f"No processes available to swap out. Process {process.name} (PID: {process.pid}) cannot be allocated.")
                    return False
        else:
            print(f"Unknown allocation algorithm: {self.allocation_algorithm}")
            return False

    def first_fit_allocation(self, process):
        for partition in self.partitions:
            if partition.is_free() and partition.size >= process.size:
                partition.process = process
                print(f"Process {process.name} (PID: {process.pid}) allocated to partition of size {partition.size} (First-Fit).")
                return True
        return False

    def best_fit_allocation(self, process):
        best_partition = None
        for partition in self.partitions:
            if partition.is_free() and partition.size >= process.size:
                if not best_partition or partition.size < best_partition.size:
                    best_partition = partition
        if best_partition:
            best_partition.process = process
            print(f"Process {process.name} (PID: {process.pid}) allocated to partition of size {best_partition.size} (Best-Fit).")
            return True
        return False

    def worst_fit_allocation(self, process):
        worst_partition = None
        for partition in self.partitions:
            if partition.is_free() and partition.size >= process.size:
                if not worst_partition or partition.size > worst_partition.size:
                    worst_partition = partition
        if worst_partition:
            worst_partition.process = process
            print(f"Process {process.name} (PID: {process.pid}) allocated to partition of size {worst_partition.size} (Worst-Fit).")
            return True
        return False

    def deallocate_process(self, pid):
        for partition in self.partitions:
            if partition.process and partition.process.pid == pid:
                print(f"Process {partition.process.name} (PID: {pid}) removed from partition of size {partition.size}.")
                partition.process.stop()
                partition.process = None
                return True
        print(f"No process with PID {pid} found in memory.")
        return False

    def swap_out_process(self):
        allocated_partitions = [partition for partition in self.partitions if not partition.is_free()]
        if allocated_partitions:
            partition = random.choice(allocated_partitions)
            process = partition.process
            partition.process = None
            self.swapped_out_processes.append(process)
            process.stop()
            print(f"Process {process.name} (PID: {process.pid}) swapped out to secondary memory.")
            return True
        return False

    def swap_in_process(self, pid):
        for process in self.swapped_out_processes:
            if process.pid == pid:
                self.swapped_out_processes.remove(process)
                if self.allocate_process(process):
                    print(f"Process {process.name} (PID: {pid}) swapped back into memory.")
                return
        print(f"No process with PID {pid} found in secondary memory.")

    def display_memory_state(self):
        print("\nCurrent Memory State:")
        total_fragmentation = 0
        for i, partition in enumerate(self.partitions):
            if partition.is_free():
                print(f"Partition {i+1}: Size {partition.size}, Free")
                total_fragmentation += partition.size
            else:
                p = partition.process
                print(f"Partition {i+1}: Size {partition.size}, Occupied by Process {p.name} (PID: {p.pid}, Size: {p.size})")
        print(f"\nTotal Fragmentation (External): {total_fragmentation}")

        print("\nSwapped Out Processes:")
        if self.swapped_out_processes:
            for process in self.swapped_out_processes:
                print(f"Process {process.name} (PID: {process.pid}, Size: {process.size})")
        else:
            print("None")

if __name__ == "__main__":
    # Define memory configuration
    total_memory = 1000  # Total memory in MB
    partition_sizes = [300, 200, 500]  # Sizes of fixed partitions

    # Select allocation algorithm
    print("Select allocation algorithm (first-fit, best-fit, worst-fit):")
    allocation_algorithm = input("Enter algorithm: ").strip().lower()

    # Initialize memory manager
    memory_manager = MemoryManager(total_memory, partition_sizes, allocation_algorithm)

    while True:
        print("\nMenu:")
        print("1. Add a process")
        print("2. Remove a process")
        print("3. Swap in a process")
        print("4. Display memory state")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter process name: ")
            pid = int(input("Enter process PID: "))
            size = int(input("Enter process size: "))
            process = Process(name, pid, size)
            memory_manager.allocate_process(process)
        elif choice == "2":
            pid = int(input("Enter process PID to remove: "))
            memory_manager.deallocate_process(pid)
        elif choice == "3":
            pid = int(input("Enter process PID to swap in: "))
            memory_manager.swap_in_process(pid)
        elif choice == "4":
            memory_manager.display_memory_state()
        elif choice == "5":
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please try again.")
