"""
Araç Durum Modeli (Vehicle State Model)
"""
from dataclasses import dataclass
from vehicle_simulator.constants import (
    INITIAL_COOLANT_TEMP_C,
    INITIAL_FUEL_PERCENT,
    MIN_BRAKE_PERCENT,
    MIN_ENGINE_RPM,
    MIN_SPEED_KPH,
    MIN_THROTTLE_PERCENT,
)
from vehicle_simulator.validation import (
    validate_percentage,
    validate_rpm,
    validate_speed,
    validate_temperature,
)


@dataclass
class VehicleState:
    """
    Aracın anlık telemetri durumunu temsil eden veri modeli.

    Birimler:
    - speed_kph: km/h (Kilometre / Saat)
    - engine_rpm: RPM (Devir / Dakika)
    - coolant_temp_c: °C (Derece Celsius)
    - fuel_percent: % (0.0 - 100.0)
    - throttle_percent: % (0.0 - 100.0)
    - brake_percent: % (0.0 - 100.0)
    """

    ignition_on: bool = False
    engine_running: bool = False
    speed_kph: float = MIN_SPEED_KPH
    engine_rpm: int = MIN_ENGINE_RPM
    coolant_temp_c: float = INITIAL_COOLANT_TEMP_C
    fuel_percent: float = INITIAL_FUEL_PERCENT
    throttle_percent: float = MIN_THROTTLE_PERCENT
    brake_percent: float = MIN_BRAKE_PERCENT

    def __post_init__(self) -> None:
        """Nesne ilk üretildiğinde başlangıç değerlerini doğrular."""
        self.validate()

    def validate(self) -> None:
        """
        Tüm sinyal sınırlarını ve mantıksal kuralları doğrular.
        Geçersiz bir durum varsa ilgili Exception fırlatılır.
        """
        # 1. Tip Kontrolleri (bool vs int koruması)
        if not isinstance(self.ignition_on, bool):
            raise TypeError("ignition_on alanı bool tipinde olmalıdır.")
        if not isinstance(self.engine_running, bool):
            raise TypeError("engine_running alanı bool tipinde olmalıdır.")

        # 2. Mantıksal Durum İlişkisi
        if not self.ignition_on and self.engine_running:
            raise ValueError("Kontak kapalıyken (ignition_on=False) motor çalışamaz.")

        # 3. Sayısal Sinyal Validasyonları
        validate_speed(self.speed_kph)
        validate_rpm(self.engine_rpm)
        validate_temperature("coolant_temp_c", self.coolant_temp_c)
        validate_percentage("fuel_percent", self.fuel_percent)
        validate_percentage("throttle_percent", self.throttle_percent)
        validate_percentage("brake_percent", self.brake_percent)