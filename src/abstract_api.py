from abc import ABC, abstractmethod
from typing import Any

import requests


class AbstractAPI(ABC):
    """Абстрактный класс для работы с API сервисов."""

    @abstractmethod
    def _connect(self) -> requests.Session:
        """Создает HTTP-сессию для работы с API."""
        pass

    @abstractmethod
    def _get_response(self, url: str, params: dict[str, Any]) -> Any:
        """Выполняет GET-запрос и возвращает разобранный JSON."""
        pass

    @abstractmethod
    def get_country_bounding_box(self, country: str) -> tuple[float, float, float, float]:
        """Возвращает координаты страны (юг, север, запад, восток)."""
        pass

    @abstractmethod
    def get_aeroplanes(self, country: str) -> list[dict[str, Any]]:
        """Возвращает список самолетов над территорией страны."""
        pass
