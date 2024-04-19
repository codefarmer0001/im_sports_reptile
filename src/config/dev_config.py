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
    IM_REPTILE_FLAG = "zhengbo"
    