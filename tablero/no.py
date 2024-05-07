"""
    
    BUENOTA

    Returns:
        _type_: _description_
    """

import threading
import os


file_lock = threading.Lock()

def generar_arbol(movimientos: list, tablero: list, indices: dict, arbol, estados: list = [], estado_final: int = None, todas = None, ganadoras = None, lista_estados = [], lista_ganadoras = [], doctor=0) -> None:
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
        cte = 1000000
        estados.append(str(arbol.estado))


        if doctor == 0:
            arbol.seleccionar_hijos(tablero, indices, movimientos)

            if len(arbol.hijos) == 1:
                arbol = arbol.hijos[0]
                estados.append(str(arbol.estado))
                arbol.seleccionar_hijos(tablero, indices, movimientos)

            hilos = {}
            resultados = {}
            for hijo in arbol.hijos:
                resultados[hijo.estado] = [list(), list()]
                generar_arbol(movimientos, tablero, indices, hijo, list(estados), 
                                        estado_final, todas, ganadoras, resultados[hijo.estado][0], resultados[hijo.estado][1], doctor+1)


            for i in resultados.keys():
                todas.write("\n".join(resultados[i][0]))
                todas.write("\n")
                ganadoras.write("\n".join(resultados[i][1]))
                ganadoras.write("\n")



        else:
            if arbol.contador < len(movimientos):
                
                arbol.seleccionar_hijos(tablero, indices, movimientos)

                while len(arbol.hijos) != 0:
                    lista_estados, lista_ganadoras = generar_arbol(movimientos, tablero, indices, arbol.hijos[0], estados, estado_final, todas, ganadoras, lista_estados, lista_ganadoras, doctor+1)
                    arbol.hijos.pop(0)
                    estados.pop()

            else:
                if len(lista_estados) < cte:
                    lista_estados.append(f"{','.join(map(str, estados))}")
                elif len(lista_estados) >= cte:
                    lista_estados.append(f"{','.join(map(str, estados))}")
                    #print("Ya llevo 1 meloncito")
                    with file_lock:
                        todas.write("\n".join(lista_estados))
                        todas.write("\n")
                        lista_estados = []

                if str(estados[-1]) == str(estado_final) and len(lista_ganadoras) < cte:
                    lista_ganadoras.append(f"{','.join(map(str, estados))}")
                elif estados[-1] == estado_final and len(lista_ganadoras) < cte:
                    lista_ganadoras.append(f"{','.join(map(str, estados))}")
                    with file_lock:
                        ganadoras.write("\n".join(lista_ganadoras))
                        ganadoras.write("\n")
                    lista_ganadoras = []
            return lista_estados, lista_ganadoras

class ArbolN_ario:
    """Clase que creará el árbol n-ario para las jugadas de cada pieza en el tablero
    """

    def __init__(self, estado: int, contador: int) -> None:
        self.hijos = []
        self.contador = contador
        self.estado = estado

    def __str__(self) -> str:
        return f"hijo, contador={self.contador}, estado = {self.estado}, tengoHijos={len(self.hijos)>0}"

    
    def crear_matriz_ventanita(self, tablero: list, fila: int, col:int) -> list:
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


    def seleccionar_hijos(self, tablero:list , indices: dict, movimientos:list) -> None:
        """Selecciona los estados en los que podría estar la ficha de acuerdo al color siguiente en la lista de movimientos

        Args:
            tablero (list): Tablero del juego que contiene el estado, una bandera de ocupación y un color
            indices (dict): índice del estado en la matriz tablero
            movimientos (list): Cadena de juego
        """

        ventanita = self.crear_matriz_ventanita(tablero, indices[self.estado][0], indices[self.estado][1])
        for fila in ventanita:
            for casilla in fila:
                #print(self.contador)
                if casilla[0] == movimientos[self.contador]:
                    self.hijos.append(ArbolN_ario(casilla[2], self.contador+1))
                    #print(self.hijos[-1])


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
        estados.append(str(arbol.estado))
        arbol.seleccionar_hijos(tablero, indices, movimientos)

        if len(arbol.hijos) == 1:
            arbol = arbol.hijos[0]
            estados.append(str(arbol.estado))
            arbol.seleccionar_hijos(tablero, indices, movimientos)

        hilos = {}
        resultados = {}
        for hijo in arbol.hijos:
            resultados[hijo.estado] = [list(), list()]
            hilo = threading.Thread(target=generar_arbol, args=(movimientos, tablero, indices, hijo, list(estados), 
                                    estado_final, todas, ganadoras, resultados[hijo.estado][0], resultados[hijo.estado][1], 0))
            
            hilos[hijo.estado] = hilo
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
    
    """tablero = [
        [["b", False, 1], ["r", False, 2], ["b", False, 3]],
        [["r", False, 4], ["b", False, 5], ["r", False, 6]],
        [["b", False, 7], ["r", False, 8], ["b", False, 9]]
    ]

    indices = {1:(0,0), 2:(0,1), 3:(0,2),
               4:(1,0), 5:(1,1), 6:(1,2),
               7:(2,0), 8:(2,1), 9:(2,2)
    }"""

    #ruta = ["r", "b", "r", "b", "r", "b", "r", "b", "r", "b", "r", "b", "r", "b", "r", "b", "r", "b", "r", "b"]



    t = ArbolN_ario(1, 0)
    with open("todas.txt", "w") as todas, open("ganadoras.txt", "w") as ganadoras:
        ruta = ["r", "b", "b"]
        hito = threading.Thread(target=generar_arboles, args=(ruta, tablero, indices, t, [], "16", todas, ganadoras))
        hito.start()
        hito.join()
        print("popo")
        """todas.write("\n".join(estados))
        todas.write("\n")
        ganadoras.write("\n".join(lganadoras))
        ganadoras.write("\n")"""