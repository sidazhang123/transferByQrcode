# transferByQrcode

用于类似“桌面虚拟机中文件不能直接拷出”的场景
封闭环境中：
`python qrmaker.py [filepath]` 将任意小文件分片转成多个二维码
`python trigger.py` 将二维码图片轮播，并通过像素点颜色指示外部的receiver截图
外部：
`python receiver.py` 指定文件名、#1指示器、#2指示器(用俩是因为除了黑白都有色差)、截图左上、截图右下 4个坐标，跟随trigger进行截图并拼接成文件

file<->base64<->qrcodes。核心部分从某blog贴过来改了改，凑合着用。好处是不用ocr、二维码带纠错成功率很高，缺点是效率极低>1M文件基本不考虑（300B/s?）
