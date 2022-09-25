import numpy as np

from utils import load_zigzag_table


def block_to_zigzag(arr):
    rows = cols = 8
    table = load_zigzag_table()
    res = np.empty(rows * cols, dtype=int)

    for i in range(rows):
        for j in range(cols):
            res[table[i, j] - 1] = arr[i, j]

    return res


def calc(arr, height, width):
    cnt = (height // 8) * (width // 8)
    res = np.empty((cnt, 8 * 8), dtype=int)
    k = 0
    for i in range(0, height, 8):
        for j in range(0, width, 8):
            res[k] = block_to_zigzag(arr[i:i+8, j:j+8])
            k = k + 1

    for i in range(cnt - 1, 0, -1):
        res[i, 0] -= res[i - 1, 0]

    return res


def zigzag(y_arr, cr_arr, cb_arr, height, width):
    y_res = calc(y_arr, height, width)
    cr_res = calc(cr_arr, height, width)
    cb_res = calc(cb_arr, height, width)
    return y_res, cr_res, cb_res
