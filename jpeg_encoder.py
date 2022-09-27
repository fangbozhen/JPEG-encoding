import sys

import numpy as np

from readin import bin_to_array
from rgb_to_ycrcb import RGB_to_YCbCr
from Discrete_cosine_transform import dct_2d
from quantization import quantize
from zigzag import zigzag
from compress import compress
from writeout import write
from settings import DEBUG, height, width


def debug(arr_1, arr_2, arr_3):
    print('Y Matrix:\n', arr_1)
    print('-----------------------')
    print('Cb Matrix:\n', arr_2)
    print('-----------------------')
    print('Cr Matrix:\n', arr_3)
    print('=======================')


def main():

    if len(sys.argv) != 3:
        raise ValueError("请输入二进制文件名及输出的JPEG文件名")

    size = width * height

    src_filename = sys.argv[1]
    jpeg_filename = sys.argv[2]

    R, G, B = bin_to_array(src_filename, size)

    if DEBUG == 1:
        print('RGB data read finished')
        debug(R, G, B)

    Y, Cb, Cr = RGB_to_YCbCr(R, G, B, size)

    Y = Y.reshape([height, width])
    Cb = Cb.reshape([height, width])
    Cr = Cr.reshape([height, width])

    if DEBUG == 1:
        print('RGB convert YCbCr finished')
        debug(Y, Cb, Cr)

    Y -= 128
    Cb -= 128
    Cr -= 128

    blockSum = (height // 8) * (width // 8)
    blockNum = 0

    Y_res , Cb_res, Cr_res = [], [], []
    Y_DC = np.zeros(blockSum, int)
    Cb_DC = np.zeros(blockSum, int)
    Cr_DC = np.zeros(blockSum, int)
    for i in range(0, height, 8):
        for j in range(0, width, 8):
            # 离散余弦变换
            YDct = dct_2d(Y[i:i + 8, j:j + 8])
            CbDct = dct_2d(Cb[i:i + 8, j:j + 8])
            CrDct = dct_2d(Cr[i:i + 8, j:j + 8])

            YQt = quantize(YDct, 'lum')
            CbQt = quantize(CbDct, 'chrom')
            CrQt = quantize(CrDct, 'chrom')

            Y_1d = zigzag(YQt)
            Cb_1d = zigzag(CbQt)
            Cr_1d = zigzag(CrQt)

            if DEBUG == 1:
                print('blockNum:', blockNum)
                debug(YDct, CbDct, CrDct)
                debug(YQt, CbQt, CrQt)
                debug(Y_1d, Cb_1d, Cr_1d)

            Y_DC[blockNum] = Y_1d[0]
            Cb_DC[blockNum] = Cb_1d[0]
            Cr_DC[blockNum] = Cr_1d[0]
            if blockNum != 0:
                Y_1d[0] -= Y_DC[blockNum - 1]
                Cb_1d[0] -= Cb_DC[blockNum - 1]
                Cr_1d[0] -= Cr_DC[blockNum - 1]

            Y_res.append(compress(Y_1d, 'lum'))
            Cb_res.append(compress(Cb_1d, 'chrom'))
            Cr_res.append(compress(Cr_1d, 'chrom'))

            blockNum = blockNum + 1

    write(jpeg_filename, Y_res, Cb_res, Cr_res, height, width)


if __name__ == '__main__':
    main()
