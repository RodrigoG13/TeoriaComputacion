import threading
from concurrent.futures import ThreadPoolExecutor


DEPTH_THRESHOLD = 3
MAX_THREADS = 8

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

def generar_rutas(movimientos, tablero, indices, estado, ruta, estado_final, todas, ganadoras, lista_estados, lista_ganadoras):
    cte = 10000000
    
    if len(ruta) != len(movimientos):
        hijos = seleccionar_hijos(estado, tablero, indices, movimientos, len(ruta))
        for hijo in hijos:
            generar_rutas(movimientos, tablero, indices, hijo, ruta + [hijo], estado_final, todas, ganadoras, lista_estados, lista_ganadoras)

    else:
        if len(lista_estados) < cte:
            lista_estados.append(f"{','.join(map(str, ruta))}")
        elif len(lista_estados) >= cte:
            with file_lock:
                todas.write("\n".join(lista_estados))
                todas.write("\n")
                lista_estados.clear()

        if str(ruta[-1]) == str(estado_final) and len(lista_ganadoras) < cte:
            lista_ganadoras.append(f"{','.join(map(str, ruta))}")
        elif ruta[-1] == estado_final and len(lista_ganadoras) >= cte:
            with file_lock:
                ganadoras.write("\n".join(lista_ganadoras))
                ganadoras.write("\n")
                lista_ganadoras.clear()

def threaded_generar_rutas(movimientos, tablero, indices, estado_inicial, estado_final, todas, ganadoras):
    # Resultados para cada hilo
    resultados = {}
    lista_estados_global = []
    lista_ganadoras_global = []
    
    # Función interna recursiva para manejar la búsqueda
    def search(estado, ruta, depth=0):
        if not (depth < DEPTH_THRESHOLD):
            print("No")
            # Búsqueda secuencial
            generar_rutas(movimientos, tablero, indices, estado, ruta, estado_final, todas, ganadoras, lista_estados_global, lista_ganadoras_global)
        else:
            # Búsqueda en paralelo
            with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
                hijos = seleccionar_hijos(estado, tablero, indices, movimientos, len(ruta))
                futures = [executor.submit(generar_rutas, movimientos, tablero, indices, hijo, ruta + [hijo], estado_final, todas, ganadoras, [], []) for hijo in hijos]
                
                for future in futures:
                    res_estados, res_ganadoras = future.result()
                    lista_estados_global.extend(res_estados)
                    lista_ganadoras_global.extend(res_ganadoras)
    
    # Iniciar búsqueda desde estado inicial
    search(estado_inicial, [estado_inicial])

    # Guardar resultados en el diccionario para ser devuelto
    resultados[estado_inicial] = [lista_estados_global, lista_ganadoras_global]
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
    ruta = ["r", "r", "b", "r", "b", "r", "b", "r", "b", "r", "b", "r", "b", "r", "b", "r"]
    resultados = threaded_generar_rutas(ruta, tablero, indices, 1, 9, todas, ganadoras)

    for i in resultados.keys():
        todas.write("\n".join(resultados[i][0]))
        todas.write("\n")
        ganadoras.write("\n".join(resultados[i][1]))
        ganadoras.write("\n")
