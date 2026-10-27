from typing import Any

import requests

from abstract_api import AbstractAPI

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
OPENSKY_URL = "https://opensky-network.org/api/states/all"

# Ключи для расшифровки ответа от OpenSky
_STATES_KEYS = (
    "icao24",
    "callsign",
    "origin_country",
    "time_position",
    "last_contact",
    "longitude",
    "latitude",
    "baro_altitude",
    "on_ground",
    "velocity",
    "true_track",
    "vertical_rate",
    "sensors",
    "geo_altitude",
    "squawk",
    "spi",
    "position_source",
)


class AeroplanesAPI(AbstractAPI):
    """Реализация API для Nominatim и OpenSky."""

    USER_AGENT = "course-project/0.1 (katkova.a1997@gmail.com)"

    def _connect(self) -> requests.Session:
        session = requests.Session()
        session.headers.update({"User-Agent": self.USER_AGENT})
        return session

    def _get_response(self, url: str, params: dict[str, Any]) -> Any:
        session = self._connect()
        try:
            response = session.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as exc:
            raise ConnectionError(f"Ошибка при запросе к {url}: {exc}") from exc
        finally:
            session.close()

    def get_country_bounding_box(self, country: str) -> tuple[float, float, float, float]:
        data = self._get_response(NOMINATIM_URL, {"q": country, "format": "json", "limit": 1})
        if not data:
            raise ValueError(f"Страна {country!r} не найдена")

        bbox = data[0].get("boundingbox")
        if not bbox or len(bbox) != 4:
            raise ValueError(f"Некорректный boundingbox: {bbox}")

        south, north, west, east = (float(x) for x in bbox)
        return south, north, west, east

    def get_aeroplanes(self, country: str) -> list[dict[str, Any]]:
        south, north, west, east = self.get_country_bounding_box(country)

        data = self._get_response(
            OPENSKY_URL,
            {"lamin": south, "lamax": north, "lomin": west, "lomax": east},
        )

        states = data.get("states") or []
        return [dict(zip(_STATES_KEYS, state)) for state in states]
