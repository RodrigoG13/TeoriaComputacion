'''
INSTITUTO POLITÉCNICO NACIONAL
ESCUELA SUPERIOR DE CÓMPUTO

INGENIERÍA EN INTELIGENCIA ARTIFICIAL

TEORÍA DE LA COMPUTACIÓN
AUTÓMATA DE PILA

GRUPO: 5BM1
ALUMNO: TREJO ARRIAGA RODRIGO GERARDO

ESTE PROGRAMA GENERA UN AUTÓMATA DE PILA QUE VALIDA SI UNA CADENA PERTENECE AL LENGUAJE 0^n1^n Y:
i) SOLICITA AL USUARIO UNA CADENA A VALIDAR O LA GENERA DE MANERA RANDOM
ii) ANIMA EL AUTÓMATA DE PILA SI LA LONGITUD DE LA PALABRA ES MENOR A 10
iii) GENERA LA HISTORIA DE ID's EN UN ARCHIVO DE TEXTO

ÚLTIMA MODIFICACIÓN: 23/12/2023
'''

#  --------------------------------------------------------------------------------------------------------------------
# MÓDULOS Y LIBRERÍAS IMPORTADAS

import pygame
import sys
from stack_tda import Stack
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


def generar_cadena(long_cadena:int) -> str:
    """Función que genera la cadena binaria random

    Args:
        long_cadena (int): Longitud de la palabra binaria

    Returns:
        str: Palabra binarias
    """
    return ''.join([str(random.randint(0, 1)) for _ in range(random.randint(2, long_cadena))])


def animar_automata(estado: str, cadena:str, pila: Stack) -> None:
    """
    Función que anima el autómata de pila.

    Args:
        estado (str): Estado actual del autómata.
        cadena (str): La cadena de entrada que se está procesando.
        pila (Stack): El objeto pila que representa la pila del autómata.

    Esta función actualiza la ventana de pygame con la representación visual del estado actual del autómata, 
    la cadena de entrada restante y el contenido actual de la pila. Dibuja el estado, la cadena y la pila, 
    junto con flechas para indicar el movimiento actual.
    """
    screen.fill(WHITE)
    estado_autom = pygame.Rect(width // 2 - 25, height // 2 - 25, 50, 50)
    pygame.draw.rect(screen, LIGHT_GREEN, estado_autom)
    
    texto_estado = font.render(estado, True, BLACK)
    estado_rect = texto_estado.get_rect(center=(width // 2, height // 2))
    screen.blit(texto_estado, estado_rect)

    cadena_letra = font.render(cadena, True, BLACK)
    pila_letra = font.render(pila, True, BLACK)
    cadena_rect = cadena_letra.get_rect(center=(width // 2, height // 2 - 90))
    pila_rect = pila_letra.get_rect(center=(width // 2, height // 2 + 90))
    screen.blit(cadena_letra, cadena_rect)
    screen.blit(pila_letra, pila_rect)
    
    pygame.draw.line(screen, BLACK, (width // 2, height // 2 - 50), (width // 2, height // 2 - 70), 2)
    pygame.draw.polygon(screen, BLACK, [(width // 2, height // 2 - 75), (width // 2 - 5, height // 2 - 70), (width // 2 + 5, height // 2 - 70)])
    pygame.draw.line(screen, BLACK, (width // 2, height // 2 + 50), (width // 2, height // 2 + 70), 2)
    pygame.draw.polygon(screen, BLACK, [(width // 2, height // 2 + 75), (width // 2 - 5, height // 2 + 70), (width // 2 + 5, height // 2 + 70)])

    pygame.display.flip()


def automata_pila(cadena: str, lista_cadena: str, animar:bool, arch) -> bool:
    """
    Función que ejecuta el autómata de pila para una cadena dada.

    Args:
        cadena (str): La cadena de entrada para validar.
        lista_cadena (str): Lista de caracteres de la cadena.
        animar (bool): Indica si se debe animar el proceso del autómata.
        arch: Archivo donde se escribe el historial de transiciones.

    Returns:
        bool: Retorna True si la cadena es aceptada por el autómata, False en caso contrario.

    Esta función ejecuta el autómata de pila para determinar si la cadena dada pertenece al lenguaje 0^n1^n. 
    """

    global estado
    lista_cadena.append("")
    str_aux = cadena

    arch.write(f"({estado}, {str_aux[:]}, {''.join(pila.read_stack2())})->")
    for num_car, caracter in enumerate(lista_cadena):
        
        if estado == "q":
            if caracter == "0":
                pila.stack_push("X")
            elif caracter == "1":
                estado = "p"
                if pila.stack_pop() == "Z0":
                    return False
            else:
                return False

        elif estado == "p":
            if caracter == "1":
                if pila.stack_pop() == "Z0":
                    return False
                
            elif caracter == "0":
                return False
            
            elif caracter == "":
                if pila.stack_pop() == "Z0":
                    estado = 'f'
                    pila.stack_push('Z0')
                    if animar:
                        animar_automata(estado, ''.join(lista_cadena[num_car:]), ','.join(pila.read_stack2()))
                        pygame.time.delay(1000)  # Retardo para visualizar cada paso
                    arch.write(f"({estado}, ε, {''.join(pila.read_stack2())})")
                    return True
                
                else:
                    return False
            else:
                return False
        
        if animar:
            animar_automata(estado, ''.join(lista_cadena[num_car+1:]), ','.join(pila.read_stack2()))
            pygame.time.delay(1000)  # Retardo para visualizar cada paso
        
        arch.write(f"({estado}, {str_aux[num_car+1:] if str_aux[num_car+1:] != '' else 'ε'}, {''.join(pila.read_stack2())})->")

    return False


if __name__ == "__main__":
    os.system('clear')
    nombre_arch = "ids_pila"
    eliminar_archs(f"{nombre_arch}.txt")
    arch = open(f"{nombre_arch}.txt", "a+", encoding="utf-8")

    print("\t\t\t***AUTÓMATA DE PILA PARA EL LENGUAJE [0^n1^n]")
    op = input("Desea ejecutar el programa en modo manual o automático? [a/m]: ")
    while op!="a" and op != "m":
        print("Modo inválido, inténtelo nuevamente ):")
        op = input("Desea ejecutar el programa en modo manual o automático? [a/m]: ")
    
    cadena = input("Ingresa la cadena: ") if op == "m" else generar_cadena(100000)

    print(f"La cadena es {cadena}") if op == "a" else None

    animar = len(cadena) <= 10

    lista_cadena = list(cadena)

    arch.write(f"LA CADENA ES: {cadena}\n\n")

    pygame.init()

    size = width, height = 800, 600
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Autómata de Pila")

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    LIGHT_GREEN = (144, 238, 144)

    font = pygame.font.Font(None, 36)

    pila = Stack()
    pila.stack_push("Z0")
    estado = "q"

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        if automata_pila(cadena, lista_cadena, animar, arch):
            print("\n\t>>>COMPUTACIÓN EXITOSA")
            arch.write("\n\nCOMPUTACIÓN EXITOSA")
        else:
            print("\n\t>>>COMPUTACIÓN NO EXITOSA")
            arch.write("\n\nCOMPUTACIÓN NO EXITOSA")

        run = False

    pygame.quit()
    sys.exit()
