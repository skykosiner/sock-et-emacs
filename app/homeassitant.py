import requests
import json
from dataclasses import dataclass

@dataclass
class Device:
    name: str
    entity_id: str
    rgb_color: list[int] | None
    hs__color: list[int] | None

class HomeAssistant:
    devices: list[Device]

    def __init__(self, url: str, token: str) -> None:
        self.url = url
        self.token = token
        self._fetch_devices()


    def _fetch_devices(self):
        headers = { "Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}
        resp = requests.get(f"{self.url}/api/state", headers=headers)
        self.devices =

        print(resp)
