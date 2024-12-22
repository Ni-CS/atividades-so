from Page import Page

class MemoryManager:
    def __init__(self, physical_memory_size, virtual_memory_size, page_size):
        self.physical_memory_size = physical_memory_size
        self.virtual_memory_size = virtual_memory_size
        self.page_size = page_size
        self.num_physical_pages = physical_memory_size // page_size
        self.num_virtual_pages = virtual_memory_size // page_size
        self.physical_memory = [None] * self.num_physical_pages
        self.virtual_memory = [None] * self.num_virtual_pages
        self.page_faults = 0
        self.processes = []
        self.page_replacement_queue = []

    def allocate_process(self, process):
            num_pages = -(-process.size // self.page_size)  # Calculate number of pages (ceil)
            if num_pages > self.num_virtual_pages:
                print(f"Processo {process.name} (PID: {process.pid}) ultrapassa o tamanho da memória virtual e não pode ser alocado.")
                return False

            process.pages = [Page(process.pid, i) for i in range(num_pages)]
            allocated_pages = 0
            for page in process.pages:
                if allocated_pages < self.num_virtual_pages:
                    self.virtual_memory[allocated_pages] = page
                    allocated_pages += 1
                else:
                    print(f"Memória virtual insuficiente para o processo {process.name} (PID: {process.pid}).")
                    return False

            print(f"Processo {process.name} (PID: {process.pid}) alocado com {num_pages} páginas.")
            self.processes.append(process)
            return True

    def access_page(self, process_id, page_number):
        page = next((p for p in self.virtual_memory if p and p.process_id == process_id and p.page_number == page_number), None)
        if not page:
            print(f"Página {page_number} do processo {process_id} não foi encontrada na memória virtual.")
            return

        if page not in self.physical_memory:
            self.page_faults += 1
            print(f"Falha de página para o processo {process_id}, página {page_number}.")
            self.handle_page_fault(page)
        else:
            print(f"Página {page_number} do processo {process_id} já está na memória física.")

    def handle_page_fault(self, page):
        if None in self.physical_memory:
            free_index = self.physical_memory.index(None)
            self.physical_memory[free_index] = page
            self.page_replacement_queue.append(page)
            print(f"Página {page.page_number} do processo {page.process_id} carregada na memória física no frame {free_index}.")
        else:
            victim_page = self.page_replacement_queue.pop(0)
            victim_index = self.physical_memory.index(victim_page)
            self.physical_memory[victim_index] = page
            self.page_replacement_queue.append(page)
            print(f"Página {victim_page.page_number} do processo {victim_page.process_id} substituída pela página {page.page_number} do processo {page.process_id}.")

    def display_memory_state(self):
        print("\nEstado da memória física:")
        for i, page in enumerate(self.physical_memory):
            if page:
                print(f"Frame {i}: Processo {page.process_id}, Página {page.page_number}")
            else:
                print(f"Frame {i}: Livre")

        print("\nEstado da memória virtual:")
        for i, page in enumerate(self.virtual_memory):
            if page:
                print(f"Slot {i}: Processo {page.process_id}, Página {page.page_number}")
            else:
                print(f"Slot {i}: Livre")

        print(f"\nFalhas de páginas: {self.page_faults}")
        
    def calculate_internal_fragmentation(self):
        fragmentation = 0
        for process in self.processes:
            total_pages = len(process.pages)
            last_page_size = process.size % self.page_size or self.page_size
            fragmentation += (self.page_size - last_page_size) if total_pages > 0 else 0
        print(f"\nFragmentação Interna Total: {fragmentation} MB")