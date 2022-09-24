import numpy as np

from utils import load_quantization_table


def calc(arr, q, rows, cols):
    res = np.empty((rows, cols), dtype=int)
    for i in range(0, rows, 8):
        for j in range(0, cols, 8):
            block = arr[i:i+8, j:j+8]
            res[i:i+8, j:j+8] = (block / q).round().astype(int)
    return res


def quantize(y_arr, cr_arr, cb_arr, height, width):
    q = load_quantization_table('lum')
    y_res = calc(y_arr, q, height, width)
    q = load_quantization_table('chrom')
    cr_res = calc(cr_arr, q, height, width)
    cb_res = calc(cb_arr, q, height, width)
    return y_res, cr_res, cb_res
