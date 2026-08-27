import time
import pytest
from virtual_ecu import PowertrainECU, BodyECU, DiagnosticECU

def collect_message_timestamps(generator_func, target_period_s: float, count: int = 15):
    """Mesaj aralıklarını ve zaman damgalarını toplar."""
    timestamps = []
    messages = []
    last_run = time.time()

    while len(timestamps) < count:
        now = time.time()
        if (now - last_run) >= target_period_s:
            msg = generator_func()
            timestamps.append(msg.timestamp)
            messages.append(msg)
            last_run = now
        time.sleep(0.001)

    return timestamps, messages


def test_powertrain_period_and_jitter():
    ecu = PowertrainECU()
    target_period = 0.100  # 100 ms
    timestamps, _ = collect_message_timestamps(ecu.generate_powertrain_status, target_period, count=10)

    intervals = [t2 - t1 for t1, t2 in zip(timestamps[:-1], timestamps[1:])]
    avg_interval = sum(intervals) / len(intervals)

    # Ortalama periyot toleransı: ±10 ms
    assert abs(avg_interval - target_period) < 0.010
    
    # Maksimum jitter kontrolü (±15 ms sınırında olmalı)
    max_jitter = max(abs(dt - target_period) for dt in intervals)
    assert max_jitter < 0.015


def test_alive_counter_monotonic_increment():
    ecu = BodyECU()
    prev_counter = -1
    for _ in range(20):
        msg = ecu.generate_body_status()
        current_counter = msg.payload["AliveCounter"]
        if prev_counter != -1:
            expected = (prev_counter + 1) % 16
            assert current_counter == expected
        prev_counter = current_counter


def test_diagnostic_extended_id():
    diag = DiagnosticECU()
    msg = diag.generate_diagnostic_status()
    assert msg.is_extended is True
    assert msg.can_id == 0x18DAF110