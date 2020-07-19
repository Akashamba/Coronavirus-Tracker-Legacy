import requests, json


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


total = json.loads(get_url("https://api.covid19api.com/summary"))
print(total)




