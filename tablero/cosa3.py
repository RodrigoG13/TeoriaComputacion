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

def seleccionar_hijos(tablero, indices, movimientos, lista):
    hijos = []
    ventanita = crear_matriz_ventanita(tablero, indices[int(lista[-1])][0], indices[int(lista[-1])][1])
    for fila in ventanita:
        for casilla in fila:
            if casilla[0] == movimientos[len(lista)-1]:
                hijos.append(casilla[2])
    return hijos


def generar_arbol(arch, movimientos, tablero, indices, lista):
    if len(lista) <= len(movimientos):
        hijos = seleccionar_hijos(tablero, indices, movimientos, lista)
        futures = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
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
            arch.write(", ".join(lista) + "\n")

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

    ruta = ["r", "b", "r", "b", "r", "b", "r", "b", "r", "b", "r", "b", "r", "b"]

    with open("puerco.txt", "w+") as puerco:
        generar_arbol(puerco, ruta, tablero, indices, ["1"])

    print("quien sabe")
