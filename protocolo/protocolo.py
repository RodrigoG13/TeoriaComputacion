'''
INSTITUTO POLITÉCNICO NACIONAL
ESCUELA SUPERIOR DE CÓMPUTO

INGENIERÍA EN INTELIGENCIA ARTIFICIAL

TEORÍA DE LA COMPUTACIÓN
PROTOCOLO

GRUPO: 5BM1
ALUMNO: TREJO ARRIAGA RODRIGO GERARDO

ESTE PROGRAMA SIMULA UN PROTOCOLO EN EL QUE CLASIFICA PALABRAS BINARIAS SEGÚN SU PARIDAD:

i) GENERA PALABRAS RANDOM Y LAS CLASIFICA DEPENDIENDO SI LA CANTIDAD DE UNOS Y CEROS QUE TIENEN
    ES PAR O NO
ii) ESCRIBE LAS PALABRAS CON UNOS Y CEROS PAR EN UN ARCHIVO DE TEXTO
iii) GRAFICA EL AUTÓMATA DEL PROTOCOLO Y EL DE PARIDAD

ÚLTIMA MODIFICACIÓN: 13/10/2023
'''

#  --------------------------------------------------------------------------------------------------------------------
# MÓDULOS Y LIBRERÍAS IMPORTADAS


import random
import os
from graficadorAutomata import *

#  --------------------------------------------------------------------------------------------------------------------
# FUNCIONES


def eliminar_archs(nombre_arch):
    """Función que elimina un archivo si existe en el directorio

    Args:
        nombre_arch (str): Nombre del archivo que deseas eliminar
    """
    archivo1 = nombre_arch
    if os.path.exists(archivo1):
        os.remove(archivo1)


def automata_paridad(transiciones:dict, palabra: str) -> int:
    """Función que simula las trancisiones del autómata de paridad para evaluar una palabra

    Args:
        transiciones (dict): Diciionario de transiciones del autómata
        palabra (str): Palabra que se evalúa en el autómata

    Returns:
        int: Estado en el que se quedó la palabra
    """
    estado = 0
    for caracter in palabra:
        estado = transiciones[(estado, caracter)]
    return estado


def generar_palabras(num_palabras: int, long_cadena:int) -> list:
    """Función que genera la lista de palabras binarias random

    Args:
        num_palabras (int): Número de palabras que tendrá la lista
        long_cadena (int): Longitud de cada palabra binaria

    Returns:
        list: Lista de palabras binarias
    """
    return [''.join([str(random.randint(0, 1)) for _ in range(long_cadena)]) for _ in range(num_palabras)]


def filtrar_palabras(palabras:list, transiciones) -> tuple:
    """Función que filtra palabras binarias según su paridad de unos y ceros

    Args:
        palabras (list): Lista de palabras que se evaluarán
        transiciones (_type_): Diccionario con las transiciones del autómata

    Returns:
        tuple: Lista de palabras aceptadas y rechazadas por el autómata
    """
    aceptadas = []
    rechazadas = []
    for palabra in palabras:
        if automata_paridad(transiciones, palabra) == 0:
            aceptadas.append(palabra)
        else:
            rechazadas.append(palabra)
    return aceptadas, rechazadas


def escribir_en_archivo(nombre_arch: str, datos:list) -> None:
    """Función que escribe una lista de palabras en un archiivo

    Args:
        nombre_arch (str): Nombre del archivo en el que se escribirán los datos
        datos (list): Lista de datos que se escribirán
    """
    if datos:
        with open(nombre_arch, "a+") as archivo:
            archivo.write("\n ".join(datos))
            archivo.write("\n ")


def graficar_estados(graficador)-> None:
    """Función que dibuja los estados

    Args:
        drawer (graphic): Objeto que dibuja un autómata
    """
    graficador.dibujar_estado(200, 150, 2.5, radio=50, flag_inicial=False, etiqueta="Ready")
    graficador.dibujar_estado(600, 150, 2.7, radio=50, flag_inicial=False, etiqueta="Sending")
    graficador.dibujar_estado(400, 300, 2.7, radio=45, flag_inicial=True, etiqueta="q0")
    graficador.dibujar_estado(200, 450, 2.7, radio=45, flag_inicial=False, etiqueta="q1")
    graficador.dibujar_estado(600, 450, 2.7, radio=45, flag_inicial=False, etiqueta="q3")
    graficador.dibujar_estado(400, 630, 2.7, radio=45, flag_inicial=False, etiqueta="q4")


def graficar_transiciones(graficador)->None:
    """Función quen dibuja las transiciones

    Args:
        drawer (graphic): Objeto que dibuja un autómata
    """
    graficador.dibujar_transicion(250, 150, 550, 150, "data in", 15, 2, 10, -20)
    graficador.dibujar_ciclo(650, 150, radio=30, etiqueta="time_out", cte_x=17, cte_y=-37, cte_text=0.1)
    graficador.dibujar_transicion(225, 190, 358, 290, ancho_linea=2)
    graficador.dibujar_transicion(445, 290, 570, 190, ancho_linea=2)
    graficador.dibujar_transicion(232, 420, 358, 320, "1", ancho_linea=2, cte_y=-26)
    graficador.dibujar_transicion(243, 445, 372, 340, "1", ancho_linea=2, cte_y=35)
    graficador.dibujar_transicion(570, 420, 440, 315, "0", ancho_linea=2, cte_y=-26)
    graficador.dibujar_transicion(555, 445, 427, 339, "0", ancho_linea=2, cte_y=35)
    graficador.dibujar_transicion(440, 620, 575, 490, "1", ancho_linea=2, cte_y=35)
    graficador.dibujar_transicion(400, 630, 560, 470, "1", ancho_linea=2, cte_y=-26)
    graficador.dibujar_transicion(355, 630, 210, 490, "0", ancho_linea=2, cte_y=35)
    graficador.dibujar_transicion(365, 605, 235, 480, "0", ancho_linea=2, cte_y=-26)


def graficar_uniones(graficador) ->None:
    """Función que dinuja las uniones

    Args:
        drawer (graphic): Objeto que dibuja un autómata
    """
    graficador.dibujar_circulo(545, 150, 7)
    graficador.dibujar_circulo(650, 120, 7)
    graficador.dibujar_circulo(228, 193, 7)
    graficador.dibujar_circulo(448, 287, 7)
    graficador.dibujar_circulo(355, 317, 7)
    graficador.dibujar_circulo(243, 445, 7)
    graficador.dibujar_circulo(565, 417, 7)
    graficador.dibujar_circulo(430, 340, 7)
    graficador.dibujar_circulo(445, 614, 7)
    graficador.dibujar_circulo(557, 473, 7)
    graficador.dibujar_circulo(213, 496, 7)
    graficador.dibujar_circulo(360, 600, 7)


def graficar_protocolo():
    """Función que genera el autómata
    """
    graficador = AutomataDrawer(850, 800)
    graficador.colocar_titulo("Autómata de Protocolo")
    graficar_transiciones(graficador)
    graficar_uniones(graficador)
    graficar_estados(graficador)
    input("Presiona Enter para cerrar la ventana...")
    graficador.close()

#  --------------------------------------------------------------------------------------------------------------------
# FUNCIÓN PRINCIPAL MAIN


if __name__ == "__main__":

    transiciones = {
        (0, '0'): 1, (0, '1'): 3,
        (1, '0'): 0, (1, '1'): 2,
        (2, '0'): 3, (2, '1'): 1,
        (3, '0'): 2, (3, '1'): 0
    }

    nombre_aceptadas = "aceptadas.txt"
    nombre_rechazadas = "rechazadas.txt"

    long_cadena = 64
    num_palabras = 1000000
    num_act = 0

    os.system('clear')
    print("\t\t\t***PROTOCOLO***\n")

    eliminar_archs(nombre_aceptadas)
    eliminar_archs(nombre_rechazadas)

    while random.randint(0,1):
        print("Protocolo en ejecución")
        palabras = generar_palabras(num_palabras, long_cadena)
        print("\t>> Esperando ...")
        aceptadas, rechazadas = filtrar_palabras(palabras, transiciones)
        escribir_en_archivo(nombre_aceptadas, aceptadas)
        escribir_en_archivo(nombre_rechazadas, rechazadas)
        print("Palabras clasificadas\n")
        num_act += 1
        
    if num_act != 0:
        print(f"Numero de ejecuciones del protocolo: {num_act}\n")
        print(f"Puedes consultar la clasificación de palabras en {nombre_aceptadas} & {nombre_rechazadas}")
    else:
        print("El protocolo no se ha podido ejecutar, inténtalo nuevamente.")

    graficar_protocolo()
