import requests


def call_api_moto(url):
    r = requests.post(url)
    r = r.json()
    #print(r)
    return r