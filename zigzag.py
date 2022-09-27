import numpy as np

from utils import load_zigzag_table


def zigzag(arr):
    rows = cols = 8
    table = load_zigzag_table()
    res = np.empty(rows * cols, dtype=int)

    for i in range(rows):
        for j in range(cols):
            res[table[i, j] - 1] = arr[i, j]

    return res
