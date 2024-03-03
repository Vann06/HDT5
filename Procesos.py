#Algoritmos y Estructura de Datos
#Facultad de Ingenieria
#Vianka Castro
#23201
#Hoja de Trabajo 5
#2/03/24


import simpy
import random
import numpy as np

semilla_aleatoria = 42
capacidad_ram = 100
intervalo_creacion_procesos = 1 #tambien cambia
instrucciones_cpu_por_tiempo = 3 #cambios
cantidad_procesos = 100 #varia

random.seed(semilla_aleatoria)

def main():

    tiempos_procesos = []
    for _ in range(cantidad_procesos):
        env = simpy.Environment()
        ram = simpy.Container(env, init=capacidad_ram, capacity=capacidad_ram)
        cpu = simpy.Resource(env, capacity=2)
        env.process(generar_procesos(env, ram, cpu, tiempos_procesos))
        env.run(until=100)

    print(f"Para {cantidad_procesos} procesos:")
    calcular_estadisticas(tiempos_procesos)

def generar_procesos(env, ram, cpu, tiempos_procesos):
    num_proceso = 0
    for num_proceso in range(1, cantidad_procesos + 1):
        tiempo_inicio = env.now
        yield env.timeout(random.expovariate(1.0 / intervalo_creacion_procesos))
        env.process(crear_proceso(env, f"Proceso {num_proceso}", ram, cpu, tiempos_procesos, tiempo_inicio))


def crear_proceso(env, nombre, ram, cpu, tiempos_procesos, tiempo_inicio):

    memoria_necesaria = random.randint(1, 10)
    instrucciones_totales = random.randint(1, 10)

    print(f"{nombre} solicita {memoria_necesaria} memoria RAM en {env.now}")
    yield ram.get(memoria_necesaria)

    print(f"{nombre} asigna {memoria_necesaria} memoria de RAM en {env.now}")
    instrucciones_faltantes = instrucciones_totales

    while instrucciones_faltantes > 0:
        with cpu.request() as req:
            print(f"{nombre} Solicitando ejecución del CPU en tiempo  {env.now}")
            yield req

            print(f"{nombre} obtiene CPU en {env.now}")
            yield env.timeout(1)
            instrucciones_faltantes -= instrucciones_cpu_por_tiempo

            if instrucciones_faltantes <= 0:
                tiempo_fin = env.now
                tiempo = tiempo_fin - tiempo_inicio
                print(f"{nombre} completó el proceso en tiempo {env.now}")
                tiempos_procesos.append(tiempo)

            print(f"{nombre} procesando en CPU en tiempo {env.now}")
            espera = random.randint(1, 2)

            if espera == 1:
                print(f"{nombre} pasa a estado Waiting en tiempo {env.now}")
                yield env.timeout(random.randint(1, 10))
                print(f"{nombre} regresa a estado Ready en tiempo {env.now}")
            elif espera == 2:
                print(f"{nombre} está listo {env.now}")
                continue

            print(f"{nombre} terminó su proceso, liberando {memoria_necesaria} de RAM en tiempo {env.now}")
            yield ram.put(memoria_necesaria)


def calcular_estadisticas(tiempos_procesos):
    tiempo_promedio = np.mean(tiempos_procesos)
    desviacion_estandar = np.std(tiempos_procesos)

    print(f"Tiempo promedio de procesamiento: {tiempo_promedio}")
    print(f"Desviación estándar: {desviacion_estandar}")


if __name__ == '__main__':
    main()

