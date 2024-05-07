'''
INSTITUTO POLITÉCNICO NACIONAL
ESCUELA SUPERIOR DE CÓMPUTO

INGENIERÍA EN INTELIGENCIA ARTIFICIAL

TEORÍA DE LA COMPUTACIÓN
BAKUS-NAUR CONDITIONAL IF

GRUPO: 5BM1
ALUMNO: TREJO ARRIAGA RODRIGO GERARDO

ESTE PROGRAMA GENERA EL PSEUDOCÓDIGO DE UN PROGRAMA DE SENTENCIAS IF GENERADO A TRAVES DE BAKUS-NAUR CONDITIONAL IF:
i) SOLICITA AL USUARIO EL NÚMERO DE SENTENCIAS IF O LO GENERA DE MANERA AUTOMÁTICA
ii) ESCRIBE EN UN ARCHIVO LAS REGLAS DE PRODUCCIÓN DEL IF
iii) ESCRIBE EN UN ARCHIVO EL PSEUDOCÓDIGO GENERADO
iii) IMPRIME EN PANTALLA LA EXPRESIÓN GENERADA SI TIENE MENOS DE 50 IF

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


def reemplazar_nesima_ocurrencia(cadena: str, c_reemplazar: str, c_reemplazo: str, n:int) -> str:
    """
    Reemplaza la n-ésima ocurrencia de un carácter en una cadena.

    Args:
        cadena (str): Cadena en la que se realizará el reemplazo.
        c_reemplazar (str): Carácter que se buscará y reemplazará.
        c_reemplazo (str): Carácter con el que se reemplazará la n-ésima ocurrencia.
        n (int): Número de ocurrencia que se desea reemplazar.

    Returns:
        str: Cadena resultante después del reemplazo.
    """
    contador = 0
    resultado = ""

    for char in cadena:
        if char == c_reemplazar:
            contador += 1
            if contador == n:
                resultado += c_reemplazo
            else:
                resultado += char
        else:
            resultado += char

    return resultado


def format_bnf_to_pseudocode(expresion:str):
    """
    Convierte una expresión en formato BNF (Backus-Naur Form) a pseudocódigo
    con estructuras de control if.

    Args:
        expresion (str): Expresión en formato BNF.

    Returns:
        str: Pseudocódigo resultante.
    """
    nivel_ident = 0
    pseudocodigo = ""
    i = 0

    while i < len(expresion):
        if expresion[i] == 'i':
            pseudocodigo += ' ' * nivel_ident + 'if (condition) {\n'
            nivel_ident += 4 
        elif expresion[i] == 'e':
            nivel_ident -= 4
            pseudocodigo += ' ' * nivel_ident + '} else {\n'
            nivel_ident += 4
        elif expresion[i] == 'S':
            pseudocodigo += ' ' * nivel_ident + '//instrucciones//;\n'
        elif expresion[i] == ';':
            nivel_ident -= 4
            pseudocodigo += ' ' * nivel_ident + '}\n'

        i += 1

    while nivel_ident > 0:
        nivel_ident -= 4
        pseudocodigo += ' ' * nivel_ident + '}\n'

    return pseudocodigo


def aplicar_bnif(expresion:str, num_ifs:int, arch_cadena, arch_pseudo) -> str:
    """
    Aplica las reglas de producción de una gramática BNF condicional if para
    generar una expresión y su pseudocódigo asociado.

    Args:
        expresion (str): Expresión inicial en formato BNF.
        num_ifs (int): Número de instrucciones if a generar.
        arch_cadena: Archivo para registrar la cadena generada.
        arch_pseudo: Archivo para registrar el pseudocódigo.

    Returns:
        str: Expresión resultante.
    """
    print(f"La cantidad de if's elegida es: {num_ifs}") if op == "a" else None

    arch_cadena.write(f"La cantidad de if's será de {num_ifs}\n\n")

    arch_cadena.write(f"{expresion} // inicio\n")

    while expresion.count("i") < num_ifs:
        if "A" in expresion:
            rand = random.choice(a_rules)
            arch_cadena.write(f"{expresion} // A -> {'ε' if rand == '' else rand}: {expresion.replace('A', rand)}\n")
            expresion = expresion.replace("A", rand)

        else:
            rand = random.randint(1, expresion.count("S"))
            arch_cadena.write(f"{expresion} // {rand}S -> {s_rule}: {reemplazar_nesima_ocurrencia(expresion, 'S', s_rule, rand)  }\n")
            expresion = reemplazar_nesima_ocurrencia(expresion, "S", s_rule, rand)      
    arch_cadena.close()

    expresion = expresion.replace("A", "")

    pseudocode = format_bnf_to_pseudocode(expresion)

    arch_pseudo.write(pseudocode)
    arch_pseudo.close()
    return expresion


#  --------------------------------------------------------------------------------------------------------------------
# FUNCIÓN PPRINCIPAL


if __name__ == "__main__":

    conta_ifs = 1
    expresion = "iCtSA"
    a_rules = [";eS", ""]
    s_rule = "iCtSA"

    os.system('clear')
    nombre_arch_cadena = "generacion_if"
    eliminar_archs(f"{nombre_arch_cadena}.txt")
    arch_cadena = open(f"{nombre_arch_cadena}.txt", "a+", encoding="utf-8")

    nombre_arch_pseudo = "pseudocodigo_if"
    eliminar_archs(f"{nombre_arch_pseudo}.txt")
    arch_pseudo = open(f"{nombre_arch_pseudo}.txt", "a+", encoding="utf-8")

    print("\t\t\t***Bakus-Naur Condicional IF**")
    op = input("Desea ejecutar el programa en modo manual o automático? [a/m]: ")
    while op!="a" and op != "m":
        print("Modo inválido, inténtelo nuevamente ):")
        op = input("Desea ejecutar el programa en modo manual o automático? [a/m]: ")
    
    num_ifs = int(input("Ingresa la cantidad de if's: ")) if op == "m" else random.randint(0, 1000)

    expresion = aplicar_bnif(expresion, num_ifs, arch_cadena, arch_pseudo)
    
    print(f"\nExpresión generada: {expresion}")
    print(f"\nPuedes consultar la historia de generación en {nombre_arch_cadena}.txt")
    print(f"Y el pseudocódigo en {nombre_arch_pseudo}.txt (:")