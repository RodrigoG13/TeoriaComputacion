def create_mask_3x3(matrix, center_row, center_col):
    mask = []
    for i in range(center_row - 1, center_row + 2):
        row = []
        for j in range(center_col - 1, center_col + 2):
            if 0 <= i < len(matrix) and 0 <= j < len(matrix[0]):
                row.append(matrix[i][j])
            else:
                row.append((None, None, None))
        mask.append(tuple(row))
    return tuple(mask)


if __name__ == "__main__":

    tablero = (
        (("b", False, 1), ("r", False, 2), ("b", False, 3), ("r", False, 4)),
        (("r", False, 5), ("b", False, 6), ("r", False, 7), ("b", False, 8)),
        (("b", False, 9), ("r", False, 10), ("b", False, 11), ("r", False, 12)),
        (("r", False, 13), ("b", False, 14), ("r", False, 15), ("b", False, 16))
    )

    indices = {1: (0,0), 2: (0,1), 3: (0,2), 4: (0,3),
               5: (1,0), 6: (1,1), 7: (1,2), 8: (1,3),
               9: (2,0), 10: (2,1), 11: (2,2), 12: (2,3),
               13: (4,0), 14: (4,1), 15: (4,2), 16: (4,3)}

    # Especifica la fila y columna central deseada
    fila_central = 0
    columna_central = 0

    mascara = create_mask_3x3(tablero, fila_central, columna_central)

    # Imprime la máscara resultante
    for fila in mascara:
        print(fila)





