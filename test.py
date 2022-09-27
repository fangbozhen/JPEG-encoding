import numpy as np

from utils import load_huffman_table


def bin_to_hex(ss):
    """二进制转十六进制"""
    res = ''
    print(len(ss))
    cnt = 1
    for i in range(0, len(ss) - 2, 4):
        x = int(ss[i]) * 8 + int(ss[i+1]) * 4 + int(ss[i+2]) * 2 + int(ss[i+3])
        if x <= 9:
            res = res + str(x)
        else:
            res = res + chr(ord('A') + x - 10)
        if (i + 4) % 8 == 0:
            res = res + ' '
            if cnt % 32 == 0:
                res = res + '\n'
        cnt = cnt + 1

    return res


def main():
    file = open('demo.jpg', 'r')
    file_w = open('out.txt', 'w')
    file_w.write(bin_to_hex(file.read()))


if __name__ == '__main__':
    main()