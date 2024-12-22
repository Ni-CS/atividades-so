from MemoryPartition import MemoryPartition

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
                print(f"Falha ao alocar o processo {process.name} (PID: {process.pid}). Não foi encontrado uma partição apropriada. Swapping out...")
                if not self.swap_out_process():
                    print(f"Não há processos disponíveis para o swap out. Processo {process.name} (PID: {process.pid}) não pode ser alocado.")
                    return False
        else:
            print(f"Algoritmo de alocação desconhecido: {self.allocation_algorithm}")
            return False

    def first_fit_allocation(self, process):
        for partition in self.partitions:
            if partition.is_free() and partition.size >= process.size:
                partition.process = process
                print(f"Processo {process.name} (PID: {process.pid}) alocado em uma partição de tamanho {partition.size} (First-Fit).")
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
            print(f"Processo {process.name} (PID: {process.pid}) alocado em uma partição de tamanho {best_partition.size} (Best-Fit).")
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
            print(f"Processo {process.name} (PID: {process.pid}) alocado em uma partição de tamanho {worst_partition.size} (Worst-Fit).")
            return True
        return False

    def deallocate_process(self, pid):
        for partition in self.partitions:
            if partition.process and partition.process.pid == pid:
                print(f"Processo {partition.process.name} (PID: {pid}) removido da partição de tamanho {partition.size}.")
                partition.process.stop()
                partition.process = None
                return True
        print(f"Não foi encontrado um processo com ID {pid} na memória.")
        return False

    def swap_out_process(self):
        for partition in self.partitions:
            if not partition.is_free():
                process = partition.process
                partition.process = None
                self.swapped_out_processes.append(process)
                process.stop()
                print(f"Processo {process.name} (PID: {process.pid}) swapped out para a memória secundária.")
                return True
        return False

    def swap_in_process(self, pid):
        for process in self.swapped_out_processes:
            if process.pid == pid:
                self.swapped_out_processes.remove(process)
                if self.allocate_process(process):
                    print(f"Processo {process.name} (PID: {pid}) swapped de volta para a memória.")
                return
        print(f"Não foi encontrado um processo de ID {pid} na memória secundária.")

    def display_memory_state(self):
        print("\nAtual estado da memória:")
        for i, partition in enumerate(self.partitions):
            if partition.is_free():
                print(f"Partição {i+1}: Tamanho {partition.size}, Livre")
            else:
                p = partition.process
                print(f"Partição {i+1}: Tamanho {partition.size}, Ocupada pelo processo {p.name} (PID: {p.pid}, Tamanho: {p.size})")
        print("\nProcessos Swapped Out:")
        if self.swapped_out_processes:
            for process in self.swapped_out_processes:
                print(f"Processo {process.name} (PID: {process.pid}, Tamanho: {process.size})")
        else:
            print("Nada")