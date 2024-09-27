import requests
import time
from dataclasses import dataclass

@dataclass
class Light:
    name: str
    entity_id: str
    state: str
    brightness: int | None = None
    rgb_color: list[int] | None = None
    hs_color: list[int] | None = None


class HomeAssistant:
    _lights: list[Light]

    def __init__(self, url: str, token: str) -> None:
        self.url = url
        self.token = token
        self._fetch_devices()

    def _fetch_devices(self) -> None:
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

        resp = requests.get(f"{self.url}/api/states", headers=headers)
        assert resp.status_code == 200, "it's so over didn't get 200 status from home assistant"

        self._lights = [
            self._create_light(device) for device in resp.json()
            if device["entity_id"].startswith("light.")
        ]


    def _create_light(self, device: dict) -> Light:
        attributes = device.get("attributes", {})
        return Light(
            name=attributes.get("friendly_name", ""),
            entity_id=device["entity_id"],
            state=device["state"],
            brightness=attributes.get("brightness"),
            rgb_color=attributes.get("rgb_color"),
            hs_color=attributes.get("hs_color")
        )

    def _toggle_light_power(self, entity_id: str) -> None:
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

        data = {
            "entity_id": entity_id
        }

        resp = requests.post(f"{self.url}/api/services/light/toggle", headers=headers, json=data)
        assert resp.status_code == 200, "Couldn't change the state of ceiling lights, it's so over"

    def toggle_ceiling_lights(self) -> None:
        spot_lights = [light for light in self._lights if "hue_ambiance_spot" in light.entity_id]

        for _ in range(10):
            for light in spot_lights:
                self._toggle_light_power(light.entity_id)
            time.sleep(1)

    def set_lights_red(self) -> None:
        old_ligth_state: list[Light] = []
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

        for light in self._lights:
            if (light.name != "studio" and light.entity_id != "light.bedroom") and (light.rgb_color or light.hs_color):
                old_ligth_state.append(light)
                data = {
                    "entity_id": light.entity_id,
                    "rgb_color": [255, 0, 0],
                }

                resp = requests.post(f"{self.url}/api/services/light/turn_on", headers=headers, json=data)
                assert resp.status_code == 200, "Couldn't change light color to red :("
        time.sleep(5)
        for light in old_ligth_state:
              data = {
                  "entity_id": light.entity_id,
                  "rgb_color": light.rgb_color,
              }

              service = "turn_on" if light.state == "on" else "turn_off"
              resp = requests.post(f"{self.url}/api/services/light/{service}", headers=headers, json=data)
              assert resp.status_code == 200, "Couldn't change light color to red :("
