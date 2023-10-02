def leer_aux():
    with open('aux_univ.txt', 'r') as archivo:
        for linea in archivo:
            palabras = linea.strip().split(",")
            for palabra in palabras:
                print(f"palabra = {palabra}, type={type(palabra)}")
                yield palabra

for palabra in leer_aux():
    print(f"palabra = {palabra}")

