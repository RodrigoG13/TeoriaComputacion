import threading

def posibles_movimientos(estado, tablero, indices, movimiento):
    fila, col = indices[estado]
    posibles_estados = []
    for i in range(fila - 1, fila + 2):
        for j in range(col - 1, col + 2):
            if 0 <= i < len(tablero) and 0 <= j < len(tablero[0]) and (i, j) != (fila, col):
                if tablero[i][j][0] == movimiento:
                    posibles_estados.append(tablero[i][j][2])
    return posibles_estados


def generar_rutas(movimientos, tablero, indices, estado_inicial):
    rutas = [[estado_inicial]]

    for movimiento in movimientos:
        nuevas_rutas = []

        for ruta in rutas:
            ultimo_estado = ruta[-1]
            for siguiente_estado in posibles_movimientos(ultimo_estado, tablero, indices, movimiento):
                nuevas_rutas.append(ruta + [siguiente_estado])
    
        if len(nuevas_rutas) == 1000000:
            print("melon")

        rutas = nuevas_rutas

    return rutas

if __name__ == "__main__":
    # Usaré tu tablero e índices para la demostración.
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

    ruta = ["r", "b", "r", "b", "r", "b", "r", "b", "r", "b", "r", "b", "r", "b", "r", "b"]

    rutas = generar_rutas(ruta, tablero, indices, 1)
    for r in rutas:
        print(r)
