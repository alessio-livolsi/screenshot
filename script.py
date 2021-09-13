import requests
from requests.models import HTTPBasicAuth
import json
from pprint import pprint


r = requests.get(
    "http://127.0.0.1:8000/api/url/",
    auth=HTTPBasicAuth("user_screenshot", "myvoiceismypassword"),
)

response = r.json()


for url in response["results"]:
    print("url found")
    pprint(url["url"])


# if response.status_code == 200:
#     print("The request was a success!")
#     # Code here will only run if the request is successful
# elif response.status_code == 404:
#     print("Result not found")
#     # Code here will react to failed requests


# TODO: once response is done via the GET method, loop through the response and for each iteration,
# take the screenshot and then send it to the screenshot rest end point, when sent screenshot to end point include URL,
# so we understand what website it is.
