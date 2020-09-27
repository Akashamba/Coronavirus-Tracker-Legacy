from flask import Flask, render_template  # , request, redirect, url_for
import requests
import json
import urllib3

urllib3.disable_warnings()


def comma(n):
    s, *d = str(n).partition(".")
    r = ",".join([s[x - 2:x] for x in range(-3, -len(s), -2)][::-1] + [s[-3:]])
    return "".join([r] + d)


def reorder(name):
    try:
        name.index(',')
        return str(name.split(',', 1)[1] + " " + name.split(',', 1)[0])
    except ValueError:
        return name


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_india_data():
    total = json.loads(get_url("https://api.covid19india.org/data.json"))

    india_data = [{"Confirmed": [int(total["statewise"][0]["confirmed"]), int(total["statewise"][0]["deltaconfirmed"])],
                   "Active": [int(total["statewise"][0]["active"]), int(total["statewise"][0]["deltaconfirmed"])],
                   "Recovered": [int(total["statewise"][0]["recovered"]), int(total["statewise"][0]["deltarecovered"])],
                   "Deaths": [int(total["statewise"][0]["deaths"]), int(total["statewise"][0]["deaths"])]}]
    for i in range(1, len(total["statewise"])):
        india_data.append({"id": i + 1, "State": total["statewise"][i]["state"],
                           "Confirmed": [int(total["statewise"][0]["confirmed"]),
                                         int(total["statewise"][i]["deltaconfirmed"])],
                           "Active": [int(total["statewise"][i]["active"]), int(total["statewise"][i]["deltaconfirmed"])],
                           "Recovered": [int(total["statewise"][i]["recovered"]),
                                         int(total["statewise"][i]["deltarecovered"])],
                           "Deaths": [int(total["statewise"][i]["deaths"]), int(total["statewise"][i]["deaths"])]})
    india_data.sort(key=lambda x: (x['Confirmed'][0], x['Deaths'][0]), reverse=True)

    india_data.append(total["statewise"][0]["lastupdatedtime"].replace('/', '.'))

    for i in range(len(total["statewise"])):
        if i != 0:
            india_data[i]["id"] = i
        india_data[i]["Confirmed"][0] = comma(india_data[i]["Confirmed"][0])
        india_data[i]["Active"][0] = comma(india_data[i]["Active"][0])
        india_data[i]["Recovered"][0] = comma(india_data[i]["Recovered"][0])
        india_data[i]["Deaths"][0] = comma(india_data[i]["Deaths"][0])
        
        india_data[i]["Confirmed"][1] = comma(india_data[i]["Confirmed"][1])
        india_data[i]["Active"][1] = comma(india_data[i]["Active"][1])
        india_data[i]["Recovered"][1] = comma(india_data[i]["Recovered"][1])
        india_data[i]["Deaths"][1] = comma(india_data[i]["Deaths"][1])

    return india_data


def get_state_data(curr_state):
    total = json.loads(get_url("https://api.covid19india.org/state_district_wise.json"))[curr_state]["districtData"]
    state_data = []
    i = 0
    for district in total:
        state_data.append({"id": i+1, "District": district,
                           "Confirmed": [total[district]["confirmed"], total[district]["delta"]["confirmed"]],
                           "Active": [total[district]["active"], total[district]["delta"]["confirmed"]],
                           "Recovered": [total[district]["recovered"], total[district]["delta"]["recovered"]],
                           "Deaths": [total[district]["deceased"], total[district]["delta"]["deceased"]]})
        i += 1
    state_data.sort(key=lambda x: (x['Confirmed'][0], x['Deaths'][0]), reverse=True)
    for i in range(len(state_data)):
        if i != 0:
            state_data[i]["id"] = i
        state_data[i]["Confirmed"][0] = comma(state_data[i]["Confirmed"][0])
        state_data[i]["Active"][0] = comma(state_data[i]["Active"][0])
        state_data[i]["Recovered"][0] = comma(state_data[i]["Recovered"][0])
        state_data[i]["Deaths"][0] = comma(state_data[i]["Deaths"][0])

        state_data[i]["Confirmed"][1] = comma(state_data[i]["Confirmed"][1])
        state_data[i]["Active"][1] = comma(state_data[i]["Active"][1])
        state_data[i]["Recovered"][1] = comma(state_data[i]["Recovered"][1])
        state_data[i]["Deaths"][1] = comma(state_data[i]["Deaths"][1])

    return state_data


def get_world_data():
    total = json.loads(get_url("https://api.covid19api.com/summary"))

    world_data = [{"Confirmed": [total["Global"]["TotalConfirmed"], total["Global"]["NewConfirmed"]],
                   "Recovered": [total["Global"]["TotalRecovered"], total["Global"]["NewRecovered"]],
                   "Deaths": [total["Global"]["TotalDeaths"], total["Global"]["NewDeaths"]]}]

    for i in range(len(total["Countries"])):
        world_data.append({"id": i + 1, "Country": reorder(total["Countries"][i]["Country"]),
                           "Confirmed": [total["Countries"][i]["TotalConfirmed"],
                                         total["Countries"][i]["NewConfirmed"]],
                           "Recovered": [total["Countries"][i]["TotalRecovered"],
                                         total["Countries"][i]["NewRecovered"]],
                           "Deaths": [total["Countries"][i]["TotalDeaths"],
                                      total["Countries"][i]["NewDeaths"]]})
    world_data.sort(key=lambda x: (x['Confirmed'][0], x['Deaths'][0]), reverse=True)

    date = total["Countries"][0]["Date"][0:10].split("-")
    world_data.append(date[2] + "-" + date[1] + "-" + date[0] + " " + total["Countries"][0]["Date"][11:19])

    for i in range(len(total["Countries"])):
        if i != 0:
            world_data[i]["id"] = i
        world_data[i]["Confirmed"][0] = comma(world_data[i]["Confirmed"][0])
        world_data[i]["Recovered"][0] = comma(world_data[i]["Recovered"][0])
        world_data[i]["Deaths"][0] = comma(world_data[i]["Deaths"][0])

        world_data[i]["Confirmed"][1] = comma(world_data[i]["Confirmed"][1])
        world_data[i]["Recovered"][1] = comma(world_data[i]["Recovered"][1])
        world_data[i]["Deaths"][1] = comma(world_data[i]["Deaths"][1])

    return world_data


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html', india=get_india_data(), world=get_world_data())


@app.route('/india')
def india():
    return render_template('india.html', india=get_india_data())


@app.route('/state/<state>')
def state(state):
    return render_template('state.html', state=get_state_data(state), state_name=state)


@app.route('/world')
def world():
    return render_template('world.html', world=get_world_data())


@app.route('/donate')
def donate():
    return render_template('donate.html')


@app.route('/credits')
def credit():
    return render_template('credits.html')


@app.route("/dos-and-donts")
def dos():
    return render_template('dos.html')


@app.errorhandler(500)
def error(e):
    return render_template('india.html', india=get_india_data()), 500


if __name__ == "__main__":
    app.run()
