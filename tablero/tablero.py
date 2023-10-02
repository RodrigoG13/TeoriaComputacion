import pygame
import sys

# Dimensiones del tablero y tamaño de celda
DIMENSIONES = 4
TAMANO_CELDA = 100

# Colores
#ROJO = (177, 11, 87)
ROJO = (124,18,66)
NEGRO = (0, 0, 0)

# Inicializa Pygame
pygame.init()

# Crear la ventana
VENTANA_TAMANO = (DIMENSIONES * TAMANO_CELDA, DIMENSIONES * TAMANO_CELDA)
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
            color = NEGRO if (fila + columna) % 2 == 0 else ROJO
            pygame.draw.rect(ventana, color, (columna * TAMANO_CELDA, fila * TAMANO_CELDA, TAMANO_CELDA, TAMANO_CELDA))

# Función para dibujar las piezas
def dibujar_piezas():
    pygame.draw.circle(ventana, (255, 207, 216), (pieza1_pos[1] * TAMANO_CELDA + TAMANO_CELDA // 2, pieza1_pos[0] * TAMANO_CELDA + TAMANO_CELDA // 2), TAMANO_CELDA // 3)
    pygame.draw.circle(ventana, (236, 234, 175), (pieza2_pos[1] * TAMANO_CELDA + TAMANO_CELDA // 2, pieza2_pos[0] * TAMANO_CELDA + TAMANO_CELDA // 2), TAMANO_CELDA // 3)

# Bucle principal del juego
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_UP and pieza1_pos[0] > 0:
                pieza1_pos = (pieza1_pos[0] - 1, pieza1_pos[1])
            elif evento.key == pygame.K_DOWN and pieza1_pos[0] < DIMENSIONES - 1:
                pieza1_pos = (pieza1_pos[0] + 1, pieza1_pos[1])
            elif evento.key == pygame.K_LEFT and pieza1_pos[1] > 0:
                pieza1_pos = (pieza1_pos[0], pieza1_pos[1] - 1)
            elif evento.key == pygame.K_RIGHT and pieza1_pos[1] < DIMENSIONES - 1:
                pieza1_pos = (pieza1_pos[0], pieza1_pos[1] + 1)

    ventana.fill(ROJO)
    dibujar_tablero()
    dibujar_piezas()
    pygame.display.flip()
