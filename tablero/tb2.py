import pygame
import sys
import time
import os
from rutas import *
import random
import time
import multiprocessing
import pandas as pd

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

        self.movs_casillas_ficha1 = None
        self.movs_casillas_ficha16 = None

        self.pieza1_pos = (0, 0)
        self.pieza16_pos = (0, 3)
        self.tiempo_siguiente_movimiento = 2
        self.indice_movimiento_p1 = 0
        self.indice_movimiento_p16 = 0
        self.archivo_pieza1 = open("f1_ganadoras.txt", "w+")
        self.archivo_pieza16 = open("f16_ganadoras.txt", "w+")
        self.aux_pos_p1 = (0,0)
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

        """print(movs_casillas_ficha1)
        print(movs_casillas_ficha16)"""
        self.ruta_pieza1 = self.archivo_pieza1.readline()
        self.ruta_pieza1 = self.ruta_pieza1[0: len(self.ruta_pieza1)-1].split(",")
        self.ruta_pieza16 = self.archivo_pieza16.readline()
        self.ruta_pieza16 = self.ruta_pieza16 [0: len(self.ruta_pieza16)-1].split(",")
        print(self.ruta_pieza1)
        print(self.ruta_pieza16)
        self.num_movs = n


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


    def revisar_existencia_movs(self, num_mov, casilla_actual, evitar, casilla):
        if casilla == 1:
            for elemento in self.movs_casillas_ficha1[num_mov][casilla_actual]:
                if str(elemento) != str(evitar):
                    return True
        else:
            for elemento in self.movs_casillas_ficha16[num_mov][casilla_actual]:
                if str(elemento) != str(evitar):
                    return True


    def dame_mov(self, num_mov, casilla_actual, evitar, casilla):
        bandera_otro_mov = self.revisar_existencia_movs(num_mov, casilla_actual, evitar, casilla)
        
        if casilla == 1:
            if bandera_otro_mov:
                nueva_ruta = self.read_and_filter(f"f{casilla}_ganadoras.txt", num_mov, evitar, self.indices[self.aux_pos_p1])
                self.ruta_pieza1 = nueva_ruta
        else:
            if bandera_otro_mov:
                nueva_ruta = self.read_and_filter(f"f{casilla}_ganadoras.txt", num_mov, evitar, self.indices[self.aux_pos_p2])
                self.ruta_pieza16 = nueva_ruta
        
        

    def read_and_filter(self, file_path, n, x, y, chunk_size=10000):
        """
        Lee un archivo en chunks y avanza hasta encontrar una fila donde en la columna "n" haya un elemento 
        distinto de x, pero en la columna "n-1" haya un elemento y. Retorna la fila encontrada 
        como un string separado por comas.
        
        Args:
        - file_path (str): Ruta al archivo.
        - n (int): Índice de la columna n.
        - x: Valor que no debe estar en la columna n.
        - y: Valor que debe estar en la columna n-1.
        - chunk_size (int): Tamaño del chunk para leer el archivo.

        Returns:
        - String que representa la fila encontrada o None si no se encuentra.
        """
        
        chunk_iter = pd.read_csv(file_path, sep=',', header=None, chunksize=chunk_size)

        for chunk in chunk_iter:
            mask = (chunk[n] != x) & (chunk[n-1] == y)
            filtered_chunk = chunk[mask]
            
            # Si encontramos al menos una fila que cumpla los criterios
            if not filtered_chunk.empty:
                # Convertir la primera fila que cumple con los criterios a string
                found_row = filtered_chunk.iloc[0]
                return ','.join(map(str, found_row))

        # Si se recorrieron todos los chunks y no se encontró ninguna fila que cumpla los criterios
        return None
    

    def bucle_1(self):
        bandera = True
        bandera2 = False
        print("Aqui")
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            tiempo_actual = time.time()

            if tiempo_actual > self.tiempo_siguiente_movimiento and self.indice_movimiento_p1 <= self.num_movs and self.indice_movimiento_p16 <= self.num_movs:

                if bandera:
                    aux = self.indices[int(self.ruta_pieza1[self.indice_movimiento_p1])]

                    if aux != self.indices[self.pieza16_pos]:
                        print("Fue dif")
                        print(aux)
                        print(self.pieza16_pos)
                        self.pieza1_pos = aux
                        self.tiempo_movimiento_pieza2 = tiempo_actual + 2  # programamos el movimiento de la segunda pieza en 2 segundos
                        self.indice_movimiento_p1 += 1
                        self.aux_pos_p1 = self.pieza1_pos
                        bandera = False
                        bandera2 = True
                    else:
                        print("Fue igu")
                        ruta = self.dame_mov(self.indice_movimiento_p1, self.indices[self.aux_pos_p1], aux, 1)
                        if ruta != None:
                            print("Ajusto")
                            self.pieza1_pos = ruta
                            self.pieza1_pos = self.indices[int(self.ruta_pieza1[self.indice_movimiento_p1])]
                            self.tiempo_movimiento_pieza2 = tiempo_actual + 2  # programamos el movimiento de la segunda pieza en 2 segundos
                            self.indice_movimiento_p1 += 1
                            self.aux_pos_p1 = self.pieza1_pos
                            bandera = False
                            bandera2 = True
                        else:
                            print("Ceder")
                            self.tiempo_movimiento_pieza2 = tiempo_actual + 2 
                            bandera = False
                            bandera2 = True
                        


                elif bandera2 and tiempo_actual > self.tiempo_movimiento_pieza2:
                    print("Dos")
                    aux = self.indices[int(self.ruta_pieza16[self.indice_movimiento_p16])]

                    if aux != indices[self.pieza1_pos]:
                        self.pieza16_pos = self.indices[int(self.ruta_pieza16[self.indice_movimiento_p16])]
                        self.tiempo_movimiento_pieza2 = tiempo_actual + 2  # programamos el movimiento de la segunda pieza en 2 segundos
                        self.indice_movimiento_p16 += 1
                        self.aux_pos_p16 = self.pieza16_pos
                        bandera = True
                        bandera2 = False
                    else:
                        ruta = self.dame_mov(self.indice_movimiento_p16, self.indices[self.aux_pos_p16], aux, 16)
                        if ruta != None:
                            self.pieza16_pos = ruta
                            self.pieza16_pos = self.indices[int(self.ruta_pieza16[self.indice_movimiento_p16])]
                            self.tiempo_movimiento_pieza2 = tiempo_actual + 2  # programamos el movimiento de la segunda pieza en 2 segundos
                            self.indice_movimiento_p16 += 1
                            self.aux_pos_p16 = self.pieza16_pos
                            bandera = True
                            bandera2 = False
                        else:
                            self.tiempo_movimiento_pieza2 = tiempo_actual + 2 
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
               13: (3,0), 14: (3,1), 15: (3,2), 16: (3,3),
                (0,0):1, (0,1):2, (0,2):3, (0,3):4,
               (1,0):5, (1,1):6, (1,2):7, (1,3):8,
               (2,0):9,(2,1):10,(2,2):11,(2,3):12,
               (3,0):13, (3,1):14,(3,2):15,(3,3):16}
    

    juego = Tablero(4, tablero, indices, 0, cant_fichas=2)
    juego.calcular_ganadoras()
    juego.bucle_1()
