from aeroplane import Aeroplane


def filter_by_origin_country(aeroplanes: list[Aeroplane], countries: list[str]) -> list[Aeroplane]:
    """Оставляет самолеты, чья страна регистрации входит в список countries."""
    if not countries:
        return aeroplanes

    # Приводим к нижнему регистру для удобного поиска
    wanted = {c.strip().lower() for c in countries if c.strip()}
    return [a for a in aeroplanes if a.origin_country.lower() in wanted]


def filter_by_altitude_range(aeroplanes: list[Aeroplane], min_altitude: float, max_altitude: float) -> list[Aeroplane]:
    """Оставляет самолеты, чья высота в диапазоне [min, max]."""
    if min_altitude > max_altitude:
        raise ValueError("Минимальная высота не может быть больше максимальной")

    return [a for a in aeroplanes if min_altitude <= a.baro_altitude <= max_altitude]


def sort_by_altitude_desc(aeroplanes: list[Aeroplane]) -> list[Aeroplane]:
    """Сортирует самолеты по убыванию высоты полета."""
    return sorted(aeroplanes, key=lambda a: a.baro_altitude, reverse=True)


def get_top_n(aeroplanes: list[Aeroplane], n: int) -> list[Aeroplane]:
    """Возвращает топ-N самолетов по высоте (сортировка DESC)."""
    if n <= 0:
        raise ValueError("Количество самолетов (N) должно быть положительным")

    return sort_by_altitude_desc(aeroplanes)[:n]
