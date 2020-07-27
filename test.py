import requests
import json


def comma(n):
    s, *d = str(n).partition(".")
    r = ",".join([s[x-2:x] for x in range(-3, -len(s), -2)][::-1] + [s[-3:]])
    return "".join([r] + d)


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_india_data():
    total = json.loads(get_url("https://api.covidindiatracker.com/total.json"))
    state = json.loads(get_url("https://api.covidindiatracker.com/state_data.json"))
    india_data = [{"Confirmed": total["confirmed"], "Active": total["active"],
                   "Recovered":total["recovered"], "Deaths": total["deaths"]}]
    for i in range(len(state)):
        india_data.append({"id": i + 1, "State": state[i]["state"], "Confirmed": comma(state[i]["confirmed"]),
                           "Active": state[i]["active"], "Recovered": state[i]["recovered"], "Deaths": state[i]["deaths"]})

    print(india_data)


get_india_data()