def celsius_to_fahrenheit(celsius: float) -> float:
    return round(celsius * 9 / 5 + 32, 2)

def is_valid_celsius(celsius: float) -> bool:
    return -273.15 <= celsius <= 1_000_000