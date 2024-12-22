from MemoryManager import MemoryManager
from Process import Process

if __name__ == "__main__":
    while True:
        physical_memory_size = int(input("Digite o tamanho da memória física (em MB): "))
        virtual_memory_size = int(input("Digite o tamanho da memória virtual (em MB): "))
        if virtual_memory_size <= physical_memory_size:
            print("O tamanho da memória virtual deve ser maior que o tamanho da memória física. Por favor digite novamente.")
            continue

        page_size = int(input("Digite o tamanho da página (em MB): "))
        if page_size <= 0 or physical_memory_size % page_size != 0 or virtual_memory_size % page_size != 0:
            print("O tamanho da página deve ser um divisor positivo do tamanho de ambas as memórias, física e virtual. Por favor digite novamente.")
            continue

        break

    manager = MemoryManager(physical_memory_size, virtual_memory_size, page_size)

    while True:
        print("\nMenu:")
        print("1. Adicionar um processo")
        print("2. Acessar uma página")
        print("3. Exibir o estado da memória")
        print("4. Calcular fragmentação interna")
        print("5. Sair")

        choice = input("Digite a operação desejada: ")

        if choice == "1":
            name = input("Digite o nome do processo: ")
            pid = int(input("Digite o ID do processo: "))
            size = int(input("Digite o tamanho do processo (em MB): "))
            process = Process(name, pid, size)
            manager.allocate_process(process)

        elif choice == "2":
            pid = int(input("Digite o ID do processo: "))
            page_number = int(input("Digite o número da página: "))
            manager.access_page(pid, page_number)

        elif choice == "3":
            manager.display_memory_state()

        elif choice == "4":
            manager.calculate_internal_fragmentation()

        elif choice == "5":
            print("Encerrando programa.")
            break

        else:
            print("Opção Inválida. Por favor digite novamente.")
