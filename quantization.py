import numpy as np

from utils import load_quantization_table


def quantize(arr, typ):
    q = load_quantization_table(typ)
    return (arr / q).round().astype(int)
