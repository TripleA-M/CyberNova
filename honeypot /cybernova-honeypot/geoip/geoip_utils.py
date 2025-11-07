import requests

def get_geo_data(ip_address):
    response = requests.get(f"http://ip-api.com/json/{ip_address}")
    if response.status_code == 200:
        return response.json()
    else:
        return None