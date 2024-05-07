'''
INSTITUTO POLITÉCNICO NACIONAL
ESCUELA SUPERIOR DE CÓMPUTO

INGENIERÍA EN INTELIGENCIA ARTIFICIAL

TEORÍA DE LA COMPUTACIÓN
PARTICIÓN DEL UNIVERSO DE PALABRAS BINARIAS

GRUPO: 5BM1
ALUMNO: TREJO ARRIAGA RODRIGO GERARDO

ESTE PROGRAMA GENERA UNA PARTICIÓN DEL UNIVERSO DE PALABRAS BINARIAS:
i) ESCRIBE LA PARTICIÓN EN UN ARCHIVO DE TEXTO
ii) GENERA UNA GRÁFICA DE LAS PALABRAS BINARIAS VS EL NÚMERO DE UNOS QUE TIENEN
iii) GENERA UNA GRÁFICA DE LAS PALABRAS BINARIAS VS EL LOGARITMO DEL NÚMERO DE UNOS
    PARA APRECIAR MEJOR SU CRECIMIENTO

ÚLTIMA MODIFICACIÓN: 13/10/2023
'''

#  --------------------------------------------------------------------------------------------------------------------
# MÓDULOS Y LIBRERÍAS IMPORTADAS


import os
import time
import random
import matplotlib.pyplot as plt
import csv
import math

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

#  --------------------------------------------------------------------------------------------------------------------
# CLASES


class ParticionUniverso:

    def __init__(self, tam_particion: int, nombre_arch="particionUniverso", nombre_aux="aux_univ.txt") -> None:
        """Constructor de la clase que hace la partición del universo

        Args:
            tam_particion (int): Tamaño de la particion que se desea reaizar
            nombre_arch (str, optional): Nombre del archivo donde se almacena la particion de longitud especificada. Defaults to "particionUniverso".
            nombre_aux (str, optional): Archivo que sirve como auxiliar de las particiones. Defaults to "aux_univ.txt".
        """
        self.nombre_arch = nombre_arch
        self.tam_particion = tam_particion
        self.universo = ["0", "1"]
        self.archivo_universo = open(f"{nombre_arch}.txt", "a+", encoding="utf-8")
        self.archivo_universo.write("Σ = {ε, 0, 1, ")
        self.aux_universo = open(nombre_aux, "a+", encoding="utf-8")
        self.contador = 2
        self.unos = ["1, 0", "2, 1"]
        self.num_palabra = [1, 2]
        self.arch_num_unos = open("unos.csv", "a+", encoding="utf-8")


    def escribir_en_archivo(self, datos:list, escribir_coma: bool)-> None:
        """Método que escribe datos en el archivo de particion de universo

        Args:
            datos (list): Datos pertenecientes a la partición
            escribir_coma (bool): Bandera para escribir coma al final del uktimo caracter
        """
        self.archivo_universo.write(", ".join(datos))
        if escribir_coma:
            self.archivo_universo.write(", ")


    def escribir_en_archivo_unos(self, escribir_salto: bool)-> None:
        """Método que escribe datos en el archivo de particion de universo

        Args:
            datos (list): Datos pertenecientes a la partición
            escribir_coma (bool): Bandera para escribir coma al final del uktimo caracter
        """
        self.arch_num_unos.write("\n".join(self.unos))
        if escribir_salto:
            self.arch_num_unos.write("\n")


    def leer_linea_n(self, n:int) -> list:
        """Método que lee la linea n-ésima de un archivo

        Args:
            n (int): Número de linea que se desea leer

        Returns:
            list: Lista de palabras que corresponden a la n-ésima linea del archuvo
        """
        self.aux_universo.seek(0)
        contador = 0
        for linea in self.aux_universo:
            contador += 1
            if contador == n:
                return linea.strip().split(",")
            

    def generar_particion_universo(self) -> None:
        """Método que genera una aprtición del universo
        """
        long = 1
        datos_para_escribir = []
        conta_llenado = 0
        leidas = 0
        bandera_kill = False
        lim_escritura = 1677721

        while long < self.tam_particion and not bandera_kill:
            aux_universo, datos_para_escribir, bandera_kill = self.procesar_palabras(datos_para_escribir, lim_escritura, bandera_kill)

            if conta_llenado == 0:
                self.universo = aux_universo
                long += 1
            else:
                leidas += 1
                self.universo = self.leer_linea_n(leidas)

        if datos_para_escribir:
            self.escribir_en_archivo(datos_para_escribir, False)
            self.escribir_en_archivo_unos(False)
            self.archivo_universo.write("}")


    def contar_unos(self, palabra:str, cte_escritura:int):
        """Método que cuenta los unos en una palabra binaria

        Args:
            palabra (str): Palabra de la que se contarán los unos
            cte_escritura (int): límite de cadenas a almacenar antes de escribir en el archivo 
        """
        self.unos.extend([f"{self.contador+1}, {(palabra+'0').count('1')}", f"{self.contador+2}, {(palabra+'1').count('1')}"])
        self.contador += 2

        if len(self.unos) > cte_escritura:
            self.escribir_en_archivo_unos(True)
            self.unos = []


    def procesar_palabras(self, datos_para_escribir:list , lim_escritura:list , bandera_kill: bool) -> tuple:
        """Método que genera nuevas palabras y las escribe en el archivo de texto

        Args:
            datos_para_escribir (list): Datos almacenados en una lista antes de su escritura
            lim_escritura (list): Número máximo de elementos en la lista antes de escribir en el archivo
            bandera_kill (bool): Bandera que termina el bucle cuando se termina la partición

        Returns:
            tuple: Tupla con la lista auxiliar de la corrida anterior del universo,
                    la lista de datos que esperan ser escritos 
                    y la bandera de término de ciclo
        """
        aux_universo = []
        conta_llenado = 0
        for palabra in self.universo:

            if self.tam_particion == 28:
                if (self.contador+2) % 1000:
                    self.contar_unos(palabra, lim_escritura)
            else:
                self.contar_unos(palabra, lim_escritura)
            aux_universo.extend([palabra + "0", palabra + "1"])
            datos_para_escribir.extend([palabra + "0", palabra + "1"])

            if len(datos_para_escribir) >= lim_escritura:
                self.escribir_en_archivo(datos_para_escribir, True)
                datos_para_escribir = []

            if len(aux_universo) == lim_escritura:
                self.aux_universo.write(",".join(aux_universo))
                self.aux_universo.write("\n")
                conta_llenado += 1
                aux_universo = []

            if palabra.count("1") + 1 == self.tam_particion:
                bandera_kill = True

        return aux_universo, datos_para_escribir, bandera_kill
    

    def plotear_grafico(self, x, y, label_x, label_y, titulo):
        """Método que plotea una gráfica según dos listas

        Args:
            x (list): Lista de datos que irán en el eje x 
            y (list): Lista de datos que irán en el eje y
            titulo (str): Título de la gráfica
            label_x (str): Etiqueta del eje x
            label_y (str): Etiqueta del eje y
        """
        plt.figure(figsize=(10, 6))
        plt.plot(x, y, marker='o', linestyle='-', color='b', markersize=3)
        plt.title(titulo)
        plt.xlabel(label_x)
        plt.ylabel(label_y)
        plt.grid(True)
        plt.show()
    

    def graficar_num_unos(self):
        """Función que hace la gráfica del número de unos por número primo
        """
        columna_izquierda = []
        columna_derecha = []

        with open("unos.csv", 'r+') as archivo_csv:
            reader = csv.reader(archivo_csv)


            for fila in reader:
                columna_izquierda.append(int(fila[0]))
                columna_derecha.append(int(fila[1]))

        logaritmo = [0 if valor == 0 else math.log(valor) for valor in columna_derecha]

        self.plotear_grafico(columna_izquierda, columna_derecha, 'Número', 'Número de Unos', 'Número vs Número de Unos')

        self.plotear_grafico(columna_izquierda, logaritmo, "Numero", "log(num. de unos)", 'Número vs log()')

#  --------------------------------------------------------------------------------------------------------------------
# FUNCIÓN PRINCIPAL MAIN
            

if __name__ == "__main__":
    os.system('clear')
    eliminar_archs("particionUniverso.txt")
    eliminar_archs("aux_univ.txt")
    eliminar_archs("unos.csv")
    print("\t\t\t***PARTICIÓN DEL UNIVERSO***")
    print("Este programa generará una partición del alfabeto binario, según una longitud 'n'")
    modo = input("\n\t>>Deseas que 'n' se elija de manera automática o manual? [a/m]: ")
    while not modo.lower() != "a" and not modo.lower() != "m":
        print("Modo inválido, ingreséselo nuevamente para continuar")
        modo = input("\t>>Deseas que 'n' se elija de manera automática o manual? [a/m]: ")
    
    match modo:
        case "a":
            n = random.randint(0, 28)
            print(f"\nSe ha elegido un n={n}")
        case _:
            n = int(input("\nIngresa un n ∈ [0,100]: "))

    print("\nSe está ejecutando la partición, espera un momento.")
    inicio = time.perf_counter()
    test = ParticionUniverso(n)
    test.generar_particion_universo()
    fin = time.perf_counter()
    tiempo_transcurrido = fin - inicio
    test.arch_num_unos.close()
    test.graficar_num_unos()
    eliminar_archs("aux_univ.txt")
    eliminar_archs("unos.csv")
    print("\nListo, puedes consultar la partición en el archivo: 'particionUniverso.txt'.")
    print(f"Tiempo de generacion de la particion: {tiempo_transcurrido:.5f} segundos")
