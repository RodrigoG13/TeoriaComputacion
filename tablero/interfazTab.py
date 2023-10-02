import pygame
import sys
from pygame_menu import Menu

# Dimensiones del tablero y tamaño de celda
DIMENSIONES = 4
TAMANO_CELDA = 100

# Colores
ROJO = (124, 18, 66)
NEGRO = (0, 0, 0)

# Inicializa Pygame
pygame.init()

# Crear la ventana de Pygame
VENTANA_TAMANO = (DIMENSIONES * TAMANO_CELDA + 200, DIMENSIONES * TAMANO_CELDA)
ventana = pygame.display.set_mode(VENTANA_TAMANO)
pygame.display.set_caption("Simulación de Ajedrez")

# Matriz para representar el tablero (4x4)
tablero = [[0, 0, 0, 0],
           [0, 0, 0, 0],
           [0, 0, 0, 0],
           [0, 0, 0, 0]]

# Posiciones iniciales de las piezas
pieza1_pos = (0, 0)
pieza2_pos = (3, 3)

# Función para dibujar el tablero
def dibujar_tablero():
    for fila in range(DIMENSIONES):
        for columna in range(DIMENSIONES):
            color = ROJO if (fila + columna) % 2 == 0 else NEGRO
            pygame.draw.rect(ventana, color, (columna * TAMANO_CELDA, fila * TAMANO_CELDA, TAMANO_CELDA, TAMANO_CELDA))

# Función para dibujar las piezas
def dibujar_piezas():
    pygame.draw.circle(ventana, (255, 207, 216), (pieza1_pos[1] * TAMANO_CELDA + TAMANO_CELDA // 2, pieza1_pos[0] * TAMANO_CELDA + TAMANO_CELDA // 2), TAMANO_CELDA // 3)
    pygame.draw.circle(ventana, (236, 234, 175), (pieza2_pos[1] * TAMANO_CELDA + TAMANO_CELDA // 2, pieza2_pos[0] * TAMANO_CELDA + TAMANO_CELDA // 2), TAMANO_CELDA // 3)

# Función para iniciar el juego
def iniciar_juego():
    running = True
    clock = pygame.time.Clock()

    while running:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                running = False

        ventana.fill(ROJO)
        dibujar_tablero()
        dibujar_piezas()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

# Crear el menú principal
menu = Menu(VENTANA_TAMANO[0], VENTANA_TAMANO[1], 'Menú Principal')

# Agregar ComboBox y campo de texto al menú
menu.add_selector('ComboBox: ', [('Opción 1', 1), ('Opción 2', 2), ('Opción 3', 3)], onchange=None)
menu.add_text_input('Campo de Texto: ', default='Texto aquí')

menu.add_button('Jugar', iniciar_juego)
menu.add_button('Salir', pygame.quit)

# Bucle principal para mostrar el menú
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    menu.mainloop(ventana)
