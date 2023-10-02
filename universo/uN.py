import os
import time

class ParticionUniverso:
    def __init__(self, tam_particion: int, nombre_arch="particionUniverso") -> None:
        self.nombre_arch = nombre_arch
        self.tam_particion = tam_particion
        self.universo = ["0", "1"]
        self.archivo_universo = open(f"{nombre_arch}.txt", "a+", encoding="utf-8")

    def escribir_en_archivo(self, datos):
        self.archivo_universo.write(", ".join(datos))
        self.archivo_universo.write(", ")

    def generar_particion_universo(self) -> None:
        long = 1
        datos_para_escribir = []
        while long < self.tam_particion:
            nueva_universo = []
            for palabra in self.universo:
                nueva_universo.extend([palabra + "0", palabra + "1"])
                datos_para_escribir.extend([palabra + "0", palabra + "1"])
                # Escribir en el archivo en lotes para evitar problemas de memoria
                if len(datos_para_escribir) >= 1048576:  # Puedes ajustar este número según tus necesidades
                    self.escribir_en_archivo(datos_para_escribir)
                    del datos_para_escribir
                    datos_para_escribir = []
                    #print(f"cosa")
            self.universo = nueva_universo
            long += 1
            print(f"long = {long}")


        # Escribir cualquier dato restante en el archivo
        if datos_para_escribir:
            self.escribir_en_archivo(datos_para_escribir)

if __name__ == "__main__":
    os.system('clear')
    inicio = time.perf_counter()
    n = 26
    test = ParticionUniverso(n)
    test.generar_particion_universo()
    fin = time.perf_counter()
    tiempo_transcurrido = fin - inicio
    print(f"Tiempo de ejecución: {tiempo_transcurrido:.5f} segundos")
