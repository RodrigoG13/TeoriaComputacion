import os
import time

class ParticionUniverso:
    def __init__(self, tam_particion: int, nombre_arch="particionUniverso") -> None:
        self.nombre_arch = nombre_arch
        self.tam_particion = tam_particion
        self.universo = open(f"aux_univ.txt", "a+", encoding="utf-8")
        self.universo.write("0,1\n")
        self.archivo_universo = open(f"{nombre_arch}.txt", "a+", encoding="utf-8")

    
    def leer_aux(self):
        with open('aux_univ.txt', 'r') as archivo:
            for linea in archivo:
                palabras = linea.strip().split(",")
                for palabra in palabras:
                    yield palabra



    def escribir_en_archivo(self, datos):
        self.archivo_universo.write(", ".join(datos))
        self.archivo_universo.write(", ")


    def eliminar_contenido(self, nombre_archivo):
        with open(nombre_archivo, "w") as archivo:
            # No necesitas escribir nada dentro, simplemente abrirlo y cerrarlo lo limpiará
            pass

    def generar_particion_universo(self) -> None:
        long = 1
        datos_para_escribir = []
        kill_flag = False
        while long < self.tam_particion:
            nueva_universo = []

            for palabra in self.leer_aux():
                print(f"{palabra}, type = {type(palabra)}")
                nueva_universo.extend([palabra + "0", palabra + "1"])
                datos_para_escribir.extend([palabra + "0", palabra + "1"])
                if len(datos_para_escribir) >= 3:  
                    self.escribir_en_archivo(datos_para_escribir)
                    del datos_para_escribir
                    datos_para_escribir = []
                    print(nueva_universo)
                    print(datos_para_escribir)
                    

            #self.universo = nueva_universo
            self.eliminar_contenido("aux_univ.txt")
            long += 1
            print(f"long = {long}")


        # Escribir cualquier dato restante en el archivo
        if datos_para_escribir:
            self.escribir_en_archivo(datos_para_escribir)

if __name__ == "__main__":
    os.system('clear')
    inicio = time.perf_counter()
    n = 3
    test = ParticionUniverso(n)
    test.generar_particion_universo()
    fin = time.perf_counter()
    tiempo_transcurrido = fin - inicio
    print(f"Tiempo de ejecución: {tiempo_transcurrido:.5f} segundos")
