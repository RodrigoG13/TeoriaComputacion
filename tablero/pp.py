import pandas as pd

def read_and_filter(file_path, n, x, y, chunk_size=10000):
    """
    Lee un archivo en chunks y filtra las filas donde en la columna "n" haya un elemento 
    distinto de x, pero en la columna "n-1" haya un elemento y.
    
    Args:
    - file_path (str): Ruta al archivo.
    - n (int): Índice de la columna n.
    - x: Valor que no debe estar en la columna n.
    - y: Valor que debe estar en la columna n-1.
    - chunk_size (int): Tamaño del chunk para leer el archivo.

    Returns:
    - DataFrame filtrado.
    """
    
    chunk_iter = pd.read_csv(file_path, sep=',', header=None, chunksize=chunk_size)

    # Inicializar un DataFrame vacío para almacenar los datos filtrados
    filtered_df = pd.DataFrame()

    for chunk in chunk_iter:
        mask = (chunk[n] != x) & (chunk[n-1] == y)
        filtered_chunk = chunk[mask]
        filtered_df = pd.concat([filtered_df, filtered_chunk], ignore_index=True)

    return filtered_df

# Ejemplo de uso:
"""file_path = "f1_ganadoras.txt"
n = 3  # Índice de la columna "n"
x = 10  # Valor que no queremos en la columna "n"
y = 7   # Valor que queremos en la columna "n-1"
filtered_data = read_and_filter(file_path, n, x, y)
print(filtered_data.head())"""
print(type((1,1)))

"""1,6,2,7,11,16
1,6,5,10,11,16
1,6,7,10,11,16
1,6,7,12,11,16
1,6,10,7,11,16
1,6,10,15,11,16"""""