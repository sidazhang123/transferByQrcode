# 1. 将原始文件使用最高压缩率bz2 进行压缩
#
# 2. 将压缩文件转成base64
#
# 3. 将base64 进行拆分，拆分内容中拼上序号
#
# 4. 将上方base64及序号内容转二维码
#
# 5. 存储二维码
# 外部解码程序需要固定位置截图，搞个流程让用户点击指定屏幕位置；截图保存要自动
# 把bz2转化为截图后，轮动按顺序打开图，同时打开一个悬浮指示窗，红绿切换颜色表示换图了（开始时蓝色、结束时黄色，4种状态让外部程序准备和下一步拼文件），每过5秒切
# 外部解码程序识别指示窗（蓝色），对用户定义的区域进行截图，红绿截图并编号，指示器黄色则结束截图开始拼装

import base64
import os
import sys
import qrcode
from PIL import Image, ImageDraw, ImageFont

qr_w=qr_h=0
# 文件转 base64
def fileToBase64(filePath):
    base64Text = ''
    with open(filePath, 'rb') as f1:

        base64Data = base64.b64encode(f1.read())  # base64类型
        #  b'JVBERi0xLjUNCiXi48
        base64Text = base64Data.decode('utf-8')  # str
        # JVBERi0xLjUNCiXi48/

    return base64Text


# 写文件文本内容
def writeFileText(filePath, text):
    with open(filePath, 'wb') as f1:

        f1.write(text.encode('utf-8'))

# 编码成二维码
def writeQrcode(outPath, dataText):
    global qr_h,qr_w
    imgName = os.path.basename(outPath)

    qrImg = qrcode.make(dataText)
    obj_width, obj_height = qrImg.size
    if obj_width>qr_w: qr_w=obj_width
    if obj_height > qr_h: qr_h = obj_height
    canvas_width=max(obj_width,qr_w)
    canvas_height=max(obj_height,qr_h)
    print(f'height{obj_height},width{obj_width}')
    newImage = Image.new(mode='RGB', size=(canvas_width, canvas_height + 50), color=(200, 200, 255))
    newImage.paste(qrImg, (0, 50, obj_width, obj_height + 50))
    draw = ImageDraw.Draw(newImage)
    font = ImageFont.truetype("arial.ttf", 30)
    draw.text((canvas_width / 2, 5), imgName, (255, 0, 0), font)

    newImage.save(outPath)




# 文件拆分并转二维码
def fileToQrcodes(qrcodeFolder, base64Str, textLength) -> object:
    index = 0
    startIndex = 0
    endIndex = 0

    while (endIndex < len(base64Str)):
        startIndex = index * textLength
        endIndex = startIndex + textLength

        if endIndex > len(base64Str):
            endIndex = len(base64Str)

        partText = base64Str[startIndex : endIndex]

        qrFile = qrcodeFolder + ('%d' % index) + ".jpg"
        writeQrcode(qrFile, "%d|%s" % (index, partText))

        print("%d | %s" % (index, partText))

        index = index + 1



if __name__ == "__main__":
    if len(sys.argv) > 1:
        filePath = sys.argv[1]
    else:
        raise Exception("缺少编码文件名")

    # 二维码输出文件夹
    qrcodeFolder = ""
    # 二维码长度拆分，太长摄像头有可能无法识别
    textLength = 300


    base64Str = fileToBase64(filePath)


    #base64Str = "0123456789-=abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ~!@#$%^&*()_+:;,./?|<>"

    fileToQrcodes(qrcodeFolder, base64Str, textLength)
