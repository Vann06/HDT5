#Algoritmos y Estructura de Datos
#Facultad de Ingenieria
#Vianka Castro
#23201

#Hoja de Trabajo 5


import simpy
import random
import numpy as np

RANDOM_SEED = 42
RAM_CAP = 200
INSTRUCCIONES_CPU_POR_UNIDAD_DE_TIEMPO = 1
INTERVALO_CREACION = 10 #tambien cambia
INSTRUCCIONES_CPU_POR_UNIDAD_DE_TIEMPO = 3 #cambios
numero_procesos = 150 #varia

random.seed(RANDOM_SEED)

def main():

    tiempos_procesos = []
    for _ in range(numero_procesos):
        env = simpy.Environment()
        RAM = simpy.Container(env, init=RAM_CAP, capacity=RAM_CAP)
        CPU = simpy.Resource(env, capacity=1)  # CPU con capacidad 1 (un solo proceso a la vez)
        env.process(generar_procesos(env, RAM, CPU, tiempos_procesos))
        env.run(until=100)

    print(f"para {numero_procesos} :")
    calcular_estadisticas(tiempos_procesos)

def generar_procesos(env, RAM, CPU, tiempos_procesos):
    num_proceso = 0
    for num_proceso in range(1, numero_procesos + 1):
        tiempo_inicio = env.now
        yield env.timeout(random.expovariate(1.0 / INTERVALO_CREACION))
        env.process(crear_proceso(env, f"Proceso {num_proceso}", RAM, CPU, tiempos_procesos, tiempo_inicio))


def crear_proceso(env, nombre, RAM, CPU, tiempos_procesos, tiempo_inicio):

    memoria_necesaria = random.randint(1, 10)
    instrucciones_totales = random.randint(1, 10)

    print(f"{nombre} solicita {memoria_necesaria} memoria RAM en {env.now}")
    yield RAM.get(memoria_necesaria)

    print(f"{nombre} asigna {memoria_necesaria} memoria de RAM en {env.now}")
    instrucciones_faltantes = instrucciones_totales

    while instrucciones_faltantes > 0:
        with CPU.request() as req:
            print(f"{nombre} Solicitando ejecución del CPU en tiempo  {env.now}")
            yield req

            print(f"{nombre} obtiene CPU en {env.now}")
            yield env.timeout(1)  # Tiempo de ejecución de 1 unidad de tiempo
            instrucciones_faltantes -= INSTRUCCIONES_CPU_POR_UNIDAD_DE_TIEMPO

            if instrucciones_faltantes <= 0:
                tiempo_fin = env.now
                tiempo = tiempo_fin - tiempo_inicio
                print(f"{nombre} completó el proceso en tiempo {env.now}")
                tiempos_procesos.append(tiempo)


            print(f"{nombre} procesando en CPU en tiempo {env.now}")
            espera = random.randint(1,2) # Generar número al azar para verificar si pasa a Waiting

            if espera == 1:
                print(f"{nombre} pasa a estado Waiting en tiempo {env.now}")
                yield env.timeout(random.randint(1, 10))
                print(f"{nombre} regresa a estado Ready en tiempo {env.now}")
            elif espera == 2:
                print(f"{nombre} esta listo {env.now}")
                continue

            print(f"{nombre} termino su proceso,liberando {memoria_necesaria} de RAMen tiempo {env.now}")
            yield RAM.put(memoria_necesaria)  # Liberar memoria


def calcular_estadisticas(tiempos_procesos):
    tiempo_promedio = np.mean(tiempos_procesos)
    desviacion_estandar = np.std(tiempos_procesos)

    print(f"Tiempo promedio de procesamiento: {tiempo_promedio}")
    print(f"Desviación estándar: {desviacion_estandar}")


if __name__ == '__main__':
    main()
