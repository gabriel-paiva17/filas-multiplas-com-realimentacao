from collections import deque
import time

def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()  # Captura o tempo inicial
        result = func(*args, **kwargs)  # Executa a função original
        end_time = time.time()  # Captura o tempo após a execução
        execution_time = end_time - start_time  # Calcula o tempo de execução
        print(f"Function '{func.__name__}' executed in {execution_time:.6f} seconds")
        return result  # Retorna o resultado da função original
    return wrapper

class Process:
    def __init__(self, pid, burst_time):
        self.pid = pid
        self.remaining_time = burst_time

    def __repr__(self):
        return f"(ID = {self.pid})"

class MultiLevelFeedbackQueue:
    def __init__(self, num_queues, quantums):
        self.queues = [deque() for _ in range(num_queues)]
        self.quantums = quantums

    def add_process(self, process):
        self.queues[0].append(process)

    def print_queues(self):
        print("\n\n")
        for i in range (len(self.queues)):
            print(f"{i+1} - {self.queues[i]}")

    @timing_decorator
    def execute(self):
        while any(self.queues):  # Verifica se ainda há processos em alguma fila
            for i in range(len(self.queues)):
                queue = self.queues[i]
                while queue:  # Processa todos os processos na fila atual

                    self.print_queues()

                    process = queue.popleft()

                    execution_time = min(self.quantums[i], process.remaining_time)

                    print(f"Executing {process} from Queue {i + 1}/ Remaining time: {process.remaining_time}")

                    process.remaining_time -= execution_time

                    time.sleep(execution_time)
                    
                    if process.remaining_time > 0:

                        print(f"Quantum expired for {process}. Remaining time: {process.remaining_time}")

                        if i < len(self.queues) - 1:  # Move para a próxima fila
                            self.queues[i + 1].append(process)
                            print(f"Moving {process} to Queue {i + 2}")
                        else:  # Se estiver na última fila, mantém na mesma fila
                            queue.append(process)
                            print(f"{process} stays in Queue {i + 1}")
                    else:
                        print(f"Process {process.pid} completed execution.")

        print("All processes have been executed.")

# Exemplo de uso
num_queues = 3
quantums = [5, 10, 20]  # Define os tempos de quantum para cada fila

scheduler = MultiLevelFeedbackQueue(num_queues, quantums)

# Adicionando processos ao escalonador
scheduler.add_process(Process(pid=1, burst_time=10))
scheduler.add_process(Process(pid=2, burst_time=15))
scheduler.add_process(Process(pid=3, burst_time=25))
scheduler.add_process(Process(pid=4, burst_time=5))

# Executando o escalonamento
scheduler.execute()
