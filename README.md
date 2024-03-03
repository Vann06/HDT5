#Simulador de Gestión de Procesos#

Este proyecto es un simulador básico de gestión de procesos en un sistema operativo. 
Utiliza SimPy para simular la ejecución de procesos en la CPU y la gestión de la memoria RAM.

Parámetros Personalizables
semilla_aleatoria: La semilla para la generación de números aleatorios.
capacidad_ram: La capacidad total de la memoria RAM en unidades.
intervalo_creacion_procesos: El intervalo medio de creación de nuevos procesos.
instrucciones_cpu_por_tiempo: La cantidad de instrucciones de CPU ejecutadas por unidad de tiempo.
cantidad_procesos: El número total de procesos a simular.


#Decisión Final#

Tomando en cuenta todos los resultados obtenidos se puede reflejar un cambio drástico entre los tiempos 
promedio de cada tipo de proceso dependiendo de cada intervalo y memoria  accesible. Al analizar los resultados,
se puede notar que no existió mucha diferencia entre las cantidades de memoria. Por otro lado, el tiempo promedio 
se reduce significativamente cuando se pueden realizar más rápidamente las instrucciones por unidad de tiempo de 6.
Incluso con dos procesadores es aún mejor su rendimiento. Se puede deducir que, la mejor estrategia es la ii ya que 
al utilizar una memoria RAM baja o simple pero con un procesador rápido el tiempo de proceso es el menor entre todos.  
