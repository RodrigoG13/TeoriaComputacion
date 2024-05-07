'''
INSTITUTO POLITÉCNICO NACIONAL
ESCUELA SUPERIOR DE CÓMPUTO

INGENIERÍA EN INTELIGENCIA ARTIFICIAL

TEORÍA DE LA COMPUTACIÓN
LENGUAJES LIBRES DE CONTEXTO - PALÍNDROMOS

GRUPO: 5BM1
ALUMNO: TREJO ARRIAGA RODRIGO GERARDO

ESTE PROGRAMA GENERA UN PALÍNDROMO DE LONGITUD <<tam>>:
i) SOLICITA AL USUARIO EL TAMAÑO DEL PALÍNDROMO O LO GENERA DE MANERA AUTOMÁTICA
ii) ESCRIBE EN UN ARCHIVO LAS REGLAS DE PRODUCCIÓN DEL PALÍNDROMO
iii) IMPRIME EN PANTALLA EL PALÍNDROMO OBTENIDO SI SU LONGITUD ES MENOR O IGUAL A 100

ÚLTIMA MODIFICACIÓN: 24/12/2023
'''

#  --------------------------------------------------------------------------------------------------------------------
# MÓDULOS Y LIBRERÍAS IMPORTADAS

import os
import random

#  --------------------------------------------------------------------------------------------------------------------
# FUNCIONES

def eliminar_archs(nombre_arch: str) -> None:
    """Función que elimina un archivo si existe en el directorio

    Args:
        nombre_arch (str): Nombre del archivo que deseas eliminar
    """
    archivo1 = nombre_arch
    if os.path.exists(archivo1):
        os.remove(archivo1)


#  --------------------------------------------------------------------------------------------------------------------
# FUNCIÓN PPRINCIPAL


if __name__ == "__main__":
    
    palindromo = "P"
    reglas = {1:"", 2:"0", 3:"1", 4:"0P0", 5:"1P1"}
    reglas_constr = [4,5]
    regla_fin_par = 1
    reglas_fin_imp = [2,3]

    os.system('clear')
    nombre_arch = "reglas_palindromo"
    eliminar_archs(f"{nombre_arch}.txt")
    arch = open(f"{nombre_arch}.txt", "a+", encoding="utf-8")

    print("\t\t\t***LENGUAJES LIBRES DE CONTEXTO - PALÍNDROMOS")
    op = input("Desea ejecutar el programa en modo manual o automático? [a/m]: ")
    while op!="a" and op != "m":
        print("Modo inválido, inténtelo nuevamente ):")
        op = input("Desea ejecutar el programa en modo manual o automático? [a/m]: ")
    
    tam = int(input("Ingresa el tamaño de la cadena: ")) if op == "m" else random.randint(0, 10000)

    print(f"El tamaño elegido es {tam}") if op == "a" else None

    arch.write(f"El tamaño del palíndromo será de {tam}\n\n")

    bandera_par = tam % 2 == 0
    arch.write(f"{palindromo}; inicio \n")

    while len(palindromo) <= tam+1:
        if bandera_par and len(palindromo) > tam:
            palindromo = palindromo.replace("P", reglas[regla_fin_par])
            arch.write(f"{palindromo}; P -> ε\n")
            break
        elif not bandera_par and len(palindromo) == tam:
            rand = random.choice(reglas_fin_imp)
            palindromo = palindromo.replace("P", reglas[rand])
            arch.write(f"{palindromo}; P ->  {reglas[rand]}\n")
            break
        rand = random.choice(reglas_constr)
        palindromo = palindromo.replace("P", reglas[rand])
        arch.write(f"{palindromo}; P ->  {reglas[rand]}\n")
    
    arch.close()

    print(f"El tamaño elegido es {tam}") if tam <= 100 else None

    print(f"El palíndromo generado fue: {palindromo}\n") if tam <= 100 else None

    print(f"Puedes consultar las reglas de su producción en {nombre_arch}.txt (:")