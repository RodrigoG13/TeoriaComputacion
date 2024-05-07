from rutas import *
import random
import time
import multiprocessing

def generar_rutas_s(res, tablero: tuple, indices: dict, estado_inicial:int, estado_final: int, ruta_colores:list, 
                  nombre_arch:str, q=None):
    file_lock = threading.Lock()
    variable_lock = threading.Lock()

    movs_casillas = {}

    for i in range(1, len(ruta_colores)+1):
        movs_casillas[i] = {}
    
    with open(f"{nombre_arch}_todas.txt", "w") as todas, open(f"{nombre_arch}_ganadoras.txt", "w") as ganadoras:
        resultados = threaded_generar_rutas(file_lock, variable_lock, ruta_colores, tablero, indices, estado_inicial, estado_final,todas, ganadoras, movs_casillas, res)
        for i in resultados.keys():
            todas.write("\n".join(resultados[i][0]))
            todas.write("\n")
            ganadoras.write("\n".join(resultados[i][1]))
            ganadoras.write("\n")

    if q:
        q.put(movs_casillas)
    return movs_casillas


if __name__ == "__main__":

    tablero = (
        (("b", False, 1), ("r", False, 2), ("b", False, 3), ("r", False, 4)),
        (("r", False, 5), ("b", False, 6), ("r", False, 7), ("b", False, 8)),
        (("b", False, 9), ("r", False, 10), ("b", False, 11), ("r", False, 12)),
        (("r", False, 13), ("b", False, 14), ("r", False, 15), ("b", False, 16))
    )

    indices = {1: (0,0), 2: (0,1), 3: (0,2), 4: (0,3),
               5: (1,0), 6: (1,1), 7: (1,2), 8: (1,3),
               9: (2,0), 10: (2,1), 11: (2,2), 12: (2,3),
               13: (3,0), 14: (3,1), 15: (3,2), 16: (3,3)}

    n = 10

    cadenas = ["r", "b"]

    ruta_colores = [random.choice(cadenas) for _ in range(0, n)]
    #ruta_colores = ["r", "b", "b"]

    resultados1 = {}
    resultados16 = {}

    q1 = multiprocessing.Queue()
    q2 = multiprocessing.Queue()

    inicio = time.time()

    generar_rutas_ficha1 = multiprocessing.Process(target=generar_rutas_s, args=(resultados1, tablero, indices, 1, 9, ruta_colores, "f1", q1))
    generar_rutas_ficha16 = multiprocessing.Process(target=generar_rutas_s, args=(resultados16, tablero, indices, 4, 13, ruta_colores, "f16", q2))

    generar_rutas_ficha1.start()
    generar_rutas_ficha16.start()

    movs_casillas_ficha1 = q1.get()  # Captura el resultado de movs_casillas para el primer proceso
    movs_casillas_ficha16 = q2.get()  # Captura el resultado de movs_casillas para el segundo proceso

    generar_rutas_ficha1.join()
    generar_rutas_ficha16.join()

    fin = time.time()
    tiempo_transcurrido = fin - inicio

    print(movs_casillas_ficha1)
    print(movs_casillas_ficha16)

    print(f"\nEl programa tardó {tiempo_transcurrido} segundos en ejecutarse.")