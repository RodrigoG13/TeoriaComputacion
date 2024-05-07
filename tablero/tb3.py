import pygame
import sys
import time
import os
from rutas import *
import random
import time
import multiprocessing

def eliminar_archs(nombre_arch):
    """Función que elimina un archivo si existe en el directorio

    Args:
        nombre_arch (str): Nombre del archivo que deseas eliminar
    """
    archivo1 = nombre_arch
    if os.path.exists(archivo1):
        os.remove(archivo1)


class Tablero:
    def __init__(self, dimension, tablero, indices, num_movs, cant_fichas=1):
        self.DIMENSIONES = dimension
        self.TAMANO_CELDA = 100
        self.ROJO = (124, 18, 66)
        self.NEGRO = (0, 0, 0)
        pygame.init()
        self.tablero = tablero
        self.indices = indices
        self.cant_fichas = cant_fichas
        self.num_movs = num_movs

        self.VENTANA_TAMANO = (self.DIMENSIONES * self.TAMANO_CELDA, self.DIMENSIONES * self.TAMANO_CELDA)
        self.ventana = pygame.display.set_mode(self.VENTANA_TAMANO)
        pygame.display.set_caption("Simulación de Ajedrez")

        self.pieza1_pos = (0, 0)
        self.pieza16_pos = (0, 3)
        self.tiempo_siguiente_movimiento = 2
        self.indice_movimiento_p1 = 0
        self.indice_movimiento_p16 = 0
        self.archivo_pieza1 = open("f1_ganadoras.txt", "a+")
        self.archivo_pieza16 = open("f16_ganadoras.txt", "a+")
        self.aux_pos_p1 = (0,0)
        self.movs_casillas_ficha1 = None
        self.movs_casillas_ficha16 = None
        self.aux_pos_p16 = (0,3)
        self.ruta_pieza1 = None
        self.ruta_pieza16 = None

    def calcular_ganadoras(self):
        n = 5

        cadenas = ["r", "b"]

        ruta_colores = [random.choice(cadenas) for _ in range(0, n-1)]
        #ruta_colores = ["r", "b", "b"]
        #print(ruta_colores+["r"])

        resultados1 = {}
        resultados16 = {}

        q1 = multiprocessing.Queue()
        q2 = multiprocessing.Queue()

        generar_rutas_ficha1 = multiprocessing.Process(target=self.generar_rutas_s, args=(resultados1, tuple(self.tablero), dict(self.indices), 1, 16, ruta_colores+["b"], "f1", q1))
        generar_rutas_ficha16 = multiprocessing.Process(target=self.generar_rutas_s, args=(resultados16, tuple(self.tablero), dict(self.indices), 4, 13, ruta_colores+["r"], "f16", q2))

        generar_rutas_ficha1.start()
        generar_rutas_ficha16.start()

        self.movs_casillas_ficha1 = q1.get()  # Captura el resultado de movs_casillas para el primer proceso
        self.movs_casillas_ficha16 = q2.get()  # Captura el resultado de movs_casillas para el segundo proceso

        generar_rutas_ficha1.join()
        generar_rutas_ficha16.join()

        self.ruta_pieza1 = self.archivo_pieza1.readline()
        self.ruta_pieza1 = self.ruta_pieza1[0: len(self.ruta_pieza1)-1].split(",")
        self.ruta_pieza16 = self.archivo_pieza16.readline()
        self.ruta_pieza16 = self.ruta_pieza16 [0: len(self.ruta_pieza16)-1].split(",")
        print(self.ruta_pieza1)
        print(self.ruta_pieza16)


    def generar_rutas_s(self, res, tablero: tuple, indices: dict, estado_inicial:int, estado_final: int, ruta_colores:list, 
                  nombre_arch:str, q=None):
        
        file_lock = threading.Lock()
        variable_lock = threading.Lock()

        movs_casillas = {}

        for i in range(1, len(ruta_colores)+1):
            movs_casillas[i] = {}
        
        with open(f"{nombre_arch}_todas.txt", "w") as todas, open(f"{nombre_arch}_ganadoras.txt", "w") as ganadoras:
            resultados = threaded_generar_rutas(file_lock, variable_lock, ruta_colores, tablero, indices, estado_inicial, estado_final,todas, ganadoras, movs_casillas, res)
            for i in resultados.keys():
                todas.write("\n".join(resultados[i][0]))
                todas.write("\n")
                ganadoras.write("\n".join(resultados[i][1]))
                ganadoras.write("\n")

        if q:
            q.put(movs_casillas)
        return movs_casillas
    


    def dibujar_tablero(self):
        for fila in range(self.DIMENSIONES):
            for columna in range(self.DIMENSIONES):
                color = self.NEGRO if (fila + columna) % 2 == 0 else self.ROJO
                pygame.draw.rect(self.ventana, color, (columna * self.TAMANO_CELDA, fila * self.TAMANO_CELDA, self.TAMANO_CELDA, self.TAMANO_CELDA))


    def dibujar_piezas(self):
        if self.cant_fichas >= 1:
            pygame.draw.circle(self.ventana, (255, 207, 216), (self.pieza1_pos[1] * self.TAMANO_CELDA + self.TAMANO_CELDA // 2, self.pieza1_pos[0] * self.TAMANO_CELDA + self.TAMANO_CELDA // 2), self.TAMANO_CELDA // 3)
        if self.cant_fichas >= 2:
            pygame.draw.circle(self.ventana, (236, 234, 175), (self.pieza16_pos[1] * self.TAMANO_CELDA + self.TAMANO_CELDA // 2, self.pieza16_pos[0] * self.TAMANO_CELDA + self.TAMANO_CELDA // 2), self.TAMANO_CELDA // 3)


    def bucle_principal(self):
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_UP and self.pieza1_pos[0] > 0:
                        self.pieza1_pos = (self.pieza1_pos[0] - 1, self.pieza1_pos[1])
                    elif evento.key == pygame.K_DOWN and self.pieza1_pos[0] < self.DIMENSIONES - 1:
                        self.pieza1_pos = (self.pieza1_pos[0] + 1, self.pieza1_pos[1])
                    elif evento.key == pygame.K_LEFT and self.pieza1_pos[1] > 0:
                        self.pieza1_pos = (self.pieza1_pos[0], self.pieza1_pos[1] - 1)
                    elif evento.key == pygame.K_RIGHT and self.pieza1_pos[1] < self.DIMENSIONES - 1:
                        self.pieza1_pos = (self.pieza1_pos[0], self.pieza1_pos[1] + 1)

            self.ventana.fill(self.ROJO)
            self.dibujar_tablero()
            self.dibujar_piezas()
            pygame.display.flip()


    def dame_mov():
        pass

    

    def bucle_1(self):
        bandera = True
        bandera2 = False

        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            tiempo_actual = time.time()

            if tiempo_actual > self.tiempo_siguiente_movimiento and self.indice_movimiento_p1 <= self.num_movs and self.indice_movimiento_p16 <= self.num_movs:

                if bandera:
                    self.pieza1_pos = self.indices[int(self.ruta_pieza1[self.indice_movimiento_p1])]
                    print("Primero")
                    if self.pieza1_pos != self.pieza16_pos:
                        self.tiempo_movimiento_pieza2 = tiempo_actual + 2  # programamos el movimiento de la segunda pieza en 2 segundos
                        self.indice_movimiento_p1 += 1
                        bandera = False
                        bandera2 = True
                    """else:
                        break
                        pass"""


                elif bandera2 and tiempo_actual > self.tiempo_movimiento_pieza2:
                    print("Segundo")
                    self.pieza16_pos = self.indices[int(self.ruta_pieza16[self.indice_movimiento_p1])]
                    self.indice_movimiento_p16 += 1
                    self.tiempo_siguiente_movimiento = tiempo_actual + 2  # programamos el siguiente movimiento de la primera pieza en 2 segundos
                    bandera = True
                    bandera2 = False

            self.ventana.fill(self.ROJO)
            self.dibujar_tablero()
            self.dibujar_piezas()
            pygame.display.flip()


if __name__ == "__main__":

    eliminar_archs("f1_ganadoras.txt")
    eliminar_archs("f1_todas.txt")
    eliminar_archs("f16_ganadoras.txt")
    eliminar_archs("f16_todas.txt")

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
    

    juego = Tablero(4, tablero, indices, 3, cant_fichas=2)
    juego.calcular_ganadoras()
    """juego.ruta_pieza1 = juego.archivo_pieza1.readline()
    juego.ruta_pieza1 = juego.ruta_pieza1[0: len(juego.ruta_pieza1)-1].split(",")
    juego.ruta_pieza16 = juego.archivo_pieza16.readline()
    juego.ruta_pieza16 = juego.ruta_pieza16 [0: len(juego.ruta_pieza16)-1].split(",")"""
    print(juego.movs_casillas_ficha1)
    print(juego.movs_casillas_ficha16)
    print(juego.ruta_pieza1)
    print(juego.ruta_pieza16)
    juego.bucle_1()
