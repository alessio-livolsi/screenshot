import requests
from requests.models import HTTPBasicAuth
import json
from pprint import pprint
from datetime import datetime
import html
import random


from selenium import webdriver
import datetime, time, pyautogui
import os
from webdriver_manager.chrome import ChromeDriverManager

from PIL import Image


API_URL_ROOT = "http://10.10.8.196:8000"


def stitch_images(websitePath: str, windowPath: str, targetPath: str):
    desktop = Image.open(windowPath)
    topBar = desktop.crop((0, 0, 1920, 115))
    bottomBar = desktop.crop((0, 1080 - 40, 1920, 1080))
    screenshot = Image.open(websitePath)
    images = [topBar, screenshot, bottomBar]
    widths, heights = zip(*(i.size for i in images))
    total_width = max(widths)
    print(total_width)
    max_height = sum(heights)
    print(max_height)
    new_im = Image.new("RGB", (total_width, max_height))
    y_offset = 0
    for im in images:
        new_im.paste(im, (0, y_offset))
        y_offset += im.size[1]
    new_im.save(targetPath)


r = requests.get(
    f"{API_URL_ROOT}/api/url/",
    auth=HTTPBasicAuth("user_screenshot", "myvoiceismypassword"),
)
response = r.json()


for index, url in enumerate(response["results"]):
    for i in range(10):
        name = url["website"]
        height = url["height"]
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument(f"window-size=1280x{height}")
        driver = webdriver.Chrome(
            ChromeDriverManager().install(), options=chrome_options
        )
        driver.get(url["url"])
        time.sleep(1.5)
        browserFilename = f"{name}_{random.randint(1, 10000000)}.png"
        driver.save_screenshot(browserFilename)
        driver.close()
        time.sleep(1)
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(url["url"])
        driver.maximize_window()
        time.sleep(1)
        pic = pyautogui.screenshot()
        driver.close()
        desktopFilename = f"desktop_{random.randint(1, 10000000)}.png"
        pic.save(desktopFilename)
        stitch_images(
            websitePath=browserFilename,
            windowPath=desktopFilename,
            targetPath=f"{name}-screenshot.png",
        )

        upload = {"image": open("image.jpeg", "rb")}
        data = {"url": url["id"], "created": datetime.datetime.now()}
        resp = requests.post(
            f"{API_URL_ROOT}/api/screenshot/",
            files=upload,
            data=data,
            auth=HTTPBasicAuth("user_screenshot", "myvoiceismypassword"),
        )
