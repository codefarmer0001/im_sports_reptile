from aip import AipOcr

""" 你的 APPID AK SK """
APP_ID = '77012511'
API_KEY = 't7SDy4Kk4W3V8rQjtZLFndFv'
SECRET_KEY = 'y5GcGtfcYzEwqPT7Smh2oAeZqMS32RmH'

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)


""" 读取文件 """
def get_file_content(filePath):
    with open(filePath, "rb") as fp:
        return fp.read()

image = get_file_content('/Users/mac/Downloads/aaaa.jpeg')

   
# 调用通用文字识别（高精度版）
res_image = client.basicAccurate(image)
print(res_image)


# 如果有可选参数
# options = {}
# options["detect_direction"] = "true"
# options["probability"] = "true"
# res_image = client.basicAccurate(image, options)
# res_url = client.basicAccurateUrl(url, options)
# res_pdf = client.basicAccuratePdf(pdf_file, options)   
# print(res_image)
# print(res_url)
# print(res_pdf)   

