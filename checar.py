import threading

# Define una función que será ejecutada en cada hilo
def mi_funcion(id):
    # Realiza algún trabajo en el hilo y retorna un valor
    resultado = f'Resultado del hilo {id}'
    return resultado

# Crea una lista para almacenar los hilos
hilos = []

# Crea un diccionario para almacenar los resultados de cada hilo
resultados = {}

# Número de hilos que deseas crear
num_hilos = 5

# Inicia los hilos y almacena sus objetos en la lista 'hilos'
for i in range(num_hilos):
    hilo = threading.Thread(target=lambda i=i: resultados.update({i: mi_funcion(i)}))
    hilos.append(hilo)
    hilo.start()

# Espera a que todos los hilos terminen
for hilo in hilos:
    hilo.join()

# Ahora, puedes acceder a los resultados de cada hilo usando el diccionario 'resultados'
for i, resultado in resultados.items():
    print(f'Hilo {i}: {resultado}')
