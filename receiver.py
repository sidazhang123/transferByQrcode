import win32gui, time,os,base64
from PIL import ImageGrab,Image
from pyzbar import pyzbar


def base64ToFile(base64Data, filePath):
    with open(filePath, 'wb') as f1:
        fileBytes = base64.b64decode(base64Data)
        f1.write(fileBytes)
    print("qrcode_files_decode_done ... ")


# 写文件文本内容
def writeFileText(filePath, text):
    with open(filePath, 'wb') as f1:
        f1.write(text.encode('utf-8'))


# 解码成原始文件
def readQrcode(qrcodePath):
    qrcodeText = ""
    qucodeImg = Image.open(qrcodePath)
    pzDecodeImg = pyzbar.decode(qucodeImg)
    for barcode in pzDecodeImg:
        qrcodeText = barcode.data.decode("utf-8")  ##二维码的data信息
    return qrcodeText


def getBase64Array(files):
    base64Array = [""] * len(files)

    for qr in files:
        qrText = readQrcode(qr)
        splitIndex = qrText.find('|')
        qrIndex = int(qrText[0: splitIndex])
        partBase64 = qrText[splitIndex + 1:]
        base64Array[qrIndex] = partBase64
        print(qrText)
    indexTmp = 0
    for oneText in base64Array:
        if oneText.strip() == '':
            # print("二维码对应base64段缺失 ：%d" % indexTmp)
            raise Exception(print("二维码解码异常 ：对应base64段缺失 ：%d" % indexTmp))
        indexTmp = indexTmp + 1

    return base64Array


# 多个二维码转成文件
def qrcodesToFile(decode_file_name):
    files = [i for i in os.listdir('.') if i.endswith('.jpg')]
    files.sort(key=lambda x: int(x.split('.jpg')[0]))

    base64Array = getBase64Array(files)

    fullBase64Data = ''.join(base64Array)

    base64ToFile(fullBase64Data, decode_file_name)
    print(base64Array)
    print("文件还原成功")


def get_pixel_color_hex(x, y):
    hdc = win32gui.GetDC(0)
    color = win32gui.GetPixel(hdc, x, y)
    win32gui.ReleaseDC(0, hdc)
    return "#{:02X}{:02X}{:02X}".format(color & 0xFF, (color >> 8) & 0xFF, (color >> 16) & 0xFF)


def get_indicator_result()->int:
    #1:准备 2&3:进行（2个码用于切换） 4:结束 5:识别ind异常
    ind1=get_pixel_color_hex(coords['indicator1'][0], coords['indicator1'][1])
    ind2=get_pixel_color_hex(coords['indicator2'][0], coords['indicator2'][1])
    if ind1=='#000000' and ind2=='#000000':
        return 1
    elif ind1=='#FFFFFF' and ind2=='#FFFFFF':
        return 4
    elif ind1=='#000000' and ind2=='#FFFFFF':
        return 2
    elif ind1=='#FFFFFF' and ind2=='#000000':
        return 3
    else:
        return 5


coords = dict()
decode_file_name=input('输入解码后文件名，带扩展名\n')
while True:
    if 'm' == input('激活本cmd窗口，鼠标放到【top_indicator】，输入“M”并回车记录该坐标\n'):
        coords['indicator1'] = win32gui.GetCursorPos()
        break
while True:
    if 'm' == input('激活本cmd窗口，鼠标放到【bottom_indicator】，输入“M”并回车记录该坐标\n'):
        coords['indicator2'] = win32gui.GetCursorPos()
        break
while True:
    if 'm' == input('激活本cmd窗口，鼠标放到【二维码左上角】，输入“M”并回车记录该坐标\n'):
        coords['qrtopleft'] = win32gui.GetCursorPos()
        break
while True:
    if 'm' == input('激活本cmd窗口，鼠标放到【二维码右下角】，输入“M”并回车记录该坐标\n'):
        coords['qrbottomright'] = win32gui.GetCursorPos()
        break
print('坐标记录完毕...')
r0=get_indicator_result()
if 1 == r0:
    print('找到indicator 准备')
    print('去点【START】，indicator变色后自动开始工作')
else:
    raise Exception(
        f"indicator不为准备状态 {coords['indicator1']},{coords['indicator2']},返回码{r0}")

cur_indicator_res = 0
index = 0

while True:
    r1 = get_indicator_result()
    r2 = get_indicator_result()
    # print(r1, r2,cur_indicator_res)
    if r1!=r2:
        # print('残影导致2次结果不同，立刻重判')
        continue

    # 终止符
    if r1 ==4:
        print('终止符')
        break

    elif r1==2 or r1==3:
        if r1 != cur_indicator_res:
            cur_indicator_res = r1
            ImageGrab.grab(coords['qrtopleft'] + coords['qrbottomright']).save(f'{index}.jpg', 'JPEG')
            print(f'保存{index}.jpg')
            index += 1
    elif r1==5:
        raise Exception(f'indicator识别错误，{r1}')
    time.sleep(0.2)
print('全部截图完毕，开始组装')
qrcodesToFile(decode_file_name)

