import os
import random
from stack_tda import *

def eliminar_archs(nombre_arch):
    """Función que elimina un archivo si existe en el directorio

    Args:
        nombre_arch (str): Nombre del archivo que deseas eliminar
    """
    archivo1 = nombre_arch
    if os.path.exists(archivo1):
        os.remove(archivo1)


def generar_cadena(long_cadena:int) -> str:
    """Función que genera la cadena binaria random

    Args:
        long_cadena (int): Longitud de la palabra binaria

    Returns:
        str: Palabra binarias
    """
    return ''.join([str(random.randint(0, 1)) for _ in range(random.randint(2, long_cadena))])


def automata_pila(lista_cadena):
    lista_cadena.append("")
    pila = Stack()
    pila.stack_push("Z0")
    estado = "q"
    str_aux = cadena
    print(f"{str_aux[0:]} <- {estado} -> {','.join(pila.read_stack2())}")
    for num_car, caracter in enumerate(lista_cadena):
        
        if estado == "q":
            if caracter == "0":
                pila.stack_push("X")
            elif caracter == "1":
                estado = "p"
                if pila.stack_pop() == "Z0":
                    break
            else:
                estado = None
                break

        elif estado == "p":
            if caracter == "1":
                if pila.stack_pop() == "Z0":
                    break
            elif caracter == "0":
                estado = None
                break
            elif caracter == "":
                if pila.stack_pop() == "Z0":
                    estado = 'f'
                    pila.stack_push('Z0')
                    print(f"{str_aux[num_car:]} <- {estado} -> {','.join(pila.read_stack2())}")
                    break
                else:
                    estado = None
                    break
            else:
                break
        print(f"{str_aux[num_car+1:]} <- {estado} -> {','.join(pila.read_stack2())}")
    if estado == "f":
        print("COMPUTACIÓN EXITOSA")
    
    else:
        print("COMPUTACIÓN NO EXITOSA")
    

if __name__ == "__main__":

    print("\t\t\t***AUTÓMATA DE PILA PARA EL LENGUAJE [0^n1^n]")
    op = input("Desea ejecutar el programa en modo manual o automático? [a/m]: ")
    while op!="a" and op != "m":
        print("Modo inválido, inténtelo nuevamente ):")
        op = input("Desea ejecutar el programa en modo manual o automático? [a/m]: ")
    
    cadena = input("Ingresa la cadena: ") if op == "m" else generar_cadena(100000)

    animar = len(cadena) <= 10

    lista_cadena = list(cadena)
    automata_pila(lista_cadena)



    
