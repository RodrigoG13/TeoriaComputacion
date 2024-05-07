from graphics import *
import math

class AutomataDrawer:
    def __init__(self, width, height):
        self.win = GraphWin("Automata Drawer", width, height)
        self.states = []

    def draw_state(self, x, y, radius=20, is_initial=False, label=None):
        # Dibuja un estado personalizable con un círculo y un texto opcional en el centro
        state = Circle(Point(x, y), radius)
        state.setFill("lightblue")
        state.setOutline("black")
        state.draw(self.win)

        if is_initial:
            # Dibuja un círculo adicional dentro del estado para representar el estado inicial
            inner_circle = Circle(Point(x, y), radius - 5)
            inner_circle.setFill("white")
            inner_circle.draw(self.win)

        if label:
            # Dibuja un texto en el centro del estado
            text = Text(Point(x, y), label)
            text.setSize(int(radius / 2))  # Ajusta el tamaño del texto
            text.draw(self.win)

        self.states.append(state)

    def draw_transition(self, x1, y1, x2, y2):
        # Dibuja una línea entre dos puntos para representar una transición
        line = Line(Point(x1, y1), Point(x2, y2))
        line.setOutline("black")
        line.draw(self.win)


    def draw_loop_transition(self, x, y, radius=20, label=None, is_horizontal=False):
        # Dibuja una transición de un estado a sí mismo en forma de semicírculo
        num_segments = 20
        if is_horizontal:
            start_angle = 0
            end_angle = 180
        else:
            start_angle = -90
            end_angle = 90
        angle_increment = (end_angle - start_angle) / num_segments

        for i in range(num_segments + 1):
            angle = start_angle + i * angle_increment
            x1 = x + radius * math.cos(math.radians(angle))
            y1 = y + radius * math.sin(math.radians(angle))
            angle += angle_increment
            x2 = x + radius * math.cos(math.radians(angle))
            y2 = y + radius * math.sin(math.radians(angle))
            line = Line(Point(x1, y1), Point(x2, y2))
            line.setOutline("black")
            line.draw(self.win)

        if label:
            if is_horizontal:
                # Dibuja una etiqueta en el centro del semicírculo horizontal
                text = Text(Point(x, y), label)
                text.setSize(int(radius / 2))
                text.draw(self.win)
            else:
                # Dibuja una etiqueta en el centro del semicírculo vertical
                text = Text(Point(x, y - radius * 0.5), label)
                text.setSize(int(radius / 2))
                text.draw(self.win)



    def clear(self):
        # Borra todos los elementos dibujados en la ventana
        for state in self.states:
            state.undraw()
        self.states = []
        self.win.update()

    def close(self):
        # Cierra la ventana
        self.win.close()

# Ejemplo de uso:
if __name__ == "__main__":
    drawer = AutomataDrawer(800, 800)

    # Dibuja estados con radio y etiquetas personalizadas
    drawer.draw_state(100, 100, radius=30, is_initial=True, label="q0")
    drawer.draw_state(200, 200, radius=25, label="q1")
    drawer.draw_state(300, 300, radius=35, label="q2")

    # Dibuja transiciones
    drawer.draw_transition(125, 125, 175, 175)
    drawer.draw_transition(225, 225, 275, 275)

    # Dibuja una transición de un estado a sí mismo
    drawer.draw_loop_transition(130, 70, radius=30, label="a")
    
    # Dibuja una transición de un estado a sí mismo en forma de semicírculo horizontal
    drawer.draw_loop_transition(300, 390, radius=25, label="b", is_horizontal=True)

    input("Presiona Enter para cerrar la ventana...")
    drawer.close()