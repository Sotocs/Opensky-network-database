import requests

def get_planes_in_country(country_name):
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

    response = requests.get(
        "https://opensky-network.org/api/states/all",
        params=params
    )
    return (response.json())
