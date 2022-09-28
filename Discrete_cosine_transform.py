import numpy as np
from scipy import fftpack


def dct_2d(mat):
    """二维离散余弦变换"""

    rows = cols = 8
    Mat = np.zeros((rows, cols), dtype=float)
    for i in range(rows):
        for j in range(cols):
            x = 1 if i else 0.5 ** 0.5
            Mat[i][j] = x * np.cos(np.pi * (2 * j + 1) * i / 16)

    res = Mat.dot(Mat.T)
    return res


    # 用scipy包实现的DCT
    # return fftpack.dct(fftpack.dct(mat, norm='ortho').T, norm='ortho').T

    '''
    rows = cols = 8
    res = np.zeros((rows, cols), dtype=float)

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
    '''
