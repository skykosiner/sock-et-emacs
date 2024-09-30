import requests
import time

from dataclasses import dataclass
from typing import Callable, Dict


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
    headers: Dict[str, str]

    def __init__(self, url: str, token: str) -> None:
        self.url = url
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        self._fetch_devices()

    def _fetch_devices(self) -> None:
        resp = requests.get(f"{self.url}/api/states", headers=self.headers)
        assert (
            resp.status_code == 200
        ), "it's so over didn't get 200 status from home assistant"

        self._lights = [
            self._create_light(device)
            for device in resp.json()
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
            hs_color=attributes.get("hs_color"),
        )

    def _toggle_light_power(self, entity_id: str) -> None:
        data = {"entity_id": entity_id}

        resp = requests.post(
            f"{self.url}/api/services/light/toggle", headers=self.headers, json=data
        )
        assert (
            resp.status_code == 200
        ), f"Couldn't change the state of ceiling lights, it's so over {resp=}"

    def _get_current_light_state(self, entity_id: str) -> Light:
        resp = requests.get(f"{self.url}/api/states/{entity_id}", headers=self.headers)
        assert (
            resp.status_code == 200
        ), f"Couldn't fetch the state of a light. It's joever. {resp=}"
        return self._create_light(resp.json())

    def toggle_ceiling_lights(self) -> None:
        state_to_bool: Callable[[str], bool] = lambda x: True if x == "on" else False
        old_light_state: Dict[str, Light] = {}
        spot_lights = [
            light for light in self._lights if "hue_ambiance_spot" in light.entity_id
        ]

        for _ in range(10):
            for light in spot_lights:
                old_light_state[light.entity_id] = light
                self._toggle_light_power(light.entity_id)
            time.sleep(1)

        # Check each light if it's state is not the same it was before then set it to that
        for light in spot_lights:
            old_state = state_to_bool(old_light_state[light.entity_id].state)
            current_state = state_to_bool(
                self._get_current_light_state(light.entity_id).state
            )

            if current_state != old_state:
                self._toggle_light_power(light.entity_id)

    def set_lights_red(self) -> None:
        old_ligth_state: list[Light] = []
        for light in self._lights:
            if (light.name != "studio" and light.entity_id != "light.bedroom") and (
                light.rgb_color or light.hs_color
            ):
                old_ligth_state.append(light)
                data = {
                    "entity_id": light.entity_id,
                    "rgb_color": [255, 0, 0],
                }

                resp = requests.post(
                    f"{self.url}/api/services/light/turn_on",
                    headers=self.headers,
                    json=data,
                )
                assert (
                    resp.status_code == 200
                ), f"Couldn't change light color to red :( {resp=}"
        time.sleep(5)
        for light in old_ligth_state:
            data = {
                "entity_id": light.entity_id,
                "rgb_color": light.rgb_color,
            }

            service = "turn_on" if light.state == "on" else "turn_off"
            resp = requests.post(
                f"{self.url}/api/services/light/{service}",
                headers=self.headers,
                json=data,
            )
            assert (
                resp.status_code == 200
            ), f"Couldn't change light color to red :( {resp=}"

    def thats_what_she_said(self) -> None:
        data = {
            "entity_id": "media_player.skys_room_display",
            "message": "That's what she said"
        }
        resp = requests.post(
            f"{self.url}/api/services/tts/google_translate_say",
            headers=self.headers,
            json=data,
        )
        assert (
            resp.status_code == 200
        ), f"Couldn't that's what she said, it's joever.{resp=}"
