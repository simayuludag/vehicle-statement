"""
Araç Simülatörü ve Telemetri Sinyal Sınırları Sabitleri
"""

# Hız Sınırları (km/h)
MIN_SPEED_KPH: float = 0.0
MAX_SPEED_KPH: float = 250.0

# Motor Devri Sınırları (RPM)
MIN_ENGINE_RPM: int = 0
MAX_ENGINE_RPM: int = 8000
IDLE_ENGINE_RPM: int = 800

# Soğutma Sıvısı Sıcaklık Sınırları (°C)
MIN_COOLANT_TEMP_C: float = -40.0
MAX_COOLANT_TEMP_C: float = 150.0
INITIAL_COOLANT_TEMP_C: float = 20.0

# Yüzdelik Sinyal Sınırları (%)
MIN_PERCENTAGE: float = 0.0
MAX_PERCENTAGE: float = 100.0

# Yakıt Seviyesi Sınırları (%)
MIN_FUEL_PERCENT: float = MIN_PERCENTAGE
MAX_FUEL_PERCENT: float = MAX_PERCENTAGE
INITIAL_FUEL_PERCENT: float = 100.0

# Pedal Sınırları (%)
MIN_THROTTLE_PERCENT: float = MIN_PERCENTAGE
MAX_THROTTLE_PERCENT: float = MAX_PERCENTAGE
MIN_BRAKE_PERCENT: float = MIN_PERCENTAGE
MAX_BRAKE_PERCENT: float = MAX_PERCENTAGE