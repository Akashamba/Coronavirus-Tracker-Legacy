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
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_india_data():
    total = json.loads(get_url("https://api.covid19india.org/data.json"))

    india_data = [{"Confirmed": int(total["statewise"][0]["confirmed"]),
                   "Active": int(total["statewise"][0]["active"]),
                   "Recovered": int(total["statewise"][0]["recovered"]),
                   "Deaths": int(total["statewise"][0]["deaths"])}]
    for i in range(1, len(total["statewise"])):
        india_data.append({"id": i + 1, "State": total["statewise"][i]["state"],
                           "Confirmed": int(total["statewise"][i]["confirmed"]),
                           "Active": int(total["statewise"][i]["active"]),
                           "Recovered": int(total["statewise"][i]["recovered"]),
                           "Deaths": int(total["statewise"][i]["deaths"])})
    india_data.sort(key=lambda x: (x['Confirmed'], x['Deaths']), reverse=True)

    for i in range(len(total["statewise"])):
        if i != 0:
            india_data[i]["id"] = i
        india_data[i]["Confirmed"] = comma(india_data[i]["Confirmed"])
        india_data[i]["Active"] = comma(india_data[i]["Active"])
        india_data[i]["Recovered"] = comma(india_data[i]["Recovered"])
        india_data[i]["Deaths"] = comma(india_data[i]["Deaths"])

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
