import http
import mimetypes
import json
import os
key = '4a94d85587aa216232df1be199b36b69'
conn = http.client.HTTPSConnection("developers.zomato.com")


def city_id(city):
    payload = ''
    headers = {
        'user-key': key,
    }

    link = "/api/v2.1/cities?q="
    citylink = link + city
    conn.request("GET", citylink, payload, headers)
    res = conn.getresponse()
    data = res.read()
    data = json.loads(data.decode("utf-8"))
    return str(data["location_suggestions"][0]["id"])


def top_rest(city, count):
    payload = ''
    headers = {
        'user-key': key,
    }
    entity_id = city_id(city)
    link = "/api/v2.1/search?entity_id="
    rest = link + entity_id + "&entity_type=city&count=" + str(count)
    conn.request("GET", rest, payload, headers)
    res = conn.getresponse()
    data = res.read()
    data = json.loads(data.decode("utf-8"))
    l = data["restaurants"]
    list_r = []
    for i in l:
        dict_r = {"Name":(i["restaurant"]["name"]) ,\
        "Cuisines":(i["restaurant"]["cuisines"]) , \
        "Timings":(i["restaurant"]["timings"]) , \
        "url":(i["restaurant"]["url"])}
        list_r.append(dict_r)
    return list_r