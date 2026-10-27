from unittest.mock import patch

from aeroplane import Aeroplane
from user_interaction import print_aeroplanes, user_interaction


def test_print_empty_list(capsys):
    """Тест вывода пустого списка."""
    print_aeroplanes([])
    captured = capsys.readouterr()
    assert "Нет самолетов" in captured.out


def test_print_aeroplanes(capsys):
    """Тест вывода самолетов в таблицу."""
    planes = [Aeroplane("a1", "CALL", "Spain", 100.0, 2000.0)]
    print_aeroplanes(planes)
    captured = capsys.readouterr()
    assert "CALL" in captured.out
    assert "Spain" in captured.out


@patch("builtins.input", side_effect=["", ""])  # Имитируем ввод пустой строки
def test_user_interaction_empty_country(mock_input, capsys):
    """Тест выхода из программы при пустом вводе страны."""
    user_interaction()
    captured = capsys.readouterr()
    assert "Пустой ввод" in captured.out


# Патчим ввод и API, чтобы не делать реальных запросов
@patch("user_interaction.AeroplanesAPI")
@patch("user_interaction.JSONSaver")
@patch("builtins.input", side_effect=["Spain", "1", "", ""])
def test_user_interaction_happy_path(mock_input, mock_saver, mock_api, capsys):
    """Тест полного успешного цикла программы."""

    # Настраиваем фейковый API
    mock_api_instance = mock_api.return_value
    mock_api_instance.get_aeroplanes.return_value = [
        {"icao24": "a1", "callsign": "CALL", "origin_country": "Spain", "velocity": 100.0, "baro_altitude": 2000.0}
    ]

    user_interaction()
    captured = capsys.readouterr()

    # Проверяем, что программа дошла до вывода
    assert "Найдено самолетов: 1" in captured.out
    assert "Топ 1" in captured.out
    mock_saver.return_value.add_aeroplane.assert_called()  # Проверяем, что сохранение было вызвано
