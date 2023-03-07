from prefect import task, Flow, Parameter
import requests

#insertar api key openweathermap.org
api_key = "f4ff67ff5c2f879b19aa8b98356eadec"

@task(log_stdout=True)
def get_lan_and_lon(country):
    params = dict(
        q = country,
        appid = api_key,
        limit = 1
    )

    api_request = "http://api.openweathermap.org/geo/1.0/direct"
    r = requests.get(api_request, params=params);

    data = r.json()

    return data[0]['lat'],data[0]['lon']

@task
def get_some_information(coord):
    parms = dict(
        lat = coord[0],
        lon = coord[1],
        appid = api_key
    )

    api_request = "https://api.openweathermap.org/data/2.5/weather"
    r = requests.get(api_request,params=parms)

    json = r.json()
    data = json['main']

    print("La temperatura es {} con una minima de {} y maxima de {} en {}".format(
        data['temp'],data['temp_min'],data['temp_max'],json['name']
    ))

with Flow("Weather") as flow:
    country = Parameter('country')

    coord = get_lan_and_lon(country)
    get_some_information(coord)


flow.run(country="Mexico")