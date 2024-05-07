from graphics import *
import math

class AutomataDrawer:
    def __init__(self, width, height):
        self.win = GraphWin("Automata Drawer", width, height)
        self.states = []

    def draw_state(self, x, y, tam_text, radius=20, is_initial=False, label=None, line_width=2):
        # Dibuja un estado personalizable con un círculo y un texto opcional en el centro
        state = Circle(Point(x, y), radius)
        state.setWidth(line_width)
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
            text.setSize(int(radius / tam_text))  # Ajusta el tamaño del texto
            text.draw(self.win)

        self.states.append(state)

    def draw_transition(self, x1, y1, x2, y2, label=None, tam_text=12, line_width=1, cte_x=0, cte_y=0):
        # Dibuja una línea entre dos puntos para representar una transición
        line = Line(Point(x1, y1), Point(x2, y2))
        line.setOutline("black")
        line.setWidth(line_width) 
        line.draw(self.win)

        if label:
            # Dibuja una etiqueta (texto) en el centro de la línea de transición
            mid_x = (x1 + x2 +cte_x) / 2
            mid_y = (y1 + y2 +cte_y) / 2
            text = Text(Point(mid_x, mid_y), label)
            text.setSize(tam_text)
            text.draw(self.win)

        
    def draw_filled_circle(self, x, y, radius, color="darkblue"):
        # Dibuja un círculo relleno de color azul fuerte
        filled_circle = Circle(Point(x, y), radius)
        filled_circle.setFill(color)
        filled_circle.setOutline(color)  # Puedes configurar el color del borde al mismo color si no quieres un borde
        filled_circle.draw(self.win)


    def draw_loop_transition(self, x, y, radius=20, label=None, is_horizontal=False, cte_x=0, cte_y=0, cte_text=0, line_width=2):
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
            line.setWidth(line_width)
            line.setOutline("black")
            line.draw(self.win)

        if label:
            if is_horizontal:
                # Dibuja una etiqueta en el centro del semicírculo horizontal
                text = Text(Point(x+cte_x, y+cte_y), label)
                text.setSize(int(radius / 2+cte_text))
                text.draw(self.win)
            else:
                # Dibuja una etiqueta en el centro del semicírculo vertical
                text = Text(Point(x+cte_x, y+cte_y - radius * 0.5), label)
                text.setSize(int(radius / 2+cte_text))
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
    drawer = AutomataDrawer(850, 800)

    # Dibuja estados con radio y etiquetas personalizadas
    drawer.draw_state(200, 150, 2.5, radius=50, is_initial=False, label="Ready")

    drawer.draw_state(600, 150, 2.7, radius=50, is_initial=False, label="Sending")

    drawer.draw_transition(250, 150, 550, 150, "data in", 15, 2, 10, -20)

    drawer.draw_loop_transition(650, 150, radius=30, label="time_out", cte_x=17, cte_y=-30, cte_text=0.1)

    drawer.draw_state(400, 300, 2.7, radius=45, is_initial=True, label="q0")

    drawer.draw_transition(225, 190, 358, 290, line_width=2)

    drawer.draw_transition(445, 290, 570, 190, line_width=2)

    drawer.draw_state(200, 450, 2.7, radius=45, is_initial=False, label="q1")

    drawer.draw_transition(232, 420, 358, 320, "1", line_width=2, cte_y=-26)

    drawer.draw_transition(243, 445, 372, 340, "1", line_width=2, cte_y=35)

    drawer.draw_state(600, 450, 2.7, radius=45, is_initial=False, label="q3")

    drawer.draw_transition(570, 420, 440, 315, "0", line_width=2, cte_y=-26)

    drawer.draw_transition(555, 445, 427, 339, "0", line_width=2, cte_y=35)

    drawer.draw_transition(440, 620, 575, 490, "1", line_width=2, cte_y=35)

    drawer.draw_transition(400, 630, 560, 470, "1", line_width=2, cte_y=-26)

    drawer.draw_state(400, 630, 2.7, radius=45, is_initial=False, label="q4")

    drawer.draw_transition(355, 630, 210, 490, "0", line_width=2, cte_y=35)

    drawer.draw_transition(365, 605, 235, 480, "0", line_width=2, cte_y=-26)

    drawer.draw_filled_circle(545, 150, 7)

    drawer.draw_filled_circle(650, 120, 7)

    drawer.draw_filled_circle(228, 193, 7)

    drawer.draw_filled_circle(448, 287, 7)

    drawer.draw_filled_circle(355, 317, 7)

    drawer.draw_filled_circle(243, 445, 7)

    drawer.draw_filled_circle(565, 417, 7)

    drawer.draw_filled_circle(430, 340, 7)

    drawer.draw_filled_circle(445, 614, 7)

    drawer.draw_filled_circle(557, 473, 7)

    drawer.draw_filled_circle(213, 496, 7)

    drawer.draw_filled_circle(360, 600, 7)

    input("Presiona Enter para cerrar la ventana...")
    drawer.close()