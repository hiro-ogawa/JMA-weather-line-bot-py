import os
import json
import requests
from urllib.parse import urlencode
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

from jma_weather import JMA_Weather

api = JMA_Weather()

yahoo_client_id = os.environ["YAHOO_CLIENT_ID"]
yahoo_geo_endpoint = "https://map.yahooapis.jp/geocode/V1/geoCoder"

area_json_path = Path("asset/area.json")
class20s_json_path = Path("asset/class20s.json")

def get_coordinate(query):
    q = {
        "appid": yahoo_client_id,
        "query": query,
        "output": "json",
    }
    url = yahoo_geo_endpoint + "?" + urlencode(q)
    res = requests.get(url)
    if res.status_code != 200:
        print("requests get error")
        return None, None

    data = res.json()
    if data["ResultInfo"]["Count"] == 0:
        print(f"no result")
        return None, None
    coodinates = [float(x) for x in data["Feature"][0]["Geometry"]["Coordinates"].split(",")]

    return coodinates[1], coodinates[0]

# area.json取得
area = api.get_area()
with area_json_path.open("wt") as f:
    json.dump(area, f, indent=2, ensure_ascii=False)

centers = area["centers"]
offices = area["offices"]
class10s = area["class10s"]
class15s = area["class15s"]
class20s = area["class20s"]

# class20s.json生成
coordinates = {}
for i, (k, v) in enumerate(class20s.items()):
    area_name = v["name"]
    class20 = k
    class15 = v["parent"]
    class10 = class15s[class15]["parent"]
    office = class10s[class10]["parent"]
    center = offices[office]["parent"]

    print(f"{i+1:4}/{len(class20s)}: {k}: {area_name}")
    lat, lon = get_coordinate(area_name)

    if lat is None:
        continue

    coordinates[v["enName"]] = {
        "latitude": lat,
        "longitude": lon,
        "class20": class20,
        "class15": class15,
        "class10": class10,
        "office": office,
        "center": center,
    }

with class20s_json_path.open("wt") as f:
    json.dump(coordinates, f, indent=2, ensure_ascii=False)
