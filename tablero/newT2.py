import multiprocessing
from arbolT2 import *
import random
import time


def generar_rutas(tablero: tuple, indices: dict, estado_inicial:int, estado_final: int, id_ficha:int, colores_ruta:list, 
                  nombre_arch:str) -> None:
    """Función que genera los archivos de las rutas de una ficha según su estado inicial y los colores

    Args:
        tablero (tuple): Tupla que representa el tablero de juego
        indices (dict): índices de posicion de un estado en la matriz del tablero
        estado_inicial (int): Estado de donde parte la ficha
        estado_final (int): Estado al que deseamos que llegue la ficha
        id_ficha (int): Identificador de la ficha
        colores_ruta (list): Colores de las casillas que deben seguir las fichas
    """
    archivo_todas = open(f"{nombre_arch}_todas.txt", "a+")
    archivo_ganadoras = open(f"{nombre_arch}_ganadorasT2.txt", "a+")
    t = ArbolN_ario(estado_inicial, 0)
    estados, ganadoras = t.generar_arbol(colores_ruta, tablero, indices, t, [], estado_final, archivo_todas, archivo_ganadoras)
    archivo_todas.write("\n".join(estados))
    archivo_todas.write("\n")
    archivo_ganadoras.write("\n".join(ganadoras))
    archivo_ganadoras.write("\n")

    print("Ya construi el arbol")
    #t.recorrido_profundidad([], str(estado_final), t, id_ficha, archivo_todas, archivo_ganadoras)


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

    colores_ruta = ["r", "b", "b"]

    n = 14

    cadenas = ["r", "b"]

    colores_ruta = [random.choice(cadenas) for i in range(0, n)]
    print(colores_ruta)

    inicio = time.time()
    generar_rutas_ficha1 = multiprocessing.Process(target=generar_rutas, args=(tablero, indices, 1, 9, 1, colores_ruta, "f1"))
    generar_rutas_ficha16 = multiprocessing.Process(target=generar_rutas, args=(tablero, indices, 4, 13, 16, colores_ruta, "f16"))

    generar_rutas_ficha1.start()
    generar_rutas_ficha16.start()

    generar_rutas_ficha1.join()
    generar_rutas_ficha16.join()

    print("Ambas rutas calculadas.")

    fin = time.time()

    tiempo_transcurrido = fin - inicio

    print(f"\nEl programa tardó {tiempo_transcurrido} segundos en ejecutarse.")
