import pytest
from aeroplane import Aeroplane
from services import (
    filter_by_altitude_range,
    filter_by_origin_country,
    get_top_n,
    sort_by_altitude_desc,
)


# Вспомогательная функция для быстрого создания самолетиков в тестах
def create_plane(icao, country, alt, vel=100.0):
    return Aeroplane(icao, "CALL", country, vel, alt)


def test_filter_by_origin_country():
    planes = [
        create_plane("a1", "Spain", 100),
        create_plane("a2", "France", 200),
        create_plane("a3", "Spain", 300),
    ]
    # Ищем по Испании
    result = filter_by_origin_country(planes, ["Spain"])
    assert len(result) == 2
    assert result[0].icao24 == "a1"
    assert result[1].icao24 == "a3"

    # Пустой список стран возвращает всех
    assert len(filter_by_origin_country(planes, [])) == 3


def test_filter_by_altitude_range():
    planes = [
        create_plane("a1", "Spain", 500),
        create_plane("a2", "France", 5000),
        create_plane("a3", "Spain", 20000),
    ]
    result = filter_by_altitude_range(planes, 1000, 10000)
    assert len(result) == 1
    assert result[0].icao24 == "a2"

    # Некорректный диапазон
    with pytest.raises(ValueError):
        filter_by_altitude_range(planes, 10000, 1000)


def test_sort_by_altitude_desc():
    planes = [
        create_plane("a1", "X", 100),
        create_plane("a2", "X", 9000),
        create_plane("a3", "X", 500),
    ]
    sorted_planes = sort_by_altitude_desc(planes)
    # Должны идти по убыванию: 9000, 500, 100
    assert [p.icao24 for p in sorted_planes] == ["a2", "a3", "a1"]


def test_get_top_n():
    planes = [
        create_plane("a1", "X", 100),
        create_plane("a2", "X", 9000),
        create_plane("a3", "X", 500),
    ]
    top_2 = get_top_n(planes, 2)
    assert len(top_2) == 2
    assert top_2[0].icao24 == "a2"  # Самый высокий
    assert top_2[1].icao24 == "a3"

    # Проверка на N <= 0
    with pytest.raises(ValueError):
        get_top_n(planes, 0)
