"""
Sinyal Doğrulama (Validation) Kuralları
"""
from vehicle_simulator.constants import (
    MAX_COOLANT_TEMP_C,
    MAX_ENGINE_RPM,
    MAX_PERCENTAGE,
    MAX_SPEED_KPH,
    MIN_COOLANT_TEMP_C,
    MIN_ENGINE_RPM,
    MIN_PERCENTAGE,
    MIN_SPEED_KPH,
)


def validate_speed(speed: float) -> None:
    """
    Parametreler: speed (float) - Araç hızı.
    Dönüş Değeri: Yok (None).
    Geçersiz Durum: Değer belirlenen sınırlar dışındaysa ValueError fırlatır.
    """
    if not (MIN_SPEED_KPH <= speed <= MAX_SPEED_KPH):
        raise ValueError(
            f"Geçersiz hız değeri: speed_kph={speed} km/h. "
            f"Beklenen aralık: [{MIN_SPEED_KPH}, {MAX_SPEED_KPH}] km/h."
        )


def validate_percentage(signal_name: str, value: float) -> None:
    """
    Parametreler: signal_name (str) - Sinyal adı, value (float) - Yüzdelik değer.
    Dönüş Değeri: Yok (None).
    Geçersiz Durum: Değer %0 - %100 dışındaysa ValueError fırlatır.
    """
    if not (MIN_PERCENTAGE <= value <= MAX_PERCENTAGE):
        raise ValueError(
            f"Geçersiz {signal_name} değeri: {value} %. "
            f"Beklenen aralık: [{MIN_PERCENTAGE}, {MAX_PERCENTAGE}] %."
        )


def validate_temperature(signal_name: str, temperature: float) -> None:
    """
    Parametreler: signal_name (str) - Sinyal adı, temperature (float) - Sıcaklık.
    Dönüş Değeri: Yok (None).
    Geçersiz Durum: Değer operasyonel sıcaklık sınırları dışındaysa ValueError fırlatır.
    """
    if not (MIN_COOLANT_TEMP_C <= temperature <= MAX_COOLANT_TEMP_C):
        raise ValueError(
            f"Geçersiz {signal_name} sıcaklığı: {temperature} °C. "
            f"Beklenen aralık: [{MIN_COOLANT_TEMP_C}, {MAX_COOLANT_TEMP_C}] °C."
        )


def validate_rpm(rpm: int) -> None:
    """
    Parametreler: rpm (int) - Motor devir hızı.
    Dönüş Değeri: Yok (None).
    Geçersiz Durum: Değer belirlenen RPM limitleri dışındaysa ValueError fırlatır.
    """
    if not (MIN_ENGINE_RPM <= rpm <= MAX_ENGINE_RPM):
        raise ValueError(
            f"Geçersiz motor devri: engine_rpm={rpm} RPM. "
            f"Beklenen aralık: [{MIN_ENGINE_RPM}, {MAX_ENGINE_RPM}] RPM."
        )