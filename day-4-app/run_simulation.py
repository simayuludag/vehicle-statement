import yaml
import time
from vehicle_fsm import VehicleFSM, VehicleInputs

def run():
    fsm = VehicleFSM(dt=0.1)

    with open("normal_drive.yaml", "r") as f:
        scenario = yaml.safe_load(f)

    print(f"=== Senaryo Başlatılıyor: {scenario['metadata']['scenario']} ===\n")
    print(f"{'Zaman (s)':<10} | {'Durum':<15} | {'Hız (km/h)':<12} | {'RPM':<10} | {'Gaz (%)':<8} | {'Fren (%)':<8}")
    print("-" * 75)

    current_time = 0.0
    steps = sorted(scenario["steps"], key=lambda x: x["timestamp"])
    step_idx = 0
    current_input_data = steps[0]

    # 13 saniyelik simülasyonu 100ms adımlarla işlet
    while current_time <= 13.0:
        # Zamanı gelen yeni bir girdi var mı kontrol et
        if step_idx + 1 < len(steps) and current_time >= steps[step_idx + 1]["timestamp"]:
            step_idx += 1
            current_input_data = steps[step_idx]

        inputs = VehicleInputs(
            ignition=current_input_data.get("ignition", False),
            start_button=current_input_data.get("start_button", False),
            throttle=current_input_data.get("throttle", 0.0),
            brake=current_input_data.get("brake", 0.0),
            gear=current_input_data.get("gear", "P")
        )

        out = fsm.update(inputs)

        # Çıktıları her 0.5 saniyede bir veya durum değiştiğinde ekrana bas
        if round(current_time, 1) % 0.5 == 0:
            print(f"{current_time:<10.1f} | {out['state']:<15} | {out['speed_kmh']:<12.1f} | {out['rpm']:<10.1f} | {inputs.throttle:<8.1f} | {inputs.brake:<8.1f}")

        current_time = round(current_time + 0.1, 2)
        time.sleep(0.02)  # Simülasyonu görsel olarak izlemek için hafif gecikme

    print("-" * 75)
    print("Simülasyon başarıyla tamamlandı.")

if __name__ == "__main__":
    run()