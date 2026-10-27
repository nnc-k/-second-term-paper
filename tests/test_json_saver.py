import pytest

from aeroplane import Aeroplane
from json_saver import JSONSaver


def create_plane(icao="a1"):
    return Aeroplane(icao, "CALL", "Spain", 100.0, 1000.0)


def test_add_and_get(tmp_path):
    """Тест добавления и получения самолета."""
    file_path = tmp_path / "test_aeroplanes.json"
    saver = JSONSaver(file_path)

    plane = create_plane()
    saver.add_aeroplane(plane)

    saved_planes = saver.get_aeroplanes()
    assert len(saved_planes) == 1
    assert saved_planes[0].icao24 == "a1"


def test_add_duplicate(tmp_path):
    """Тест защиты от дубликатов (один и тот же самолет не добавится дважды)."""
    file_path = tmp_path / "test_aeroplanes.json"
    saver = JSONSaver(file_path)

    plane = create_plane()
    saver.add_aeroplane(plane)
    saver.add_aeroplane(plane)  # Добавляем второй раз

    assert len(saver.get_aeroplanes()) == 1


def test_get_with_criteria(tmp_path):
    """Тест фильтрации при чтении из файла."""
    file_path = tmp_path / "test_aeroplanes.json"
    saver = JSONSaver(file_path)

    saver.add_aeroplane(Aeroplane("a1", "X", "Spain", 100.0, 1000.0))
    saver.add_aeroplane(Aeroplane("a2", "Y", "France", 100.0, 1000.0))

    filtered = saver.get_aeroplanes({"origin_country": "Spain"})
    assert len(filtered) == 1
    assert filtered[0].icao24 == "a1"


def test_delete(tmp_path):
    """Тест удаления самолета из файла."""
    file_path = tmp_path / "test_aeroplanes.json"
    saver = JSONSaver(file_path)

    plane = create_plane()
    saver.add_aeroplane(plane)
    saver.delete_aeroplane(plane)

    assert len(saver.get_aeroplanes()) == 0


def test_invalid_json_raises_error(tmp_path):
    """Тест обработки ошибки, если файл поврежден."""
    file_path = tmp_path / "broken.json"
    file_path.write_text("{invalid json", encoding="utf-8")

    saver = JSONSaver(file_path)
    with pytest.raises(ValueError, match="Не удалось прочитать файл"):
        saver.get_aeroplanes()
