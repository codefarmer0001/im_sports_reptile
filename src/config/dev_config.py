# dev_config
#!/usr/bin/env python
from .config import Config


class DevConfig(Config):
    """
    Dev config for demo02
    """

    # Application config
    MAC_ARM64_CHROME = "src/chrome/mac/arm/chromedriver"
    YY_MAIN_URL = "https://o3q.mltyz6.com/"
    IM_REPTILE_FLAG = "negative"
    MAIN_ACCOUNT = {"account": "rmethan777", "password": "ethan7890"}
    SUB_ACCOUNT = [{"account": "RM6666", "password": "rm957957"}, {"account": "rm8888", "password": "rm999957"}]
    