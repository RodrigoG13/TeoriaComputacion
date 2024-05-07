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

    def __init__(self, cinta_string: str, simbolo_blanco: str ="B") -> None:
        """
        Inicializa la Máquina de Turing.

        Args:
            cinta_string (str): La cadena de entrada para la máquina.
            simbolo_blanco (str): El símbolo que representa un espacio en blanco en la cinta.
        """
        self.cinta = list(cinta_string) + [simbolo_blanco] * 2
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


    def es_aceptada(self) -> bool:
        """
        Verifica si la máquina de Turing ha llegado a un estado de aceptación.

        Returns:
            bool: True si está en un estado de aceptación, False de lo contrario.
        """
        return self.estado == 'q4'


    def es_rechazada(self) -> bool:
        """
        Verifica si la máquina de Turing ha llegado a un estado de rechazo.

        Returns:
            bool: True si está en un estado de rechazo, False de lo contrario.
        """
        return self.estado != 'q4'


    def transicion(self, arch) -> None:
        """
        Realiza una transición de la máquina de Turing.

        Args:
            arch: El archivo de texto donde se guarda la historia de IDs.
        """
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
    

    def run(self, arch) -> bool:
        """
        Ejecuta la Máquina de Turing hasta que se detiene.

        Args:
            arch: El archivo de texto donde se guarda la historia de IDs.

        Returns:
            bool: True si la cadena fue aceptada, False de lo contrario.
        """
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
            

def animar_turing(cinta: str, pos_cabezal: int) -> None:
    """
    Anima la representación visual de la máquina.

    Args:
        cinta (str): La representación de la cinta.
        pos_cabezal (int): La posición actual del cabezal en la cinta.

    Returns:
        None
    """
    num_celdas = len(cinta)
    acomodo = (width - (cell_size * num_celdas)) // 2
    for i in range(num_celdas):
        rect = pygame.Rect(acomodo + i * cell_size, height // 2 - cell_size // 2, cell_size, cell_size)
        pygame.draw.rect(screen, GRAY, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)
        font = pygame.font.SysFont(None, 36)
        text = font.render(cinta[i], True, BLACK)
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)
    head_rect = pygame.Rect(acomodo + pos_cabezal * cell_size, height // 2 - cell_size * 1.5, cell_size, cell_size * 2)
    pygame.draw.rect(screen, BLACK, head_rect, 2)
    pygame.draw.polygon(screen, BLACK, [
        (head_rect.centerx, head_rect.centery),
        (head_rect.centerx - 10, head_rect.centery - 20),
        (head_rect.centerx + 10, head_rect.centery - 20)
    ])


def main_animar(tm: TuringMachine, arch):
    """
    Función principal para animar la ejecución de la Máquina de Turing.

    Args:
        tm (TuringMachine): Instancia de la Máquina de Turing.
        arch: El archivo de texto donde se guarda la historia de IDs.

    Returns:
        None
    """
    running = True
    start_simulation = False

    print("\nPresione una tecla para iniciar la animación...")

    while running:
        screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                start_simulation = True

        if start_simulation:
            tm.transicion(arch)

        animar_turing(tm.cinta, tm.cabezal)

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

        WHITE = (175, 233, 236)
        BLACK = (15, 6, 88)
        GRAY = (81, 148, 240)

        cell_size = 50

        main_animar(tm, arch)
    
    else:
        is_accepted = tm.run(arch)

    if tm.es_aceptada():
        print("\nCadena aceptada")
    elif tm.es_rechazada():
        print("\nCadena rechazada")
    else:
        print("\nDetenida!!!")

    print(f"Estado final de la cinta: {''.join(tm.cinta)}")
    arch.close()