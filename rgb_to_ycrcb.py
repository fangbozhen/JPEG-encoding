import numpy as np


def RGB_to_YCrCb(r_arr, g_arr, b_arr, size):
    """颜色空间转化"""

    y_arr, cr_arr, cb_arr = [], [], []

    for i in range(size):
        y_arr.append(0.299 * r_arr[i] + 0.587 * g_arr[i] + 0.144 * b_arr[i])
        cr_arr.append(0.5 * r_arr[i] - 0.4187 * g_arr[i] + 0.0813 * b_arr[i] + 128)
        cb_arr.append(-0.1687 * r_arr[i] - 0.3313 * g_arr[i] + 0.5 * b_arr[i] + 128)

    return y_arr, cr_arr, cb_arr
