import numpy as np
from math import log

from utils import load_huffman_table
from settings import DEBUG


def huffman_ac(typ, x, y):
    """交流系数转化为Huffman"""
    t = load_huffman_table(typ, 'AC')
    # 处理 EOB 和 ZRL
    if x != 0 and x != 15:
        y = y - 1
    return t[x][y]


def huffman_dc(typ, x):
    """直流系数转化为Huffman"""
    t = load_huffman_table(typ, 'DC')
    return t[x]


def get_bin(val, length):

    if length == 0:
        return ''

    res = ''
    while val:
        res += str(val % 2)
        val = val // 2
    for i in range(length - len(res)):
        res += '0'
    res = res[::-1]

    return res


def solve_block(arr, typ):
    cnt = 64
    res = ''

    # 处理直流系数
    length = int(log(abs(arr[0]), 2)) + 1 if arr[0] else 0
    if arr[0] < 0:
        dis = (2 ** length) - 1 - abs(arr[0])
    else:
        dis = arr[0]
    res += huffman_dc(typ, length)
    res += get_bin(dis, length)

    if DEBUG == 1:
        print('type:', typ)
        print('DC (length, value) = ({}, {}),  encode = [{}], [{}]'.format(
                length, arr[0], huffman_dc(typ, length), get_bin(dis, length)
        ))

    # 处理交流系数
    i = 1
    while i < cnt - 1:
        if arr[i] == 0:
            st = i
            while i < cnt - 1 and arr[i] == 0:
                i = i + 1
            # 处理 EOB
            if i == cnt - 1:
                res += huffman_ac(typ, 0, 0)

                if DEBUG == 1:
                    print('EOB: {}'.format(huffman_ac(typ, 0, 0)))

                return res
            if i - st > 15:
                i = st + 15
            x = i - st
        else:
            x = 0

        y = int(log(abs(arr[i]), 2)) + 1 if arr[i] else 0
        if arr[i] < 0:
            dis = 2 ** y - 1 - abs(arr[i])
        else:
            dis = arr[i]
        res += huffman_ac(typ, x, y)
        res += get_bin(dis, y)

        if DEBUG == 1:
            print('AC value = {}, (run, size) = ({}, {}), encode = [{}], [{}]'.format(
                arr[i], x, y, huffman_ac(typ, x, y), get_bin(dis, y)
            ))

        i = i + 1

    if DEBUG == 1:
        print('======================')

    return res


def calc(arr, rows, cols, typ):
    cnt = (rows // 8) * (cols // 8)
    res = []
    for i in range(cnt):
        res.append(solve_block(arr[i], typ))

    return res


def compress(y_arr, cb_arr, cr_arr, height, width):
    y_res = calc(y_arr, height, width, 'lum')
    cb_res = calc(cb_arr, height, width, 'chrom')
    cr_res = calc(cr_arr, height, width, 'chrom')
    return y_res, cb_res, cr_res


if __name__ == '__main__':
    pass
