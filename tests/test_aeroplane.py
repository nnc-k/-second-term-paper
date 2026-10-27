import pytest

from aeroplane import Aeroplane


def test_init_valid_data():
    """Проверка создания объекта с корректными данными."""
    plane = Aeroplane("abc123", "UAL1621", "United States", 250.0, 10000.0)
    assert plane.icao24 == "abc123"
    assert plane.callsign == "UAL1621"
    assert plane.origin_country == "United States"
    assert plane.velocity == 250.0
    assert plane.baro_altitude == 10000.0


def test_init_invalid_velocity():
    """Проверка валидации скорости (не может быть отрицательной)."""
    with pytest.raises(ValueError, match="Скорость"):
        Aeroplane("a1", "X", "Y", -10, 1000)


def test_init_invalid_altitude():
    """Проверка валидации высоты (не может быть меньше -500)."""
    with pytest.raises(ValueError, match="Высота"):
        Aeroplane("a1", "X", "Y", 100, -1000)


def test_init_empty_icao24():
    """Проверка валидации уникального номера."""
    with pytest.raises(ValueError, match="icao24"):
        Aeroplane("", "X", "Y", 100, 1000)


def test_comparison_methods():
    """Проверка методов сравнения (высота и скорость)."""
    plane1 = Aeroplane("a1", "X", "Y", 200.0, 5000.0)
    plane2 = Aeroplane("a2", "Z", "W", 300.0, 10000.0)

    # Сравнение по высоте (__lt__, __gt__)
    assert plane1 < plane2
    assert plane2 > plane1

    # Сравнение по скорости (is_faster_than)
    assert plane2.is_faster_than(plane1)
    assert not plane1.is_faster_than(plane2)

    # Сравнение по высоте (is_higher_than)
    assert plane2.is_higher_than(plane1)


def test_equality():
    """Два самолета равны, если у них одинаковый icao24."""
    plane1 = Aeroplane("a1", "X", "Y", 200.0, 5000.0)
    plane2 = Aeroplane("a1", "Z", "W", 300.0, 10000.0)
    assert plane1 == plane2


def test_cast_to_object_list():
    """Проверка преобразования сырых данных из API в объекты."""
    raw_data = [
        {"icao24": "a1", "callsign": "CALL", "origin_country": "Spain", "velocity": 200, "baro_altitude": 1000},
        {"icao24": "a2", "callsign": None, "origin_country": "France", "velocity": None, "baro_altitude": None},
        {"callsign": "NO_ICAO", "origin_country": "Germany"},  # Без icao24 должен отфильтроваться
    ]
    planes = Aeroplane.cast_to_object_list(raw_data)
    assert len(planes) == 2
    assert planes[0].callsign == "CALL"
    assert planes[1].velocity == 0.0  # None заменился на 0.0
