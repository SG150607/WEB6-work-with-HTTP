import requests
import sys
from get_coordinates import get_coordinates

toponym_to_find = " ".join(sys.argv[1:])
address_ll = ",".join(get_coordinates(toponym_to_find))

geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": address_ll,
    "format": "json",
    "kind": "district"
}

response = requests.get(geocoder_api_server, params=geocoder_params)

if not response:
    pass

json_response = response.json()
print(json_response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty'][
          'GeocoderMetaData']['Address']['Components'][5]['name'])
