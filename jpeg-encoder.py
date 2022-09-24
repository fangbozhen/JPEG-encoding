import sys

from readin import bin_to_array
from rgb_to_ycrcb import RGB_to_YCrCb


def main():

    if len(sys.argv) != 3:
        print("You must input src filename and jpeg filename")
        return

    width = 256
    height = 256
    channel = 3

    size = width * height

    src_filename = sys.argv[1]
    jpeg_filename = sys.argv[2]

    R, G, B = bin_to_array(src_filename, size)
    RGB_to_YCrCb(R, G, B, size)


if __name__ == '__main__':
    main()
