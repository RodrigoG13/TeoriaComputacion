# Abre el archivo en modo lectura
with open('particionUniverso.txt', 'r') as archivo:
    # Obtiene el tamaño del archivo
    archivo.seek(0, 2)  # Coloca el cursor al final del archivo
    tamaño = archivo.tell()
    
    # Retrocede 30 caracteres desde el final (o menos si el archivo tiene menos de 30 caracteres)
    archivo.seek(max(tamaño - 30, 0))
    
    # Lee los últimos 30 caracteres
    últimos_30_caracteres = archivo.read()

print(últimos_30_caracteres)
