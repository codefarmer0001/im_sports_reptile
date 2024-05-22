#!/usr/bin/env python
import os


class Config():
    """
    Basic config for demo02
    """
    # Application config
    MAC_ARM64_CHROME = "src/chrome/mac/arm/chromedriver"
    LINUX_64_CHROME = "src/chrome/linux/64/chromedriver"
    YY_MAIN_URL = "https://o3q.mltyz6.com/"
    IM_REPTILE_FLAG = "negative" # positive 正博 negative 反博
    MAIN_ACCOUNT = {"account": "rmethan777", "password": "ethan7890"}
    SUB_ACCOUNT = [{"account": "RM6666", "password": "rm957957"}, {"account": "rm8888", "password": "rm999957"}]
    POST_LIST_URL = "http://35.246.121.176/imList"
    POST_DETAIL_URL = "http://35.246.121.176/imDetail"
