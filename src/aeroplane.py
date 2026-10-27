from __future__ import annotations

from functools import total_ordering
from typing import Any


@total_ordering
class Aeroplane:
    """Модель самолета с инкапсулированными атрибутами."""

    # Ограничиваем набор атрибутов (оптимизация памяти и защита)
    __slots__ = (
        "__icao24",
        "__callsign",
        "__origin_country",
        "__velocity",
        "__baro_altitude",
        "__on_ground",
    )

    def __init__(
        self,
        icao24: str,
        callsign: str,
        origin_country: str,
        velocity: float | None,
        baro_altitude: float | None,
        on_ground: bool = False,
    ) -> None:
        # Валидация данных
        if not icao24 or not isinstance(icao24, str):
            raise ValueError("icao24 должен быть непустой строкой")
        if velocity is not None and velocity < 0:
            raise ValueError("Скорость (velocity) не может быть отрицательной")
        if baro_altitude is not None and baro_altitude < -500:
            raise ValueError("Высота (baro_altitude) вне допустимого диапазона")

        # Приватные атрибуты (инкапсуляция)
        self.__icao24 = icao24
        self.__callsign = (callsign or "").strip()
        self.__origin_country = origin_country or ""
        self.__velocity = float(velocity) if velocity is not None else 0.0
        self.__baro_altitude = float(baro_altitude) if baro_altitude is not None else 0.0
        self.__on_ground = bool(on_ground)

    # Свойства (геттеры) для доступа к приватным атрибутам
    @property
    def icao24(self) -> str:
        return self.__icao24

    @property
    def callsign(self) -> str:
        return self.__callsign

    @property
    def origin_country(self) -> str:
        return self.__origin_country

    @property
    def velocity(self) -> float:
        return self.__velocity

    @property
    def baro_altitude(self) -> float:
        return self.__baro_altitude

    @property
    def on_ground(self) -> bool:
        return self.__on_ground

    def to_dict(self) -> dict[str, Any]:
        """Превращает объект в словарь (пригодится для сохранения в JSON)."""
        return {
            "icao24": self.__icao24,
            "callsign": self.__callsign,
            "origin_country": self.__origin_country,
            "velocity": self.__velocity,
            "baro_altitude": self.__baro_altitude,
            "on_ground": self.__on_ground,
        }

    def __repr__(self) -> str:
        return (
            f"Aeroplane(icao24={self.__icao24!r}, callsign={self.__callsign!r}, "
            f"origin_country={self.__origin_country!r}, "
            f"velocity={self.__velocity}, baro_altitude={self.__baro_altitude})"
        )

    # --- МЕТОДЫ СРАВНЕНИЯ (по заданию) ---

    def __eq__(self, other: object) -> bool:
        """Сравнение на равенство по уникальному номеру (icao24)."""
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return self.__icao24 == other.__icao24

    def __hash__(self) -> int:
        return hash(self.__icao24)

    def __lt__(self, other: object) -> bool:
        """Сравнение 'меньше' по высоте полета."""
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return self.__baro_altitude < other.__baro_altitude

    def is_faster_than(self, other: Aeroplane) -> bool:
        """Возвращает True, если этот самолет быстрее другого."""
        return self.__velocity > other.__velocity

    def is_higher_than(self, other: Aeroplane) -> bool:
        """Возвращает True, если этот самолет летит выше другого."""
        return self.__baro_altitude > other.__baro_altitude

    # --- МЕТОД ДЛЯ ПРЕВРАЩЕНИЯ СПИСКА ИЗ API ---

    @classmethod
    def cast_to_object_list(cls, raw_data: list[dict[str, Any]]) -> list[Aeroplane]:
        """Преобразует сырые данные из API в список объектов Aeroplane."""
        aeroplanes = []
        for item in raw_data:
            # Пропускаем записи без уникального номера
            if not item.get("icao24"):
                continue

            aeroplanes.append(
                cls(
                    icao24=item["icao24"],
                    callsign=item.get("callsign", ""),
                    origin_country=item.get("origin_country", ""),
                    velocity=item.get("velocity"),
                    baro_altitude=item.get("baro_altitude"),
                    on_ground=item.get("on_ground", False),
                )
            )
        return aeroplanes
