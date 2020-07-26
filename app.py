from flask import Flask, render_template  # , request, redirect, url_for
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
    india_data = [{"Confirmed": comma(total["confirmed"]), "Active": comma(total["active"]),
                   "Recovered":comma(total["recovered"]), "Deaths": comma(total["deaths"])}]
    for i in range(len(state)):
        india_data.append({"id": i + 1, "State": state[i]["state"], "Confirmed": comma(state[i]["confirmed"]),
                           "Active": comma(state[i]["active"]), "Recovered": comma(state[i]["recovered"]),
                           "Deaths": comma(state[i]["deaths"])})
    return india_data


def get_world_data():
    total = json.loads(get_url("https://api.covid19api.com/summary"))

    world_data = [{"Confirmed": comma(total["Global"]["TotalConfirmed"]),
                   "Recovered": comma(total["Global"]["TotalRecovered"]),
                   "Deaths": comma(total["Global"]["TotalDeaths"])}]

    for i in range(len(total["Countries"])):
        world_data.append({"id": i + 1, "Country": total["Countries"][i]["Country"],
                           "Confirmed": comma(total["Countries"][i]["TotalConfirmed"]),
                           "Recovered": comma(total["Countries"][i]["TotalRecovered"]),
                           "Deaths": comma(total["Countries"][i]["TotalDeaths"])})
    return world_data


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html', india=get_india_data(), world=get_world_data())


@app.route('/india')
def india():
    return render_template('india.html', result=get_india_data())


@app.route('/world')
def world():
    return render_template('world.html', result=get_world_data())


@app.route('/donate')
def donate():
    return render_template('donate.html', result=get_india_data())


if __name__ == "__main__":
    app.run(debug=True)
