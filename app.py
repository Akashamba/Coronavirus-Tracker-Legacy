from flask import Flask, render_template  # , request, redirect, url_for
import requests
import json


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_data():
    total = json.loads(get_url("https://api.covidindiatracker.com/total.json"))
    state = json.loads(get_url("https://api.covidindiatracker.com/state_data.json"))
    all_data = [{"Confirmed": total["confirmed"], "Active": total["active"],
                 "Recovered":total["recovered"], "Deaths": total["deaths"]}]
    for i in range(10):
        all_data.append({"id": i + 1, "state": state[i]["state"], "confirmed": state[i]["confirmed"],
                         "active": state[i]["active"], "recovered": state[i]["recovered"], "deaths": state[i]["deaths"]})
    return all_data


app = Flask(__name__)


@app.route('/')
def home():
    all_data = get_data()

    return render_template('index.html', result=all_data)


if __name__ == "__main__":
    app.run(debug=True)
