import threading

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


def seleccionar_hijos(estado, tablero, indices, movimientos, contador):
    fila, col = indices[estado]
    ventanita = crear_matriz_ventanita(tablero, fila, col)
    hijos = []
    for fila in ventanita:
        for casilla in fila:
            if casilla[0] == movimientos[contador]:
                hijos.append(casilla[2])
    return hijos

def generar_rutas(file_lock, variable_lock,movs_casillas, movimientos, tablero, indices, estado, ruta, estado_final, todas, ganadoras, lista_estados, lista_ganadoras):
    cte = 1000000
    
    if len(ruta) <= len(movimientos):
        hijos = seleccionar_hijos(estado, tablero, indices, movimientos, len(ruta)-1)

        for hijo in hijos:
            with variable_lock:
                crear_bifu(movs_casillas, len(ruta), ruta[-1])
                movs_casillas[len(ruta)][ruta[-1]].add(int(hijo))
            generar_rutas(file_lock, variable_lock,movs_casillas, movimientos, tablero, indices, hijo, ruta + [hijo], estado_final, todas, ganadoras, lista_estados, lista_ganadoras)

    else:
        if len(lista_estados) < cte:
            lista_estados.append(f"{','.join(map(str, ruta))}")
        elif len(lista_estados) >= cte:
            lista_estados.append(f"{','.join(map(str, ruta))}")
            with file_lock:
                todas.write("\n".join(lista_estados))
                todas.write("\n")
            lista_estados.clear()

        if str(ruta[-1]) == str(estado_final) and len(lista_ganadoras) < cte:
            lista_ganadoras.append(f"{','.join(map(str, ruta))}")
        elif ruta[-1] == estado_final and len(lista_ganadoras) >= cte:
            lista_ganadoras.append(f"{','.join(map(str, ruta))}")
            with file_lock:
                ganadoras.write("\n".join(lista_ganadoras))
                ganadoras.write("\n")
            lista_ganadoras.clear()

def crear_bifu(dict_movs, num_mov, llave):
    if llave not in dict_movs[num_mov]:
        dict_movs[num_mov][llave] = set()

def threaded_generar_rutas(file_lock, variable_lock, movimientos, tablero, indices, estado_inicial, estado_final, todas, ganadoras, movs_casillas, resultados={}):
    
        ruta = [estado_inicial]
        hilos = {}
        
        hijos_iniciales = seleccionar_hijos(estado_inicial, tablero, indices, movimientos, 0)

        if hijos_iniciales == 1:
            ruta = [estado_inicial, hijos_iniciales[0]]
            crear_bifu(movs_casillas, len(ruta), ruta[-1])
            movs_casillas[len(ruta)][ruta[-1]].add(hijos_iniciales[0])
            hijos_iniciales = seleccionar_hijos(estado_inicial, tablero, indices, movimientos, 1)

        for hijo in hijos_iniciales:
            resultados[hijo] = [list(), list()]
            with variable_lock:
                crear_bifu(movs_casillas, len(ruta), ruta[-1])
                movs_casillas[len(ruta)][ruta[-1]].add(int(hijo))
            hilo = threading.Thread(target=generar_rutas, args=(file_lock, variable_lock,movs_casillas, movimientos, tablero, indices, hijo, ruta+[hijo], estado_final, todas, ganadoras, resultados[hijo][0], resultados[hijo][1]))
            hilos[hijo] = hilo
            hilo.start()

        for _, hilo in hilos.items():
            hilo.join()

        return resultados

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

    with open("todas.txt", "w") as todas, open("ganadoras.txt", "w") as ganadoras:
        file_lock = threading.Lock()
        variable_lock = threading.Lock()
        ruta_colores = ['r', 'b', 'b', 'r', 'b', 'b', 'r', 'b', 'b', "r"]

        movs_casillas = {}

        for i in range(1, len(ruta_colores)+1):
            movs_casillas[i] = {}

        resultados = threaded_generar_rutas(file_lock, variable_lock, ruta_colores, tablero, indices, 1, 9, todas, ganadoras, movs_casillas)

        for i in resultados.keys():
            todas.write("\n".join(resultados[i][0]))
            todas.write("\n")
            ganadoras.write("\n".join(resultados[i][1]))
            ganadoras.write("\n")
        
        print(movs_casillas)
        print(movs_casillas)
