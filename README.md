# JPEG-encoding

## 依赖

```
python >= 3.9.13
numpy >= 1.21.5
```

## 简介

这是一个JPEG图像压缩软件，能够将二进制文件转化为jpg文件

你可以通过以下命令使用

```
python ./jpeg_encoder.py img/demo.bin demo.jpg
```

两个参数分别为二进制文件名（含位置）和输出的文件名

> **注意**：二进制中只含图片的像素信息，并且顺序为R，G，B
>
>你还需要配置setting中图片的长和宽

## 图像质量及压缩比

你可以在setting中配置quality来获得你想要的图像质量及压缩比

quality为1-100中的整数值，值越大代表图像质量越高，压缩比越低

