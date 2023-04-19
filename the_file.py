import requests
import sys
from io import BytesIO
from PIL import Image
from get_coordinates import get_coordinates

search_api_server = "https://search-maps.yandex.ru/v1/"
api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"

address_ll = ",".join(get_coordinates(" ".join(sys.argv[3:])))
spn = ",".join([sys.argv[1], sys.argv[2]])

search_params = {
    "apikey": api_key,
    "text": "аптека",
    "lang": "ru_RU",
    "ll": address_ll,
    "spn": spn,
    "type": "biz"
}

response = requests.get(search_api_server, params=search_params)
if not response:
    # ...
    pass

json_response = response.json()

organization = json_response["features"][0]
org_name = organization["properties"]["CompanyMetaData"]["name"]
org_address = organization["properties"]["CompanyMetaData"]["address"]

point = organization["geometry"]["coordinates"]
org_point = "{0},{1}".format(point[0], point[1])

map_params = {
    "ll": address_ll,
    "spn": spn,
    "l": "map",
    # добавим точку, чтобы указать найденную аптеку
    "pt": "{0},pm2dgl".format(org_point)
}

map_api_server = "http://static-maps.yandex.ru/1.x/"
response = requests.get(map_api_server, params=map_params)

Image.open(BytesIO(response.content)).show()
