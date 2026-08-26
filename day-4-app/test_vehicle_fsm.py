import pytest
from vehicle_fsm import VehicleFSM, State, VehicleInputs

def test_initial_state():
    fsm = VehicleFSM()
    assert fsm.state == State.OFF
    assert fsm.rpm == 0.0
    assert fsm.speed == 0.0

def test_ignition_and_start_guard():
    fsm = VehicleFSM()
    
    # 1. Kontak açılır
    fsm.update(VehicleInputs(ignition=True))
    assert fsm.state == State.IGNITION_ON
    assert fsm.rpm == 0.0
    
    # 2. Frene basmadan marşa basılırsa motor çalışmamalı (Guard testi)
    fsm.update(VehicleInputs(ignition=True, start_button=True, brake=0.0))
    assert fsm.state == State.IGNITION_ON
    assert fsm.rpm == 0.0

    # 3. Frenle birlikte marşa basılırsa ENGINE_RUNNING olmalı (Kabul Kriteri: Rölantiye çıkış)
    fsm.update(VehicleInputs(ignition=True, start_button=True, brake=25.0))
    assert fsm.state == State.ENGINE_RUNNING
    assert fsm.rpm == 800.0

def test_throttle_increases_rpm_and_speed():
    fsm = VehicleFSM()
    # Çalıştırma sekansı
    fsm.update(VehicleInputs(ignition=True))
    fsm.update(VehicleInputs(ignition=True, start_button=True, brake=25.0))
    
    # Gaz verme
    for _ in range(20):  # 2 saniye boyunca gaz ver
        fsm.update(VehicleInputs(ignition=True, throttle=50.0, brake=0.0, gear="D"))
    
    assert fsm.state == State.DRIVING
    assert fsm.speed > 0.0
    assert fsm.rpm > 800.0

def test_engine_off_rpm_returns_to_zero():
    """Kabul Kriteri: Motor kapalıyken RPM sıfıra dönmelidir."""
    fsm = VehicleFSM()
    fsm.update(VehicleInputs(ignition=True))
    fsm.update(VehicleInputs(ignition=True, start_button=True, brake=30.0))
    assert fsm.rpm == 800.0
    
    # Kontak kapatma
    fsm.update(VehicleInputs(ignition=False))  # SHUTDOWN
    fsm.update(VehicleInputs(ignition=False))  # OFF
    
    assert fsm.state == State.OFF
    assert fsm.rpm == 0.0
    assert fsm.speed == 0.0

def test_determinism_repeatability():
    """Kabul Kriteri: Aynı senaryo her çalıştırmada tekrar üretilebilir olmalıdır."""
    scenario = [
        VehicleInputs(ignition=True),
        VehicleInputs(ignition=True, start_button=True, brake=30.0),
        VehicleInputs(ignition=True, throttle=40.0, brake=0.0, gear="D"),
        VehicleInputs(ignition=True, throttle=40.0, brake=0.0, gear="D"),
        VehicleInputs(ignition=True, throttle=0.0, brake=50.0, gear="D"),
    ]

    def run_cycle():
        f = VehicleFSM()
        return [f.update(inp) for inp in scenario]

    run_1 = run_cycle()
    run_2 = run_cycle()

    assert run_1 == run_2

