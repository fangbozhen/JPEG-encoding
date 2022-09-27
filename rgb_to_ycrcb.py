import numpy as np


def RGB_to_YCbCr(r_arr, g_arr, b_arr, size):
    """颜色空间转化"""

    y_arr, cb_arr, cr_arr = [], [], []

    for i in range(size):
        # y_arr.append(int(0.257 * r_arr[i] + 0.564 * g_arr[i] + 0.098 * b_arr[i] + 16))
        # cb_arr.append(int(-0.148 * r_arr[i] - 0.291 * g_arr[i] + 0.439 * b_arr[i] + 128))
        # cr_arr.append(int(0.439 * r_arr[i] - 0.368 * g_arr[i] - 0.071 * b_arr[i] + 128))
        y_arr.append(int(float(0.299 * r_arr[i] + 0.587 * g_arr[i] + 0.114 * b_arr[i])))
        cb_arr.append(int(float(-0.1687 * r_arr[i] - 0.3313 * g_arr[i] + 0.5 * b_arr[i]) + 128))
        cr_arr.append(int(float(0.5 * r_arr[i] - 0.4187 * g_arr[i] - 0.0813 * b_arr[i]) + 128))

    return np.array(y_arr), np.array(cb_arr), np.array(cr_arr)
