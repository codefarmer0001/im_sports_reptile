import cv2
import numpy as np
from PIL import Image
import pytesseract

# 确保你的 Tesseract 安装路径正确，如果安装在默认路径，不需要这行
# pytesseract.pytesseract.tesseract_cmd = '/usr/local/bin/tesseract'

# 打开验证码图片
image = cv2.imread('/Users/mac/Downloads/aaaa.jpeg')

# 转为灰度图像
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 应用高斯滤波去除噪点
gray = cv2.GaussianBlur(gray, (5, 5), 0)

# 使用自适应阈值进行二值化处理
binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

# 反转图像颜色
binary = cv2.bitwise_not(binary)

# 保存预处理后的图像，方便查看效果
cv2.imwrite('processed_captcha.png', binary)

# 使用 Tesseract OCR 识别验证码
captcha_text = pytesseract.image_to_string(binary, config='--psm 8')

print("识别的验证码:", captcha_text)
