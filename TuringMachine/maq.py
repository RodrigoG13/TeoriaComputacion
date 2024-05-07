'''
INSTITUTO POLITÉCNICO NACIONAL
ESCUELA SUPERIOR DE CÓMPUTO

INGENIERÍA EN INTELIGENCIA ARTIFICIAL

TEORÍA DE LA COMPUTACIÓN
MÁQUINA DE TURING

GRUPO: 5BM1
ALUMNO: TREJO ARRIAGA RODRIGO GERARDO

ESTE PROGRAMA GENERA UNA MÁQUINA DE TURING QUE VALIDA SI UNA CADENA PERTENECE AL LENGUAJE 0^n1^n Y:
i) SOLICITA AL USUARIO UNA CADENA A VALIDAR O LA GENERA DE MANERA RANDOM
ii) ANIMA LA MÁQUINA DE TURING SI LA LONGITUD DE LA PALABRA ES MENOR A 16
iii) GENERA LA HISTORIA DE ID's EN UN ARCHIVO DE TEXTO

ÚLTIMA MODIFICACIÓN: 25/12/2023
'''

#  --------------------------------------------------------------------------------------------------------------------
# MÓDULOS Y LIBRERÍAS IMPORTADAS

import pygame
import os
import random

#  --------------------------------------------------------------------------------------------------------------------
# CLASES


class TuringMachine:

    def __init__(self, cinta_string, simbolo_blanco="B"):
        self.cinta = list(cinta_string) + [simbolo_blanco] * 2  # Añade 2 blancos al final
        self.cabezal = 0
        self.estado = 'q0'
        self.simbolo_blanco = simbolo_blanco
        self.detener = False
        self.tabla_trans = {
            ('q0', '0'): ('q1', 'X', 'R'),
            ('q0', 'Y'): ('q3', 'Y', 'R'),
            ('q1', '0'): ('q1', '0', 'R'),
            ('q1', '1'): ('q2', 'Y', 'L'),
            ('q1', 'Y'): ('q1', 'Y', 'R'),
            ('q2', '0'): ('q2', '0', 'L'),
            ('q2', 'X'): ('q0', 'X', 'R'),
            ('q2', 'Y'): ('q2', 'Y', 'L'),
            ('q3', 'Y'): ('q3', 'Y', 'R'),
            ('q3', self.simbolo_blanco): ('q4', self.simbolo_blanco, 'R'),
        }


    def es_aceptada(self):
        return self.estado == 'q4'


    def es_rechazada(self):
        return self.estado != 'q4'


    def transicion(self, arch):
        if self.detener:
            return None

        simbolo_act = self.cinta[self.cabezal]

        alfa = ''.join(self.cinta[:self.cabezal]).replace("B", "")
        q = self.estado
        beta = ''.join(self.cinta[self.cabezal:]).replace("B", "")
        arch.write(f"{alfa}{q}{simbolo_act if simbolo_act != 'B' else ''}{beta} ⊦ ")

        accion = self.tabla_trans.get((self.estado, simbolo_act))

        if accion is None:
            self.detener = True
        else:
            nuevo_estado, nuevo_simbolo, direccion = accion
            self.cinta[self.cabezal] = nuevo_simbolo
            self.cabezal += 1 if direccion == 'R' else -1
            self.estado = nuevo_estado
    

    def run(self, arch):
        while not self.detener:
            self.transicion(arch)

        return self.estado == 'q4'


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
            

def draw_tape(tape, head_position):
    num_cells = len(tape)
    tape_offset_dynamic = (width - (cell_size * num_cells)) // 2
    for i in range(num_cells):
        rect = pygame.Rect(tape_offset_dynamic + i * cell_size, height // 2 - cell_size // 2, cell_size, cell_size)
        pygame.draw.rect(screen, GRAY, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)
        font = pygame.font.SysFont(None, 36)
        text = font.render(tape[i], True, BLACK)
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)
    head_rect = pygame.Rect(tape_offset_dynamic + head_position * cell_size, height // 2 - cell_size * 1.5, cell_size, cell_size * 2)
    pygame.draw.rect(screen, BLACK, head_rect, 2)
    pygame.draw.polygon(screen, BLACK, [
        (head_rect.centerx, head_rect.centery),
        (head_rect.centerx - 10, head_rect.centery - 20),
        (head_rect.centerx + 10, head_rect.centery - 20)
    ])

def main_animar(tm, arch):
    running = True
    start_simulation = False

    while running:
        screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                start_simulation = True

        if start_simulation:
            tm.transicion(arch)

        draw_tape(tm.cinta, tm.cabezal)

        if tm.detener:
            running = False

        pygame.display.flip()
        clock.tick(1)

    pygame.quit()


#  --------------------------------------------------------------------------------------------------------------------
# FUNCIÓN PRINCIPAL 

if __name__ == "__main__":


    os.system('clear')
    nombre_arch = "turing_machine"
    eliminar_archs(f"{nombre_arch}.txt")
    arch = open(f"{nombre_arch}.txt", "a+", encoding="utf-8")

    print("\t\t\t***TURING MACHINE PARA EL LENGUAJE [0^n1^n]")
    op = input("Desea ejecutar el programa en modo manual o automático? [a/m]: ")
    while op!="a" and op != "m":
        print("Modo inválido, inténtelo nuevamente ):")
        op = input("Desea ejecutar el programa en modo manual o automático? [a/m]: ")
    
    cadena = input("Ingresa la cadena: ") if op == "m" else generar_cadena(1000)

    print(f"La cadena es {cadena}") if op == "a" else None

    animar = len(cadena) < 16

    arch.write(f"LA CADENA ES: {cadena}\n\n")
    tm = TuringMachine(cadena)

    if animar:
        pygame.init()
        width, height = 800, 200
        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Turing Machine Animation')
        clock = pygame.time.Clock()

        # Colores
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        GRAY = (200, 200, 200)

        # Tamaño de la celda
        cell_size = 50

        main_animar(tm, arch)
    
    else:
        is_accepted = tm.run(arch)

    if tm.es_aceptada():
        print("Cadena aceptada")
    elif tm.es_rechazada():
        print("Cadena rechazada")
    else:
        print("Halted")

    print(f"Estado final de la cinta: {''.join(tm.cinta)}")
    arch.close()

