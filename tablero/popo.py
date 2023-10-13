import threading
import random

tablero = (
    (("b", False, 1), ("r", False, 2), ("b", False, 3), ("r", False, 4)),
    (("r", False, 5), ("b", False, 6), ("r", False, 7), ("b", False, 8)),
    (("b", False, 9), ("r", False, 10), ("b", False, 11), ("r", False, 12)),
    (("r", False, 13), ("b", False, 14), ("r", False, 15), ("b", False, 16))
)

indices = {
    1: (0,0), 2: (0,1), 3: (0,2), 4: (0,3),
    5: (1,0), 6: (1,1), 7: (1,2), 8: (1,3),
    9: (2,0), 10: (2,1), 11: (2,2), 12: (2,3),
    13: (3,0), 14: (3,1), 15: (3,2), 16: (3,3)
}

MOVIMIENTOS = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]

rutas_validas = set()  # Cambiado a conjunto para garantizar unicidad
rutas_lock = threading.Lock()  # Lock para el acceso seguro entre hilos

def es_valido(x, y):
    return 0 <= x < 4 and 0 <= y < 4

def simula_movimiento(posicion, secuencia_colores, ruta_actual):
    if not secuencia_colores:
        with rutas_lock:  # Asegura que el acceso al conjunto sea seguro
            rutas_validas.add(tuple(ruta_actual))  # Agrega la ruta como tupla al conjunto
        return
    
    x, y = posicion
    color_actual = secuencia_colores[0]

    for dx, dy in MOVIMIENTOS:
        nuevo_x, nuevo_y = x + dx, y + dy
        if es_valido(nuevo_x, nuevo_y) and tablero[nuevo_x][nuevo_y][0] == color_actual:
            nueva_pos = nuevo_x, nuevo_y
            simula_movimiento(nueva_pos, secuencia_colores[1:], ruta_actual + [tablero[nuevo_x][nuevo_y][2]])

def guardar_en_archivo():
    with open("rutas_validas.txt", "w") as f:
        for ruta in rutas_validas:
            f.write(",".join(map(str, ruta)) + "\n")

def generar_secuencia():
    # Descomenta las siguientes dos líneas si deseas una secuencia aleatoria
    # colores = ['b', 'r']
    # return [random.choice(colores) for _ in range(5)]
    return ['r', 'r', 'r', 'b', 'b', 'r', 'b', 'b', 'b', 'r']

def main():
    secuencia_colores = generar_secuencia()
    print("Secuencia generada:", secuencia_colores)
    
    threads = []
    for movimiento in MOVIMIENTOS:
        t = threading.Thread(target=simula_movimiento, args=(indices[1], secuencia_colores, [1]))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    guardar_en_archivo()
    print("Rutas válidas guardadas en rutas_validas.txt")

main()
