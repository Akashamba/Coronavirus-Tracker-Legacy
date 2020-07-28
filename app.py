from flask import Flask, render_template  # , request, redirect, url_for
import requests
import json


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

    world_data = [{"Confirmed": total["Global"]["TotalConfirmed"],
                   "Recovered": total["Global"]["TotalRecovered"],
                   "Deaths": total["Global"]["TotalDeaths"]}]

    for i in range(len(total["Countries"])):
        world_data.append({"id": i + 1, "Country": reorder(total["Countries"][i]["Country"]),
                           "Confirmed": total["Countries"][i]["TotalConfirmed"],
                           "Recovered": total["Countries"][i]["TotalRecovered"],
                           "Deaths": total["Countries"][i]["TotalDeaths"]})
    world_data.sort(key=lambda x: (x['Confirmed'], x['Deaths']), reverse=True)

    for i in range(len(total["Countries"])):
        if i != 0:
            world_data[i]["id"] = i
        world_data[i]["Confirmed"] = comma(world_data[i]["Confirmed"])
        world_data[i]["Recovered"] = comma(world_data[i]["Recovered"])
        world_data[i]["Deaths"] = comma(world_data[i]["Deaths"])

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
    return render_template('donate.html')


@app.route('/credits')
def credit():
    return render_template('credits.html')


@app.route("/do's-and-don'ts")
def dos():
    return render_template('dos.html')


if __name__ == "__main__":
    app.run(debug=True)
