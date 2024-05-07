
'''
                                    ***TDA - PILA***
* @author: Rodrigo Gerardo Trejo Arriaga
* Grupo: 2BM1
* Carrera: Ingeniería en Inteligencia Artificial
* Fecha de Última modificación: 28/03/2022
'''
#  -------------------------------------------------------------------------------------------------
# Tabla de errores

"""
_______________________________________________________________
                Error                |          Valor
Sin errores                          |                   0              
No hay elementos en la cima          |                  -1
Pila vaciía                          |                  -2
_______________________________________________________________

"""
stack_error = 0

#  --------------------------------------------------------------------------------------------------------------------
# CLASES

class StackNode:
    """
    Clase Nodo de Pila
    Inicializa sus atributos inicialmente apuntado a None
    """
    data, previous = None, None


class Stack:
    """
    Clase Stack (Pila)
    Inicializa sus atributos apuntando a None y la cima en 0
    """
    def __init__(self):
        """Crea una pila vacía"""
        self.top = None
        self.cursor_stack = 0


    def stack_push(self, dato):
        global stack_error
        """Apila un elemento en la cima de la pila
        :param dato: (generico) Dato que se apilará
        :return Vacío: El apilamiento se realiza de manera interna"""
        node = StackNode()
        node.data = dato
        node.previous = self.top
        self.top = node
        self.cursor_stack += 1
        stack_error = 0


    def stack_pop(self):
        global stack_error 
        """Desapila el elemento encontrado en la cima de la pila
        :return top_data: Dato que se encuentra en la cima de la pila"""
        if not self.is_empty():
            top_data = self.top.data
            self.top = self.top.previous
            self.cursor_stack -= 1
            stack_error = 0
            return top_data
        else:
            print("No es posible desapilar porque la pila está vacía")
            stack_error = -2
        

    def is_empty(self):
        """Informa si la pila está vacía o no"""
        global stack_error
        stack_error = 0
        return self.top == None


    def empty(self):
        """Vacía la pila"""
        global stack_error
        if not self.is_empty():
            while not self.is_empty():
                dato = self.stack_pop
                print(dato)
            print(f"La pila se ha vaciado: {self.is_empty()}")
            stack_error = 0
        else:
            print("No es posible vaciar la pila porque ya está vacía XD")
            stack_error = -2
    

    def read_top(self):
        """Lee el dato existente en la cima"""
        global stack_error
        if self.top is not None:
            stack_error = 0
            return self.top.data
        else:
            print("No es posible leer la cima porque no hay elementos en la pila")
            stack_error = -1
            return None


    def stack_size(self):
        """Indica el tamaño de la pila"""
        global stack_error
        stack_error = 0
        return self.cursor_stack


    def read_stack(self):
        """Lee el contenido de una pila, sin perder información"""
        global stack_error
        if not self.is_empty():
            stack_aux = Stack()
            while not self.is_empty():
                dato = self.stack_pop()
                print(dato)
                stack_aux.stack_push(dato)
            while not stack_aux.is_empty():
                dato = stack_aux.stack_pop()
                self.stack_push(dato)
            stack_error = 0
        else:
            print("No es posible leer la pila porque está vacía")
            stack_error = -2


    def read_stack2(self):
        """Lee el contenido de una pila, sin perder información"""
        global stack_error
        contenido = []
        if not self.is_empty():
            stack_aux = Stack()
            while not self.is_empty():
                dato = self.stack_pop()
                contenido.append(dato)
                stack_aux.stack_push(dato)
            while not stack_aux.is_empty():
                dato = stack_aux.stack_pop()
                self.stack_push(dato)
            stack_error = 0
        else:
            print("No es posible leer la pila porque está vacía")
            stack_error = -2
        return contenido

    
    def is_full(self, size):
        """
        Informa si la pila está llena
        :return cursor == size: (Bool) Estado de la lista -> Llena (True), otro caso (False)
        """
        global stack_error
        stack_error = 0
        return self.cursor_stack == size