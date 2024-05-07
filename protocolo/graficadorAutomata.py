from graphics import *
import math

class AutomataDrawer:
    """Clase que dibuja los elementos de un autómata de manera gráfica
    """


    def __init__(self, ancho:int , alto: int):
        """Constructor de la clase graficadora de autómatas

        Args:
            ancho (int): Ancho de la ventana donde se dibujará el autómata
            alto (int): Alto de la ventana donde se dibujará el autómata
        """
        self.win = GraphWin("Automata Drawer", ancho, alto)
        self.states = []


    def colocar_titulo(self, titulo: str, pos: tuple =(425, 40), tam_letra: int =24) -> None:
        """Método que añade el título del autómata

        Args:
            titulo (str): título que se colocará en la gráfica
            pos (tuple, optional): Coordenadas donde irá el título. Defaults to (425, 40).
            tam_letra (int, optional): tamaño del título. Defaults to 24.
        """
        titulo = Text(Point(pos[0], pos[1]), titulo)
        titulo.setSize(tam_letra)
        titulo.setStyle("bold")
        titulo.draw(self.win)


    def dibujar_estado(self, x:int, y:int, tam_text:int, radio:int=20, flag_inicial:bool=False, etiqueta:str=None, ancho_linea:int=2) -> None:
        """Método que dibuja un estado del autómata

        Args:
            x (int): Coordenada x del centro del círculo
            y (int): Coordenada y del centro del círculo
            tam_text (int): Tamaño del estado del autómata
            radio (int, optional): Radio del estado. Defaults to 20.
            flag_inicial (bool, optional): Bandera que indica si es estado inicial. Defaults to False.
            etiqueta (str, optional): Nombre del estado. Defaults to None.
            ancho_linea (int, optional): Ancho de la línea del círculo. Defaults to 2.
        """
        estado = Circle(Point(x, y), radio)
        estado.setWidth(ancho_linea)
        estado.setFill("green")
        estado.setOutline("blue")
        estado.draw(self.win)

        if flag_inicial:
            circulo_ini = Circle(Point(x, y), radio - 5)
            circulo_ini.setFill("white")
            circulo_ini.draw(self.win)

        if etiqueta:
            text = Text(Point(x, y), etiqueta)
            text.setSize(int(radio / tam_text))
            text.draw(self.win)

        self.states.append(estado)


    def dibujar_transicion(self, x1:int, y1:int, x2:int, y2:int, etiqueta:str=None, tam_text:int=12, ancho_linea:int=2, cte_x:int=0, cte_y:int=0) -> None:
        """Método que dinuja la linea de transición entre estados

        Args:
            x1 (int): Posicion inicial en x de la línea
            y1 (int): Posicion inicial en y de la línea
            x2 (int): Posicion final en x de la línea
            y2 (int): Posicion final en y de la línea
            etiqueta (str, optional): Etiqueta de la transición. Defaults to None.
            tam_text (int, optional): Tamaño de la etiqueta. Defaults to 12.
            ancho_linea (int, optional): Ancho de la etiqueta. Defaults to 2.
            cte_x (int, optional): Desplazamiento en x de la etiqueta con respecto al centro de la linea. Defaults to 0.
            cte_y (int, optional): Desplazamiento en y de la etiqueta con respecto al centro de la linea. Defaults to 0.
        """
        linea = Line(Point(x1, y1), Point(x2, y2))
        linea.setOutline("black")
        linea.setWidth(ancho_linea) 
        linea.draw(self.win)

        if etiqueta:
            x = (x1 + x2 +cte_x) / 2
            y = (y1 + y2 +cte_y) / 2
            text = Text(Point(x, y), etiqueta)
            text.setSize(tam_text)
            text.draw(self.win)

        
    def dibujar_circulo(self, x:int, y:int, radius:int, color:str="darkblue")->None:
        """Dibuja un círculo para simular 'la llegada' de una transición

        Args:
            x (int): Coordenada en x del centro del cículo
            y (int): Coordenada en y del centro del cículo
            radius (int): Radio del círculo
            color (str, optional): Color del círculo. Defaults to "darkblue".
        """
        circulo = Circle(Point(x, y), radius)
        circulo.setFill(color)
        circulo.setOutline(color)
        circulo.draw(self.win)


    def dibujar_ciclo(self, x:int, y:int, radio:int=20, etiqueta:str=None, flag_hor:bool=False, cte_x:int=0, cte_y:int=0, cte_text:int=0, grosor_linea:int=2)-> None:
        """Método que simula la transición al mismo estado mediante un semicírculo

        Args:
            x (int): Coordenada en x del centro del semicírculo
            y (int): Coordenada en x del centro del semicírculo
            radio (int, optional): Radio del semincírculo. Defaults to 20.
            etiqueta (str, optional): Etiqueta de la transición. Defaults to None.
            flag_hor (bool, optional): Bandera de si el semicírculo será horizontal. Defaults to False.
            cte_x (int, optional): Desplazamiento en x de la etiqueta con respecto al centro del semicirculo. Defaults to 0.
            cte_y (int, optional): Desplazamiento en y de la etiqueta con respecto al centro del semicirculo. Defaults to 0.
            cte_text (int, optional): Ajusta el tamaño del texto. Defaults to 0.
            grosor_linea (int, optional): Grosor de la línea de transición. Defaults to 2.
        """
        num_segments = 20
        if flag_hor:
            angulo_ini = 0
            end_angle = 180
        else:
            angulo_ini = -90
            end_angle = 90
        incremento = (end_angle - angulo_ini) / num_segments

        for i in range(num_segments + 1):
            angulo = angulo_ini + i * incremento
            x1 = x + radio * math.cos(math.radians(angulo))
            y1 = y + radio * math.sin(math.radians(angulo))
            angulo += incremento
            x2 = x + radio * math.cos(math.radians(angulo))
            y2 = y + radio * math.sin(math.radians(angulo))
            line = Line(Point(x1, y1), Point(x2, y2))
            line.setWidth(grosor_linea)
            line.setOutline("black")
            line.draw(self.win)

        if etiqueta:
            if flag_hor:
                text = Text(Point(x+cte_x, y+cte_y), etiqueta)
                text.setSize(int(radio / 2+cte_text))
                text.draw(self.win)
            else:
                text = Text(Point(x+cte_x, y+cte_y - radio * 0.5), etiqueta)
                text.setSize(int(radio / 2+cte_text))
                text.draw(self.win)


    def clear(self)-> None:
        """Método que borra todos los elementos dibujados en la ventana
        """
        for state in self.states:
            state.undraw()
        self.states = []
        self.win.update()


    def close(self):
        """Método que cierra la ventana de la gráfica
        """
        self.win.close()