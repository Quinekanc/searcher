import sys
import requests
import helper
from io import BytesIO
from PIL import Image


response = helper.find_obj(sys.argv[1:])

json_response = response.json()
toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
toponym_coodrinates = toponym["Point"]["pos"]

toponym_b = [float(i) for i in toponym['boundedBy']['Envelope']['lowerCorner'].split()]
toponym_a = [float(i) for i in toponym['boundedBy']['Envelope']['upperCorner'].split()]

toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

delta = helper.lonlat_distance(toponym_a, toponym_b)

map_params = {
    "ll": ",".join([toponym_longitude, toponym_lattitude]),
    "spn": f'{abs(toponym_a[0] - toponym_b[0])},{abs(toponym_b[1] - toponym_b[1])}',
    "l": "sat,skl",
    "pt": f'{",".join([toponym_longitude, toponym_lattitude])},pm2rdm'
}

map_api_server = "http://static-maps.yandex.ru/1.x/"
response = requests.get(map_api_server, params=map_params)

Image.open(BytesIO(
    response.content)).show()
