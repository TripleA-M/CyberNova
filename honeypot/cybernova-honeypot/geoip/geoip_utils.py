import requests


def get_geo_data(ip_address):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip_address}", timeout=5)
        if response.status_code == 200:
            return response.json()
    except Exception:
        # Fail closed and let caller handle None
        pass
    return None