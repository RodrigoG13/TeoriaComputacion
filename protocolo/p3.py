import random
import os

def eliminar_archs(nombre_arch):
    """Función que elimina un archivo si existe en el directorio

    Args:
        nombre_arch (str): Nombre del archivo que deseas eliminar
    """

    archivo1 = nombre_arch
    if os.path.exists(archivo1):
        os.remove(archivo1)


def automata_paridad(palabra: str) -> int:
    transiciones = {
        (0, '0'): 1, (0, '1'): 3,
        (1, '0'): 0, (1, '1'): 2,
        (2, '0'): 3, (2, '1'): 1,
        (3, '0'): 2, (3, '1'): 0
    }
    
    estado = 0
    for caracter in palabra:
        estado = transiciones[(estado, caracter)]
    return estado

def generar_palabras(num_palabras: int, long_cadena:int) -> list:
    return [''.join([str(random.randint(0, 1)) for _ in range(long_cadena)]) for _ in range(num_palabras)]

def filtrar_palabras(palabras:list) -> tuple:
    aceptadas = []
    rechazadas = []
    for palabra in palabras:
        if automata_paridad(palabra) == 0:
            aceptadas.append(palabra)
        else:
            rechazadas.append(palabra)
    return aceptadas, rechazadas

def escribir_en_archivo(nombre_arch: str, datos:list) -> None:
    if datos:
        with open(nombre_arch, "a+") as archivo:
            archivo.write("\n ".join(datos))
            archivo.write("\n ")

if __name__ == "__main__":
    nombre_aceptadas = "aceptadas.txt"
    nombre_rechazadas = "rechazadas.txt"

    long_cadena = 64
    num_palabras = 1000000
    num_act = 0

    os.system('clear')
    print("\t\t\t***PROTOCOLO***\n")

    eliminar_archs(nombre_aceptadas)
    eliminar_archs(nombre_rechazadas)

    while random.randint(0,1):
        print("Protocolo en ejecución")
        palabras = generar_palabras(num_palabras, long_cadena)
        print("\t>> Esperando ...")
        aceptadas, rechazadas = filtrar_palabras(palabras)
        escribir_en_archivo(nombre_aceptadas, aceptadas)
        escribir_en_archivo(nombre_rechazadas, rechazadas)
        print("Palabras clasificadas\n")
        num_act += 1
    
    if num_act != 0:
        print(f"Numero de ejecuciones del protocolo: {num_act}\n")
        print(f"Puedes consultar la clasificación de palabras en {nombre_aceptadas} & {nombre_rechazadas}")
    else:
        print("El protocolo no se ha podido ejecutar, inténtalo nuevamente.")

    print("No")
