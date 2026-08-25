"""
Otomotiv / Araç Simülatörü Veri Tipleri ve Temel Python Kavramları
"""
import math

# 1. Temel Tipler ve Araç Yazılımı Örnekleri
vehicle_speed: float = 88.5           # Araç hızı (km/h) - float
ignition_status: bool = True          # Kontak açık mı? - bool
gear_level: int = 4                   # Vites konumu - int
vin_number: str = "WVWZZZ1KZ9M000000" # Şasi numarası - str
sensor_fault: None = None             # Sensör arıza kodu (henüz arıza yok) - None

# 2. Liste (List) - Sinyal isimleri koleksiyonu
signal_names: list[str] = [
    "engine_rpm", 
    "vehicle_speed", 
    "battery_temp", 
    "tire_pressure"
]

# 3. Sözlük (Dictionary) - Sinyal adı ve birim eşleştirmesi
signal_units: dict[str, str] = {
    "engine_rpm": "RPM",
    "vehicle_speed": "km/h",
    "battery_temp": "°C",
    "tire_pressure": "bar"
}

# 4. Özel Sayısal Durumlar (NaN & Infinity)
corrupted_sensor_read: float = float("nan") # Hatalı sensör verisi (Not a Number)
infinite_resistance: float = float("inf")    # Açık devre sensör direnci (Sonsuz)


# -------------------------------------------------------------
# Kontrol ve Çıktılar
# -------------------------------------------------------------
if __name__ == "__main__":
    print("--- DEĞİŞKEN TİP KONTROLLERİ ---")
    print(f"vehicle_speed      : {vehicle_speed:<10} | Tip: {type(vehicle_speed)}")
    print(f"ignition_status    : {str(ignition_status):<10} | Tip: {type(ignition_status)}")
    print(f"gear_level         : {gear_level:<10} | Tip: {type(gear_level)}")
    print(f"vin_number         : {vin_number:<10} | Tip: {type(vin_number)}")
    print(f"sensor_fault       : {str(sensor_fault):<10} | Tip: {type(sensor_fault)}")
    
    print("\n--- KOLEKSİYONLAR ---")
    print(f"signal_names (list): {signal_names} | Tip: {type(signal_names)}")
    print(f"signal_units (dict): {signal_units} | Tip: {type(signal_units)}")
    
    print("\n--- ÖZEL DURUMLAR (NaN & Infinity) ---")
    print(f"corrupted_sensor_read (NaN)    : {corrupted_sensor_read} | isnan: {math.isnan(corrupted_sensor_read)}")
    print(f"infinite_resistance (Infinity) : {infinite_resistance} | isinf: {math.isinf(infinite_resistance)}")

    print("\n--- BOOL / INT İLİŞKİSİ ---")
    print(f"True + True = {True + True} (bool, int alt sınıfıdır)")