"""
VehicleState Modeli ve Validasyon Kuralları Birim Testleri
"""
import pytest
from vehicle_simulator.constants import (
    INITIAL_COOLANT_TEMP_C,
    INITIAL_FUEL_PERCENT,
    MAX_COOLANT_TEMP_C,
    MAX_ENGINE_RPM,
    MAX_SPEED_KPH,
    MIN_COOLANT_TEMP_C,
    MIN_ENGINE_RPM,
    MIN_SPEED_KPH,
)
from vehicle_simulator.vehicle_state import VehicleState


def test_vehicle_state_default_values():
    """Varsayılan değerlerle oluşturulan durumun doğruluğunu test eder."""
    state = VehicleState()

    assert state.ignition_on is False
    assert state.engine_running is False
    assert state.speed_kph == MIN_SPEED_KPH
    assert state.engine_rpm == MIN_ENGINE_RPM
    assert state.coolant_temp_c == INITIAL_COOLANT_TEMP_C
    assert state.fuel_percent == INITIAL_FUEL_PERCENT
    assert state.throttle_percent == 0.0
    assert state.brake_percent == 0.0


def test_vehicle_state_valid_custom_values():
    """Geçerli özel değerlerle başlatmanın sorunsuz çalıştığını test eder."""
    state = VehicleState(
        ignition_on=True,
        engine_running=True,
        speed_kph=110.5,
        engine_rpm=3200,
        coolant_temp_c=90.0,
        fuel_percent=75.0,
        throttle_percent=20.0,
        brake_percent=0.0,
    )

    assert state.speed_kph == 110.5
    assert state.engine_rpm == 3200
    assert state.engine_running is True


def test_invalid_speed_raises_value_error():
    """Hız sınırları aşıldığında ValueError fırlatıldığını test eder."""
    with pytest.raises(ValueError, match="Geçersiz hız değeri"):
        VehicleState(speed_kph=MAX_SPEED_KPH + 10.0)

    with pytest.raises(ValueError, match="Geçersiz hız değeri"):
        VehicleState(speed_kph=MIN_SPEED_KPH - 1.0)


def test_invalid_rpm_raises_value_error():
    """Motor devri sınırları aşıldığında ValueError fırlatıldığını test eder."""
    # Maksimum RPM aşımı (motor çalışırken)
    with pytest.raises(ValueError, match="Geçersiz motor devri"):
        VehicleState(
            ignition_on=True, engine_running=True, engine_rpm=MAX_ENGINE_RPM + 1
        )

    # Minimum RPM altı (negatif devir)
    with pytest.raises(ValueError, match="Geçersiz motor devri"):
        VehicleState(
            ignition_on=True, engine_running=True, engine_rpm=MIN_ENGINE_RPM - 1
        )


def test_invalid_coolant_temp_raises_value_error():
    """Sıcaklık sınırları aşıldığında ValueError fırlatıldığını test eder."""
    with pytest.raises(ValueError, match="Geçersiz coolant_temp_c sıcaklığı"):
        VehicleState(coolant_temp_c=MAX_COOLANT_TEMP_C + 5.0)

    with pytest.raises(ValueError, match="Geçersiz coolant_temp_c sıcaklığı"):
        VehicleState(coolant_temp_c=MIN_COOLANT_TEMP_C - 5.0)


@pytest.mark.parametrize("invalid_percent", [-1.0, 100.1, 150.0])
def test_invalid_percentages_raise_value_error(invalid_percent):
    """Yüzdelik alanların (yakıt, gaz, fren) %0-100 dışı değerlerde hata verdiğini test eder."""
    with pytest.raises(ValueError, match="fuel_percent"):
        VehicleState(fuel_percent=invalid_percent)

    with pytest.raises(ValueError, match="throttle_percent"):
        VehicleState(throttle_percent=invalid_percent)

    with pytest.raises(ValueError, match="brake_percent"):
        VehicleState(brake_percent=invalid_percent)


def test_engine_running_without_ignition_raises_value_error():
    """Kontak kapalıyken motorun çalıştırılamayacağını doğrular."""
    with pytest.raises(ValueError, match="Kontak kapalıyken .* motor çalışamaz"):
        VehicleState(ignition_on=False, engine_running=True)


def test_invalid_type_raises_type_error():
    """Bool alanlara geçersiz tip verildiğinde TypeError fırlatıldığını test eder."""
    with pytest.raises(TypeError, match="ignition_on alanı bool tipinde olmalıdır"):
        VehicleState(ignition_on="AÇIK")  # type: ignore

    with pytest.raises(TypeError, match="engine_running alanı bool tipinde olmalıdır"):
        VehicleState(engine_running=1)  # type: ignore

def test_engine_stopped_with_positive_rpm_raises_value_error():
    """Motor çalışmıyorken devrin sıfırdan büyük olamayacağını doğrular."""
    with pytest.raises(ValueError, match="Motor çalışmıyorken .* motor devri .* olamaz"):
        VehicleState(ignition_on=True, engine_running=False, engine_rpm=1200)

def test_post_modification_validation():
    """Mevcut bir nesnenin alanı sonradan bozulduğunda validate() metodunun yakaladığını test eder."""
    state = VehicleState(ignition_on=True, engine_running=True)
    state.speed_kph = 350.0  # Hatalı değer atandı

    with pytest.raises(ValueError, match="Geçersiz hız değeri"):
        state.validate()