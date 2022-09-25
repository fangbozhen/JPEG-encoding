import sys

from readin import bin_to_array
from rgb_to_ycrcb import RGB_to_YCrCb
from Discrete_cosine_transform import dct
from quantization import quantize
from zigzag import zigzag


def main():

    if len(sys.argv) != 3:
        raise ValueError("请输入二进制文件名及输出的JPEG文件名")

    width = 256
    height = 256
    channel = 3

    size = width * height

    src_filename = sys.argv[1]
    jpeg_filename = sys.argv[2]

    R, G, B = bin_to_array(src_filename, size)
    Y, Cr, Cb = RGB_to_YCrCb(R, G, B, size)
    Y_2d, Cr_2d, Cb_2d = dct(Y, Cr, Cb, height, width)
    Y_qt, Cr_qt, Cb_qt = quantize(Y_2d, Cr_2d, Cb_2d, height, width)
    Y_zz, Cr_zz, Cb_zz = zigzag(Y_qt, Cr_qt, Cb_qt, height, width)



if __name__ == '__main__':
    main()
