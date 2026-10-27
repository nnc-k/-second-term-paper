from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from abstract_saver import AbstractSaver
from aeroplane import Aeroplane

# По умолчанию сохраняем в папку data, которую мы создали на первом шаге
_DEFAULT_PATH = Path("data/aeroplanes.json")


class JSONSaver(AbstractSaver):
    """Сохраняет информацию о самолетах в JSON-файл."""

    def __init__(self, path: str | Path = _DEFAULT_PATH) -> None:
        self.__path = Path(path)
        # Создаем папку, если ее нет
        self.__path.parent.mkdir(parents=True, exist_ok=True)
        # Если файла нет, создаем пустой список
        if not self.__path.exists():
            self.__path.write_text("[]", encoding="utf-8")

    def _load(self) -> list[dict[str, Any]]:
        """Читает данные из файла."""
        try:
            return json.loads(self.__path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as exc:
            raise ValueError(f"Не удалось прочитать файл {self.__path}: {exc}") from exc

    def _dump(self, data: list[dict[str, Any]]) -> None:
        """Записывает данные в файл."""
        self.__path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    def add_aeroplane(self, aeroplane: Aeroplane) -> None:
        data = self._load()
        record = aeroplane.to_dict()
        # Защита от дубликатов
        if record not in data:
            data.append(record)
            self._dump(data)

    def get_aeroplanes(
        self, criteria: dict[str, Any] | None = None
    ) -> list[Aeroplane]:
        data = self._load()
        if criteria:
            # Фильтруем словари по ключам (например, по стране регистрации)
            data = [
                d
                for d in data
                if all(d.get(key) == value for key, value in criteria.items())
            ]
        # Превращаем обратно в объекты Aeroplane
        return Aeroplane.cast_to_object_list(data)

    def delete_aeroplane(self, aeroplane: Aeroplane) -> None:
        data = self._load()
        record = aeroplane.to_dict()
        if record in data:
            data.remove(record)
            self._dump(data)
