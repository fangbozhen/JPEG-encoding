import numpy as np


def bin_to_array(src_name, size):
    """读入二进制文件"""

    arr = np.fromfile(src_name, dtype=np.uint8)

    r_arr = g_arr = b_arr = np.empty(size, dtype=int)

    for i in range(size):
        if i % 3 == 0:
            r_arr[i] = arr[i]
        elif i % 3 == 1:
            g_arr[i] = arr[i]
        else:
            b_arr[i] = arr[i]

    return r_arr, g_arr, b_arr

