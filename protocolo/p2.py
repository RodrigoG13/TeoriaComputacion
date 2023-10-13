import random
import os
import time

def automata_paridad(palabra: str) -> int:
    """Función que pasa una palabra por el autómata de paridad y devuelve el estado en que se
        quedó

    Args:
        palabra (str): Palabra que se testeará

    Returns:
        int: Estado en el que se quedó el autómata
    """

    estado = 0
    for caracter in palabra:
        match estado:
            case 0:
                if caracter == "0":
                    estado = 1
                else:
                    estado = 3
     
            case 1:
                if caracter == "0":
                    estado = 0
                else:
                    estado = 2

            case 2:
                if caracter == "0":
                    estado = 3
                else:
                    estado = 1

            case 3:
                if caracter == "0":
                    estado = 2
                else:
                    estado = 0
        continue
    return estado


def generar_palabras(num_palabras: int, long_cadena:int) -> list:
    """Función que genera una lista de palabras binarias con longitud y numero de caracteres especificados

    Args:
        num_palabras (int): Número de palabras que tendrá la lista
        long_cadena (int): Longitud de cada cadena binaria

    Returns:
        list: Lista de palabras binarias
    """

    palabras = [''.join([str(random.randint(0, 1)) for _ in range(long_cadena)]) for _ in range(num_palabras)]
    return palabras


def filtrar_palabras(palabras:list) -> tuple:
    """Función que clasifica las palabras en rechazadas o aceptadas, según el autómata de paridad

    Args:
        palabras (list): Lista de palabras a clasificar

    Returns:
        tuple: Palabras aceptadas y rechazadas por el algoritmo
    """

    aceptadas = []
    rechazadas = []
    while len(palabras):
        edo = automata_paridad(palabras[0])

        if edo == 0:
            aceptadas.append(palabras.pop(0))
                
        else:
            rechazadas.append(palabras.pop(0))
    return aceptadas, rechazadas


def escribir_en_archivo(nombre_arch: str, datos:list) -> None:
    """Función que escribe datos en el archivo de particion de universo

    Args:
        datos (list): Datos pertenecientes a la partición
    """
    
    if len(datos) != 0:
        with open(nombre_arch, "a+") as archivo:
            archivo.write(", ".join(datos))
            archivo.write(", ")


if __name__ == "__main__":

    nombre_aceptadas = "aceptadas.txt"
    nombre_rechazadas = "rechazadas.txt"

    long_cadena = 64
    num_palabras = 1000000

    num_act = 0
    os.system('clear')
    print("\t\t\t***PROTOCOLO***\n")

    while random.randint(0,1):
        print("Protocolo en ejecución")
        palabras = generar_palabras(num_palabras, long_cadena)
        print("\t>> Esperando ...")
        time.sleep(2)
        aceptadas, rechazadas = filtrar_palabras(palabras)
        escribir_en_archivo(nombre_aceptadas, aceptadas)
        escribir_en_archivo(nombre_rechazadas, rechazadas)
        print("Palabras clasificadas\n")
        num_act += 1
        del palabras
        del aceptadas
        del rechazadas
    
    if num_act != 0:
        print(f"Numero de ejecuciones del protocolo: {num_act}\n")
        print(f"Puedes consultar la clasificación de palabras en {nombre_aceptadas} & {nombre_rechazadas}")
    
    else:
        print("El protocolo no se ha podido ejecutar, inténtalo nuevamente.")

    print("No")