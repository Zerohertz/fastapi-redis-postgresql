import requests
import zerohertzLib as zz

BASE_URL = "http://zerohertz.xyz:1547"
LOGGER = zz.logging.Logger("Client")


def create(username, password):
    url = f"{BASE_URL}/accounts/"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
    }
    data = {"username": username, "password": password}
    response = requests.post(url, headers=headers, json=data)
    LOGGER.info(f"[/accounts/] {response.status_code}")
    LOGGER.info(f"[/accounts/] {response.json()}")
    return response.json()


def me(token):
    url = f"{BASE_URL}/accounts/me/"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}",
    }
    response = requests.get(url, headers=headers)
    LOGGER.info(f"[/accounts/me/] {response.status_code}")
    LOGGER.info(f"[/accounts/me/] {response.json()}")
    return response.json()


def token(username, password):
    url = f"{BASE_URL}/accounts/token/"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {
        "grant_type": "password",
        "username": username,
        "password": password,
        "scope": "",
        "client_id": "",
        "client_secret": "",
    }
    response = requests.post(url, headers=headers, data=data)
    LOGGER.info(f"[/accounts/token/] {response.status_code}")
    LOGGER.info(f"[/accounts/token/] {response.json()}")
    return response.json()


if __name__ == "__main__":
    USERNAME = "Zerohertz"
    PASSWORD = "@qwer1234"
    create(USERNAME, PASSWORD)
    response = token(USERNAME, PASSWORD)
    me(response["access_token"])
