import threading
import random
import time

# Número de filósofos
NUM_FILOSOFOS = 5

# Semáforos para os garfos
garfos = [threading.Semaphore(1) for _ in range(NUM_FILOSOFOS)]

# Tempo máximo que um filósofo pode esperar para comer (em segundos)
TEMPO_MAXIMO_ESPERA = 5

class Filosofo(threading.Thread):
    def __init__(self, id):
        super().__init__()
        self.id = id
        self.tempo_comer = random.uniform(1, 3)  # Tempo de comer aleatório entre 1 a 3 segundos

    def pensar(self):
        print(f'Filósofo {self.id} está pensando.')
        time.sleep(random.uniform(1, 2))  # Tempo de pensar aleatório

    def comer(self):
        print(f'Filósofo {self.id} começou a comer.')
        time.sleep(self.tempo_comer)  # Tempo de comer

    def run(self):
        while True:
            self.pensar()
            self.tentar_comer()

    def tentar_comer(self):
        inicio = time.time()
        while True:
            # Tentar pegar os garfos (esquerdo e direito)
            garfo_esquerdo = self.id
            garfo_direito = (self.id + 1) % NUM_FILOSOFOS
            
            # Tentar pegar o garfo da esquerda
            if garfos[garfo_esquerdo].acquire(timeout=TEMPO_MAXIMO_ESPERA):
                # Se pegou o garfo da esquerda, tentar pegar o da direita
                if garfos[garfo_direito].acquire(timeout=TEMPO_MAXIMO_ESPERA):
                    break  # Conseguiu pegar ambos os garfos
            
            # Se não conseguir pegar ambos, liberar o garfo da esquerda
            if garfos[garfo_esquerdo].locked():
                garfos[garfo_esquerdo].release()

            # Verifica se o tempo máximo de espera foi alcançado
            if time.time() - inicio > TEMPO_MAXIMO_ESPERA:
                print(f'Filósofo {self.id} desistiu de comer após esperar muito.')
                return  # Sai do loop se passou do tempo máximo de espera

        # Come e depois libera os garfos
        self.comer()
        garfos[garfo_esquerdo].release()
        garfos[garfo_direito].release()
        print(f'Filósofo {self.id} terminou de comer e soltou os garfos.')  

# Cria e inicia os filósofos
filósofos = [Filosofo(i) for i in range(NUM_FILOSOFOS)]
for filósofo in filósofos:
    filósofo.start()
