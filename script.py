import requests
from requests.models import HTTPBasicAuth
import json
from pprint import pprint
from datetime import datetime
import html


from selenium import webdriver
import datetime, time, pyautogui
import os
from webdriver_manager.chrome import ChromeDriverManager

r = requests.get(
    "http://127.0.0.1:8000/api/url/",
    auth=HTTPBasicAuth("user_screenshot", "myvoiceismypassword"),
)

response = r.json()

for url in response["results"]:
    name = url["website"]
    driver = webdriver.Chrome(ChromeDriverManager().install())
    now = datetime.datetime.now()
    driver.maximize_window()
    driver.get(url["url"])
    time.sleep(1.5)
    pic = pyautogui.screenshot()
    filename = "image.jpeg"
    pic.save(filename)
    driver.close()
    time.sleep(1)
    upload = {"image": open("image.jpeg", "rb")}

    data = {"url": url["id"], "created": datetime.datetime.now()}

    resp = requests.post(
        "http://127.0.0.1:8000/api/screenshot/",
        files=upload,
        data=data,
        auth=HTTPBasicAuth("user_screenshot", "myvoiceismypassword"),
    )
