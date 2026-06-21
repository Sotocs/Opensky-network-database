import requests

def get_country_coordinates(country_name):
    response = requests.get(
        "https://nominatim.openstreetmap.org/search",
        params={
            "q": country_name,
            "format": "jsonv2"
        },
        headers={
            "User-Agent": "MyProject"
        }
    )
    min_lat, max_lat, min_lon, max_lon = response.json()[0]['boundingbox']
    params = {
        "lamin": min_lat,
        "lamax": max_lat,
        "lomin": min_lon,
        "lomax": max_lon
    }

    return params

par = get_country_coordinates("Germany")
print(par)

def get_planes(params):
    response = requests.get(
        "https://opensky-network.org/api/states/all",
        params=params
    )
    print(response.status_code)
    return response.json()



data = get_planes(get_country_coordinates("Germany"))
print(data.keys())
print(data)

states = data["states"]

print(len(states))
print(states[0])

#2 9 13