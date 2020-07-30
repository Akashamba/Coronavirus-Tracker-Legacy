from flask import Flask, render_template  # , request, redirect, url_for
import requests
import json
import urllib3

urllib3.disable_warnings()


def comma(n):
    s, *d = str(n).partition(".")
    r = ",".join([s[x-2:x] for x in range(-3, -len(s), -2)][::-1] + [s[-3:]])
    return "".join([r] + d)


def reorder(name):
    try:
        name.index(',')
        return str(name.split(',', 1)[1]+" "+name.split(',', 1)[0])
    except ValueError:
        return name


def get_url(url):
    response = requests.get(url, verify=False)
    content = response.content.decode("utf8")
    return content


def get_india_data():
    total = json.loads(get_url("https://api.covid19india.org/data.json"))

    india_data = [{"Confirmed": total["statewise"][0]["confirmed"],
                   "Active": total["statewise"][0]["active"],
                   "Recovered":total["statewise"][0]["recovered"],
                   "Deaths": total["statewise"][0]["deaths"]}]
    for i in range(1, len(total["statewise"])):
        india_data.append({"id": i + 1, "State": total["statewise"][i]["state"],
                           "Confirmed": int(total["statewise"][i]["confirmed"]),
                           "Active": int(total["statewise"][i]["active"]),
                           "Recovered": int(total["statewise"][i]["recovered"]),
                           "Deaths": int(total["statewise"][i]["deaths"])})

    india_data.sort(key=lambda x: (x['Deaths']), reverse=True)

    for i in range(len(total["statewise"])):
        if i != 0:
            india_data[i]["id"] = i
        india_data[i]["Confirmed"] = comma(india_data[i]["Confirmed"])
        india_data[i]["Active"] = comma(india_data[i]["Confirmed"])
        india_data[i]["Recovered"] = comma(india_data[i]["Confirmed"])
        india_data[i]["Deaths"] = comma(india_data[i]["Confirmed"])

    return india_data


for i in range(37):
    print(get_india_data()[i])