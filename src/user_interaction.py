from __future__ import annotations

from aeroplane import Aeroplane
from api import AeroplanesAPI
from json_saver import JSONSaver
from services import (
    filter_by_altitude_range,
    filter_by_origin_country,
    get_top_n,
)


def print_aeroplanes(aeroplanes: list[Aeroplane]) -> None:
    """Красиво выводит список самолетов в консоль."""
    if not aeroplanes:
        print("Нет самолетов для отображения.")
        return

    # Форматируем заголовок таблицы
    header = f"{'Позывной':<12}{'Страна':<25}{'Скорость':>10}{'Высота':>12}"
    print(header)
    print("-" * len(header))

    for a in aeroplanes:
        # Выводим данные ровными столбцами
        print(f"{a.callsign:<12}{a.origin_country:<25}" f"{a.velocity:>10.1f}{a.baro_altitude:>12.1f}")


def user_interaction() -> None:
    """Главная функция общения с пользователем через консоль."""
    print("=== Сбор данных о самолетах ===")
    country = input("Введите название страны на английском (например, Spain): ").strip()

    if not country:
        print("Пустой ввод, выходим.")
        return

    # 1. Получаем данные из API
    api = AeroplanesAPI()
    try:
        raw_data = api.get_aeroplanes(country)
    except (ConnectionError, ValueError) as exc:
        print(f"Ошибка при получении данных: {exc}")
        return

    aeroplanes = Aeroplane.cast_to_object_list(raw_data)
    print(f"\nНайдено самолетов: {len(aeroplanes)}")

    if not aeroplanes:
        return

    # 2. Сохраняем в JSON
    saver = JSONSaver()
    for a in aeroplanes:
        saver.add_aeroplane(a)
    print("Данные успешно сохранены в файл data/aeroplanes.json\n")

    # 3. Топ N самолетов по высоте
    try:
        n = int(input("Введите количество самолетов для вывода в топ N: "))
        top = get_top_n(aeroplanes, n)
        print(f"\n=== Топ {n} самолетов по высоте ===")
        print_aeroplanes(top)
    except ValueError as e:
        print(f"Некорректный ввод для топа: {e}")

    # 4. Фильтрация по стране регистрации
    countries_input = input("\nВведите страны регистрации через запятую (Enter - пропустить): ").strip()
    if countries_input:
        countries = [c.strip() for c in countries_input.split(",")]
        filtered = filter_by_origin_country(aeroplanes, countries)
        print("\n=== Самолеты по стране регистрации ===")
        print_aeroplanes(filtered)

    # 5. Фильтрация по высоте
    range_input = input("\nВведите диапазон высот (например 1000-12000, Enter - пропустить): ").strip()
    if range_input:
        try:
            lo, hi = (float(x) for x in range_input.split("-", 1))
            ranged = filter_by_altitude_range(aeroplanes, lo, hi)
            print("\n=== Самолеты в диапазоне высот ===")
            print_aeroplanes(ranged)
        except ValueError:
            print("Некорректный диапазон, пропускаем этот шаг.")


# Точка входа для запуска
if __name__ == "__main__":
    user_interaction()
