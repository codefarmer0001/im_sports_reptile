from PIL import Image, ImageEnhance, ImageFilter
import pytesseract

# 确保你的 Tesseract 安装路径正确，如果安装在默认路径，不需要这行
# pytesseract.pytesseract.tesseract_cmd = '/usr/local/bin/tesseract'

# 打开验证码图片
image = Image.open('/Users/mac/Downloads/asdfgh.jpg')

# 转为灰度图像
image = image.convert('L')

# 增强对比度
enhancer = ImageEnhance.Contrast(image)
image = enhancer.enhance(2)

# 二值化处理
image = image.point(lambda x: 0 if x < 140 else 255, '1')

# 去除噪点
image = image.filter(ImageFilter.MedianFilter())

# 保存预处理后的图像，方便查看效果
image.save('processed_captcha.png')

# 使用 Tesseract OCR 识别验证码
captcha_text = pytesseract.image_to_string(image, config='--psm 6')

print("识别的验证码:", captcha_text)
