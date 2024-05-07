import openpyxl

def es_palabra_clave(palabra, transiciones):
    estado_actual = 'q0'
    historia_temp = []
    for caracter in palabra:
        # Si el carácter no es alfabético, se reinicia al estado q0
        if not caracter.isalpha():
            estado_actual = 'q0'
            continue
        
        # Procesa el carácter con las transiciones del DFA
        if (estado_actual, caracter) in transiciones:
            estado_siguiente = transiciones[(estado_actual, caracter)]
            historia_temp.append(f"Carácter leído: '{caracter}'\tEstado actual: {estado_actual}\tEstado siguiente: {estado_siguiente}")
            estado_actual = estado_siguiente
        else:
            return False, []
    return estado_actual in estados_finales, historia_temp

def identificar_palabras_clave_en_texto(archivo, transiciones):
    historia = []  # Almacenar la historia del proceso
    palabras_encontradas = {}  # Almacenar palabras reservadas y sus posiciones
    detalles_palabras = []  # Almacenar detalles de las palabras encontradas

    with open(archivo, 'r') as archivo_texto:
        for num_linea, linea in enumerate(archivo_texto, start=1):
            palabras = linea.split()
            for num_palabra, palabra in enumerate(palabras, start=1):
                es_clave, historia_temp = es_palabra_clave(palabra, transiciones)
                historia.extend(historia_temp)
                if es_clave:
                    detalles = f"Palabra clave ANSI C encontrada: {palabra} (línea {num_linea}, palabra {num_palabra})"
                    print(detalles)
                    detalles_palabras.append(detalles)
                    palabras_encontradas[palabra] = palabras_encontradas.get(palabra, 0) + 1

    # Guarda la historia del proceso en un archivo
    with open('historia_del_proceso.txt', 'w') as historia_archivo:
        historia_archivo.write('\n'.join(historia))

    # Guarda detalles de palabras clave encontradas
    with open('palabras_encontradas.txt', 'w') as archivo_palabras:
        for detalle in detalles_palabras:
            archivo_palabras.write(detalle + '\n')

    # Imprime el resumen de palabras reservadas encontradas
    print("\nResumen de palabras reservadas encontradas:")
    for palabra, conteo in palabras_encontradas.items():
        print(f"{palabra}: {conteo} veces")
