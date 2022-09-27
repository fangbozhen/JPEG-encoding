import sys

from readin import bin_to_array
from rgb_to_ycrcb import RGB_to_YCbCr
from Discrete_cosine_transform import dct
from quantization import quantize
from zigzag import zigzag
from compress import compress
from writeout import write
from settings import DEBUG, height, width


def debug(arr_1, arr_2, arr_3):
    print('Y/R Matrix:\n', arr_1)
    print('-----------------------')
    print('Cb/G Matrix:\n', arr_2)
    print('-----------------------')
    print('Cr/B Matrix:\n', arr_3)
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

    if DEBUG == 1:
        print('RGB convert YCbCr finished')
        debug(Y, Cb, Cr)

    Y_2d, Cb_2d, Cr_2d = dct(Y, Cb, Cr, height, width)

    if DEBUG == 1:
        print('dct finished')
        debug(Y_2d, Cb_2d, Cr_2d)

    Y_qt, Cb_qt, Cr_qt = quantize(Y_2d, Cb_2d, Cr_2d, height, width)

    if DEBUG == 1:
        print('quantize finished')
        debug(Y_qt, Cb_qt, Cr_qt)

    Y_zz, Cb_zz, Cr_zz = zigzag(Y_qt, Cb_qt, Cr_qt, height, width)

    if DEBUG == 1:
        print('zigzag finished')
        debug(Y_zz, Cb_zz, Cr_zz)

    Y_res, Cb_res, Cr_res = compress(Y_zz, Cb_zz, Cr_zz, height, width)

    if DEBUG == 1:
        print('compress finished')
        debug(Y_res, Cb_res, Cr_res)

    write(jpeg_filename, Y_res, Cb_res, Cr_res, height, width)


if __name__ == '__main__':
    main()
