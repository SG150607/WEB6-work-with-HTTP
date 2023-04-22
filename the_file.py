import requests
import sys
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
    pass

json_response = response.json()

organization = json_response["features"][0]
org_name = organization["properties"]["CompanyMetaData"]["name"]
org_address = organization["properties"]["CompanyMetaData"]["address"]

point = organization["geometry"]["coordinates"]
org_point = "{0},{1}".format(point[0], point[1])

map_params = {
    "ll": "{0},{1}".format((float(address_ll.split(",")[0]) + float(org_point.split(",")[0])) / 2,
                           (float(address_ll.split(",")[1]) + float(org_point.split(",")[1])) / 2),
    "spn": spn,
    "l": "map",
    "pt": "{0},pm2dgl~{1},home".format(org_point, address_ll)
}

map_api_server = "http://static-maps.yandex.ru/1.x/"
response = requests.get(map_api_server, params=map_params)

print(response.url)

info_to_print = {"Адрес": org_address, "Название аптеки": org_name,
                 "Время работы": organization["properties"]["CompanyMetaData"]["Hours"]["text"],
                 "Расстояние до аптеки": (abs(float(address_ll.split(",")[0]) - float(org_point.split(",")[0])),
                                          abs(float(address_ll.split(",")[1]) - float(org_point.split(",")[1])))}

print(f'Адрес: {info_to_print["Адрес"]}',
      f'Название аптеки: {info_to_print["Название аптеки"]}',
      f'Время работы: {info_to_print["Время работы"]}',
      f'Расстояние до аптеки: {info_to_print["Расстояние до аптеки"]}',
      sep="\n")
