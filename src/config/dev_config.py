# dev_config
#!/usr/bin/env python
from .config import Config


class DevConfig(Config):
    """
    Dev config for demo02
    """

    # Application config
    IM_REPTILE_FLAG = "negative"
    # IM_REPTILE_FLAG = "detail" # positive 正博 negative 反博 detail 详情页
    MAIN_ACCOUNT = {"account": "CBN999", "password": "Aa147258"}
    