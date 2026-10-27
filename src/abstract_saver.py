from abc import ABC, abstractmethod
from typing import Any

from aeroplane import Aeroplane


class AbstractSaver(ABC):
    """Абстрактный интерфейс для работы с хранилищем самолетов."""

    @abstractmethod
    def add_aeroplane(self, aeroplane: Aeroplane) -> None:
        """Добавляет самолет в хранилище."""
        pass

    @abstractmethod
    def get_aeroplanes(
        self, criteria: dict[str, Any] | None = None
    ) -> list[Aeroplane]:
        """Возвращает самолеты по указанным критериям (или все)."""
        pass

    @abstractmethod
    def delete_aeroplane(self, aeroplane: Aeroplane) -> None:
        """Удаляет самолет из хранилища."""
        pass
