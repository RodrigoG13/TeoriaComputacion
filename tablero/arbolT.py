class ArbolN_ario:
    """Clase que creará el árbol n-ario para las jugadas de cada pieeza en el tablero
    """

    def __init__(self, estado: int, contador: int) -> None:
        self.hijos = []
        self.contador = contador
        self.estado = estado

    
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
                if 0 <= i < len(tablero) and 0 <= j < len(tablero[0]) and i:
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
                if casilla[0] == movimientos[self.contador]:
                    self.hijos.append(ArbolN_ario(casilla[2], self.contador+1))


    def generar_arbol(self, movimientos: list, tablero: list, indices: dict, arbol) -> None:
        """Selecciona los estados en los que podría estar la ficha de acuerdo al color siguiente en la lista de movimientos

        Args:
            tablero (list): Tablero del juego que contiene el estado, una bandera de ocupación y un color
            indices (dict): índice del estado en la matriz tablero
            movimientos (list): Cadena de juego
            arbol(ArbolN_ario): Nodo de árbol que se desarrollará
        """

        if arbol.contador != len(movimientos):
            arbol.seleccionar_hijos(tablero, indices, movimientos)
            for candidato in arbol.hijos:
                arbol.generar_arbol(movimientos, tablero, indices, candidato)
        else:
            pass

    
    def recorrido_profundidad(self, estados:list, estado_final: int, arbol, ficha:int, todas, ganadoras) -> None:
        """Método que recorre el árbol para escribir las posibles jugadas de una ficha en el tablero

        Args:
            estados (list): Estados que componen una jugada
            estado_final (int): Estado al que debe llegar la ficha
            arbol (ArbolN_ario): Nodo de árbol al que se le aplicará el recorrido
        """

        estados.append(arbol.estado)

        if len(arbol.hijos) == 0:
            estados = [str(num) for num in estados] 
            todas.write(f"{','.join(estados)}\n")

            if estados[-1] == estado_final:
                ganadoras.write(f"{','.join(estados)}\n")

            estados.pop()

        else:
            for hijo in arbol.hijos:
                arbol.recorrido_profundidad(estados, estado_final, hijo, ficha, todas, ganadoras)
                estados.pop()


if __name__ == "__main__":

    """tablero = (
        (("b", False, 1), ("r", False, 2), ("b", False, 3), ("r", False, 4)),
        (("r", False, 5), ("b", False, 6), ("r", False, 7), ("b", False, 8)),
        (("b", False, 9), ("r", False, 10), ("b", False, 11), ("r", False, 12)),
        (("r", False, 13), ("b", False, 14), ("r", False, 15), ("b", False, 16))
    )"""

    """indices = {1: (0,0), 2: (0,1), 3: (0,2), 4: (0,3),
               5: (1,0), 6: (1,1), 7: (1,2), 8: (1,3),
               9: (2,0), 10: (2,1), 11: (2,2), 12: (2,3),
               13: (3,0), 14: (3,1), 15: (3,2), 16: (3,3)}"""
    
    tablero = [
        [["b", False, 1], ["r", False, 2], ["b", False, 3]],
        [["r", False, 4], ["b", False, 5], ["r", False, 6]],
        [["b", False, 7], ["r", False, 8], ["b", False, 9]]
    ]

    indices = {1:(0,0), 2:(0,1), 3:(0,2),
               4:(1,0), 5:(1,1), 6:(1,2),
               7:(2,0), 8:(2,1), 9:(2,2)
    }

    ruta = ["r", "b", "b"]

    t = ArbolN_ario(1, 0)
    t.generar_arbol(ruta, tablero, indices, t)
    t.recorrido_profundidad([], "9", t, 1)