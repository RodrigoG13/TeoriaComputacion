'''
INSTITUTO POLITÉCNICO NACIONAL
ESCUELA SUPERIOR DE CÓMPUTO

INGENIERÍA EN INTELIGENCIA ARTIFICIAL

TEORÍA DE LA COMPUTACIÓN
RANGO DE NÚMEROS PRIMOS

GRUPO: 5BM1
ALUMNO: TREJO ARRIAGA RODRIGO GERARDO

ESTE PROGRAMA POR PARTE DEL USUARIO UN LÍMITE DE RANGO "n" Y OBTIENE:
i) TODOS LOS NUMEROS QUE SON PRIMOS EN ESE RANGO Y LOS ALMACENA EN UN ARCHIVO .TXT
ii) GENERA UNA TABLA CON TODOS LOS NÚMEROS EN ESE RANGO Y ESCRIBE EL NÚMERO DE UNOS QUE TIENE
iii) GENERA UNA GRÁFICA QUE CORRESPONDE CON LA CANTIDAD DE UNOS QUE TIENE CADA NÚMERO PRIMO
iv) GENERA LA GRÁFICA DE LA FUNCION log(x) PARA COMPARARLA CON LA GENERADA POR EL PROGRAMA

ÚLTIMA MODIFICACIÓN: 01/09/2023
'''

#  --------------------------------------------------------------------------------------------------------------------
# MÓDULOS Y LIBRERÍAS IMPORTADAS


import os
import time
import csv
import matplotlib.pyplot as plt
import random

#  --------------------------------------------------------------------------------------------------------------------
# CLASES


class ParticionNumPrimos:
    """Clase que genera la partición del universo de números primos"""


    def __init__(self, fin_rango: int) -> None:
        """Constructor de la clase

        Args:
            fin_rango (int): Límite del rango de la partición
        """
        self.fin_rango = fin_rango 
        self.arch_binprimos =  open(f"univ_binprimos.txt", "w+", encoding="utf-8") 
        self.arch_decprimos =  open(f"univ_decprimos.txt", "w+", encoding="utf-8")  
        self.arch_tablasUnos = open(f"tabla.csv", "w+")
        self.arch_tablasUnos.write("Numero, Cantidad de Unos\n" )  


    def es_primo(self, num_test: int) -> bool:
        """Método que indica si un número es primo

        Args:
            num_test (int): Número que se verifica si es primo

        Returns:
            bool: Bandera que dice si el número es primo o no
        """

        # Comprobamos si n es igual a 2 (único primo par)
        if num_test == 2:
            return True

        # Comprobamos si n es menor que 2 o es un número par
        if num_test < 2 or not num_test % 2:
            return False

        sqrt_n = int(num_test**0.5) + 1  # Calculamos la raíz cuadrada de n + 1 una vez

        # Comprobamos si n es divisible por cualquier entero impar entre 3 y la raíz cuadrada de n
        return not any(num_test % i == 0 for i in range(3, sqrt_n, 2))
    

    def convertir_a_binario(self, numero: int) -> str:
        """Método que convierte un número decimal a binario

        Args:
            numero (int): Número decimal

        Returns:
            str: Número binario
        """
        return bin(numero)[2:]
    

    def calcular_rango_primos(self):
        """Método que escribe en archivos los números primos decimales y binarios
        """
        for i in range(2, self.fin_rango+1):
            bandera_primo = self.es_primo(i)
            if bandera_primo:
                #num = self.convertir_a_binario(i)
                binario = self.convertir_a_binario(i)
                self.arch_binprimos.write(f"{binario}, ")
                self.arch_decprimos.write(f"{i}, ")
                self.arch_tablasUnos.write(f"{i}, {binario.count('1')}\n")


    def graficar_num_unos(self):
        """Función que hace la gráfica del número de unos por número primo
        """
        numeros_primos = []
        numeros_de_unos = []

        with open("tabla.csv", newline='') as archivo_csv:
            reader = csv.DictReader(archivo_csv)
            for fila in reader:
                try:
                    numeros_primos.append(int(fila["Numero"]))
                    numeros_de_unos.append(int(fila[" Cantidad de Unos"]))
                except:
                    print(f"numero = {fila['Numero']} Cantidad = {int(fila[' Cantidad de Unos'])}")
        plt.figure(figsize=(10, 6))
        plt.plot(numeros_primos, numeros_de_unos, marker='o', linestyle='-', color='b', markersize=3)
        plt.title('Número Primo vs Número de Unos')
        plt.xlabel('Número Primo')
        plt.ylabel('Número de Unos')
        plt.grid(True)
        plt.show()
                

#  --------------------------------------------------------------------------------------------------------------------
# FUNCIÓN PRINCIPAL MAIN


if __name__ == "__main__":
    os.system('clear')

    print("\t\t\t***UNIVERSO DE NÚMEROS PRIMOS***")
    modo = input("\t>>Deseas que el rango se elija de manera automática o manual? [a/m]: ")
    while modo.lower() != "a" and modo.lower() != "m":
        print("Modo inválido, ingreséselo nuevamente para continuar")
        modo = input("\t>>Deseas que 'n' se elija de manera automática o manual? [a/m]: ")

    match modo:
        case "m":
            n = int(input("\nIngresa el rango máximo para el cálculo de primos [4,10⁷]: "))
            while n > 10000000 and n < 4:
                print("Rango incorrecto! Inténtalo nuevamente.")
                n = int(input("\nIngresa el rango máximo para el cálculo de primos [4,10⁷]: "))
        case _:
            n = random.randint(0, 10000000)
            print(f"\nSe ha elegido un n={n}")

    print("\t >>Calculando números primos...\n")
    inicio = time.perf_counter()
    t = ParticionNumPrimos(n)
    t.calcular_rango_primos()
    fin = time.perf_counter()
    t.arch_binprimos.close()
    t.arch_decprimos.close()
    t.arch_tablasUnos.close()
    t.graficar_num_unos()
    tiempo_transcurrido = fin - inicio
    print(f"Se han calculado los números primos en un tiempo de: {tiempo_transcurrido:.2f} segundos")