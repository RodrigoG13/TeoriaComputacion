import os
import time


class ParticionUniverso:
    """ Clase que crea una partición del universo de las palabras del alfabeto binario
    """

    def __init__(self, tam_particion: int, nombre_arch="particionUniverso") -> None:
        """Constructor de la clase ParticionUniverso

        Args:
            tam_particion (int): Longitud máxima de la palabra que se construirá
            nombre_arch (str, optional): Nombre del archivo donde se almacenan las palabras. Defaults to "particionUniverso".
        """
        self.nombre_arch = nombre_arch
        self.arch_univ = open(f"{nombre_arch}URIAS.txt", "a+", encoding="utf-8")
        self.tam_particion = tam_particion
        self.arch_indices = open(f"indicesPyURIAS.txt", "a+")

    
    def obtener_datos_conjuntos(self) -> tuple:
        """ Método que verifica si existen datos en el archivo y otorga los índices de los últimos datos
            almacenados

        Returns:
            tuple: Tupla con la longitud de la palabra, índice de inicio y fin del subconjunto
        """
        if os.path.getsize("indicesPyURIAS.txt") == 0:
            self.arch_univ.write("Σ = {ε, 0, 1, ")
            self.arch_indices.write("1,10,13\n")
            return 1, 10, 13
        
        else:
            self.arch_indices.seek(0) 
            lineas = self.arch_indices.readlines()
            self.arch_indices.seek(0, os.SEEK_END)
            lineas = lineas[-1].strip().split(",")
            return int(lineas[0]), int(lineas[1]), int(lineas[2])
        
    
    def generar_particion_universo(self) -> None:

        long, inicio, fin = self.obtener_datos_conjuntos()
        while long < self.tam_particion:
            tupla = ()
            aux_movil = inicio
            self.arch_univ.seek(aux_movil)
            caracter = "0"
            while caracter.count("0") > 0:
                caracter = self.arch_univ.read(long)
                #self.arch_univ.write(f"{caracter}0, {caracter}1, ")
                tupla = tupla + (f"{caracter}0, ", f"{caracter}1, ")
                aux_movil += (long + 2)
                self.arch_univ.seek(aux_movil)
            long += 1
            self.arch_univ.write("".join(tupla))
            self.arch_univ.seek(0, 2)
            indice_final = self.arch_univ.tell()
            inicio = fin+3
            fin = indice_final-3
            self.arch_indices.write(f"{long},{inicio},{fin}\n")
            print(f"long = {long}")


if __name__ == "__main__":
    os.system('clear')
    inicio = time.perf_counter()
    n = 20
    test = ParticionUniverso(n)
    test.generar_particion_universo()
    fin = time.perf_counter()
    tiempo_transcurrido = fin - inicio
    print(f"Tiempo de ejecución: {tiempo_transcurrido:.5f} segundos")