# dev_config
#!/usr/bin/env python
from .config import Config


class Detail1Config(Config):
    """
    Dev config for demo02
    """

    # Application config
    MAC_ARM64_CHROME = "src/chrome/mac/arm/chromedriver"
    LINUX_64_CHROME = "src/chrome/linxu/64/chromedriver"
    YY_MAIN_URL = "https://w1.rm18gb.xyz/"
    IM_REPTILE_FLAG = "detail" # positive 正博 negative 反博 detail 详情页
    MAIN_ACCOUNT = {"account": "CZK087", "password": "Aa123456"}
    SUB_ACCOUNT = [{"account": "CZK087", "password": "Aa123456"}, {"account": "CFR750", "password": "Aa123456"}]
    POST_LIST_URL = "http://35.246.121.176/imList"
    POST_DETAIL_URL = "http://35.246.121.176/imDetail"
    BAIDU_APP_ID = "77012511"
    BAIDU_API_KEY = "t7SDy4Kk4W3V8rQjtZLFndFv"
    BAIDU_SECRET_KEY = "y5GcGtfcYzEwqPT7Smh2oAeZqMS32RmH"
    