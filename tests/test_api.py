from unittest.mock import patch
import pytest
import requests
from api import AeroplanesAPI


def test_get_country_bounding_box_success():
    """Тест получения координат страны (имитация ответа API)."""
    api = AeroplanesAPI()
    # Подменяем реальный запрос фейковым ответом
    with patch.object(AeroplanesAPI, "_get_response") as mock_get:
        mock_get.return_value = [{"boundingbox": ["10.0", "20.0", "30.0", "40.0"]}]

        result = api.get_country_bounding_box("Spain")
        assert result == (10.0, 20.0, 30.0, 40.0)


def test_get_country_not_found():
    """Тест, если страна не найдена."""
    api = AeroplanesAPI()
    with patch.object(AeroplanesAPI, "_get_response") as mock_get:
        mock_get.return_value = []  # Пустой ответ от Nominatim

        with pytest.raises(ValueError, match="не найдена"):
            api.get_country_bounding_box("Atlantis")


def test_get_aeroplanes_success():
    """Тест получения самолетов (имитация ответа OpenSky)."""
    api = AeroplanesAPI()

    # Имитируем два запроса: сначала координаты, потом сами самолеты
    with patch.object(AeroplanesAPI, "_get_response") as mock_get:
        mock_get.side_effect = [
            [{"boundingbox": ["1", "2", "3", "4"]}],  # Ответ 1 (Nominatim)
            {"states": [["icao123", "CALL", "Spain", 0, 0, 0, 0, 1000, False, 200, 0, 0, None, 1000, "0000", False, 0]]}
            # Ответ 2 (OpenSky)
        ]

        planes = api.get_aeroplanes("Spain")
        assert len(planes) == 1
        assert planes[0]["icao24"] == "icao123"


def test_get_response_connection_error():
    """Тест обработки ошибки сети."""
    api = AeroplanesAPI()

    # Имитируем ошибку сети при запросе
    with patch("requests.Session.get", side_effect=requests.RequestException("Boom")):
        with pytest.raises(ConnectionError):
            api._get_response("http://fake-url.com", {})
