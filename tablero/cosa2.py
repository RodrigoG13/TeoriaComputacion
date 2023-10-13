import threading
import copy
import os

file_lock = threading.Lock()

def crear_matriz_ventanita(tablero, fila, col):
    """Crea una máscara para delimitar el espacio de movimientos que tendrá una pieza

    Args:
        tablero (list): Tablero del juego que contiene el estado, una bandera de ocupación y un color
        fila (int): Número de la fila de la posición central
        col (int): Número de la columna de la posición central

    Returns:
        list: Máscara con las posibilidades de juego
    """

    ventanita = []
    for i in range(fila - 1, fila + 2):
        fila_aux = []
        for j in range(col - 1, col + 2):
            if 0 <= i < len(tablero) and 0 <= j < len(tablero[0]):
                fila_aux.append(tablero[i][j])
            else:
                fila_aux.append([None, None, None])
        ventanita.append(fila_aux)
    ventanita[1][1] = [None, None, None]
    return ventanita

def seleccionar_hijos(tablero, indices, movimientos, lista):
    """Selecciona los estados en los que podría estar la ficha de acuerdo al color siguiente en la lista de movimientos

    Args:
        tablero (list): Tablero del juego que contiene el estado, una bandera de ocupación y un color
        indices (dict): índice del estado en la matriz tablero
        movimientos (list): Cadena de juego
    """
    hijos = []
    ventanita = crear_matriz_ventanita(tablero, indices[int(lista[-1])][0], indices[int(lista[-1])][1])
    for fila in ventanita:
        for casilla in fila:
            if casilla[0] == movimientos[len(lista)-1]:
                hijos.append(casilla[2])
    return hijos

def generar_arbol(arch, movimientos, tablero, indices, lista):
    """Selecciona los estados en los que podría estar la ficha de acuerdo al color siguiente en la lista de movimientos

    Args:
        tablero (list): Tablero del juego que contiene el estado, una bandera de ocupación y un color
        indices (dict): índice del estado en la matriz tablero
        movimientos (list): Cadena de juego
        arbol(ArbolN_ario): Nodo de árbol que se desarrollará
    """

    hilos = []

    if len(lista) <= len(movimientos):
        hijos = seleccionar_hijos(tablero, indices, movimientos, lista)
        #print(hijos)

        for hijo in hijos:
            nueva_lista = copy.copy(lista)
            nueva_lista.append(str(hijo))
            hilo = threading.Thread(target=generar_arbol, args=(arch, movimientos, tablero, indices, nueva_lista))
            hilos.append(hilo)
            hilo.start()
        for hilo in hilos:
            hilo.join()
    else:
        with file_lock:
            arch.write(", ".join(lista) + "\n")

if __name__ == "__main__":
    tablero = [
        [["b", False, 1], ["r", False, 2], ["b", False, 3]],
        [["r", False, 4], ["b", False, 5], ["r", False, 6]],
        [["b", False, 7], ["r", False, 8], ["b", False, 9]]
    ]

    indices = {1: (0, 0), 2: (0, 1), 3: (0, 2),
               4: (1, 0), 5: (1, 1), 6: (1, 2),
               7: (2, 0), 8: (2, 1), 9: (2, 2)
    }

    ruta = ["r", "b", "r", "b", "r", "b", "r", "b", "r", "b", "r", "b", "r", "b"]

    with open("puerco.txt", "w+") as puerco:
        generar_arbol(puerco, ruta, tablero, indices, ["1"])

    print("quien sabe")
