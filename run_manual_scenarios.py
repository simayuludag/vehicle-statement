"""
VehicleState Manuel Senaryo Testleri
"""
import sys
from pathlib import Path

# Proje kaynak dizinini Python yoluna ekle
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from vehicle_simulator.vehicle_state import VehicleState

scenarios = [
    (
        "Senaryo 1 — Park halindeki araç",
        lambda: VehicleState(
            ignition_on=False, engine_running=False, speed_kph=0.0, engine_rpm=0
        ),
    ),
    (
        "Senaryo 2 — Rölantide çalışan araç",
        lambda: VehicleState(
            ignition_on=True,
            engine_running=True,
            speed_kph=0.0,
            engine_rpm=800,
            coolant_temp_c=20.0,
        ),
    ),
    (
        "Senaryo 3 — Hareket eden araç",
        lambda: VehicleState(
            ignition_on=True,
            engine_running=True,
            speed_kph=50.0,
            engine_rpm=2200,
            throttle_percent=30.0,
            brake_percent=0.0,
        ),
    ),
    (
        "Senaryo 4 — Negatif hız",
        lambda: VehicleState(speed_kph=-10.0),
    ),
    (
        "Senaryo 5 — Geçersiz pedal",
        lambda: VehicleState(throttle_percent=120.0),
    ),
    (
        "Senaryo 6 — Tutarsız motor durumu",
        lambda: VehicleState(
            ignition_on=True, engine_running=False, engine_rpm=2000
        ),
    ),
]

print("=" * 60)
print("MANUEL SENARYO TESTLERİ BAŞLATILIYOR")
print("=" * 60)

for title, scenario_func in scenarios:
    print(f"\n▶ {title}")
    try:
        state = scenario_func()
        print("  [KABUL EDİLDİ] Nesne başarıyla oluşturuldu:")
        print(f"  {state}")
    except (ValueError, TypeError) as err:
        print(f"  [REDDEDİLDİ] Beklenen hata yakalandı ({type(err).__name__}):")
        print(f"  \"{err}\"")

print("\n" + "=" * 60)
print("TÜM SENARYOLAR ÇALIŞTIRILDI")
print("=" * 60)