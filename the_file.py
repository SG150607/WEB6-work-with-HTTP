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

pt_info = "{0},home".format(address_ll)
ll_sum = [float(address_ll.split(",")[0]), float(address_ll.split(",")[1])]
for organiz_num in range(10):
    organization = json_response["features"][organiz_num]
    org_name = organization["properties"]["CompanyMetaData"]["name"]
    org_address = organization["properties"]["CompanyMetaData"]["address"]

    point = organization["geometry"]["coordinates"]
    org_point = "{0},{1}".format(point[0], point[1])

    worktime = organization["properties"]["CompanyMetaData"]["Hours"]["Availabilities"]

    for ttime in worktime:
        if "Intervals" in ttime:
            pt_param = "pm2bll"
            break
        elif "TwentyFourHours" in ttime and ttime["TwentyFourHours"]:
            pt_param = "pm2gnl"
        else:
            pt_param = "pm2grl"
    else:
        pt_param = "pm2grl"

    ll_sum[0] += float(org_point.split(',')[0])
    ll_sum[1] += float(org_point.split(',')[1])
    pt_info += f"~{org_point},{pt_param}"

map_params = {
    "ll": f"{ll_sum[0] / 11},{ll_sum[1] / 11}",
    "spn": f"{ll_sum[0] / 7200},{ll_sum[1] / 7200}",
    "l": "map",
    "pt": pt_info
}

map_api_server = "http://static-maps.yandex.ru/1.x/"
response = requests.get(map_api_server, params=map_params)

print(response.url)
