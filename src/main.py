from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
# from bs4 import BeautifulSoup
from config import CONFIG
# from time import sleep
from reptile import LoginYY
from pool import DriverPool
import asyncio

import sys
sys.setrecursionlimit(10000)


if __name__ == '__main__':

    # asyncio.run(LoginYY.main())
    LoginYY.main()
   