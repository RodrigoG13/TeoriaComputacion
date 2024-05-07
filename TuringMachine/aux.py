import pygame
import sys

# Configuración inicial de Pygame
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

# Define la clase TuringMachine
class TuringMachine:
    def __init__(self, tape_string, blank_symbol="B"):
        self.tape = list(tape_string) + [blank_symbol] * 2  # Añade 2 blancos al final
        self.head_position = 0
        self.current_state = 'q0'
        self.blank_symbol = blank_symbol
        self.halted = False
        self.transition_function = {
            ('q0', '0'): ('q1', 'X', 'R'),
            ('q0', 'Y'): ('q3', 'Y', 'R'),
            ('q1', '0'): ('q1', '0', 'R'),
            ('q1', '1'): ('q2', 'Y', 'L'),
            ('q1', 'Y'): ('q1', 'Y', 'R'),
            ('q2', '0'): ('q2', '0', 'L'),
            ('q2', 'X'): ('q0', 'X', 'R'),
            ('q2', 'Y'): ('q2', 'Y', 'L'),
            ('q3', 'Y'): ('q3', 'Y', 'R'),
            ('q3', self.blank_symbol): ('q4', self.blank_symbol, 'R'),
        }

    def is_accepted(self):
        return self.current_state == 'q4'

    def is_rejected(self):
        return self.current_state != 'q4'

    def step(self):
        if self.halted:
            return

        current_symbol = self.tape[self.head_position]
        action = self.transition_function.get((self.current_state, current_symbol))

        if action is None:
            self.halted = True
        else:
            new_state, new_symbol, move_direction = action
            self.tape[self.head_position] = new_symbol
            self.head_position += 1 if move_direction == 'R' else -1
            self.current_state = new_state

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

def main():
    tm = TuringMachine('0011')  # Reemplaza con la entrada deseada
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
            tm.step()

        draw_tape(tm.tape, tm.head_position)

        if tm.halted:
            running = False

        pygame.display.flip()
        clock.tick(1)

    pygame.quit()

    # Mensaje en consola después de cerrar la ventana de Pygame
    if tm.is_accepted():
        print("Cadena aceptada")
    elif tm.is_rejected():
        print("Cadena rechazada")
    else:
        print("Halted")

    print(f"Estado final de la cinta: {''.join(tm.tape)}")

if __name__ == "__main__":
    main()
