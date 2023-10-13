import threading
import random

# Tablero e índices
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

moves = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]  # posibles movimientos

# Bloqueos para escribir en los archivos
todas_lock = threading.Lock()
ganadoras_lock = threading.Lock()

def is_valid(x, y, color_seq, index):
    if 0 <= x < 4 and 0 <= y < 4:
        if tablero[x][y][0] == color_seq[index]:
            return True
    return False

def dfs(x, y, color_seq, index, path):
    if index == len(color_seq):
        with todas_lock:
            with open("todas.txt", "a") as file:
                file.write(f"{path}\n")
        if tablero[x][y][1]:
            with ganadoras_lock:
                with open("ganadoras.txt", "a") as file:
                    file.write(f"{path}\n")
        return

    for dx, dy in moves:
        nx, ny = x + dx, y + dy
        if is_valid(nx, ny, color_seq, index):
            dfs(nx, ny, color_seq, index+1, path+[tablero[nx][ny][2]])

def start_dfs(pos):
    x, y = indices[pos]
    dfs(x, y, color_seq, 0, [pos])

if __name__ == "__main__":
    # Ejemplo de secuencia de colores aleatoria de longitud 30
    #color_seq = [random.choice(["b", "r"]) for _ in range(30)]
    color_seq = ['r', 'r']
    print("Secuencia de colores:", color_seq)

    # Preparar archivos
    open("todas.txt", "w").close()
    open("ganadoras.txt", "w").close()

    threads = []
    for pos in range(1, 17):
        t = threading.Thread(target=start_dfs, args=(pos,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
