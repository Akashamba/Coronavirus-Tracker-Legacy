from flask import Flask, render_template  # , request, redirect, url_for
import requests
import json


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
        india_data.append({"id": i + 1, "State": state[i]["state"], "Confirmed": state[i]["confirmed"],
                           "Active": state[i]["active"], "Recovered": state[i]["recovered"], "Deaths": state[i]["deaths"]})
    return india_data


def get_world_data():
    total = json.loads(get_url("https://api.covid19api.com/summary"))

    world_data = [{"Confirmed": total["Global"]["TotalConfirmed"], "Recovered":total["Global"]["TotalRecovered"],
                   "Deaths": total["Global"]["TotalDeaths"]}]

    for i in range(len(total["Countries"])):
        world_data.append({"id": i + 1, "Country": total["Countries"][i]["Country"],
                           "Confirmed": total["Countries"][i]["TotalConfirmed"],
                           "Recovered": total["Countries"][i]["TotalRecovered"],
                           "Deaths": total["Countries"][i]["TotalDeaths"],
                           "Date Recorded": total["Countries"][i]["Date"]})
    return world_data


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html', result=get_india_data())


@app.route('/india')
def india():
    return render_template('india.html', result=get_india_data())


@app.route('/world')
def world():
    return render_template('world.html', result=get_world_data())


@app.route('/donate')
def donate():
    return render_template('donate.html', result=get_data_india())


if __name__ == "__main__":
    app.run(debug=True)
