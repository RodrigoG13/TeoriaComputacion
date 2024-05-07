import pygame
import sys
from stack_tda import Stack  # Asegúrate de que stack_tda es un módulo con la implementación de la pila
import os
import random

# --- Funciones Auxiliares ---

def eliminar_archs(nombre_arch):
    """Función que elimina un archivo si existe en el directorio."""
    if os.path.exists(nombre_arch):
        os.remove(nombre_arch)

def generar_cadena(long_cadena):
    """Función que genera una cadena binaria aleatoria."""
    return ''.join([str(random.randint(0, 1)) for _ in range(random.randint(2, long_cadena))])

# --- Funciones de Dibujo ---

def draw_state_box(screen, color, center_x, center_y, size):
    state_box = pygame.Rect(center_x - size // 2, center_y - size // 2, size, size)
    pygame.draw.rect(screen, color, state_box)

def draw_text(screen, font, text, color, center_x, center_y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(center_x, center_y))
    screen.blit(text_surface, text_rect)

def draw_arrow(screen, color, start_x, start_y, end_x, end_y, arrowhead_size):
    pygame.draw.line(screen, color, (start_x, start_y), (end_x, end_y), 2)
    pygame.draw.polygon(screen, color, [(end_x, end_y), (end_x - arrowhead_size, end_y + arrowhead_size), (end_x + arrowhead_size, end_y + arrowhead_size)])

def draw(estado, cadena, pila_content, screen, font, colors):
    screen.fill(colors['WHITE'])
    draw_state_box(screen, colors['LIGHT_GREEN'], width // 2, height // 2, 50)
    draw_text(screen, font, estado, colors['BLACK'], width // 2, height // 2)
    draw_text(screen, font, cadena, colors['BLACK'], width // 2, height // 2 - 90)
    draw_text(screen, font, pila_content, colors['BLACK'], width // 2, height // 2 + 90)
    draw_arrow(screen, colors['BLACK'], width // 2, height // 2 - 50, width // 2, height // 2 - 70, 5)
    draw_arrow(screen, colors['BLACK'], width // 2, height // 2 + 50, width // 2, height // 2 + 70, 5)
    pygame.display.flip()

# --- Lógica del Autómata ---

def handle_state_q(caracter, pila):
    if caracter == "0":
        pila.stack_push("X")
        return "q"
    elif caracter == "1":
        return "p" if pila.stack_pop() == "Z0" else None
    else:
        return None

def handle_state_p(caracter, pila):
    if caracter == "1":
        return "p" if pila.stack_pop() == "Z0" else None
    elif caracter == "0":
        return None
    elif caracter == "":
        return 'f' if pila.stack_pop() == "Z0" else None
    else:
        return None

def automata_pila_visual(lista_cadena, pila, estado, screen, font, colors):
    lista_cadena.append("")
    for num_car, caracter in enumerate(lista_cadena):
        if estado == "q":
            estado = handle_state_q(caracter, pila)
        elif estado == "p":
            estado = handle_state_p(caracter, pila)
        
        if estado is None:
            return False
        
        draw(estado, ''.join(lista_cadena[num_car:]), ','.join(pila.read_stack2()), screen, font, colors)
        pygame.time.delay(1000)  # Retardo para visualizar cada paso

        if estado == 'f':
            return True

    return False

# --- Bloque Principal ---

if __name__ == "__main__":
    print("\t\t\t***AUTÓMATA DE PILA PARA EL LENGUAJE [0^n1^n]")
    op = input("Desea ejecutar el programa en modo manual o automático? [a/m]: ")
    while op != "a" and op != "m":
        print("Modo inválido, inténtelo nuevamente ):")
        op = input("Desea ejecutar el programa en modo manual o automático? [a/m]: ")

    cadena = input("Ingresa la cadena: ") if op == "m" else generar_cadena(100000)
    lista_cadena = list(cadena)

    # Inicialización de Pygame
    pygame.init()

    # Configuración de la pantalla
    size = width, height = 800, 600
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Autómata de Pila")

    # Colores
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    LIGHT_GREEN = (144, 238, 144)
    colors = {'WHITE': WHITE, 'BLACK': BLACK, 'LIGHT_GREEN': LIGHT_GREEN}

    # Fuentes
    font = pygame.font.Font(None, 36)

    # Autómata y pila
    pila = Stack()
    pila.stack_push("Z0")
    estado = "q"

    # Bucle principal
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Ejecución del autómata de pila
        if automata_pila_visual(lista_cadena, pila, estado, screen, font, colors):
            print("COMPUTACIÓN EXITOSA")
        else:
            print("COMPUTACIÓN NO EXITOSA")

        running = False  # Detiene el bucle después de procesar la cadena

    # Salida de Pygame
    pygame.quit()
    sys.exit()
