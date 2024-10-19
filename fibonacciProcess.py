from time import time
import multiprocessing
import sys

def fibo(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibo(n - 1) + fibo(n - 2)

class FiboWorker(multiprocessing.Process):
    def _init_(self, n, pid): #se cambia que reciba en vez de un numero un array
        multiprocessing.Process._init_(self)
        self.n = n
        self._pid = pid

    def run(self): #el resultado sera un array con las posciones ya con el fibonnaci correspondiente
        resultado = []
        for n in self.n:
            resultado.append(fibo(n))
        print(f"[{self._pid}] Resultados: {resultado}")

def dividir_en(secuencia, diviciones): #18 el numero que le toca calcular a cada procesador
    intervalo = []
    acumulador = 0
    for i in range(0, len(secuencia), diviciones): #0-143 saltando de 18 en 18
        inicio = acumulador # 0
        acumulador += diviciones
        chunk = []
        for j in range(inicio, acumulador, 1):
            chunk.append(secuencia[j])  # Extraer un segmento de la lista
        intervalo.append(chunk)         # Agregarlo a la lista de chunks
    return intervalo

def main():
    secuencia = [33] * 144

    num_cpus = multiprocessing.cpu_count() # CPUs disponibles
    diviciones = len(secuencia)/num_cpus

    particion = dividir_en(secuencia, int(diviciones))

    print(f"Calculando el Fibonacci de {len(secuencia)} números usando {num_cpus} CPUs en paralelo")

    procesos = [] # Vector de procesos
    ts = time() # se toma tiempo

    for x in range(num_cpus): # Ciclo para crear trabajadores, 8 nucleos
        print(f"Iniciando trabajador {x} con {len(particion[x])} elementos.")
        print(particion[x])
        worker = FiboWorker(particion[x],x)
        worker.start()
        procesos.append(worker)

    for x in range(num_cpus): # Ciclo para esperar por trabajadores
        print(f"Esperando por trabajador {x}")
        procesos[x].join()

    print(f"Tomo {time() - ts}")

if _name_ == "_main_":
    main()
