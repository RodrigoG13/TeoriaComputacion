import copy
import threading
import concurrent.futures

file_lock = threading.Lock()

def crear_matriz_ventanita(tablero, fila, col):
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

def seleccionar_hijos(tablero, indices, movimientos, estados):
    hijos = []
    ventanita = crear_matriz_ventanita(tablero, indices[int(estados[-1])][0], indices[int(estados[-1])][1])
    for fila in ventanita:
        for casilla in fila:
            if casilla[0] == movimientos[len(estados)-1]:
                hijos.append(casilla[2])
    return hijos


def generar_arbol(arch, movimientos, tablero, indices, estados):
    if len(estados) <= len(movimientos):
        hijos = seleccionar_hijos(tablero, indices, movimientos, estados)

    for hijo in hijos:
        nueva_lista = copy.copy(estados)
        nueva_lista.append(str(hijo))

    else:
        with file_lock:
            arch.write(", ".join(estados) + "\n")


    """     with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
            for hijo in hijos:
                nueva_lista = copy.copy(lista)
                nueva_lista.append(str(hijo))
                futures.append(executor.submit(generar_arbol, arch, movimientos, tablero, indices, nueva_lista))

            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f"Error en hilo: {e}")
    else:
        with file_lock:
            arch.write(", ".join(lista) + "\n")"""
    

def generar_arboles(movimientos: list, tablero: list, indices: dict, arbol, estados: list = [], estado_final: int = None, todas = None, ganadoras = None, lista_estados = [], lista_ganadoras = []) -> None:
        """
        Selecciona los estados en los que podría estar la ficha de acuerdo al color siguiente en la lista de movimientos.

        Args:
            tablero (list): Tablero del juego que contiene el estado, una bandera de ocupación y un color.
            indices (dict): Índice del estado en la matriz tablero.
            movimientos (list): Cadena de juego.
            arbol (ArbolN_ario): Nodo de árbol que se desarrollará.
            estados (list, opcional): Lista que registra los estados a medida que se construye el árbol. Por defecto, es None.
            estado_final (int, opcional): Estado al que debe llegar la ficha. Por defecto, es None.
            todas: Opción para escribir los estados en un archivo. Por defecto, es None.
            ganadoras: Opción para escribir los estados ganadores en un archivo. Por defecto, es None.
        """
        hijos = seleccionar_hijos(tablero, indices, movimientos, estados)

        if len(hijos) == 1:
            arbol = hijos[0]
            estados.append(str(arbol.estado))
            arbol.seleccionar_hijos(tablero, indices, movimientos)

        hilos = {}
        resultados = {}
        for hijo in hijos:
            resultados[hijo] = [list(), list()]
            hilo = threading.Thread(target=generar_arbol, args=(movimientos, tablero, indices, hijo, list(estados), 
                                    estado_final, todas, ganadoras, resultados[hijo][0], resultados[hijo][1], 0))
            
            hilos[hijo] = hilo
            hilo.start()
            
        for hilo in hilos:
            hilos[hilo].join()
        #print(resultados)
            
        for i in resultados.keys():
            todas.write("\n".join(resultados[i][0]))
            todas.write("\n")
            ganadoras.write("\n".join(resultados[i][1]))
            ganadoras.write("\n")


if __name__ == "__main__":
    tablero = [
        [["b", False, 1], ["r", False, 2], ["b", False, 3]],
        [["r", False, 4], ["b", False, 5], ["r", False, 6]],
        [["b", False, 7], ["r", False, 8], ["b", False, 9]]
    ]

    indices = {
        1: (0, 0), 2: (0, 1), 3: (0, 2),
        4: (1, 0), 5: (1, 1), 6: (1, 2),
        7: (2, 0), 8: (2, 1), 9: (2, 2)
    }

    ruta = ["r", "b", "b"]

    with open(f"puerco.txt", "w") as todas, open(f"puercote.txt", "w") as ganadoras:
        generar_arboles(ruta,tablero, indices, )

    print("quien sabe")
