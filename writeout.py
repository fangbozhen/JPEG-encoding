import numpy as np

from utils import load_quantization_table, load_huffman_table


def hex_to_bin(ss):
    """十六进制转二进制"""
    res = []
    cnt = 0
    y = 0
    for i in range(len(ss)):
        if ss[i] == ' ':
            continue
        if ss[i] <= '9':
            x = int(ss[i])
        else:
            x = ord(ss[i]) - ord('A') + 10
        cnt = cnt + 1
        if cnt % 2 == 0:
            res.append(y * 16 + x)
        else:
            y = x
    res = bytes(res)
    return res


def bin_to_hex(ss):
    """二进制转十六进制"""
    res = ''
    for i in range(0, len(ss), 4):
        x = int(ss[i]) * 8 + int(ss[i+1]) * 4 + int(ss[i+2]) * 2 + int(ss[i+3])
        if x <= 9:
            res = res + str(x)
        else:
            res = res + chr(ord('A') + x - 10)
        if (i + 4) % 8 == 0:
            res = res + ' '

    return res


def dec_to_bin(x, ll):
    """十进制数转二进制"""
    res = []
    if ll == 8:
        res.append(x)
    elif ll == 16:
        res.append(x // 256)
        res.append(x % 256)

    res = bytes(res)
    return res


def write_bin(ss):
    res = ''
    for i in range(16 - len(ss)):
        res = res + '0'
    res = res + ss
    return res


def write_huffman_ac_table(typ):
    t = load_huffman_table(typ, 'AC')
    res = []

    tt = np.zeros(16, dtype=int)
    for i in range(16):
        cnt = 10
        if i == 0 or i == 15:
            cnt = cnt + 1
        for j in range(cnt):
            tt[len(t[i][j]) - 1] += 1

    for i in range(16):
        res.append(tt[i])

    for l in range(17):
        tmp = []
        for i in range(16):
            cnt = 10
            # print(i)
            if i == 0 or i == 15:
                cnt = cnt + 1
            for j in range(cnt):
                # print(j, '-', cnt)
                if len(t[i][j]) == l:
                    tmp.append(t[i][j])
        tmp.sort()
        for k in range(len(tmp)):
            for i in range(16):
                cnt = 10
                # print(i)
                if i == 0 or i == 15:
                    cnt = cnt + 1
                for j in range(cnt):
                    if tmp[k] == t[i][j]:
                        if i == 0 or i == 15:
                            res.append(i * 16 + j)
                        else:
                            res.append(i * 16 + j + 1)
    res = bytes(res)
    return res


def get_data(list_1, list_2, list_3, cnt):
    res = []
    tmp = ''

    for i in range(cnt):
        tmp = tmp + list_1[i] + list_2[i] + list_3[i]

    # 补零
    if len(tmp) % 8 != 0:
        for i in range(8 - (len(tmp) % 8)):
            tmp = tmp + '0'

    for i in range(0, len(tmp), 8):
        s = 0
        t = 128
        for j in range(8):
            s = s + int(tmp[i + j]) * t
            t = t // 2
        res.append(s)
        if s == 255:
            res.append(0)
    res = bytes(res)

    return res


def write(file, y_list, cb_list, cr_list, height, width):
    """输出jpeg文件"""
    jpegfile = open(file, "wb+")

    # 文件头添加 （具体看文档）
    # 添加 SOI start of image
    jpegfile.write(bytes(hex_to_bin('FF D8')))

    # 添加 APP0
    jpegfile.write(hex_to_bin('FF E0'))
    jpegfile.write(hex_to_bin('00 10'))
    jpegfile.write(hex_to_bin('4A 46 49 46 00'))
    jpegfile.write(hex_to_bin('01 01 01 00 90 00 90 00 00'))

    # 添加DQT
    # 第一张表
    jpegfile.write(hex_to_bin('FF DB 00 43 00'))
    t = load_quantization_table('lum').reshape([64])
    jpegfile.write(bytes(t.tolist()))
    # 第二张表
    jpegfile.write(hex_to_bin('FF DB 00 43 01'))
    t = load_quantization_table('chrom').reshape([64])
    jpegfile.write(bytes(t.tolist()))

    # 添加 SOF start of frame
    jpegfile.write(hex_to_bin('FF C0'))
    jpegfile.write(hex_to_bin('00 11'))
    # 样本位数
    jpegfile.write(hex_to_bin('08'))
    jpegfile.write(dec_to_bin(height, 16))
    jpegfile.write(dec_to_bin(width, 16))
    # 颜色分量数
    jpegfile.write(hex_to_bin('03'))
    # 各颜色信息
    jpegfile.write(hex_to_bin('01 11 00'))
    jpegfile.write(hex_to_bin('02 11 01'))
    jpegfile.write(hex_to_bin('03 11 01'))

    # 添加 DHT Define Huffman Table
    # 第一张直流表（亮度）
    jpegfile.write(hex_to_bin('FF C4'))
    jpegfile.write(hex_to_bin('00 1F'))
    jpegfile.write(hex_to_bin('00'))
    # 每一个长度的编码数量
    jpegfile.write(hex_to_bin('00 01 05 01 01 01 01 01 01 00 00 00 00 00 00 00'))
    for i in range(12):
        jpegfile.write(dec_to_bin(i, 8))

    # 第一张交流表（亮度）
    jpegfile.write(hex_to_bin('FF C4'))
    jpegfile.write(hex_to_bin('00 B5'))
    jpegfile.write(hex_to_bin('10'))
    # jpegfile.write(hex_to_bin('00 02 01 03 03 02 04 03 05 05 04 04 00 00 01 7D'))
    jpegfile.write(write_huffman_ac_table('lum'))

    # 第二张直流表 (色度)
    jpegfile.write(hex_to_bin('FF C4'))
    jpegfile.write(hex_to_bin('00 1F'))
    jpegfile.write(hex_to_bin('01'))
    jpegfile.write(hex_to_bin('00 03 01 01 01 01 01 01 01 01 01 00 00 00 00 00'))
    for i in range(12):
        jpegfile.write(dec_to_bin(i, 8))

    # 第二张交流表（色度）
    jpegfile.write(hex_to_bin('FF C4'))
    jpegfile.write(hex_to_bin('00 B5'))
    jpegfile.write(hex_to_bin('11'))
    # jpegfile.write(hex_to_bin('00 02 01 03 03 02 04 03 05 05 04 04 00 00 01 7D'))
    jpegfile.write(write_huffman_ac_table('chrom'))

    # 添加 SOS
    jpegfile.write(hex_to_bin('FF DA'))
    jpegfile.write(hex_to_bin('00 0C'))
    # 表示 YCrCb格式
    jpegfile.write(hex_to_bin('03'))
    # 各颜色分量使用的表
    jpegfile.write(hex_to_bin('01 00 02 11 03 11'))
    jpegfile.write(hex_to_bin('00 3F 00'))

    # 添加图像数据
    cnt = (height // 8) * (width // 8)
    jpegfile.write(get_data(y_list, cb_list, cr_list, cnt))

    # 添加 EOI End Of Image
    jpegfile.write(hex_to_bin('FF D9'))

    jpegfile.close()


if __name__ == '__main__':
    # print(bytes(hex_to_bin('FF')))
    pass
    # print(hex_to_bin('FF C4'))
    # print(bin_to_hex(write_huffman_ac_table('lum')))
