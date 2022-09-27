import numpy as np


def bin_to_array(src_name, size):
    """读入二进制文件"""

    arr = np.fromfile(src_name, dtype=np.uint8)

    r_arr, g_arr, b_arr = [], [], []

    for i in range(size * 3):
        if i % 3 == 0:
            r_arr.append(arr[i])
        elif i % 3 == 1:
            g_arr.append(arr[i])
        else:
            b_arr.append(arr[i])

    return np.array(r_arr), np.array(g_arr), np.array(b_arr)

