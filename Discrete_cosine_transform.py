import numpy as np
from scipy import fftpack


def dct_2d(mat):
    """二维离散余弦变换"""
    rows = cols = 8
    res = np.zeros((rows, cols))

    for u in range(rows):
        for v in range(cols):
            cu = 1 if u else 0.5 ** 0.5
            cv = 1 if v else 0.5 ** 0.5
            cnt = 0
            for i in range(rows):
                for j in range(cols):
                    cos1 = np.cos((2 * i + 1) * u * np.pi / 16)
                    cos2 = np.cos((2 * j + 1) * v * np.pi / 16)
                    cnt += mat[i, j] * cos1 * cos2
            res[u, v] = 1 / 4 * cu * cv * cnt

    return res


def to_2d(arr, height, width):
    """将一维数组转换为二维数组"""
    res = np.empty((height, width), dtype=float)
    for i in range(height):
        for j in range(width):
            res[i, j] = arr[i * width + j]
    return res


def calculate(arr, height, width):
    """将图片划分成8 * 8的区块并计算DCT"""
    if width % 8 != 0 or height % 8 != 0:
        raise ValueError("图片的长和宽必须是8的倍数")

    rows, cols = height // 8, width // 8

    arr_2d = to_2d(arr, height, width)
    res = np.empty((height, width), dtype=float)

    for i in range(0, height, 8):
        for j in range(0, width, 8):
            # res[i:i+8, j:j+8] = dct_2d(arr_2d[i:i+8, j:j+8] - 128)
            res[i:i+8, j:j+8] = fftpack.dct(fftpack.dct(arr_2d[i:i + 8, j:j + 8] - 128, norm='ortho').T, norm='ortho').T
    return res


def dct(y_arr, cb_arr, cr_arr, height, width):
    y = calculate(y_arr, height, width)
    cb = calculate(cb_arr, height, width)
    cr = calculate(cr_arr, height, width)
    return y, cb, cr
