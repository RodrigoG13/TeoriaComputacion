from stack_tda import *

pdatos = Stack()
ppar = Stack()
pimpar = Stack()
dato = int(input("Ingrese un número, 0 para salir: "))

while dato != 0:
    pdatos.stack_push(dato)
    dato = int(input("Ingrese un número, 0 para salir: "))

print("Se leerá la pila de datos")
u = pdatos.read_stack2()
print(u)

while not pdatos.is_empty():
    dato = pdatos.stack_pop()
    if dato % 2 == 0:
        ppar.stack_push(dato)
    else:
        pimpar.stack_push(dato)

print("Datos pares")
while not ppar.is_empty():
    dato = ppar.stack_pop()
    print(dato)

print("\nDatos impares")
while not pimpar.is_empty():
    dato = pimpar.stack_pop()
    print(dato)