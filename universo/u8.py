import os
import time
import random


def eliminar_archs(nombre_arch):
    archivo1 = nombre_arch
    if os.path.exists(archivo1):
        os.remove(archivo1)


class ParticionUniverso:
    def __init__(self, tam_particion: int, nombre_arch="particionUniverso", nombre_aux="aux_univ.txt") -> None:
        self.nombre_arch = nombre_arch
        self.tam_particion = tam_particion
        self.universo = ["0", "1"]
        self.archivo_universo = open(f"{nombre_arch}.txt", "a+", encoding="utf-8")
        self.aux_universo = open(nombre_aux, "a+", encoding="utf-8")


    def escribir_en_archivo(self, datos):
        self.archivo_universo.write(", ".join(datos))
        self.archivo_universo.write(", ")


    def leer_linea_n(self, n):
        self.aux_universo.seek(0)
        contador = 0
        for linea in self.aux_universo:
            contador += 1
            if contador == n:
                return linea.strip().split(",")

    def generar_particion_universo(self) -> None:
        long = 1
        datos_para_escribir = []
        conta_llenado = 0
        leidas = 0
        kill = False
        lim_escritura = 16777216
        while long < self.tam_particion:
            nueva_universo = []
            for palabra in self.universo:
                nueva_universo.extend([palabra + "0", palabra + "1"])
                datos_para_escribir.extend([palabra + "0", palabra + "1"])

                if len(datos_para_escribir) >= lim_escritura:
                    self.escribir_en_archivo(datos_para_escribir)
                    del datos_para_escribir
                    datos_para_escribir = []
                
                if len(nueva_universo) == lim_escritura:
                    self.aux_universo.write(",".join(nueva_universo))
                    self.aux_universo.write("\n")
                    conta_llenado += 1
                    nueva_universo = []

                if palabra.count("1") + 1 == self.tam_particion:
                    kill = True

            if kill:
                break

            if conta_llenado == 0:
                self.universo = nueva_universo
                long += 1

            else:
                leidas += 1
                self.universo = self.leer_linea_n(leidas)

                if conta_llenado == leidas:
                    long += 1
                    print(f"long = {long}")
                    leidas = 0
                    conta_llenado = 0
                    with open("aux_univ.txt", "w") as archivo:
                        pass

        if datos_para_escribir:
            self.escribir_en_archivo(datos_para_escribir)

if __name__ == "__main__":
    os.system('clear')
    eliminar_archs("particionUniverso.txt")
    eliminar_archs("aux_univ.txt")

    print("\t\t\t***PARTICIÓN DEL UNIVERSO***\n")
    print("Este programa generará una partición del alfabeto binario, según una longitud 'n'.\n")
    modo = input("\t>>Deseas que 'n' se elija de manera automática o manual? [a/m]: ")
    while modo.lower() != "a" and modo.lower != "m":
        print("Modo inválido, ingreséselo nuevamente para continuar")
        modo = input("\t>>Deseas que 'n' se elija de manera automática o manual? [a/m]: ")
    
    match modo:
        case "a":
            n = random.randint(0, 28)
            print(f"Se ha elegido un n={n}")
        case _:
            n = int(input("Ingresa un n ∈ [0,28]: "))

    print("Se está ejecutando la partición, espera un momento.")
    inicio = time.perf_counter()
    test = ParticionUniverso(n)
    test.generar_particion_universo()
    fin = time.perf_counter()
    tiempo_transcurrido = fin - inicio
    eliminar_archs("aux_univ.txt")
    print("Listo, puedes consultar la partición en el archivo: 'particionUniverso.txt'.")
    print(f"Tiempo de ejecución : {tiempo_transcurrido:.2f} segundos")