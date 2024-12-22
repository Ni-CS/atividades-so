from Process import Process
from MemoryManager import MemoryManager

if __name__ == "__main__":
    #configuracoes da memoria
    total_memory = 1000  #memoria total em mb
    partition_sizes = [300, 200, 500]  #tamanho das particoes fixas

    #selecao do algoritmo de alocacao
    print("Selecione um algoritmo de alocação (first-fit, best-fit, worst-fit):")
    allocation_algorithm = input("Digite o algoritmo: ").strip().lower()

    #iniciar o gerenciador de memoria
    memory_manager = MemoryManager(total_memory, partition_sizes, allocation_algorithm)

    while True:
        print("\nMenu:")
        print("1. Adicionar um processo")
        print("2. Remover um processo")
        print("3. Fazer Swap in de um processo")
        print("4. Mostrar o estado da memória")
        print("5. Sair")

        choice = input("Digite a operação desejada: ")

        if choice == "1":
            name = input("Digite o nome do processo: ")
            pid = int(input("Digite o ID do processo: "))
            size = int(input("Digite o tamanho do processo: "))
            process = Process(name, pid, size)
            if not memory_manager.allocate_process(process):
                break
        elif choice == "2":
            pid = int(input("Digite o ID do processo a ser removido: "))
            memory_manager.deallocate_process(pid)
        elif choice == "3":
            pid = int(input("Digite o ID do processo para fazer o Swap in: "))
            memory_manager.swap_in_process(pid)
        elif choice == "4":
            memory_manager.display_memory_state()
        elif choice == "5":
            print("Fechando programa.")
            break
        else:
            print("Escolha Inválida. Digite novamente.")
