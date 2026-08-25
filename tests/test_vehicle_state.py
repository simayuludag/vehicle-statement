"""
VehicleState Modeli ve Validasyon Kuralları Birim Testleri
"""
import pytest
from vehicle_simulator.constants import (
    INITIAL_COOLANT_TEMP_C,
    INITIAL_FUEL_PERCENT,
    MAX_COOLANT_TEMP_C,
    MAX_ENGINE_RPM,
    MAX_PERCENTAGE,
    MAX_SPEED_KPH,
    MIN_COOLANT_TEMP_C,
    MIN_ENGINE_RPM,
    MIN_PERCENTAGE,
    MIN_SPEED_KPH,
)
from vehicle_simulator.vehicle_state import VehicleState


# ---------------------------------------------------------------------------
# 1. Varsayılan ve Geçerli Durum Testleri
# ---------------------------------------------------------------------------


def test_vehicle_state_default_values():
    """Varsayılan araç durumunun geçerli ve beklenen değerlerde olduğunu test eder."""
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
    """Geçerli çalışan araç durumunun kabul edildiğini test eder."""
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


# ---------------------------------------------------------------------------
# 2. Sınır Değer Analizi (Boundary Value Testing: Min-e, Min, Nom, Max, Max+e)
# ---------------------------------------------------------------------------


def test_speed_boundary_values():
    """Hız sınır değerlerini (Min altı, Min, Normal, Max, Max üstü) test eder."""
    # Minimumun hemen altı (Negatif hız reddedilmeli)
    with pytest.raises(ValueError, match="Geçersiz hız değeri"):
        VehicleState(speed_kph=MIN_SPEED_KPH - 0.1)

    # Minimum değer (Geçerli)
    assert VehicleState(speed_kph=MIN_SPEED_KPH).speed_kph == MIN_SPEED_KPH

    # Geçerli normal değer (Geçerli)
    assert VehicleState(speed_kph=90.0).speed_kph == 90.0

    # Maksimum değer (Geçerli)
    assert VehicleState(speed_kph=MAX_SPEED_KPH).speed_kph == MAX_SPEED_KPH

    # Maksimumun hemen üstü (Maksimumdan yüksek hız reddedilmeli)
    with pytest.raises(ValueError, match="Geçersiz hız değeri"):
        VehicleState(speed_kph=MAX_SPEED_KPH + 0.1)


def test_engine_rpm_boundary_values():
    """Motor devri sınır değerlerini (motor çalışırken) test eder."""
    # Minimumun hemen altı (Negatif RPM reddedilmeli)
    with pytest.raises(ValueError, match="Geçersiz motor devri"):
        VehicleState(
            ignition_on=True, engine_running=True, engine_rpm=MIN_ENGINE_RPM - 1
        )

    # Minimum değer (Geçerli)
    state_min = VehicleState(
        ignition_on=True, engine_running=True, engine_rpm=MIN_ENGINE_RPM
    )
    assert state_min.engine_rpm == MIN_ENGINE_RPM

    # Geçerli normal değer (Geçerli)
    state_nom = VehicleState(
        ignition_on=True, engine_running=True, engine_rpm=3000
    )
    assert state_nom.engine_rpm == 3000

    # Maksimum değer (Geçerli)
    state_max = VehicleState(
        ignition_on=True, engine_running=True, engine_rpm=MAX_ENGINE_RPM
    )
    assert state_max.engine_rpm == MAX_ENGINE_RPM

    # Maksimumun hemen üstü (Maksimumdan yüksek RPM reddedilmeli)
    with pytest.raises(ValueError, match="Geçersiz motor devri"):
        VehicleState(
            ignition_on=True, engine_running=True, engine_rpm=MAX_ENGINE_RPM + 1
        )


def test_coolant_temperature_boundary_values():
    """Soğutma suyu sıcaklığı sınır değerlerini test eder."""
    # Minimumun hemen altı (Geçersiz sıcaklık reddedilmeli)
    with pytest.raises(ValueError, match="coolant_temp_c"):
        VehicleState(coolant_temp_c=MIN_COOLANT_TEMP_C - 0.1)

    # Minimum değer (Geçerli)
    assert (
        VehicleState(coolant_temp_c=MIN_COOLANT_TEMP_C).coolant_temp_c
        == MIN_COOLANT_TEMP_C
    )

    # Geçerli normal değer (Geçerli)
    assert VehicleState(coolant_temp_c=90.0).coolant_temp_c == 90.0

    # Maksimum değer (Geçerli)
    assert (
        VehicleState(coolant_temp_c=MAX_COOLANT_TEMP_C).coolant_temp_c
        == MAX_COOLANT_TEMP_C
    )

    # Maksimumun hemen üstü (Geçersiz sıcaklık reddedilmeli)
    with pytest.raises(ValueError, match="coolant_temp_c"):
        VehicleState(coolant_temp_c=MAX_COOLANT_TEMP_C + 0.1)


# ---------------------------------------------------------------------------
# 3. Pedal ve Yüzdelik Değer Testleri
# ---------------------------------------------------------------------------


def test_invalid_throttle_above_max_raises_value_error():
    """%100 üzerindeki gaz pedalı değerinin reddedildiğini test eder."""
    with pytest.raises(ValueError, match="throttle_percent"):
        VehicleState(throttle_percent=MAX_PERCENTAGE + 0.1)


def test_invalid_negative_brake_raises_value_error():
    """Negatif fren pedalı değerinin reddedildiğini test eder."""
    with pytest.raises(ValueError, match="brake_percent"):
        VehicleState(brake_percent=MIN_PERCENTAGE - 0.1)


@pytest.mark.parametrize("invalid_percent", [-1.0, 100.1, 150.0])
def test_invalid_percentages_raise_value_error(invalid_percent):
    """Yüzdelik alanların (yakıt, gaz, fren) sınır dışı değerlerde hata verdiğini test eder."""
    with pytest.raises(ValueError, match="fuel_percent"):
        VehicleState(fuel_percent=invalid_percent)

    with pytest.raises(ValueError, match="throttle_percent"):
        VehicleState(throttle_percent=invalid_percent)

    with pytest.raises(ValueError, match="brake_percent"):
        VehicleState(brake_percent=invalid_percent)


# ---------------------------------------------------------------------------
# 4. Alanlar Arası Tutarlılık (Cross-Field Invariants)
# ---------------------------------------------------------------------------


def test_engine_stopped_with_positive_rpm_raises_value_error():
    """Motor çalışmıyorken pozitif RPM değerinin reddedildiğini test eder."""
    with pytest.raises(
        ValueError, match="Motor çalışmıyorken .* motor devri .* olamaz"
    ):
        VehicleState(ignition_on=True, engine_running=False, engine_rpm=1200)


def test_engine_running_without_ignition_raises_value_error():
    """Kontak kapalıyken çalışan motorun reddedildiğini test eder."""
    with pytest.raises(ValueError, match="Kontak kapalıyken .* motor çalışamaz"):
        VehicleState(ignition_on=False, engine_running=True)


# ---------------------------------------------------------------------------
# 5. Tip Güvenliği ve Doğrulama Mekanizması Testleri
# ---------------------------------------------------------------------------


def test_invalid_type_raises_type_error():
    """Bool alanlara geçersiz tip verildiğinde TypeError fırlatıldığını test eder."""
    with pytest.raises(
        TypeError, match="ignition_on alanı bool tipinde olmalıdır"
    ):
        VehicleState(ignition_on="AÇIK")  # type: ignore

    with pytest.raises(
        TypeError, match="engine_running alanı bool tipinde olmalıdır"
    ):
        VehicleState(engine_running=1)  # type: ignore


def test_post_modification_validation():
    """Mevcut bir nesnenin alanı sonradan bozulduğunda validate() metodunun yakaladığını test eder."""
    state = VehicleState(ignition_on=True, engine_running=True)
    state.speed_kph = 350.0

    with pytest.raises(ValueError, match="Geçersiz hız değeri"):
        state.validate()


# ---------------------------------------------------------------------------
# 6. Sayısal Güvenlik (NaN ve Sonsuzluk) Testleri
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "invalid_val", [float("nan"), float("inf"), float("-inf")]
)
def test_non_finite_values_raise_value_error(invalid_val):
    """NaN ve sonsuzluk değerlerinin tüm alanlarda reddedildiğini test eder."""
    with pytest.raises(ValueError, match="speed_kph"):
        VehicleState(speed_kph=invalid_val)

    with pytest.raises(ValueError, match="engine_rpm"):
        VehicleState(
            ignition_on=True, engine_running=True, engine_rpm=invalid_val
        )  # type: ignore

    with pytest.raises(ValueError, match="coolant_temp_c"):
        VehicleState(coolant_temp_c=invalid_val)

    with pytest.raises(ValueError, match="fuel_percent"):
        VehicleState(fuel_percent=invalid_val)

    with pytest.raises(ValueError, match="throttle_percent"):
        VehicleState(throttle_percent=invalid_val)

    with pytest.raises(ValueError, match="brake_percent"):
        VehicleState(brake_percent=invalid_val)