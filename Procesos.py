#Algoritmos y Estructura de Datos
#Facultad de Ingenieria
#Vianka Castro
#23201

#Hoja de Trabajo 5 -


import simpy
import random
import numpy as np

random_seed = 42
RAM_cap = 100
intervalo_de_creacion = 1
instrucciones_CPU = 6
num_procesos = 200

tiempos_procesos = []

def main():
    random.seed(random_seed)

    env = simpy.Environment()
    RAM = simpy.Container(env, capacity=RAM_cap, init=RAM_cap)
    CPU = simpy.Resource(env, capacity=2)

    env.process(generar_procesos(env, RAM, CPU))

    env.run(until=100)  # Ejecutar la simulación durante 100 unidades de tiempo

    calcular_estadisticas()


def crear_proceso(env, nombre, RAM, CPU):
    inicio = env.now
    memoria_necesaria = random.randint(1, 10)
    instrucciones_totales = random.randint(1, 10)

    print(f"{nombre} solicita {memoria_necesaria} memoria RAM en {env.now}")
    yield RAM.get(memoria_necesaria)

    print(f"{nombre} asigna {memoria_necesaria} memoria de RAM en {env.now}")
    instrucciones_faltantes = instrucciones_totales

    while instrucciones_faltantes > 0:
        with CPU.request() as req:
            print(f"{nombre} está esperando en {env.now}")
            yield req

            print(f"{nombre} obtiene CPU en {env.now}")
            instrucciones_CPU = min(instrucciones_faltantes, instrucciones_totales)
            yield env.timeout(1)  # Simular tiempo de ejecución

            instrucciones_faltantes -= instrucciones_CPU

            if instrucciones_faltantes <= 0:
                tiempo_fin = env.now
                tiempo_proceso = tiempo_fin - inicio
                print(f"{nombre} completó el proceso en tiempo {env.now}")
                tiempos_procesos.append(tiempo_proceso)  # Se agrega el tiempo de proceso a la lista
                yield RAM.put(memoria_necesaria)  # Liberar memoria
                break

            print(f"{nombre} procesando en CPU en tiempo {env.now}")
            espera = random.randint(1, 2)

            if espera == 1:
                tiempo_espera = random.randint(1, 10)
                print(f"{nombre} esperando por I/O durante {tiempo_espera} unidades de tiempo en t: {env.now}")
                yield env.timeout(tiempo_espera)
            elif espera == 2:
                print(f"{nombre} listo para ejecutar (ir a ready) nuevamente en t: {env.now}")
                continue

def generar_procesos(env, RAM, CPU):
    num_procesos = 0
    while True:
        yield env.timeout(random.expovariate(1.0 / intervalo_de_creacion))
        num_procesos += 1
        env.process(crear_proceso(env, f"Proceso {num_procesos}", RAM, CPU))

def calcular_estadisticas():
    tiempo_promedio = np.mean(tiempos_procesos)
    desviacion_estandar = np.std(tiempos_procesos)

    print(f"Tiempo promedio de procesamiento: {tiempo_promedio}")
    print(f"Desviación estándar: {desviacion_estandar}")

if __name__ == '__main__':
    main()
