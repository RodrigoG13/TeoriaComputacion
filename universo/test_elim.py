def leer_linea_n(nombre_archivo, n):
    try:
        with open(nombre_archivo, 'r') as archivo:
            contador = 0
            for linea in archivo:
                contador += 1
                if contador == n:
                    return linea.strip().split(",")  # Strip para eliminar el salto de línea al final
    except FileNotFoundError:
        return f"El archivo '{nombre_archivo}' no existe."
    except Exception as e:
        return f"Se produjo un error: {str(e)}"

n = 4  # Reemplaza esto con el valor de la línea que deseas leer
nombre_archivo = "jambas.txt"  # Reemplaza con el nombre de tu archivo

linea = leer_linea_n(nombre_archivo, n)

if linea is not None:
    print(f"Línea {n}: {linea}")
else:
    print("No se pudo leer la línea especificada.")
