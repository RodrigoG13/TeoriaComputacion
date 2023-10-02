import multiprocessing
from arbol import *
import random
import time


def generar_rutas(tablero: tuple, indices: dict, estado_inicial:int, estado_final: int, id_ficha:int, colores_ruta:list) -> None:
    """Función que genera los archivos de las rutas de una ficha según su estado inicial y los colores

    Args:
        tablero (tuple): Tupla que representa el tablero de juego
        indices (dict): índices de posicion de un estado en la matriz del tablero
        estado_inicial (int): Estado de donde parte la ficha
        estado_final (int): Estado al que deseamos que llegue la ficha
        id_ficha (int): Identificador de la ficha
        colores_ruta (list): Colores de las casillas que deben seguir las fichas
    """

    t = ArbolN_ario(estado_inicial, 0)
    t.generar_arbol(colores_ruta, tablero, indices, t)
    t.recorrido_profundidad([], str(estado_final), t, id_ficha)


if __name__ == "__main__":

    tablero = (
        (("b", False, 1), ("r", False, 2), ("b", False, 3)),
        (("r", False, 4), ("b", False, 5), ("r", False, 6)),
        (("b", False, 7), ("r", False, 8), ("b", False, 9))
    )

    indices = {
            1:(0,0), 2:(0,1), 3:(0,2),
            4:(1,0), 5:(1,1), 6:(1,2),
            7:(2,0), 8:(2,1), 9:(2,2)
    }

    colores_ruta = ["r", "b", "b"]

    n = 15

    cadenas = ["r", "b"]

    colores_ruta = [random.choice(cadenas) for i in range(0, n)]
    print(colores_ruta)

    inicio = time.time()

    generar_rutas_ficha1 = multiprocessing.Process(target=generar_rutas, args=(tablero, indices, 1, 9, 1, colores_ruta))
    generar_rutas_ficha16 = multiprocessing.Process(target=generar_rutas, args=(tablero, indices, 7, 3, 16, colores_ruta))

    generar_rutas_ficha1.start()
    generar_rutas_ficha16.start()

    generar_rutas_ficha1.join()
    generar_rutas_ficha16.join()

    print("Ambos procesos han terminado.")

    fin = time.time()

    # Calcula el tiempo transcurrido en segundos
    tiempo_transcurrido = fin - inicio

    print(f"El programa tardó {tiempo_transcurrido} segundos en ejecutarse.")
